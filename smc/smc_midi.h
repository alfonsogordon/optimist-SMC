/* SPDX-License-Identifier: GPL-3.0-only
 * SMC-Mixer MIDI message classifier.
 * Mapping based on Mixxx MVave-SMC-Mixer.midi.xml; verify with physical hardware.
 * Header-only and independent of Optimist so it can be host-tested.
 */
#ifndef SMC_MIDI_H
#define SMC_MIDI_H
#include <stdint.h>
enum smc_kind { SMC_OTHER=0, SMC_BUTTON, SMC_KNOB, SMC_FADER };
struct smc_event { enum smc_kind kind; uint8_t index, value; uint16_t wide; };
static inline struct smc_event smc_decode(uint8_t status, uint8_t d1, uint8_t d2) {
    struct smc_event e={SMC_OTHER,0,0,0};
    if (d1>127 || d2>127) return e;
    if (status==0x90 || status==0x80) {
        /* 0..31: eight columns of R/S/M/square; 0x2e/2f, 0x5b..0x63: navigation */
        if (d1<=0x1f || d1==0x2e || d1==0x2f || (d1>=0x5b && d1<=0x63)) {
            e.kind=SMC_BUTTON; e.index=d1; e.value=(status==0x90 && d2!=0);
        }
    } else if (status==0xb0 && d1>=0x10 && d1<=0x17) {
        e.kind=SMC_KNOB; e.index=d1-0x10; e.value=d2;
    } else if (status>=0xe0 && status<=0xe7) {
        e.kind=SMC_FADER; e.index=status-0xe0;
        e.wide=(uint16_t)d1 | ((uint16_t)d2<<7);
        e.value=(uint8_t)((e.wide*127u+8191u)/16383u);
    }
    return e;
}
#endif
