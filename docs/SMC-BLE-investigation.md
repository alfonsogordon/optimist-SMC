# SMC-Mixer BLE investigation — 2026-11-09

## Confirmed sources
- Hortator https://github.com/DeadActive/hortator : firmware/src/ble/ble_scan.c lists all nearby advertisers; firmware/src/smc.c implements SMC DAW control and LED feedback. README documents hardware-tested pairing: SMC in DAW mode, FM1 ROLE HOST, MODE AUTO or SMC DAW, scan, choose SMC.
- Optimist https://github.com/w0ts/optimist : firmware/src/ble/ble_scan.c retains advertisers without advertised MIDI UUID temporarily but ble_scan_list() lists only e->midi. Consequently a device without UUID in advertisement/scan response is invisible in DEVICES. Central GATT client assumes BLE-MIDI service.
- SMC-Mixer documented as standards-compliant BLE-MIDI: https://github.com/Bulrok/smc-mixer-linux ; control messages and LED feedback documented in README.
- RemoteFM1 https://github.com/Quixotic7/RemoteFM1 release v0.3.6: BLE MIDI peripheral is enabled, not central in firmware/fm1.toml.
- Manufacturer's Windows Sinco Connector supports SMC-Mixer: https://www.sincoaudio.com/appdownload

## Safe next changes
1. Add a diagnostic scan page that reports raw scan counts, name and advertised MIDI UUID status for all nearby connectable advertisers. Do not auto-connect or save devices until service discovery confirms MIDI.
2. Compare Hortator's BLE scanner, central GATT and SMC event mapping to Optimist's equivalents, preserving licensing and credit.
3. Use hardware test: mixer DAW mode, BT flashing, unpaired from other hosts; note raw advertisements and scan responses. Verify service UUID and characteristic by GATT.
4. Add SMC connection identity check and enable mapping only for identified mixer. Current tools/apply_smc.py intentionally has SMC_LINK_IDENTIFIED=0.
5. Keep firmware size below Skiff-compatible 0x93000 image and do not change bootloader. Latest build fits (image 563668 B), but test package not yet verified with actual Skiff updater.

## Caution
A zero-item BLE-MIDI list is not evidence of zero advertisements. Conversely, documentation of standards-compliant BLE MIDI does not prove the user's mixer is advertising correctly or that FM1's radio scan works. Avoid further flash attempts until loader compatibility is verified.
