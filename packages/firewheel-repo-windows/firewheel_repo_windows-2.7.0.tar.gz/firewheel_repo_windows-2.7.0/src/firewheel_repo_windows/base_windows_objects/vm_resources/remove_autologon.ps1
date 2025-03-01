if(Test-Path "state_file") {
    start-sleep 2
    exit 0
}

$path = "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\WinLogon"
New-ItemProperty -Path $path -Name AutoAdminLogon -Value 0 -PropertyType String -Force
New-ItemProperty -Path $path -Name DefaultDomainName -Value "" -PropertyType String -Force
New-ItemProperty -Path $path -Name DefaultUserName -Value "" -PropertyType String -Force
New-ItemProperty -Path $path -Name DefaultPassword -Value "" -PropertyType String -Force

Add-Content -Path "state_file" -Value "ran once"

start-sleep 2
Add-Content -Path "reboot" -Value "reboot"
Exit 10
