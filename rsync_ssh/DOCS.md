# Setup

1. Mount an **ext4** disk in Home Assistant Storage with **Media** usage,
   for example `/media/backup_disk`. Its root must be owned by `root:root` with mode `755`.
2. Configure the add-on with the client's public key and a folder name:

   ```yaml
   authorized_keys:
     - "ssh-ed25519 AAAA... backups"
   storage_root: /media/backup_disk
   directory: friend
   ```

3. Start the add-on. It creates the folder with UID/GID `1000` and mode `700`.
   Use an empty folder or ensure existing files belong to UID/GID `1000`.
4. Connect as **`backup`** on SSH port **`2222`**. Verify the host-key fingerprint
   against the add-on log on the first connection.

To use internal storage temporarily, set `storage_root: /media` and `directory: backup`.

All configured keys access the same folder. Only rsync is supported; shell and
SFTP access are disabled. The disk must remain mounted; restart the add-on after
reconnecting it.

# Usage

Replace `HA_HOST` with your server address. Remote paths are relative to the
configured folder. Add `-i /path/to/private_key` to the SSH command if needed.

```bash
# Upload
rsync -rt --partial -e 'ssh -p 2222' ~/backups/ backup@HA_HOST:./

# List stored files
rsync --list-only -r -e 'ssh -p 2222' backup@HA_HOST:./

# Restore all files
rsync -rt --partial -e 'ssh -p 2222' backup@HA_HOST:./ ~/restored-backups/

# Restore one file
rsync -e 'ssh -p 2222' backup@HA_HOST:./example.tar ~/Downloads/
```
