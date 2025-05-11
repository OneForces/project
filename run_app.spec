# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=[('ui', 'ui'), ('static', 'static'), ('uploads', 'uploads'), ('C:/Users/nikit/Desktop/project/.venv/Lib/site-packages/PyQt5/Qt/plugins/platforms', 'PyQt5/Qt/plugins/platforms')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='run_app',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='run_app',
)
