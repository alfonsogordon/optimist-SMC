# Optimist SMC integration

Development branch for adding M-VAVE SMC-Mixer support to [Optimist](https://github.com/w0ts/optimist).

## Baseline

- Keep upstream Optimist BLE central role, scanning, BLE-MIDI GATT client, reconnect and device storage.
- Investigate the SMC-Mixer advertising and BLE MIDI service before changing the radio stack.
- Use the [Mixxx SMC-Mixer MIDI mapping](https://github.com/mixxxdj/mixxx/blob/main/res/controllers/MVave-SMC-Mixer.midi.xml) as a control-message reference. Verify messages against the actual controller.
- Compare with Hortator's known-working SMC connection if its source is accessible.
- Integrate controls at the Optimist MIDI routing boundary, with a dedicated opt-in mapping to avoid changing normal MIDI behaviour.
- Add host-side tests for button/fader mapping, note-off, reconnect and invalid messages.
- Build the complete firmware with Optimist's original toolchain and check firmware size before hardware flashing.
- Provide a browser-based flasher only after an actual firmware build has passed checks.

## Safety gates

No firmware is currently built or validated for hardware. Keep a backup of existing FM-1 data and a known-good recovery method. Never assume a successful compile proves Bluetooth pairing or hardware safety.

## Development sequence

1. Import upstream Optimist source with its required submodules or pinned dependencies.
2. Verify the unmodified baseline builds.
3. Confirm SMC-Mixer BLE advertising, service UUID and MIDI messages.
4. Add a separate SMC input mapper and tests.
5. Integrate, compile, inspect size and exercise the simulator.
6. Publish a test firmware and browser flasher, with explicit experimental labelling.
