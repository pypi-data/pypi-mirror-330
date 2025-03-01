Param(
[Parameter(Mandatory=$True)][string]$username,
[Parameter(Mandatory=$True)][string]$password
)

net user $username $password

start-sleep 1
