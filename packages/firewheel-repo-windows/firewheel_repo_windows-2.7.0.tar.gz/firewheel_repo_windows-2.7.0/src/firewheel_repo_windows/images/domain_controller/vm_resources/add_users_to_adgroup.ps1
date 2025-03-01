Param(
[Parameter(Mandatory=$True)][string]$users,
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

foreach($user in $users.split(',')) {

    $result = $false
    while($result -ne $true) {
        try {
            try {
                Get-ADGroup -Identity "$group"
            } catch {
                New-ADGroup -Name "$group" -GroupScope Global
                start-sleep 5
                continue
            }
            Add-ADGroupMember "$group" "$username"
            $result = $?
            if($result -ne $true) {
                start-sleep 5
            }
        } catch {
            Write-Output "Group $group does not exist"
            start-sleep 5
        }
    }
}

Exit 0
