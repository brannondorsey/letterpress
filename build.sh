#!/bin/bash
pyinstaller --onefile src/keylogger.py
rm -rf build
mv dist/keylogger keylogger
rmdir dist
rm keylogger.spec