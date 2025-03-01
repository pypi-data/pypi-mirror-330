Param(
[Parameter(Mandatory=$True)][string]$username,
[Parameter(Mandatory=$True)][string]$password,
[Parameter(Mandatory=$False)][string]$domain
)

if(Test-Path "state_file") {
    start-sleep 2
    exit 0
}

if(-not ($PSBoundParameters.ContainsKey('domain'))) {
    $domain = '.'
}

$path = "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\WinLogon"
New-ItemProperty -Path $path -Name AutoAdminLogon -Value 1 -PropertyType String -Force
New-ItemProperty -Path $path -Name DefaultDomainName -Value $domain -PropertyType String -Force
New-ItemProperty -Path $path -Name DefaultUserName -Value $username -PropertyType String -Force
New-ItemProperty -Path $path -Name DefaultPassword -Value $password -PropertyType String -Force

Add-Content -Path "state_file" -Value "ran once"

start-sleep 2
Add-Content -Path "reboot" -Value "reboot"
Exit 10
