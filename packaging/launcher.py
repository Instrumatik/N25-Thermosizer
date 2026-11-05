"""Punto de entrada del ejecutable empaquetado con PyInstaller."""

import sys

from thermowell_sizer.ui.app import main

if __name__ == "__main__":
    sys.exit(main())
