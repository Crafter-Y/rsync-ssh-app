# SPDX-License-Identifier: GPL-2.0-only
"""Configuration and mounted-storage checks shared by startup and sessions."""
import json
import os
from pathlib import Path
import re
import stat

SETTINGS = Path('/etc/rsync-ssh.json')

def mount_path(value):
    return re.sub(r'\\([0-7]{3})', lambda m: chr(int(m[1], 8)), value)

def mount_identity(root):
    for line in Path('/proc/self/mountinfo').read_text().splitlines():
        fields = line.split()
        if mount_path(fields[4]) == str(root):
            split = fields.index('-')
            return [fields[2], mount_path(fields[3]), *fields[split + 1:split + 3]]
    raise ValueError(f'{root} is not a mounted disk; refusing internal-storage fallback')

def check_storage(root, expected=None):
    root = Path(root)
    if not root.is_absolute() or not root.is_relative_to('/media'):
        raise ValueError('storage_root must be /media or a mounted directory below it')
    if '..' in root.parts or str(root.resolve(strict=True)) != str(root):
        raise ValueError('storage_root must exist and must not contain symlinks or ..')
    identity = mount_identity(root)
    details = root.stat()
    if details.st_uid != 0 or details.st_mode & 0o022:
        raise ValueError('storage_root must be root-owned and not group/other-writable (use ext4)')
    if not details.st_mode & 0o001:
        raise ValueError('storage_root must allow directory traversal; use root:root mode 755')
    observed = {'mount': identity, 'device': details.st_dev, 'inode': details.st_ino}
    if expected is not None and observed != expected:
        raise ValueError('storage mount changed; restart the app after checking the disk')
    return observed

def open_directory(root, directory, identity):
    # Open relative to the verified disk, refusing a symlink as the export root.
    check_storage(root, identity)
    root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        disk = os.fstat(root_fd)
        if (disk.st_dev, disk.st_ino) != (identity['device'], identity['inode']):
            raise ValueError('storage changed while opening it')
        fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=root_fd)
        details = os.fstat(fd)
        if not stat.S_ISDIR(details.st_mode) or details.st_dev != disk.st_dev:
            os.close(fd)
            raise ValueError('backup directory must be on the configured disk')
        check_storage(root, identity)
        return fd
    finally:
        os.close(root_fd)
