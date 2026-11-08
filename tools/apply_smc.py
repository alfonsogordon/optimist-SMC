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
src.write_text(s)
print("Patched Optimist MIDI event entrypoint with non-invasive SMC probe")
