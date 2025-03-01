Param(
[Parameter(Mandatory=$True)][string]$hostname
)

if(Test-Path "state_file") {
    Exit 0
}

while($true) {
    try {
        $simplified_hostname = $hostname.split('.')[0]

        $computer_info = Get-WmiObject Win32_ComputerSystem

        # If it is named correctly, we can exit.
        if($computer_info.name -eq $simplified_hostname) {
            Exit 0
        }

        $computer_info.Rename($simplified_hostname)

        start-sleep 1

        # NOTE: Setting the hostname on windows generally requires a reboot for
        # it to take effect. Exit code 10 will trigger this.
        Add-Content -Path "state_file" -Value "ran once"
        Exit 10
    } catch {
        $ErrorMessage = $_.Exception.Message
        $ItemName = $_.Exception.ItemName
        Write-Output "$ItemName -- $ErrorMessage"
    }
    start-sleep 2
}
