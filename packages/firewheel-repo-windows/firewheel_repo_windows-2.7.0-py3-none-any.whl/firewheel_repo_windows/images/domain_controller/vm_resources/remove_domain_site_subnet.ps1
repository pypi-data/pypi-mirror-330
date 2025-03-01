Param(
[Parameter(Mandatory=$True)][string]$subnet
)

Import-Module ActiveDirectory

Remove-ADReplicationSubnet -Identity $subnet -Confirm:$False

start-sleep 2
