#!/bin/bash

CURRENT_DIR="$(dirname "$(realpath "$0")")"

"$CURRENT_DIR/export.py"

"$CURRENT_DIR/card_fix.py"
"$CURRENT_DIR/cover_fix.py"
"$CURRENT_DIR/friends_updater.py"
"$CURRENT_DIR/reading_sync.py"
