Param(
[Parameter(Mandatory=$True)][string]$Users
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

foreach($line in Get-Content $Users) {
    while($true) {
        try {
            $username, $password = $line.split(' ')
            $user = Get-ADUser -Filter "samaccountname -eq '$username'"
            if($user -eq $null) {
                $sec_pass = ConvertTo-SecureString -AsPlainText $password -Force
                New-ADUser -Name $username -AccountPassword $sec_pass -PassThru | Enable-ADAccount
                Write-Output "Added user: $username"
            }
            else {
                # User exists, update its password
                Set-ADAccountPassword -Identity $username -NewPassword (ConvertTo-SecureString -AsPlainText "$password" -Force)
                Write-Output "Changed user password: $username"
            }
            break
        } catch {
            $ErrorMessage = $_.Exception.Message
            $ItemName = $_.Exception.GetType().fullname
            Write-Output "Error: $ItemName -- $ErrorMessage"
            start-sleep 5
        }
    }
}
start-sleep 1
