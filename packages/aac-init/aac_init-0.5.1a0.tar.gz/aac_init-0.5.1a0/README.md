[![Tests](https://github.com/nac-aci/aac-init/actions/workflows/test.yml/badge.svg)](https://github.com/nac-aci/aac-init/actions/workflows/test.yml)
![Python Support](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-informational "Python Support: 3.11, 3.12")

# aac-init

A CLI tool to bootstrap and configure ACI fabric using ACI as Code.

```bash
$ aac-init -h
Usage: aac-init [OPTIONS]

  A CLI tool to bootstrap and configure ACI fabric using ACI as Code.

Options:
  --version                       Show the version and exit.
  -d, --data PATH                 Path to aac-init YAML data files.
                                  [required]
  -l, --log-level [debug|info|warning|error|critical]
                                  Specify the logging level. Default setting
                                  is 'info'.  [default: info]
  -t, --max-switch-concurrent INTEGER
                                  A number of max TFTP concurrent requests.
  -h, --help                      Show this message and exit.
```

All data from the YAML files (`-d/--data` option) will use to bootstrap and configure ACI fabric.

In case there's bandwidth limitation with TFTP server and cannot support a large concurrent switch requests, use `-t` to limit switch concurrent requests, there's no limitation by default.

The data folder **MUST** use following structure, `00-global_policy.yml` and `01-fabric_mgmt.yml` are **mandatory required**, see `docs/data_template` for details.

```bash
data/
├── 00-global_policy.yml      # mandatory, ACI fabric global policies
└── nac_data
    ├── 01-fabric_mgmt.yml    # mandatory, ACI fabric switch connection information
    └── other-yaml-files..    # optional, other ACI as Code configurations
```

## Prerequisite

- Working knowledge of ACI and [Network as Code - ACI](https://netascode.cisco.com/)
- A HTTP/TFTP server is required to store APIC/ACI switch image for wiping/booting APIC/ACI switch to particular version. See `docs/image_server` if you don't have experience on setting up image server.

## Installation

Python 3.10+ is required to install `aac-init`. Don't have Python 3.10 or later? See [Python 3 Getting Started](https://www.python.org/about/gettingstarted/).

`aac-init` can be installed using `pip`:

```bash
pip install aac-init
```

You will also need to install ansible and related NetworkAsCode dependencies, see Cisco [Network As Code - Ansible](https://netascode.cisco.com/solutions/aci/ansible/quick_start/#local-installation) for details. You can also find `requirements.yml/requirements.txt` at `docs/requirements`.

```bash
apt-get install ansible
ansible-galaxy install -r requirements.yml
pip install -r requirements.txt
```

## Usage

```bash
$ aac-init -d data/
Select single or multiple choice(s) to init ACI Fabric:
[1]  Wipe and boot APIC/switch to particular version
[2]  APIC initial setup (Single Pod)
[3]  Init ACI Fabric via NaC (Network as Code)
Example: (1,2,.. or *): *

Are you sure to proceed with the following choice(s)?
[1] Wipe and boot APIC/switch to particular version
[2] APIC initial setup (Single Pod)
[3] Init ACI Fabric via NaC (Network as Code)
 (yes, no) [yes]:
```

## Update aac-init to latest version

```bash
pip install aac-init --upgrade
```

## Uninstallation

```bash
pip uninstall aac-init
```

## FAQ

## Contact

[Rudy Lei](shlei@cisco.com)

## Contributors

[Rudy Lei](shlei@cisco.com)  
[Yang Bian](yabian@cisco.com)  
[Xiao Wang](xiawang3@cisco.com)  
[Song Wang](songwa@cisco.com)  
[Linus Xu](linxu3@cisco.com)  
