Param(
[Parameter(Mandatory=$True)][string]$name,
[Parameter(Mandatory=$True)][string]$path
)

while($true) {
    try {
        Import-Module ActiveDirectory
        break
    } catch {
        Write-Output "Could not import Active Directory module, sleeping and trying again"
        start-sleep 5
    }
}

New-ADOrganizationalUnit -Name $name -Path $path

$ecode = $?

start-sleep 1

Exit $ecode
