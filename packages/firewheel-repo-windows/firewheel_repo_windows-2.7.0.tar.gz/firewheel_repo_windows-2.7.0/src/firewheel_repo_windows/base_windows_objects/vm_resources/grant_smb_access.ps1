Param(
[Parameter(Mandatory=$True)][string]$name,
[Parameter(Mandatory=$True)][string]$account
)

Grant-SmbShareAccess -Name $name -AccountName $account -AccessRight Full -Force

$ecode = $?

start-sleep 2

Exit $ecode
