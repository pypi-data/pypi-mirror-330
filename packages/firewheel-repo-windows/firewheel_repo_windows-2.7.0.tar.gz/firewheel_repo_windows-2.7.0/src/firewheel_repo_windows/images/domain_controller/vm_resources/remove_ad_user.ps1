Param(
[Parameter(Mandatory=$True)][string]$name
)
while($true) {
    try {
        Write-Output "Removing user: $name"
        $user = Get-ADUser -Filter {name -like $name}
        if($user.count -eq 0){
            Write-Output "Could not find user"
            start-sleep 5
        } else {
            Get-ADUser -Filter {name -like $name} | Remove-ADUser -Confirm:$False
            break
        }
    } catch {
        Write-Output "User not found, sleeping"
        start-sleep 5
    }
}
