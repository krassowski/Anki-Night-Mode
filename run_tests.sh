#!/usr/bin/env bash
source anki_testing/install_anki.sh
pip freeze
python3.6 -m pytest tests
