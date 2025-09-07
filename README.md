# APKPatcher

A powerful command-line tool for Android APK manipulation, including Frida gadget injection, APK decoding/building, and package management.

## Features

- **APK Management**: Pull, decode, build, and sign APK files
- **Frida Integration**: Inject Frida gadgets for runtime manipulation
- **Split APK Support**: Automatically merge split APKs into single files
- **Package Renaming**: Change APK package names
- **Auto-bootstrap**: Automatically downloads and manages required tools

## Installation

```bash
pip install apkpatcher
```

## Usage

### Pull APK from device
```bash
apkpatcher pull com.example.app
```

### Decode APK
```bash
apkpatcher decode app.apk
```

### Build APK from source
```bash
apkpatcher build app_src/
```

### Patch APK with Frida gadget
```bash
apkpatcher patch app.apk --arch arm64
```

### Rename APK package
```bash
apkpatcher rename app.apk com.newpackage.name
```

### Sign APK
```bash
apkpatcher sign app.apk
```

## Architecture Support

- ARM (`arm`)
- ARM64 (`arm64`) 
- x86 (`x86`)
- x86_64 (`x86_64`)

## Requirements

- Python 3.8+
- Java Runtime Environment (JRE 8+)
- ADB (for device operations)

## Tool Management

APKPatcher automatically downloads and manages required tools in `~/.apkpatcher/tools/`:

- apktool
- Android SDK build-tools
- Platform tools (adb)
- dexpatch
- Frida gadgets

## License

MIT License - see LICENSE file for details.
