# Set up paths for rebooting.
Param(
[Parameter(Mandatory=$True)][string]$domain,
[Parameter(Mandatory=$True)][string]$netBiosName,
[Parameter(Mandatory=$True)][string]$safe_mode_admin_password,
[Parameter(Mandatory=$False)][string]$upstream_dns,
[Parameter(Mandatory=$False)][string]$site
)

$reboot_file = "reboot"
$state_file = "install_domain_finished"
$winfeatures_state_file = "windows_features_finished"

# If we've run before, just exit--we're done.
if(Test-Path $state_file) {
    start-sleep 2
    Exit 0
}

$OS = Get-WmiObject -class Win32_Operatingsystem

If ($OS.caption -match '2012') { 
    # Install the domain controller components for Server 2012
    if(Test-Path $winfeatures_state_file) {
        while($true) {
            try {
                Write-Output "Importing ServerManager"
                Import-Module ServerManager
                break
            } catch {
                Write-Output "Could not import ServerManager, sleeping and trying again"
                start-sleep 5
            }
        }

        while($true) {
            try {
                if($upstream_dns) {
                    Set-DnsServerForwarder -IPAddress $upstream_dns
                }
                break
            } catch {
                Write-Output "Failed adding DNS Forwarding, sleeping and trying again"
                start-sleep 5
            }
        }

        $ecode = $LastExitCode

        # Make sure we know we've run.
        Add-Content -Path $state_file -Value "ran twice"

        Add-Content -Path $reboot_file -Value "reboot"
        Exit 10
    } else {
        Get-WindowsFeature AD-Domain-Services
        Write-Output "Installaing AD-Domain-Services"
        Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools
        Import-Module ADDSDeployment
        Write-Output "Imported ADDSDeployment"

        if($PSBoundParameters.ContainsKey('site')) {
            $parent_netbios = $domain.split('.')[0]
            $username = "$parent_netbios\Administrator"
            $password = ConvertTo-SecureString -String $safe_mode_admin_password -AsPlainText -Force
            $Credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $username, $password
            Install-ADDSDomain -NoGlobalCatalog:$true `
                -DomainMode "Win2012R2" -DomainType "ChildDomain" `
                -ParentDomainName "$domain" -InstallDns:$false `
                -NewDomainName "$netBiosName" -NewDomainNetbiosName "$netBiosName" `
                -SiteName "$site" -Credential $Credential `
                -SafeModeAdministratorPassword (ConvertTo-SecureString -AsPlainText -Force "$safe_mode_admin_password") `
                -Force:$true
        } else {
            while($true) {
                try {
                    Install-ADDSForest -DomainName "$domain" -DomainNetbiosName "$netBiosName" `
                        -Force -NoRebootOnCompletion `
                        -SafeModeAdministratorPassword (ConvertTo-SecureString -AsPlainText -Force "$safe_mode_admin_password")

                    break
                } catch {
                    Write-Output $_.Exception.Message
                    start-sleep 2
                }
            }
        }

        $ecode = $LastExitCode

        # Create state file for pre-DCPROMO
        Add-Content -Path $winfeatures_state_file -Value "ran once"

        # Inform the launcher we need to reboot.
        Add-Content -Path $reboot_file -Value "reboot"
        Exit 10
    }
}
ElseIf ($OS.caption -match '2008') { 
    # Run dcpromo to promote if Windows features have been installed
    if(Test-Path $winfeatures_state_file) {
        $command = @'
dcpromo.exe /unattend /InstallDns:yes /dnsOnNetwork:yes /replicaOrNewDomain:domain /newDomain:forest /newDomainDnsName:$domain /DomainNetbiosName:$netBiosName /safeModeAdminPassword:"$safe_mode_admin_password" /forestLevel:4 /domainLevel:4 /rebootOnCompletion:no
'@
        Invoke-Expression -Command:$command


        # Make sure we know we've run.
        echo $command > $state_file

        # Inform the launcher we need to reboot.
        Add-Content -Path $reboot_file -Value "reboot"

        while(!(Test-Path $reboot_file)) {
            start-sleep 1
        }

        Exit
    } else {
        # Install the domain controller components for Server 2008 R2 
        Import-Module ServerManager
        while($true) {
            try {
                Get-WindowsFeature AD-Domain-Services | Add-WindowsFeature
                break
            } catch {
                Write-Output "Error while installing AD Domain Services, sleeping and trying again"
                start-sleep 5
            }
        }

        # Create state file for pre-DCPROMO
        Add-Content -Path $winfeatures_state_file -Value "ran once"

        # Inform the launcher we need to reboot.
        Add-Content -Path $reboot_file -Value "reboot"

        while(!(Test-Path "reboot")) {
            start-sleep 1
        }

        Exit
    }
    
}
