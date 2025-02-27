# yum adapter

Inmanta module to manage dnf/yum packages in rpm based linux distribution.

## Features

This module supports:
- Installing and deleting rpm packages.
- Managing the rpm repositories of the host.

## Usage example

Here is a simple example of managing the wget package on a remote host via ssh.

```
import yum
import mitogen

svc = yum::Package(host=host, name="wget", purged=false)
host = std::Host(
    name="server",
    os=std::linux,
    via=mitogen::Sudo(
        via=mitogen::Ssh(
            name="server",
            hostname="1.2.3.4",
            port=22,
            username="user",
        ),
    ),
)
```

```{toctree}
:maxdepth: 1
autodoc.rst
CHANGELOG.md
```