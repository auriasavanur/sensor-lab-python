# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all, collect_submodules

# Gather everything Streamlit needs
streamlit_datas, streamlit_binaries, streamlit_hiddenimports = collect_all('streamlit')
streamlit_submodules = collect_submodules('streamlit')

a = Analysis(
    ['gui_app.py'],
    pathex=[],
    binaries=streamlit_binaries,
    datas=[
        ("images/qr_codes/rtd_qr.png", "images/qr_codes"),
        ("images/qr_codes/strain_qr.png", "images/qr_codes"),
        ("images/qr_codes/lvdt_qr.png", "images/qr_codes"),
        ("images/qr_codes/pulse_qr.png", "images/qr_codes")
    ] + streamlit_datas,
    hiddenimports=[
        "importlib_metadata",
        "altair",
        "matplotlib",
        "pandas",
        "numpy"
    ] + streamlit_hiddenimports + streamlit_submodules,
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
    a.binaries,
    a.datas,
    [],
    name='SensorLabDashboard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)