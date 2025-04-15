# Proxmox Node role

This role installs and configures a Proxmox node,
that is a server which is part of a Proxmox cluster.

It take cares of:
* installing ZFS
* installing and configuring Proxmox
* configure network interfaces

## Creating partitions

You can declare partitions to ensure they are as expected.

By default this is just a check.

If you need to remove/create them then you will need to add
`-e proxmox_node_mkparts=true` to you ansible-playbook command line.

You might also bring modifications manually on the host,
and check back by running ansible again.

This prevent altering partitions by error !
