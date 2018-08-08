#!/bin/bash
cd night_mode
zip -r night_mode.zip * -x __pycache__/* -x __pycache__/
cp night_mode.zip ..
