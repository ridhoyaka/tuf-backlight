# TUF Backlight

**TUF Backlight** is a lightweight **CLI** tool designed to control **ASUS TUF keyboard RGB backlight** on **Linux systems**.
It provides an intuitive, menu-driven interface for adjusting lighting modes, colors, and effects directly from the terminal, using the official **Linux SysFS interface**.
**Built with Python and Rich**, this tool focuses on simplicity, safety, and a clean user experience without relying on desktop environments or graphical applications.

---

## Features

- Mengatur mode backlight:
  - Static
  - Breathing
  - Color Cycle
  - Strobing
- Pengaturan warna RGB (0–255)
- Pengaturan speed (Slow / Medium / Fast)
- Aman (langsung menulis ke SysFS resmi kernel)

---

## System Requirements

### Hardware
- Laptop **ASUS TUF** yang mendukung RGB keyboard
- Driver keyboard ASUS tersedia di kernel
- Cara Mengecek Driver :
```bash
ls /sys/class/leds/ | grep asus
```
Harus muncul :
```bash
asus::kbd_backlight
```

### Operating System
- Linux (tested on **Ubuntu**)
- Other Distro :
  - Debian
  - Arch Linux
  - Fedora
  - Linux Mint
  - dll
- Desktop Environment :
  - GNOME
  - KDE
  - XFCE
  - i3
  - Cinnamon

### Software
- Python **3.8+**
- Kernel Linux **≥ 5.15** (disarankan 6.x)

---

## Dependencies

- **Python 3**
- **Python module: Rich**
- **Figlet**
- **Figlet font: smkeyboard**

---

## Installation Guide

```bash
git clone https://github.com/ridhoyaka/tuf-backlight.git
cd tuf-backlight
chmod +x tufbacklight.py
pip3 install rich
sudo apt install figlet
sudo wget http://www.figlet.org/fonts/smkeyboard.flf
```

---

## Usage

```bash
sudo ./tufbacklight.py
```

---

## Screenshot

## 📸 Screenshot

![TUF Backlight CLI](preview-tuf-backlight.png)

---

## License

MIT License
Free to use, modify, and distribute.

---

## Author

Akay / Ridhoyaka
GitHub: https://github.com/ridhoyaka

---

## Credits

Python
Rich library
Linux kernel ASUS WMI
figlet & figlet-fonts
