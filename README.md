# APK-Patchx
## ⚠️ It's in development mode now (mostly vibe coded), use it carefully, suggest fixes and PR. ⚠️
---
<p align="center">
  <img src="https://placehold.co/1000x280/0d1117/39ff14?font=Fira%20Code&text=apk-patchx%20%E2%80%A2%20APK%20Manipulation%20Toolkit" alt="apk-patchx Banner - Android APK Manipulation Toolkit">
</p>

<p align="center">
  <b>⚡ apk-patchx</b><br>
  <sub>
    A modern Python-powered toolkit for <b>reverse engineering</b>, <b>patching</b>, and <b>rebuilding</b> Android APKs.<br>
    Seamlessly integrates with apktool, smali/dex patching, Frida gadget injection, ADB utilities, and signing workflows.
  </sub>
</p>

---

### 🔥 What is apk-patchx?
`apk-patchx` is a command-line tool that makes APK manipulation fast, modular, and developer-friendly.  
Whether you’re a security researcher, reverse engineer, or power user — it gives you a one-stop solution for:  

- 📦 **Pulling & merging split APKs** directly from connected Android devices  
- 🔍 **Decoding & rebuilding** APKs with apktool  
- 🧩 **Injecting Frida gadgets** into any architecture (`arm`, `arm64`, `x86`, `x86_64`)  
- 📝 **Patching smali/dex** code with your own hooks  
- 🔑 **Auto-signing** APKs for immediate deployment  
- 🎛️ **Custom decode/build options** for advanced workflows  

---

<p align="center">
  <img src="https://placehold.co/950x250/000000/39ff14?font=JetBrains%20Mono&text=%24%20apk-patchx%20patch%20app.apk%20--arch%20arm64%20--frida-version%2016.1.2" alt="apk-patchx Terminal Example">
</p>

## Installation

```bash
pip install apk-patchx
```

## Usage

### Pull APK from device
```bash
apk-patchx pull com.example.app
```

### Decode APK
```bash
apk-patchx decode app.apk
```

### Build APK from source
```bash
apk-patchx build app_src/
```

### Patch APK with Frida gadget
```bash
apk-patchx patch app.apk --arch arm64
```

### Rename APK package
```bash
apk-patchx rename app.apk com.newpackage.name
```

### Sign APK
```bash
apk-patchx sign app.apk
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

APK-Patchx automatically downloads and manages required tools in `~/.apk-patchx/tools/`:

- apktool
- Android SDK build-tools
- Platform tools (adb)
- dexpatch
- Frida gadgets

## License

MIT License - see LICENSE file for details.
