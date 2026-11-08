/* SPDX-License-Identifier: GPL-3.0-only
 * Source-aware SMC MIDI input dispatcher, independent of Optimist internals.
 * Hardware mode selection must be explicit: never hijack ordinary BLE MIDI.
 */
#ifndef SMC_ROUTE_H
#define SMC_ROUTE_H
#include "smc_midi.h"
#include <stdint.h>
enum smc_action { SMC_ACT_NONE, SMC_ACT_REC_ARM, SMC_ACT_SOLO, SMC_ACT_MUTE,
                  SMC_ACT_SELECT, SMC_ACT_PLAY, SMC_ACT_STOP, SMC_ACT_RECORD,
                  SMC_ACT_PREV, SMC_ACT_NEXT, SMC_ACT_ENCODER, SMC_ACT_LEVEL };
struct smc_command { enum smc_action action; uint8_t track; int16_t amount; };
static inline struct smc_command smc_route(uint8_t enabled, uint8_t source_is_smc,
                                           uint8_t status, uint8_t d1, uint8_t d2) {
    struct smc_command cmd={SMC_ACT_NONE,0,0};
    struct smc_event e;
    if (!enabled || !source_is_smc) return cmd;
    e=smc_decode(status,d1,d2);
    if (e.kind==SMC_FADER) {
        cmd.action=SMC_ACT_LEVEL;cmd.track=e.index;cmd.amount=e.value;
    } else if (e.kind==SMC_KNOB && e.delta) {
        cmd.action=SMC_ACT_ENCODER;cmd.track=e.index;cmd.amount=e.delta;
    } else if (e.kind==SMC_BUTTON && e.value) {
        if (e.index<32) {
            cmd.track=e.index&7u;
            cmd.action=(enum smc_action)(SMC_ACT_REC_ARM+(e.index>>3));
        } else {
            switch(e.index) {
            case 0x5e:cmd.action=SMC_ACT_PLAY;break;
            case 0x5d:cmd.action=SMC_ACT_STOP;break;
            case 0x5f:cmd.action=SMC_ACT_RECORD;break;
            case 0x2e:case 0x30:cmd.action=SMC_ACT_PREV;break;
            case 0x2f:case 0x31:cmd.action=SMC_ACT_NEXT;break;
            default:break;
            }
        }
    }
    return cmd;
}
#endif
