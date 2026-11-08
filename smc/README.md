# SMC-Mixer input prototype

Standalone MIDI decoder; **not integrated with Optimist firmware yet**.

Reference: [Mixxx mapping](https://github.com/mixxxdj/mixxx/blob/main/res/controllers/MVave-SMC-Mixer.midi.xml).

- Buttons: channel 1 note messages, notes 0x00..0x1f, 0x2e..0x2f and 0x5b..0x63.
- Knobs: channel 1 CC 0x10..0x17.
- Faders: pitch bend on channels 1..8 (0xe0..0xe7), 14-bit.
- The classifier deliberately does not interpret controls as transport/mute until a verified control scheme is chosen.
- Do not route this classifier blindly to every MIDI input: ordinary keyboards may use these messages.
- Bluetooth service discovery and SMC-specific connection handling remain unverified.
