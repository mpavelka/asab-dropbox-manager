# asab-dropbox-manager
An ASAB service for managing Dropbox files.

## Prerequisites

```
pip install asab dropbox
```

## Configure

Minimal configuration looks like this:

```
[dropbox]
access_token=[DROPBOX_OAUTH_ACCESS_TOKEN]
```

Store this configuration to `./dboxman.conf`

## Upload files

```
./dboxman.py -c ./dboxman.conf upload -i /path/to/a/file
```
