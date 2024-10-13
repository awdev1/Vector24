# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
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
    name='Vector24',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  
    icon='icon.icns'  
)

app = BUNDLE(
    exe,
    name='Vector24.app',  
    icon='icon.icns',     
    bundle_identifier='com.awdev.vector24',  
)
