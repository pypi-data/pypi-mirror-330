# sshkey-switch

## Overview
sshkey-switch is a command-line utility that allows users to easily switch between multiple SSH keys in the same terminal. It automates the process of managing SSH keys by listing available keys, selecting one interactively, and adding it to the ssh-agent.

## Supported Operating System
- Mac Os
- Linux

## Features
- Lists all valid SSH private keys from `~/.ssh/`
- Allows interactive selection of an SSH key
- Automatically starts `ssh-agent` if not running
- Removes previously added SSH keys before adding the new one
- Stores recently used keys for quick selection
- Provides instructions to activate the environment variables

## Installation
```sh
# pip install sshkey-switch
```

## Usage
```sh
# sshkey-switch
```
Follow the on-screen instructions to select an SSH key.

## Example Output
```
# sshkey-switch
? Select SSH private key: (Use arrow keys)
 » deploy1 *recent
   github_repo1
   id_rsa
   gitlab_repo2
✅ SSH key switched to: ~/.ssh/github_key
✅ ssh-agent is working correctly.
```

## Notes
- Ensure you run `source ~/.bashrc` if prompted to activate environment variables.
- The script only lists valid SSH private keys and excludes public keys or other files.

## License
This project is licensed under the MIT License.

