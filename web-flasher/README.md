# FM1 safe flashing route (work in progress)

**Do not flash the current upstream baseline artifact expecting SMC-Mixer support.** The full firmware build is proven, but the SMC code is not integrated.

## Use the established updater, not a new untested flasher

The [Optimist web installer](https://w0ts.github.io/optimist/webapp/installer/) already accepts a local `.fwsc` file. It checks package integrity, identifies the connected update loader, handles resume and exposes backup and recovery paths. We should reuse and audit its updater, not duplicate flash-writing logic.

## Release gate (must all pass before an SMC package is offered)

1. Complete firmware source and pinned public dependencies are available.
2. SMC-specific MIDI mapping and routing compiled into the **same** package.
3. Host MIDI mapping tests, upstream firmware tests, firmware build and package validation pass.
4. Package is named as experimental and accompanied by SHA-256 digest computed from the built bytes.
5. Installer validates the exact SHA-256 before any update action; a mismatch blocks.
6. Installer identifies an FM1 and a compatible loader; unknown firmware/loader blocks, rather than guesses.
7. User is offered a project/preset/sample backup and a recovery guide before flashing.
8. Browser must not erase bootloader or calibration; cross-loader transitions go through an explicit recovery tool.
9. Power and cable checks and a user confirmation are required; no silent auto-flash.
10. Interrupted transfers may only resume when the loader and package agree on a safe resume path; otherwise stop.
11. Successful write alone is not a pass: verify completion and reboot, with recovery steps on failure.
12. Hardware testing is required to verify the BLE connection and control behaviour; CI alone cannot prove it.

**Important:** No browser updater can guarantee a zero-brick risk, especially with power loss, unknown prior firmware, incompatible bootloader or flash hardware defects. A recovery tool and verified flash backup are recommended.

## When an SMC package is available

Use the existing [Optimist installer](https://w0ts.github.io/optimist/webapp/installer/) and choose **a .fwsc of yours**, rather than flashing an unverified file through a new custom page. Do not switch bootloaders through USB MIDI.
