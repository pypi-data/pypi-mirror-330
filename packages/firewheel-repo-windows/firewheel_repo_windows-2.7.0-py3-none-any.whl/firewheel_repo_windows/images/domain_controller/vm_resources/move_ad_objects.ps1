Param(
[Parameter(Mandatory=$True)][string]$filename
)

while($true) {
    try {
        Import-Module ActiveDirectory
        break
    } catch {
        Write-Output "Could not import Active Directory module, sleeping and trying again"
        start-sleep 5
    }
}

$output = "move_output.txt"

$objects = New-Object System.Collections.ArrayList
$retry = New-Object System.Collections.ArrayList

foreach($line in Get-Content -Path $filename) {
    $objects.add($line)
}

$count = 1
while($objects.Count -gt 0 -And $count -lt 20) {
    foreach($line in $objects) {

        if($line.length -eq 0) {
            continue
        }

        $identity = $line.split()[0].trim()
        $target = $line.split()[1].trim() -replace "`n|`r",""

        Try {
            Move-ADObject -Identity $identity -TargetPath $target
        } Catch {
            $err = $_.Exception.Message
            #echo 'Can not move ' $identity >> $output
            #echo $err >> $output
            $retry.add($line)
        }
    }
    $objects = $retry.clone()
    $retry.clear()
    $count += 1
    echo "Waiting for the the following machines:" >> $output
    echo $objects >> $output
    echo "" >> $output
    Start-Sleep -s 10
}

if($objects.Count -gt 0) {
    echo 'FAILED' >> $output
    echo $objects >> $output
}
else {
    Remove-Item -Path $filename
    Remove-Item -Path $output
}
