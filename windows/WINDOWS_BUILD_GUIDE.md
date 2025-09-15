# 🪟 Windows Application Build Guide

This guide explains how to create a standalone Windows executable for the Teacher Question Paper Drafting System.

## 📋 Prerequisites

### For Building the Application
- **Windows 10/11** (recommended) or Windows 7+
- **Python 3.8+** installed and added to PATH
- **pip** (Python package installer)
- **Git** (optional, for cloning repository)

### System Requirements for End Users
- **Windows 7 or later**
- **4GB RAM minimum** (8GB recommended)
- **500MB free disk space**
- **Internet connection** (for initial setup only)

## 🔧 Build Process

### Method 1: Automatic Build (Recommended)

1. **Open Command Prompt or PowerShell as Administrator**

2. **Navigate to the project directory**
   ```cmd
   cd path\to\notebook
   ```

3. **Run the build script**
   ```cmd
   # Using batch file
   build.bat

   # OR using PowerShell
   powershell -ExecutionPolicy Bypass -File build.ps1
   ```

4. **Wait for completion** (5-15 minutes depending on system)

### Method 2: Manual Build

1. **Install PyInstaller**
   ```cmd
   pip install pyinstaller
   ```

2. **Install all dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Build the application**
   ```cmd
   pyinstaller app.spec --clean
   ```

4. **Run the post-build script**
   ```cmd
   python build_windows_app.py
   ```

## 📦 Distribution Package Structure

After successful build, you'll find:

```
Windows_App_Distribution/
├── TeacherQuestionPaperSystem/          # Main application folder
│   ├── TeacherQuestionPaperSystem.exe   # Main executable
│   ├── app.py                           # Application source
│   └── [various library files]         # Python runtime & libraries
├── Start_Question_Paper_System.bat     # Double-click to run
├── papers/                              # Saved question papers folder
├── metadata/                            # Application data folder
├── downloads/                           # Downloaded assets folder
├── USER_GUIDE.txt                      # End-user instructions
├── README.md                            # Complete documentation
└── requirements.txt                     # Dependency list
```

## 🚀 End User Instructions

### Installing the Application

1. **Download** the Windows_App_Distribution folder (usually as a ZIP file)
2. **Extract** to a location like `C:\TeacherQuestionPaper\`
3. **Double-click** `Start_Question_Paper_System.bat`
4. **Wait** for the application to load (30-60 seconds first time)
5. **Use** the application in your web browser

### First Run Notes

- **Windows Defender** may show a warning - click "More info" → "Run anyway"
- **Antivirus software** might scan the executable - this is normal
- **First launch** takes longer as Windows extracts files
- **Subsequent launches** will be much faster

## 🛠️ Troubleshooting Build Issues

### Common Build Problems

**PyInstaller not found**
```cmd
pip install --upgrade pip
pip install pyinstaller
```

**Missing dependencies**
```cmd
pip install --upgrade -r requirements.txt
```

**Build fails with import errors**
- Ensure all imports work: `python app.py` (should not crash)
- Check Python version: `python --version` (should be 3.8+)
- Try: `pip install --upgrade streamlit markdown-pdf`

**Executable too large**
- This is normal - the exe includes Python runtime (~150-300MB)
- Use UPX compression (already enabled in spec file)

### Runtime Issues

**Application won't start**
- Check antivirus isn't blocking the executable
- Ensure sufficient disk space (500MB+)
- Try running as Administrator

**Browser doesn't open**
- Check firewall settings
- Manually navigate to the URL shown in console
- Try different browser

**PDF generation fails**
- Ensure temp folder has write permissions
- Check disk space for temporary files

## 🔒 Security Considerations

### Code Signing (Optional but Recommended)

To avoid Windows security warnings:

1. **Get a code signing certificate** from a trusted CA
2. **Sign the executable** using:
   ```cmd
   signtool sign /f certificate.p12 /p password /t http://timestamp.url TeacherQuestionPaperSystem.exe
   ```

### Antivirus Whitelisting

For corporate deployment:
- Add executable to antivirus whitelist
- Test on clean machines before distribution
- Consider deploying via MSI installer

## 📊 Build Optimization

### Reducing Size
- Use `--exclude-module` for unused packages
- Enable UPX compression
- Remove debug information

### Improving Performance
- Use `--onefile` for single executable (slower startup)
- Use `--onedir` for faster startup (current default)
- Precompile Python modules

## 🚀 Advanced Distribution

### Creating an Installer

1. **Install NSIS** or **Inno Setup**
2. **Create installer script** including:
   - Application files
   - Desktop shortcut creation
   - Start menu integration
   - Uninstaller

### MSI Package (Enterprise)

1. **Use WiX Toolset** to create MSI
2. **Include dependencies** and prerequisites
3. **Enable silent installation** for group policy deployment

### Portable Version

The current build is already portable:
- No registry modifications
- All files in one folder
- Can run from USB drive
- No admin rights required

## 📋 Quality Assurance

### Testing Checklist

Before distribution, test:
- [ ] Application starts without errors
- [ ] Browser opens automatically
- [ ] All features work (create, save, preview, PDF)
- [ ] Files save/load correctly
- [ ] PDF generation works
- [ ] Application closes cleanly

### Test Environments

Test on:
- [ ] Clean Windows 10/11 machine
- [ ] Machine without Python installed
- [ ] Different user accounts (admin/standard)
- [ ] Various screen resolutions
- [ ] Different browsers (Chrome, Firefox, Edge)

## 📞 Support

### For Build Issues
1. Check this guide first
2. Verify Python installation
3. Update all dependencies
4. Check system requirements

### For Distribution Issues
1. Test on clean machine
2. Check antivirus logs
3. Verify file permissions
4. Review Windows Event Log

---

**Happy Building! 🎉**

*This build process creates a completely self-contained Windows application that end users can run without installing Python or any dependencies.*