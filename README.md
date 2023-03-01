## SD WebUi Connect Extension

This is extension for [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
This is an Connector for saving image to remote repositories E.g. GDrive, SFTP, SMB, etc.(In future implemetaions)


# Installing
Go Extensions tab -> Install from url -> paste repo url -> install

```bash
https://github.com/Maszz/sd-web-ui-connect-extention.git
```

# Feature

    - Gdrive With Oauth authentication(not supported service account)
    - SMB Connection
    - SFTP Connection

When you want to connect to new google oauth account you need to delete credentials.json in extensions folder
by default this extension try to find access token in credentials.json file(**Don't exposed your credentials.json)

# Troubleshooting
for mac user that stuck with can't find /usr/lib/libffi.8.dylib when you install libffi from homebrew, homebrew install libffi in `/opt/homebrew/opt/libffi/lib/libffi.8.dylib`, but python find it from /usr/lib/libffi.8.dylib you need to link the binary from `/opt/homebrew/opt/libffi/lib/libffi.8.dylib` to `/usr/lib/libffi.8.dylib`.(if SIP disable,you can link it direcly)

for user with SIP enabled you need to linked it to `/usr/local/lib/libffi.8.dylib` intread(python use this path for alternative when can't find it on `/usr/lib/libffi.8.dylib`)

```bash
sudo ln -s /opt/homebrew/opt/libffi/lib/libffi.8.dylib /usr/local/lib/libffi.8.dylib  
```


# Authors
- [Maszz](https://github.com/Maszz)
sd-web-ui-connect-extention