#!/usr/bin/env python3
"""Patch a pinned Optimist checkout with an opt-in, side-effect-free SMC MIDI probe.

The probe intentionally does not steal ordinary note messages. It only records
decoded events when explicitly enabled in the build. Transport/mutes await
source-aware BLE routing and hardware verification.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1])
src = root / "firmware/src/io/midi/midi_control.c"
dst = root / "firmware/src/io/midi/smc_midi.h"
if not src.is_file():
    raise SystemExit("missing upstream MIDI control source")
dst.write_bytes((Path(__file__).resolve().parent.parent / "smc/smc_midi.h").read_bytes())
s = src.read_text()
anchor = "static void __attribute__((noinline)) midi_event(uint32_t st, uint32_t ch, uint32_t d1, uint32_t d2)\n{"
if s.count(anchor) != 1:
    raise SystemExit("upstream MIDI entrypoint changed; refusing patch")
probe = """/* Opt-in SMC protocol probe: never intercepts normal MIDI or changes sound. */
#include "smc_midi.h"
static volatile uint32_t smc_seen;
static volatile uint8_t smc_last_kind, smc_last_index, smc_last_value;
static void smc_probe(uint32_t st, uint32_t ch, uint32_t d1, uint32_t d2)
{
    struct smc_event e = smc_decode((uint8_t)(st | (ch & 15u)),
                                    (uint8_t)d1, (uint8_t)d2);
    if (e.kind != SMC_OTHER) {
        smc_seen++;
        smc_last_kind = (uint8_t)e.kind;
        smc_last_index = e.index;
        smc_last_value = e.value;
    }
}
"""
replacement = anchor + """
#if defined(SMC_MIDI_PROBE) && SMC_MIDI_PROBE
    smc_probe(st, ch, d1, d2);
#endif"""
s = s.replace(anchor, replacement)
s = s.replace(anchor, anchor, 0)
s = s.replace("/* the occasional controller / panic: out of the render path's inlining */", probe + "\n/* the occasional controller / panic: out of the render path's inlining */")
# Patch the source-aware MIDI consumer only after verifying the exact upstream callsite.
seq = root / "firmware/src/seq/seq.c"
q = seq.read_text()
call = "FAST_CALL(seqev, midi_event)(st, ch, d1, d2);"
if q.count(call) != 1:
    raise SystemExit("upstream MIDI queue consumer changed; refusing patch")
route_header = root / "firmware/src/seq/smc_route.h"
route_header.write_bytes((Path(__file__).resolve().parent.parent / "smc/smc_route.h").read_bytes())
(root / "firmware/src/seq/smc_midi.h").write_bytes((Path(__file__).resolve().parent.parent / "smc/smc_midi.h").read_bytes())
# The SMC-Mixer must be positively identified by the BLE connection layer.
# Until that exists, SMC_LINK_IDENTIFIED is 0 and routing cannot activate.
route = """#include "smc_route.h"
#ifndef SMC_LINK_IDENTIFIED
#define SMC_LINK_IDENTIFIED 0
#endif
static int smc_command_try(uint32_t source, uint32_t st, uint32_t ch, uint32_t d1, uint32_t d2)
{
    struct smc_command c = smc_route(1, SMC_LINK_IDENTIFIED && source == MSRC_BLE,
                                      (uint8_t)(st | ch), (uint8_t)d1, (uint8_t)d2);
    if (c.action == SMC_ACT_PLAY) {
        if (!song.playing) transport_req = 1;
    } else if (c.action == SMC_ACT_STOP) {
        if (song.playing) transport_req = 2;
    } else return 0;
    return 1;
}
"""
q = route + q if False else q
# Include after the upstream module's own initial declarations, before events_block.
# The insertion immediately before events_block is after transport_req declaration.
marker = "static void events_block_(uint32_t n);"
if q.count(marker) != 1:
    raise SystemExit("upstream events_block declaration changed; refusing patch")
q = q.replace(marker, route + "\n" + marker)
q = q.replace(call, """if (!smc_command_try(midi_in_src[(mi_r - 1u) % MQ],
                             st, ch, d1, d2))
            FAST_CALL(seqev, midi_event)(st, ch, d1, d2);""")
seq.write_text(q)
src.write_text(s)

# Diagnostic scan: expose all nearby connectable advertisers in the DEVICES
# list, but NEVER connect to one unless the standard BLE-MIDI UUID was seen.
scan = root / "firmware/src/ble/ble_scan.c"
scan_src = scan.read_text()
old = "if (t->e[i].used && t->e[i].midi) {"
new = "if (t->e[i].used) { /* SMC diagnostic: also show unconfirmed advertisers */"
if scan_src.count(old) != 1:
    raise SystemExit("BLE scan listing changed; refusing diagnostic patch")
scan.write_text(scan_src.replace(old, new))
devices = root / "firmware/src/io/midi/ble_devices.c"
dev_src = devices.read_text()
pick = "    ble_connect_pick(&ble_found.e[near[row - 1u - (last >= 0 ? 1u : 0u) - nk]]);"
guard = """    {
        const struct ble_found *candidate = &ble_found.e[near[row - 1u - (last >= 0 ? 1u : 0u) - nk]];
        if (!candidate->midi) {
            ble_dev_say("NO MIDI UUID - SCAN ONLY", BDL_WARN);
            return;
        }
        ble_connect_pick(candidate);
    }"""
if dev_src.count(pick) != 1:
    raise SystemExit("BLE pick callsite changed; refusing diagnostic patch")
dev_src = dev_src.replace(pick, guard)
tag = '        *bars = ble_scan_bars(&ble_found, (uint32_t)(e - ble_found.e));'
if dev_src.count(tag) != 1:
    raise SystemExit("BLE nearby display changed; refusing diagnostic patch")
dev_src = dev_src.replace(tag, tag + '\n        if (!e->midi) *tag = "NO MIDI UUID"; /* visible, never selectable */')
devices.write_text(dev_src)
print("SMC diagnostic: show all nearby advertisers, tag missing UUID, block unsafe connections")

print("Patched Optimist MIDI event entrypoint with non-invasive SMC probe")
