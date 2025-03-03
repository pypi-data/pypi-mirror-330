# Plex Content Manager

[![PyPI version](https://img.shields.io/pypi/v/plexcontentmanager.svg)](https://pypi.org/project/plexcontentmanager/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/github/stars/alexboutros/plexcontentmanager?style=social)](https://github.com/alexboutros/plexcontentmanager)

A command-line tool for managing and curating Plex Media Server content.

## Features

- Connect to your Plex server securely
- List all empty collections across your libraries
- Delete empty collections with confirmation
- Batch operations with force option to skip confirmations

## Installation

### From PyPI (Recommended)

```bash
pip install plexcontentmanager
```

### From Source
```bash
git clone https://github.com/alexboutros/plexcontentmanager.git
cd plexcontentmanager
pip install -e .
```

## Security & Privacy

This application stores your Plex token locally in `~/.plexcontentmanager/config.json`. The token is:
- Never transmitted to any server other than your specified Plex server
- Stored as plaintext in the configuration file
- Only used to authenticate with your Plex server

For security reasons:
- The source code is available on [GitHub](https://github.com/alexboutros/plexcontentmanager) for review
- You can optionally use a dedicated Plex account with limited permissions for this tool
- You can delete the configuration file (`~/.plexcontentmanager/config.json`) when not in use

