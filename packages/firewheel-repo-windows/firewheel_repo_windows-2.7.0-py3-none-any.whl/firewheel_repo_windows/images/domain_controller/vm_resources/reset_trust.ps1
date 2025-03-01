Param(
[Parameter(Mandatory=$True)][string]$localForestName,
[Parameter(Mandatory=$True)][string]$remoteForestName,
[Parameter(Mandatory=$True)][string]$remoteUser,
[Parameter(Mandatory=$True)][string]$remotePassword
)

$retcode = 1
while($retcode -ne 0) {
    netdom.exe trust $localForestname /d:$remoteForestName /ud:$remoteUser /pd:$remotePassword /reset
    $retcode = $LASTEXITCODE
    if($retcode -ne 0){
        start-sleep 5
    }
}

start-sleep 2
Exit $retcode
