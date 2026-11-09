# Contributing

Contributions are welcome — whether that's code, bug reports, or ideas via issues and pull requests.

## Guidelines

- **Test your changes** before submitting if at all possible. Run the add-on locally using the devcontainer.
- **AI-assisted contributions are fine**, but please review and clean up generated output before opening a PR. Low-effort slop will be asked to be revised.
- **Use Conventional Commits** to describe your changes. Dependency updates use `fix(deps):`.
- **Do not manually bump the version or edit the changelog.** Releases generate both automatically.

## Releases

Every push to `main` runs semantic-release:

- `fix:` produces a patch release.
- `feat:` produces a minor release.
- `!` or a `BREAKING CHANGE:` footer produces a major release.

Documentation-only changes do not publish a release.

Project contributions are licensed GPL-2.0-only.
