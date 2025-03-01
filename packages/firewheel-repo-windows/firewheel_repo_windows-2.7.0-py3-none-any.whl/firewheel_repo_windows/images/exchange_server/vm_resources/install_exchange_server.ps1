param(
[Parameter(Mandatory=$True)][string]$exchangeZip,
[Parameter(Mandatory=$True)][string]$domainController,
[Parameter(Mandatory=$True)][string]$orgName
)

$reboot_file = "reboot"
$state_file = "exchange_run"

if(Test-Path $state_file) {
    Write-Output "exchange: state file exists; exiting"
    start-sleep 2
    Exit 0
}

C:\launch\UcmaRuntimeSetup.exe -q

# Unzip the exchange files
Add-Type -AssemblyName System.IO.Compression.FileSystem
$extractedDir = 'C:\temp'
[System.IO.Compression.ZipFile]::ExtractToDirectory($exchangeZip, $extractedDir)

# Install
C:\temp\exchange_server\Setup.exe /Mode:Install /Roles:Mailbox,ClientAccess,ManagementTools /DomainController:$domainController /InstallWindowsComponents /OrganizationName:$orgName /DisableAMFiltering /IAcceptExchangeServerLicenseTerms /SourceDir:'C:\temp\exchange_server' /CustomerFeedbackEnabled:$False

Add-Content -Path $state_file -Value "done"
Add-Content -Path $reboot_file -Value "reboot"
Exit 10
