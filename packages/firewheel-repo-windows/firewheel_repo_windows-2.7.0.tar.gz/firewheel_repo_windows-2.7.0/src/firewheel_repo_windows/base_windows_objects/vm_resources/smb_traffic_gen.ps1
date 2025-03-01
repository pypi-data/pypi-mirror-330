param(
[Parameter(Mandatory=$True)][string]$share
)

while($true) {
    # Generate a file
    $base = $env:UserProfile -replace "C:"
    $filename = [System.IO.Path]::GetRandomFilename()
    $localFilename = $base + "\Documents\" + $filename
    $remoteFilename = $share  + "\" + $filename
    Write-Output "Generating file: $localFilename"
    $out = New-Object byte[] $(Get-Random -Minimum 2048 -Maximum 2097152)
    (New-Object Random).NextBytes($out)
    [System.IO.File]::WriteAllBytes($localFilename, $out)

    # Upload it to the share
    Copy-Item -Path $localFilename -Destination $remoteFilename -Force
    Remove-Item -Path $localFilename -ErrorAction Ignore

    # Pull two files from the share for every one file that is uploaded
    $availableFiles = Get-ChildItem -Path $share -Name
    for($i = 0; $i -lt 2; $i++) {
        $pullFilename = Get-Random -InputObject $availableFiles
        $pullPath = $share + "/" + $pullFilename
        $localPullPath = $base + "\Documents\" + $pullFilename
        try {
            Write-Output "Pulling: $pullFilename"
            Copy-Item -Path $pullPath -Destination $localPullPath -Force
            Remove-Item -Path $localPullPath -ErrorAction Ignore
        } catch { }
    }
    start-sleep $(Get-Random -Minimum 5 -Maximum 30)
}
