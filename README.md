

# Open Food Facts Ops

## Pre-requisite

* git
* python3 (>3.7)
* pip
* virtualenv

### Installation by Platform

#### Debian-based Linux
```bash
sudo apt install git python3 python3-pip python3-venv
```

#### OSX
```bash
brew install git python
python3 -m ensurepip --upgrade
pip3 install virtualenv
```

#### Windows (using WSL)
```bash
sudo apt install git python3 python3-pip python3-venv   
```

## Setup

Clone the repository:
```bash
git clone git@github.com:openfoodfacts/openfoodfacts-ops.git
cd openfoodfacts-ops
```

Create and activate virtual environment:
```bash
python3 -m venv ./venv
source venv/bin/activate
```

Install dependencies
```bash
python3 -m pip install -r requirements.pip
ansible-galaxy install -r requirements.yml
```


## Usage


### Verify Installation
```bash
ansible all -m ping
```


### Common Tasks

#### Configure Servers
```bash
ansible-playbook jobs/configure.yml
```

#### Deploy Monitoring
```bash
ansible-playbook sites/monitoring.openfoodfacts.org.yml
```

#### User Management

##### Add New User
1. Edit `group_vars/all/sshd.yml` to add user to `sshd_github_authorized_users`
2. Run:
```bash
ansible-playbook jobs/configure.yml
```

##### Revoke User Access
1. Remove user from `sshd_github_authorized_users`
2. Add to `sshd_github_revoked_users`
3. Run:
```bash
ansible-playbook jobs/configure.yml
```



## Repository structure

```
├── docs                                # Documentation in Markdown
│   ├── index.md
│   ├── *.md
│   └── ...
├── group_vars                          # Configuration per group
│   ├── all                             # Common configuration
│   │   ├── base.yml
│   │   └── sshd.yml
│   ├── group-1
│   │   ├── config.yml                  # Configuration of group in plain text
│   │   └── secret.yml                  # Configuration of group encrypted
│   └── group-X.yml                     # Configuration of group in a single file
├── host_vars                           # Configuration per host
│   ├── server-XX.yml                   
│   └── server-YY.yml                   
├── jobs                                # Maintenance tasks as playbooks
│   ├── configure.yml
│   └── ...
├── keys                                # SSH keys
│   ├── default.pub                     # default public key
│   └── ... 
├── plugins                             # Ansible plugins
│   ├── filters
│   ├── lookup
│   └── ...
├── roles                               # Ansible roles
│   ├── role-X
│   └── ...
├── sites                               # Ansible playbooks to deploy sites
│   ├── public.url.yml
│   └── ...
├── .gitattributes                      # Specifies (among others) the files to encrypt
├── .gitignore                          # Files ignored by git
├── ansible.cfg                         # Ansible configuration for this repository
├── inventory.production.ini            # Ansible inventory: all servers are there
├── requirements.pip                    # Python dependencies
└── requirements.yml                    # Ansible dependencies

## Contributing

Please use ansible-lint before submitting a PR.
