param(
[Parameter(Mandatory=$True)][string]$ips
)

if(Test-Path "state_file") {
    start-sleep 2
    Exit 0
}

foreach($line in Get-Content $ips) {
    $mac, $ip, $netmask, $gateway, $dns = $line.split(' ')
    while($True) {
        $nic = get-wmiobject win32_networkadapterconfiguration -filter "macaddress = '$mac'"
        if(!$nic) {
            write-output "Could not find $mac, sleeping"
            start-sleep 2
            continue
        }
        write-output "Setting $mac to $ip"
        $nic.EnableStatic($ip, $netmask)
        if(-Not $?) {
            echo "Unable to set static IP"
            Exit $LASTEXITCODE
        }

        try {
            [System.Net.IPAddress] $gateway
            $nic.SetGateways($gateway)
            if(-Not $?) {
                echo "Unable to set gateway"
                Exit $LASTEXITCODE
            }
        } catch {
            echo "Gateway not set"
        }

        try {
            [System.Net.IPAddress] $dns
            $nic.SetDNSServerSearchOrder($dns)
            if(-Not $?) {
                echo "Unable to set DNS"
                Exit $LASTEXITCODE
            }
        } catch {
            echo "DNS Server not set."
        }
        break
    }
}

Add-Content -Path "state_file" -Value "ran once"

start-sleep 2
Exit 10
