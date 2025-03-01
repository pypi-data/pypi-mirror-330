Param(
[Parameter(Mandatory=$True)][string]$site,
[Parameter(Mandatory=$True)][string]$subnet
)

Import-Module ActiveDirectory

New-ADReplicationSubnet -Name $subnet -Site $site

start-sleep 2
