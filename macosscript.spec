# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # Replace with your actual entry-point script
    pathex=[],
    binaries=[],
    datas=[('startup.mp3', '.'), ('config.json', '.')],
    hiddenimports=['pypresence', 'pygame'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Vector24',  # The name of your executable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set this to False to avoid the terminal window opening
    icon='icon.icns',  # The icon for the macOS .app, make sure it's an .icns file
)

app = BUNDLE(
    exe,
    name='Vector24.app',  # The output will be a macOS .app bundle
    icon='icon.icns',
    bundle_identifier='com.awdev.vector24'
)
