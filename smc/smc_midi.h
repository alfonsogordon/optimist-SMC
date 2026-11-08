/* SPDX-License-Identifier: GPL-3.0-only
 * SMC-Mixer DAW-mode MIDI classifier, informed by Hortator's tested mapping.
 * No connection or transport side effects. Opt-in routing required.
 */
#ifndef SMC_MIDI_H
#define SMC_MIDI_H
#include <stdint.h>
enum smc_kind { SMC_OTHER=0, SMC_BUTTON, SMC_KNOB, SMC_FADER };
struct smc_event { enum smc_kind kind; uint8_t index, value; uint16_t wide; int8_t delta; };
static inline struct smc_event smc_decode(uint8_t status, uint8_t d1, uint8_t d2) {
    struct smc_event e={SMC_OTHER,0,0,0,0};
    uint8_t ch=status&15u, type=status&0xf0u;
    if (d1>127 || d2>127) return e;
    if ((type==0x90 || type==0x80) && ch==0) {
        if (d1<=0x1f || (d1>=0x2e && d1<=0x31) || (d1>=0x5b && d1<=0x63)) {
            e.kind=SMC_BUTTON; e.index=d1; e.value=(type==0x90 && d2!=0);
        }
    } else if (type==0xb0 && ch==0 && d1>=0x10 && d1<=0x17) {
        /* SMC rotary encoders are relative sign-magnitude, not absolute CC. */
        e.kind=SMC_KNOB; e.index=d1-0x10; e.value=d2;
        e.delta=(int8_t)((d2&0x40u) ? -(int)(d2&0x3fu) : (int)(d2&0x3fu));
    } else if (type==0xe0 && ch<8) {
        e.kind=SMC_FADER; e.index=ch;
        e.wide=(uint16_t)d1 | ((uint16_t)d2<<7);
        /* Hortator's working DAW mapping uses the high seven bits. */
        e.value=(uint8_t)(e.wide>>7);
    }
    return e;
}
#endif
