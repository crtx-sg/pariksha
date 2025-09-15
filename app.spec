# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect Streamlit files
streamlit_data = collect_data_files('streamlit')

# Collect markdown-pdf data
markdown_pdf_data = collect_data_files('markdown_pdf')

# Hidden imports for Streamlit and dependencies
hidden_imports = [
    'streamlit',
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner.script_runner',
    'streamlit.runtime.state',
    'streamlit.components',
    'streamlit.components.v1',
    'markdown',
    'markdown_pdf',
    'markdownpdf',
    'markdown_it_py',
    'json',
    'tempfile',
    'base64',
    'webbrowser',
    'socket',
    'threading',
    'subprocess',
    'PyMuPDF',
    'fitz'
]

# Add all streamlit submodules
hidden_imports.extend(collect_submodules('streamlit'))
hidden_imports.extend(collect_submodules('markdown_pdf'))

block_cipher = None

a = Analysis(
    ['launch_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app.py', '.'),
        ('README.md', '.'),
        ('requirements.txt', '.'),
        *streamlit_data,
        *markdown_pdf_data,
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Pariksha',
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
    icon=None,  # Add icon path here if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Pariksha',
)