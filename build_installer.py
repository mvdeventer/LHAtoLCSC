"""
Build Windows Installer for LHAtoLCSC

This script:
1. Creates a standalone executable using PyInstaller
2. Generates an InnoSetup installer (.exe)
3. Optionally uploads to GitHub release

Requirements:
- PyInstaller: pip install pyinstaller
- InnoSetup: https://jrsoftware.org/isdl.php (must be in PATH)
"""

import subprocess
import sys
import shutil
import os
from pathlib import Path
from datetime import datetime
import re


class Colors:
    """ANSI color codes."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def run_command(cmd: list, cwd: Path = None) -> bool:
    """Run command and return success status."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return False


def get_version() -> str:
    """Get version from config.py."""
    config_path = Path('src/lhatolcsc/core/config.py')
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'self\.version\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return "0.0.0"


def check_requirements() -> bool:
    """Check if required tools are installed."""
    print_info("Checking requirements...")
    
    # Check PyInstaller (prefer venv version)
    venv_pyinstaller = Path('venv/Scripts/pyinstaller.exe')
    if venv_pyinstaller.exists():
        print_success(f"PyInstaller is installed (venv)")
    else:
        try:
            # Try both direct command and module form
            try:
                subprocess.run(['pyinstaller', '--version'], capture_output=True, check=True)
                print_success("PyInstaller is installed (system)")
            except (subprocess.CalledProcessError, FileNotFoundError):
                subprocess.run([sys.executable, '-m', 'PyInstaller', '--version'], capture_output=True, check=True)
                print_success("PyInstaller is installed (module)")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print_error("PyInstaller not found. Install with: pip install pyinstaller")
            return False
    
    # Check InnoSetup (optional but recommended)
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ]
    
    inno_found = False
    for path in inno_paths:
        if Path(path).exists():
            print_success(f"InnoSetup found at {path}")
            inno_found = True
            break
    
    if not inno_found:
        print_info("InnoSetup not found (optional). Download from: https://jrsoftware.org/isdl.php")
        response = input("Continue without InnoSetup installer? (y/n): ")
        if response.lower() != 'y':
            return False
    
    return True


def clean_build_dirs():
    """Clean previous build directories."""
    print_info("Cleaning previous build directories...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print_success(f"Removed {dir_name}/")
    
    # Remove .spec files
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print_success(f"Removed {spec_file}")


def create_pyinstaller_spec(version: str) -> bool:
    """Create PyInstaller spec file."""
    print_info("Creating PyInstaller spec file...")
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/lhatolcsc', 'lhatolcsc'),
        ('README.md', '.'),
        ('LICENSE', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageTk',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'xlwings',
        'pandas',
        'numpy',
        'rapidfuzz',
        'yaml',
        'dateutil',
        'tqdm',
        'pydantic',
        'pydantic_core',
        'diskcache',
        # python-dotenv imports
        'dotenv',
        'dotenv.main',
        'dotenv.parser',
        'dotenv.variables',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'tests',
        'docs',
        'htmlcov',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LHAtoLCSC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Temporarily enable console to see errors
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if Path('icon.ico').exists() else None,
    version='version_info.txt' if Path('version_info.txt').exists() else None,
)
'''
    
    with open('LHAtoLCSC.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print_success("Created LHAtoLCSC.spec")
    return True


def create_version_info(version: str) -> bool:
    """Create Windows version info file."""
    print_info("Creating version info file...")
    
    version_parts = version.split('.')
    while len(version_parts) < 4:
        version_parts.append('0')
    
    version_info = f'''VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({version_parts[0]}, {version_parts[1]}, {version_parts[2]}, {version_parts[3]}),
    prodvers=({version_parts[0]}, {version_parts[1]}, {version_parts[2]}, {version_parts[3]}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'LHAtoLCSC'),
        StringStruct(u'FileDescription', u'BOM to LCSC Part Matcher'),
        StringStruct(u'FileVersion', u'{version}'),
        StringStruct(u'InternalName', u'LHAtoLCSC'),
        StringStruct(u'LegalCopyright', u'Copyright (c) {datetime.now().year}'),
        StringStruct(u'OriginalFilename', u'LHAtoLCSC.exe'),
        StringStruct(u'ProductName', u'LHAtoLCSC'),
        StringStruct(u'ProductVersion', u'{version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print_success("Created version_info.txt")
    return True


def build_executable() -> bool:
    """Build executable with PyInstaller."""
    print_info("Building executable with PyInstaller...")
    print_info("This may take several minutes...")
    
    # Use venv's pyinstaller if available, otherwise system pyinstaller
    venv_pyinstaller = Path('venv/Scripts/pyinstaller.exe')
    if venv_pyinstaller.exists():
        cmd = [str(venv_pyinstaller), '--clean', '--noconfirm', 'LHAtoLCSC.spec']
    else:
        # Try direct command first, then module form
        try:
            subprocess.run(['pyinstaller', '--version'], capture_output=True, check=True)
            cmd = ['pyinstaller', '--clean', '--noconfirm', 'LHAtoLCSC.spec']
        except (subprocess.CalledProcessError, FileNotFoundError):
            cmd = [sys.executable, '-m', 'PyInstaller', '--clean', '--noconfirm', 'LHAtoLCSC.spec']
    
    if not run_command(cmd):
        return False
    
    exe_path = Path('dist/LHAtoLCSC.exe')
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print_success(f"Built executable: {exe_path} ({size_mb:.2f} MB)")
        return True
    else:
        print_error("Executable not found after build")
        return False


def create_innosetup_script(version: str) -> bool:
    """Create InnoSetup installer script."""
    print_info("Creating InnoSetup installer script...")
    
    # Check for optional files
    has_icon = Path('icon.ico').exists()
    has_env_example = Path('.env.example').exists()
    has_docs = Path('docs').exists()
    
    icon_line = f'SetupIconFile=icon.ico' if has_icon else '; No icon.ico found'
    env_line = f'Source: ".env.example"; DestDir: "{{{{app}}}}"; Flags: ignoreversion' if has_env_example else '; No .env.example found'
    docs_line = f'Source: "docs\\*"; DestDir: "{{{{app}}}}\\docs"; Flags: ignoreversion recursesubdirs createallsubdirs' if has_docs else '; No docs folder found'
    
    inno_script = f'''#define MyAppName "LHAtoLCSC"
#define MyAppVersion "{version}"
#define MyAppPublisher "LHAtoLCSC"
#define MyAppURL "https://github.com/mvdeventer/LHAtoLCSC"
#define MyAppExeName "LHAtoLCSC.exe"

[Setup]
AppId={{{{A1B2C3D4-E5F6-4A5B-8C9D-0E1F2A3B4C5D}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer
OutputBaseFilename=LHAtoLCSC-{version}-Setup
{icon_line}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

[Files]
Source: "dist\\LHAtoLCSC.exe"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{{app}}"; Flags: ignoreversion
{env_line}
{docs_line}

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent
'''
    
    with open('installer.iss', 'w', encoding='utf-8') as f:
        f.write(inno_script)
    
    print_success("Created installer.iss")
    return True


def build_installer(version: str) -> bool:
    """Build installer with InnoSetup."""
    print_info("Building installer with InnoSetup...")
    
    # Find InnoSetup compiler
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ]
    
    iscc_path = None
    for path in inno_paths:
        if Path(path).exists():
            iscc_path = path
            break
    
    if not iscc_path:
        print_info("InnoSetup not found, skipping installer creation")
        print_info("You can still use the executable from dist/LHAtoLCSC.exe")
        return True
    
    # Create installer directory
    Path('installer').mkdir(exist_ok=True)
    
    # Build installer
    cmd = [iscc_path, 'installer.iss']
    if not run_command(cmd):
        return False
    
    installer_path = Path(f'installer/LHAtoLCSC-{version}-Setup.exe')
    if installer_path.exists():
        size_mb = installer_path.stat().st_size / (1024 * 1024)
        print_success(f"Built installer: {installer_path} ({size_mb:.2f} MB)")
        return True
    else:
        print_error("Installer not found after build")
        return False


def create_portable_zip(version: str) -> bool:
    """Create portable ZIP distribution."""
    print_info("Creating portable ZIP distribution...")
    
    import zipfile
    
    zip_path = Path(f'installer/LHAtoLCSC-{version}-Portable.zip')
    zip_path.parent.mkdir(exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add executable
        zipf.write('dist/LHAtoLCSC.exe', 'LHAtoLCSC.exe')
        
        # Add documentation
        if Path('README.md').exists():
            zipf.write('README.md', 'README.md')
        if Path('LICENSE').exists():
            zipf.write('LICENSE', 'LICENSE')
        if Path('.env.example').exists():
            zipf.write('.env.example', '.env.example')
        
        # Add docs folder
        docs_path = Path('docs')
        if docs_path.exists():
            for doc_file in docs_path.rglob('*'):
                if doc_file.is_file():
                    arcname = str(doc_file.relative_to('.'))
                    zipf.write(doc_file, arcname)
    
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print_success(f"Created portable ZIP: {zip_path} ({size_mb:.2f} MB)")
    return True


def main():
    """Main build process."""
    print_header("LHAtoLCSC Installer Builder")
    
    # Get version
    version = get_version()
    print_info(f"Building version: {version}")
    
    # Check requirements
    if not check_requirements():
        print_error("Requirements check failed")
        sys.exit(1)
    
    # Clean previous builds
    clean_build_dirs()
    
    # Create build files
    if not create_version_info(version):
        print_error("Failed to create version info")
        sys.exit(1)
    
    if not create_pyinstaller_spec(version):
        print_error("Failed to create PyInstaller spec")
        sys.exit(1)
    
    # Build executable
    if not build_executable():
        print_error("Failed to build executable")
        sys.exit(1)
    
    # Create InnoSetup script
    if not create_innosetup_script(version):
        print_error("Failed to create InnoSetup script")
        sys.exit(1)
    
    # Build installer
    if not build_installer(version):
        print_error("Failed to build installer")
        # Don't exit - we still have the executable
    
    # Create portable ZIP
    if not create_portable_zip(version):
        print_error("Failed to create portable ZIP")
        # Don't exit - not critical
    
    # Summary
    print_header("Build Complete!")
    print_success(f"Version {version} built successfully")
    print_info("\nBuild artifacts:")
    print(f"  • Executable: dist/LHAtoLCSC.exe")
    
    installer_path = Path(f'installer/LHAtoLCSC-{version}-Setup.exe')
    if installer_path.exists():
        print(f"  • Installer: {installer_path}")
    
    zip_path = Path(f'installer/LHAtoLCSC-{version}-Portable.zip')
    if zip_path.exists():
        print(f"  • Portable ZIP: {zip_path}")
    
    print("\nNext steps:")
    print("  1. Test the executable: dist\\LHAtoLCSC.exe")
    print("  2. Test the installer (if created)")
    print("  3. Upload to GitHub release with: gh release upload v{version} installer/*")


if __name__ == '__main__':
    main()
