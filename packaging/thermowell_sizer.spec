# -*- mode: python ; coding: utf-8 -*-
# Empaquetado de ThermoWell Sizer con PyInstaller (carpeta única, sin consola).
#   pyinstaller packaging/thermowell_sizer.spec --noconfirm
# Resultado: dist/ThermoWellSizer/ThermoWellSizer(.exe)
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules

ROOT = Path(SPECPATH).parent  # noqa: F821 - lo define PyInstaller
SRC = ROOT / "src"

datas = [
    (str(SRC / "thermowell_sizer" / "assets"), "thermowell_sizer/assets"),
    (str(SRC / "thermowell_sizer" / "data" / "schema.sql"), "thermowell_sizer/data"),
    (str(ROOT / "LICENSE.txt"), "."),
]
datas += collect_data_files("CoolProp")
datas += collect_data_files("reportlab")
datas += collect_data_files("docx")
binaries = collect_dynamic_libs("CoolProp")
hidden = (
    collect_submodules("thermowell_sizer")
    + collect_submodules("CoolProp")
    + ["matplotlib.backends.backend_qtagg", "matplotlib.backends.backend_agg",
       "reportlab.graphics.barcode", "openpyxl", "docx"]
)

a = Analysis(  # noqa: F821
    [str(ROOT / "packaging" / "launcher.py")],
    pathex=[str(SRC)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden,
    excludes=[
        "tkinter", "PyQt5", "PyQt6", "PySide2", "IPython", "pytest", "pandas",
        # Módulos de Qt que el programa no usa (reducen mucho el tamaño).
        "PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets", "PySide6.QtWebEngineQuick",
        "PySide6.QtWebChannel", "PySide6.QtWebSockets", "PySide6.Qt3DCore",
        "PySide6.Qt3DRender", "PySide6.Qt3DExtras", "PySide6.Qt3DInput", "PySide6.Qt3DLogic",
        "PySide6.Qt3DAnimation", "PySide6.QtQuick", "PySide6.QtQuick3D", "PySide6.QtQml",
        "PySide6.QtQuickWidgets", "PySide6.QtMultimedia", "PySide6.QtMultimediaWidgets",
        "PySide6.QtCharts", "PySide6.QtDataVisualization", "PySide6.QtGraphs",
        "PySide6.QtLocation", "PySide6.QtPositioning", "PySide6.QtBluetooth",
        "PySide6.QtNfc", "PySide6.QtSerialPort", "PySide6.QtSensors", "PySide6.QtSql",
        "PySide6.QtTest", "PySide6.QtDesigner", "PySide6.QtHelp", "PySide6.QtPdf",
        "PySide6.QtPdfWidgets", "PySide6.QtRemoteObjects", "PySide6.QtScxml",
        "PySide6.QtSpatialAudio", "PySide6.QtTextToSpeech", "PySide6.QtHttpServer",
    ],
    noarchive=False,
)
pyz = PYZ(a.pure)  # noqa: F821
exe = EXE(  # noqa: F821
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ThermoWellSizer",
    console=False,
    icon=str(ROOT / "packaging" / "thermowell_sizer.ico"),
)
coll = COLLECT(exe, a.binaries, a.datas, name="ThermoWellSizer")  # noqa: F821
