# main.linux.spec

from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
import os

block_cipher = None

a = Analysis(
    ['backend/index.py'],
    pathex=[],
    binaries=[],
    datas=[('dist/front', 'dist/front')],
    hiddenimports=collect_submodules('webview'),
    hookspath=[],
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'unittest',
        'email',
        'http',
        'xml',
        'html',
        'pydoc_data',
        'multiprocessing',
        'concurrent',
        'asyncio',
        'doctest'
    ],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='taktak_linux',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=True, 
)
