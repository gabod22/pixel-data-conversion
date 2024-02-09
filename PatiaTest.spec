# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['PatiaTest.py'],
    pathex=[],
    binaries=[],
    datas=[('config_files/*', 'config_files'), ('programs/*', 'programs'), ('assets/*', 'assets'), ('.env', '.')],
    hiddenimports=['pywintypes'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PatiaTest',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon=['C:\\Users\\brian\\Proyectos\\patiatest\\assets\\logo_min.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PatiaTest',
)
