# Rsync SSH Home Assistant Add-on Repository

[![License: GPL-2.0-only][license-shield]](LICENSE.md)

## Add-ons

This repository contains the following add-ons:

### [Rsync SSH][addon-rsync-ssh]

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

An rsync backup destination with SSH public-key authentication, encrypted transfers,
and access restricted to one directory on a mounted disk.

## Installation

### One-click install

Click the button below to add this repository to your Home Assistant instance:

[![Add this repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FCrafter-Y%2Frsync-ssh-app)

Then find the **Rsync SSH** add-on in the store and install it.

### Manual install

1. Navigate in your Home Assistant frontend to **Settings** → **Add-ons** → **Add-on Store**.
2. Click the three-dot menu (⋮) in the top-right corner and select **Repositories**.
3. Add this repository URL: `https://github.com/Crafter-Y/rsync-ssh-app`
4. Find the **Rsync SSH** add-on and install it.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

rsync-ssh-app (c) by Crafter-Y

This project is licensed under **GNU GPL version 2 only**. See [LICENSE.md](LICENSE.md).

Published container images also include rsync/rrsync under GPL-3.0-or-later
and OpenSSH under its BSD-style licenses. These programs retain their upstream licenses.

[addon-rsync-ssh]: rsync_ssh/DOCS.md
[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[license-shield]: https://img.shields.io/badge/License-GPL--2.0--only-blue.svg
