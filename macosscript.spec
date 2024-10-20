# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],  # Entry-point script
    pathex=[],  # Add additional paths if necessary
    binaries=[],
    datas=[('startup.mp3', '.'), ('config.json', '.')],  # Ensure the paths are correct
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
    [],
    exclude_binaries=True,
    name='Vector24',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Set to False if UPX causes issues
    console=False,  # Prevent terminal window from opening
    icon='icon.icns',  # Ensure the icon file path is correct
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Vector24'
)

app = BUNDLE(
    coll,
    name='Vector24.app',  # The macOS .app bundle name
    icon='icon.icns',  # Path to the icon, ensure it's .icns format
    bundle_identifier='com.awdev.vector24',  # Update if necessary
)
