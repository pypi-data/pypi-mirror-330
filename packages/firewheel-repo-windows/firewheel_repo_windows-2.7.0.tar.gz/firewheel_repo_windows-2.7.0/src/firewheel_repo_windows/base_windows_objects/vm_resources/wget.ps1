param(
[Parameter(Mandatory=$True)][string]$address,
[Parameter(Mandatory=$False)][string]$filter
)

while($True) {
    $client = New-Object System.Net.WebClient
    $directoryListing = $client.DownloadString($address)

    if($PSBoundParameters.ContainsKey('filter')) {
        ForEach($line in $directoryListing.split([Environment]::NewLine)) {
            $href = $line.IndexOf("href")
            if($href -gt 0) {
                try {
                    echo $href | Select-String -Pattern $filter
                } catch {
                    start-sleep $(Get-Random -Minimum 2 -Maximum 30)
                    continue
                }
                $filenameStart = $line.IndexOf('"')
                $filenameEnd = $line.LastIndexOf('"')
                $filename = $line.Substring($filenameStart + 1, $filenameEnd - $filenameStart - 1)
                $fileAddress = $address + "/$filename"
                Write-Output "Querying: $fileAddress"
                $client.DownloadFile($fileAddress, $filename)
                Remove-Item -Path $filename
                start-sleep $(Get-Random -Minimum 2 -Maximum 30)
            }
        }
    }
    start-sleep $(Get-Random -Minimum 2 -Maximum 30)
}
