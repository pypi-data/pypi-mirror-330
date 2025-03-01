param(
[Parameter(Mandatory=$True)][string]$filepath,
[Parameter(Mandatory=$True)][string]$share,
[Parameter(Mandatory=$True)][string]$username,
[Parameter(Mandatory=$True)][string]$password
)

$name = "SMB" + $share.split('.')[1] + $share.split('\')[-1]
$trigger = New-ScheduledTaskTrigger -AtLogon
$action = New-ScheduledTaskAction -Execute Powershell.exe -Argument "-ExecutionPolicy ByPass $filepath -Share $share"
while ($true) {
    try {
        write-output 'Registering Scheduled Task'
        Register-ScheduledTask -TaskName $name -Trigger $trigger -Action $action -User $username -Password $password -Force
        break
    } catch {
    	write-output $_.Exception.Message
        start-sleep 2
    }
}

while ($true) {
    try {
        write-output 'Modifying Scheduled Task'
        $principal = New-ScheduledTaskPrincipal -UserId $username
        Set-ScheduledTask -TaskName $name -Principal $principal
        break
    } catch {
    	write-output $_.Exception.Message
        start-sleep 2
    }
}
Exit 0
