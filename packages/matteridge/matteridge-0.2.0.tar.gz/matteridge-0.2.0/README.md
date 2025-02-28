# matteridge

A
[feature-rich](https://slidge.im/docs/matteridge/main/features.html)
[Mattermost](https://mattermost.com) to
[XMPP](https://xmpp.org/) puppeteering
[gateway](https://xmpp.org/extensions/xep-0100.html), based on
[slidge](https://slidge.im) and
[mattermost-api-reference-client](https://git.sr.ht/~nicoco/mattermost-api-reference-client).

[![PyPI package version](https://badge.fury.io/py/matteridge.svg)](https://pypi.org/project/matteridge/)
[![CI pipeline status](https://ci.codeberg.org/api/badges/14070/status.svg)](https://ci.codeberg.org/repos/14070)
[![Chat](https://conference.nicoco.fr:5281/muc_badge/slidge@conference.nicoco.fr)](https://conference.nicoco.fr:5281/muc_log/slidge/)

## Installation

Refer to the [slidge admin documentation](https://slidge.im/docs/slidge/main/admin/)
for general info on how to set up an XMPP server component.

### Containers

From [the codeberg package registry](https://codeberg.org/slidge/-/packages?q=&type=container)

```sh
docker run codeberg.org/slidge/matridge
```

### Python package

With [pipx](https://pypa.github.io/pipx/):

```sh

# for the latest stable release (if any)
pipx install matridge

# for the bleeding edge
pipx install matridge==0.0.0.dev0 \
    --pip-args='--extra-index-url https://codeberg.org/api/packages/slidge/pypi/simple/'

# to update bleeding edge installs
pipx install matridge==0.0.0.dev0 \
    --pip-args='--extra-index-url https://codeberg.org/api/packages/slidge/pypi/simple/' --force

matridge --help
```

## Dev

```sh
git clone https://codeberg.org/slidge/matteridge
cd matteridge
docker-compose up
```
