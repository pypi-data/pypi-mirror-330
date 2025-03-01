param(
[Parameter(Mandatory=$True)][string]$share,
[Parameter(Mandatory=$True)][int]$max
)

while($true) {
    $availableFiles = Get-ChildItem -Path $share | sort LastWriteTime | ForEach-Object {$_.Name}

    if($availableFiles.length -gt $max) {
        for($i = 0; $i -lt ($availableFiles.length - $max); $i++) {
            $share_path = $share + "\" + $availableFiles[$i]
            Write-Output "Removing: $share_path"
            Remove-Item -Path $share_path
        }
    }

    start-sleep 60
}
