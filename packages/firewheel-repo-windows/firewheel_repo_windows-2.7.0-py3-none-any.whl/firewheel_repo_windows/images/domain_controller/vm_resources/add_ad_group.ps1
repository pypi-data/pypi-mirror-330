Param(
[Parameter(Mandatory=$True)][string]$group,
[Parameter(Mandatory=$True)][string]$scope
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

while($true) {
    try {
        Get-ADGroup -Identity "$group"
        break
    } catch {
        New-ADGroup -Name "$group" -GroupScope $scope
        start-sleep 2
    }
}

start-sleep 1
Exit 0
