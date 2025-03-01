Param(
[Parameter(Mandatory=$True)][string]$remoteForestName,
[Parameter(Mandatory=$True)][string]$remoteUser,
[Parameter(Mandatory=$True)][string]$remotePassword
)

$attempts = 1
$max = 10

while($attempts -le $max) {
    try {
        $localforest = [System.DirectoryServices.ActiveDirectory.Forest]::getCurrentForest()
        $remoteContext = New-Object System.DirectoryServices.ActiveDirectory.DirectoryContext('Forest', $remoteForestName, $remoteUser, $remotePassword)
        $remoteForest = [System.DirectoryServices.ActiveDirectory.Forest]::getForest($remoteContext)
        $localForest.CreateTrustRelationship($remoteForest, 'Bidirectional')
        break
    } catch {
        Write-Output "Caught exception setting up trust domain: $PSItem"
        if($PSItem.Exception.Message -Match "trust relationship exists") {
            break
        }
        $attempts += 1
        start-sleep 10
    }
}

start-sleep 2
Exit 0
