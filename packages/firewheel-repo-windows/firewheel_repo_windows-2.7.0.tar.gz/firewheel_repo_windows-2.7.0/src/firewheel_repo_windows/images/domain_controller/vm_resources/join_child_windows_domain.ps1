# Join the domain.

Param(
[Parameter(Mandatory=$True)][string]$domain_name,
[Parameter(Mandatory=$True)][string]$admin_user,
[Parameter(Mandatory=$True)][string]$admin_password,
[Parameter(Mandatory=$True)][string]$domain_controller_ip
)

# Set up paths for rebooting.
$reboot_file = "reboot"
$state_file = "domain_join_run"

Write-Output "join_windows_domain: starting agent"
Add-Content -Path "output" -Value "join_windows_domain: starting agent"

if(Test-Path $state_file) {
    Write-Output "join_windows_domain: state file exists; exiting"
    start-sleep 2
    Exit
}
try {

    # First, set the DNS server to the domain controller.
    Write-Output "join_windows_domain: setting DNS server to the domain controller IP"
    Add-Content -Path "output" -Value "join_windows_domain: setting DNS server to the domain controller IP"
    Get-WmiObject win32_networkadapterconfiguration -filter "ipenabled = 'true'" | ForEach-Object { $_.SetDNSServerSearchOrder($domain_controller_ip) }

    # Next, actually issue the domain join.
    # For this operation, we need a domain user that can add machines.

    # We must specify a "qualified" username (that is, DOMAIN\user). To do this
    # we need the NetBIOS/WINS name for the domain. We have prior knowledge of
    # the DC IP address, so we can use that to find the 1C record--the domain's
    # name.
    Write-Output "join_windows_domain: beginning nbtstat loop"
    Add-Content -Path "output" -Value "join_windows_domain: beginning nbtstat loop"
    do {
        Write-Output "join_windows_domain: sleeping 30 sec"
        Add-Content -Path "output" -Value "join_windows_domain: sleeping 30 sec"
        Start-Sleep -s 30
        Write-Output "join_windows_domain: calling nbtstat"
        Add-Content -Path "output" -Value "join_windows_domain: calling nbtstat"
        $NBName = nbtstat -A $domain_controller_ip | Select-String -Pattern "^ *(.*) *<1C>.*$" | % {$_ -replace '^ *(.*) *<1C>.*$','$1'}
        Write-Output "join_windows_domain: nbtstat finished, NBName: $NBName"
        Add-Content -Path "output" -Value "join_windows_domain: nbtstat finished, NBName: $NBName"

    } while ($NBName -eq $null)
    Write-Output "join_windows_domain: finished nbtstat loop"
    Add-Content -Path "output" -Value "join_windows_domain: finished nbtstat loop"

    # How we join changes with PowerShell 3.0. Before 3.0, there is no
    # confirmation dialog. After 3.0, the -Force argument is added to suppress
    # a dialog. We must behave appropriately.
    # Make sure we retry on error--otherwise we have a race condition when
    # NetBIOS resolves before the DC properly responds.
    if ($PSVersionTable['PSVersion'].Major -lt 3) {
        $add_block = {
            # (Apparently because we're passing a complex object, as opposed to a
            # list, or maybe because we care about the type when we pass to
            # -Credential) we are given a "GetReadEnumerator" object as $input.
            # The easiest way to get a PSCredential object like we want is to use
            # a pipe. The value stored in $c ends up being a PSCredential object,
            # which is what we are expecting in the call to add-computer.
            # See http://powershell.org/wp/2010/06/03/a-look-at-powershell-jobs-part-1/
            $c = $input | %{$_}
            $domain_name = $args[0]
            add-computer -Credential $c -DomainName $domain_name
        }
    }
    else {
        $add_block = {
            $c = $input | %{$_}
            $domain_name = $args[0]
            add-computer -Credential $c -DomainName $domain_name -Force
        }
    }

    do {
        do {
            Write-Output "join_windows_domain: sleeping 2 sec for second nbtstat"
            Add-Content -Path "output" -Value "join_windows_domain: sleeping 2 sec for second nbtstat"
            Start-Sleep -s 2
            Write-Output "join_windows_domain: calling second nbtstat"
            Add-Content -Path "output" -Value "join_windows_domain: calling second nbtstat"
            $NBName = nbtstat -A $domain_controller_ip | Select-String -Pattern "^ *(.*) *<1C>.*$" | % {$_ -replace '^ *(.*) *<1C>.*$','$1'}
            Write-Output "join_windows_domain: second nbtstat finished, NBName: $NBName"
            Add-Content -Path "output" -Value "join_windows_domain: second nbtstat finished, NBName: $NBName"
        } while ($NBName -eq $null)
        $User = $NBName.Trim() + "\$admin_user"
        $PWord = ConvertTo-SecureString -String $admin_password -AsPlainText -Force
        $Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, $PWord
        Write-Output "join_windows_domain: credential generated: $Credential"
        Add-Content -Path "output" -Value "join_windows_domain: credential generated: $Credential"

        Write-Output "join_windows_domain: detected powershell < 3, not including 'Force', calling add-computer"
        Add-Content -Path "output" -Value "join_windows_domain: detected powershell < 3, not including 'Force', calling add-computer"
        # Use a background job so we can have a timeout and retry if this hangs
        # The hang may happen, especially at density.
        # We have chosen the name and timeout arbitrarily
        $join_job = Start-Job -Name "domain" -scriptblock $add_block -InputObject $Credential -ArgumentList $domain_name
        Wait-Job -Id $join_job.Id -Timeout 120
        # Check the state of the job. According to https://technet.microsoft.com/library/hh847783.aspx
        # we are looking for a state of "Completed".
        Write-Output "Join job state:  $join_job.State."
        Add-Content -Path "output" -Value "Join job state:  $join_job.State."
        if ($join_job.State -eq "Completed") {
            $cs = Get-WmiObject Win32_ComputerSystem
            if ($cs.Domain -ne $domain_name) {
                Write-Output "Domain join completed but failed."
                Add-Content -Path "output" -Value "Domain join completed but failed: $cs.Domain"
                $joined = $False
            }
            else {
                Write-Output "Domain join completed successfully."
                Add-Content -Path "output" -Value "Domain join completed successfully."
                $joined = $True
            }
            Write-Output "join_windows_domain: joined: $joined"
            Add-Content -Path "output" -Value "join_windows_domain: joined: $joined"
        }
        else {
            $joined = $False
            Stop-Job -Id $join_job.Id
            Remove-Job -Id $join_job.Id

            Write-Output "join_windows_domain: joined: $joined"
            Add-Content -Path "output" -Value "join_windows_domain: joined: $joined"

            # Wait a random time.
            $Timer = Get-Random -Maximum 60 -Minimum 1
            Write-Output "Sleeping $Timer"
            Add-Content -Path "output" -Value "Sleeping $Timer"
            Start-Sleep $Timer
        }
    } while( $joined -eq $False)

} catch {
    $ErrorMessage = $_.Exception.Message
    $ItemName = $_.Exception.ItemName
    Add-Content -Path "output" -Value "Caught exception from item $ItemName -- $ErrorMessage"
}

Write-Output "join_windows_domain: finished joining, alerting for reboot"
Add-Content -Path "output" -Value "join_windows_domain: finished joining, alerting for reboot"

# Inform the launcher we need to reboot.
Add-Content -Path $reboot_file -Value "reboot"
# Make sure we know we've run.
Add-Content -Path $state_file -Value "ran already"

while(!(Test-Path "reboot")) {
    start-sleep 1
}

Write-Output "join_windows_domain: exiting"
Add-Content -Path "output" -Value "join_windows_domain: exiting"
Exit 10
