# SMC-Mixer DAW MIDI prototype

**Standalone, not yet integrated with Optimist, not flashable.**

Hortator source `firmware/src/smc.c` and its [documented, hardware-tested SMC DAW mapping](https://github.com/deadactive/hortator/blob/main/docs/superpowers/specs/2026-10-10-midi-bt-smc-design.md) are the primary reference. [Mixxx mapping](https://github.com/mixxxdj/mixxx/blob/main/res/controllers/MVave-SMC-Mixer.midi.xml) is a cross-check.

- Controller must be in **DAW / Mackie Control** mode.
- Buttons: channel 1 note 0x00..0x1f, 0x2e..0x31, 0x5b..0x63; releases are ignored by the eventual action mapper.
- Knobs: channel 1 CC 0x10..0x17, **relative sign-magnitude**, bit 6 means negative.
- Faders: 14-bit pitch bend on channels 1..8 (0xe0..0xe7), with level from high 7 bits.
- Buttons: REC 0x00..07, SOLO 0x08..0f, MUTE 0x10..17, SELECT 0x18..1f, PLAY 0x5e, STOP 0x5d, REC 0x5f.
- Fader pickup/soft takeover and LED feedback are necessary for a polished integration.
- Source-aware routing is essential: normal MIDI instruments must not trigger SMC commands.

## Build blocker
Optimist's upstream `fm1base` submodule points at a private repository and its own workflow documents the requirement for `FM1BASE_TOKEN`. We cannot claim an independently built firmware until that dependency is available or an alternative permitted build base is chosen.
