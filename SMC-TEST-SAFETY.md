# FM1 SMC BLE connection test — safety and installation gate

Build run: https://github.com/alfonsogordon/optimist-SMC/actions/runs/42519425921

**Experimental, not tested on an FM1. Do not flash until the existing firmware and recovery method are known.**

## What the tests establish
- Full FM1 firmware compiled and package size verified against the app slot.
- Upstream Optimist install-route tests passed using a fake flasher, not an actual FM1.
- Upstream web tests passed, including package identity/integrity checks.
- A SHA-256 digest for the exact FWSC is included in the GitHub build artifact as `smc-test-manifest.json`.
- Bluetooth CENTRAL is compiled in. SMC-specific command handling is *disabled* pending positive mixer identification. This build only tests discovery and BLE-MIDI connectivity.
- Three optional synth engines (Plaits, Strings, Physical Model) were disabled to fit the app slot.

## Pre-flash gate (must all be true)
1. Record current FM1 firmware name/version and whether it still boots and responds over USB MIDI.
2. Back up projects, presets and samples using the current firmware's supported export or Optimist editor. Confirm the backup file exists.
3. Confirm the recovery path for this exact installed firmware and bootloader. Optimist documents M-Flasher download-mode backup/restore, but this has **not** been verified on the user's hardware.
4. Prefer a verified full-flash backup with M-Flasher and check that it can read the FM1 without changing its contents. Do not erase or replace the bootloader just for this test.
5. Confirm the installer accepts the package identity, image integrity, and firmware route; stop on any compatibility or bootloader warning. Do not force a refused write.
6. Compare the FWSC SHA-256 with the manifest. Ensure stable power and a data-capable USB cable.

## Test sequence (after the gate)
- Boot and check normal display, buttons, audio, and stored data.
- Enable Bluetooth manually; if it hangs, restarts or shows Felucca red crash screen, stop testing and do not keep retrying.
- Put SMC-Mixer in DAW/Mackie BLE mode; open SYSTEM > BT MIDI on FM1; record whether the mixer is discovered and connects.
- Do **not** expect SMC faders, knobs or buttons to control Optimist yet.
- Record exact error and current firmware/bootloader if connection fails. Never attempt repeated flashing without a recovery backup.

## Remaining risks
- The actual device's bootloader, firmware and flash layout are unknown.
- No physical-device boot, BLE, audio regression, flash/restore or power-loss tests have been run.
- Upstream installer tests use mocks and cannot prove that recovery works on this unit.
- Existing settings and projects may not be compatible with this Optimist build.

Upstream documentation: https://github.com/w0ts/optimist/blob/main/docs/INSTALL-PATHS.md
