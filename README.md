# 🔍 Screen Search (Google Lens for Wayland)

A lightweight, standalone desktop utility for Linux (Wayland) that allows you to select a screen region and instantly perform a reverse image search using **Google Lens** directly in your default browser.

Built and optimized specifically for **CachyOS**, **Niri**, and **Hyprland** compositors.

![Linux](https://img.shields.io/badge/Linux-Wayland-blue?style=flat-square&logo=linux)
![CachyOS](https://img.shields.io/badge/Distro-CachyOS-green?style=flat-square)
![Niri](https://img.shields.io/badge/Compositor-Niri-purple?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.12+-yellow?style=flat-square&logo=python)

---

## ✨ Features

- **Instant Region Selection:** Uses `grim` and `slurp` for fast, lightweight selection.
- **Direct Google Lens Integration:** Sends image data directly to Google Lens without third-party storage delays.
- **Zero Runtime Dependencies:** Compiles into a single standalone binary (`PyInstaller`) — runs cleanly on systems without Python or additional libraries installed.
- **Automated Deployment:** Included `setup.sh` handles virtual environment isolation (`PEP 668` compliant), compilation, binary relocation, and keybinding configuration.

---

## 📋 Prerequisites

Before installing, ensure the following native Wayland utilities are installed on your system:

- **`grim`**: Image grabber for Wayland.
- **`slurp`**: Region selector for Wayland.

On **CachyOS / Arch Linux**, install them via `pacman`:

```bash
sudo pacman -S grim slurp
```

---

## 🚀 Quick Installation

Clone this repository and run the automated setup script:

```bash
git clone https://github.com/your-username/screen-search.git
cd screen-search
chmod +x setup.sh
./setup.sh
```

### What `setup.sh` does:
1. Creates a isolated temporary virtual environment (`.venv`).
2. Installs dependencies and packages the code into a standalone binary using `PyInstaller`.
3. Moves the compiled binary to `~/.local/bin/screen-search`.
4. Automatically injects the default shortcut (`Mod+Shift+G`) into your Niri configuration (`~/.config/niri/config.d/70-binds.kdl`).
5. Cleans up all build artifacts and virtual environments upon completion.

---

## ⌨️ Usage & Keybindings

### **Niri Window Manager**
The setup script automatically adds the following keybinding to `~/.config/niri/config.d/70-binds.kdl`:

```kdl
binds {
    Mod+Shift+G { spawn "/home/YOUR_USER/.local/bin/screen-search"; }
}
```

*Press **`Super + Shift + G`** to trigger the screen selection overlay, drag your mouse over any region, and the search results will open in your browser.*

---

### **Hyprland**
If you are using **Hyprland**, add this line manually to your `hyprland.conf`:

```ini
bind = $mainMod SHIFT, G, exec, ~/.local/bin/screen-search
```

---

## 📁 Repository Structure

```text
screen-search/
├── main.py              # Main Python script for capture & Lens upload logic
├── setup.sh             # Automated build, install, and configuration script
├── requirements.txt     # Python build dependencies (requests, pyinstaller)
└── README.md            # Documentation
```

---

## 🛠️ Manual Build (Optional)

If you prefer to build the executable manually without running `setup.sh`:

```bash
# 1. Set up a temporary environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pyinstaller

# 2. Compile into a single binary
pyinstaller --onefile --noconsole --log-level ERROR main.py --name "screen-search"

# 3. Move the executable to your local PATH
mkdir -p ~/.local/bin
mv dist/screen-search ~/.local/bin/
chmod +x ~/.local/bin/screen-search

# 4. Cleanup
deactivate
rm -rf .venv build dist screen-search.spec
```

---


