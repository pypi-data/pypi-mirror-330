Param(
[Parameter(Mandatory=$True)][string]$username,
[Parameter(Mandatory=$True)][string]$group
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

do {
    $result = $false
    try {
        Get-ADGroup -Identity "$group"
        Add-ADGroupMember "$group" "$username"
        $result = $?
        if($result -ne $true) {
            start-sleep 5
        }
    } catch {
        Write-Output "Group $group does not exist"
        start-sleep 5
    }
} while($result -ne $true)

start-sleep 2
exit 0
