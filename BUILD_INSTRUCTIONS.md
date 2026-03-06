# 🔧 How to Build Quadrant.exe for Windows

This document provides **two methods** to build the Windows executable. Choose the one that works best for your situation.

---

## Overview

| Method | Requires Python? | Difficulty | Best For |
|--------|-----------------|------------|----------|
| **GitHub Actions** (Recommended) | ❌ No | Easy | Anyone, no software installation |
| **Manual Build** | ✅ Yes | Medium | IT staff with Python installed |

---

## 🌐 Method 1: GitHub Actions (Recommended)

**No software installation required** - uses free cloud build service.

📖 **See: [GITHUB_BUILD_GUIDE.md](GITHUB_BUILD_GUIDE.md)** for complete step-by-step instructions.

### Quick Summary:
1. Create free GitHub account at https://github.com
2. Create a new repository
3. Upload all project files (including `.github` folder)
4. Go to Actions tab → Run "Build Windows Executable"
5. Download `Quadrant.exe` from Artifacts

**Time required**: ~15-20 minutes first time, ~5 minutes for rebuilds

---

## 💻 Method 2: Manual Build (Requires Python)

Use this method if you have Python installed on a Windows machine.

### Prerequisites

- Windows 10 or 11
- Python 3.8 or newer ([Download from python.org](https://www.python.org/downloads/))

### Option A: Use the Build Script (Easiest)

1. Open the folder containing the project files

2. Double-click **`build.bat`**

3. Wait for the build to complete (2-5 minutes)

4. Find `Quadrant.exe` in the `dist` folder

### Option B: Manual Commands

1. Open **Command Prompt** or **PowerShell**

2. Navigate to the project folder:
   ```cmd
   cd C:\path\to\quadrant-project
   ```

3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

4. Build the executable:
   ```cmd
   pyinstaller --onefile --name Quadrant --clean quadrant.py
   ```

5. Find `Quadrant.exe` in the `dist` folder

---

## 📁 Files in This Package

```
quadrant-project/
├── quadrant.py              # Main Python source code
├── quadrant_config.json     # Configuration file
├── requirements.txt         # Python dependencies
├── build.bat                # Windows build script
├── README.md                # Full documentation
├── BUILD_INSTRUCTIONS.md    # This file
├── GITHUB_BUILD_GUIDE.md    # Detailed GitHub Actions guide
└── .github/
    └── workflows/
        └── build-windows-exe.yml  # GitHub Actions workflow
```

---

## 📋 After Building

### Required files to run Quadrant.exe:

1. `Quadrant.exe` - The application
2. `quadrant_config.json` - Configuration file
3. Your Excel data file (`.xlsx`)

### To run:
1. Copy all three files to the same folder
2. Double-click `Quadrant.exe`
3. View the generated `quadrant.html` in your browser

---

## ❓ FAQ

### Q: Which method should I choose?
**A**: If you don't have Python installed and don't want to install it, use **GitHub Actions**. It's free and requires no software installation on your computer.

### Q: Is GitHub Actions really free?
**A**: Yes! GitHub gives you 2,000 free build minutes per month. Building Quadrant.exe takes about 3 minutes.

### Q: Do I need to rebuild when I change the config?
**A**: No! Just edit `quadrant_config.json` with any text editor. The config is read at runtime.

### Q: Do I need to rebuild when I change the Excel data?
**A**: No! Just replace your Excel file and re-run `Quadrant.exe`.

### Q: When DO I need to rebuild?
**A**: Only if you modify `quadrant.py` (the Python source code).

---

## 🆘 Getting Help

- **For GitHub Actions issues**: See the Troubleshooting section in `GITHUB_BUILD_GUIDE.md`
- **For Python/build issues**: See the Troubleshooting section in `README.md`
