#!/bin/bash
# Compilazione dell'app Clocki2GSheet per macOS
pyinstaller --onefile --windowed clockify_export_gui.py --name "Clocki2GSheet"
echo "Build completata. Troverai l'app in dist/Clocki2GSheet"
