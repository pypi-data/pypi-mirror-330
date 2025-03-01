# edwh-multipass-plugin

[![PyPI - Version](https://img.shields.io/pypi/v/edwh-multipass-plugin.svg)](https://pypi.org/project/edwh-multipass-plugin)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/edwh-multipass-plugin.svg)](https://pypi.org/project/edwh-multipass-plugin)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [mp.fix-host](#mpfix-host)
- [mp.install](#mpinstall)
- [mp.prepare](#mpprepare)

## Installation

Install just this plugin:

```console
pip install edwh-multipass-plugin
```

But probably you want to install the whole `edwh` package:

```console
pipx install edwh[plugins,omgeving]
# or
pipx install edwh[multipass]
```

if you want to use the `edwh` command line tool with just the `multipass` plugin:

```console
pipx install edwh
edwh plugin.add multipass
```

---

## mp.fix-host
>  aka `mp.fix-dns`

Fixes the ip adres in the hosts file for a multipass instance.

When issuing on the first run fix-host will add an entry to your hosts file, and you can enter 
different hostnames you want to register for the instance.

```
mp.fix-host dockers -h dockers.local -h delen.dockers.local -h web2py.dockers.local ... 
```

After this initial registration, you can update the ip address of the instance by running `mp.fix-host dockers` again.
Be aware that you cannot register new hostnames after the initial registration. Update your 
`/etc/hosts` file instead. 

---
## mp.install 
Installs multipass on an ubuntu based machine if not already installed. 


---
## mp.prepare 
Allows you to ssh into a multipass instance, so you are able to run fabric commands against it. 


`mp.prepare` will generate a multipass_keyfile `~/.ssh/multipass.key` (if not already present) 
and add the public key to the multipass instance's `authorized_keys` file. 

`mp.prepares` automatically runs `mp.install`. 

---
## License

`edwh-multipass-plugin` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
See [the license](LICENSE.txt) for details. 
