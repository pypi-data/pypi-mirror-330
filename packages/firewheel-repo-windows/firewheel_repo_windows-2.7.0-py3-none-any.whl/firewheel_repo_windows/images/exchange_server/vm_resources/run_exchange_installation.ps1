param(
[Parameter(Mandatory=$True)][string]$username,
[Parameter(Mandatory=$True)][string]$password,
[Parameter(Mandatory=$True)][string]$installerPath,
[Parameter(Mandatory=$True)][string]$exchangeZip,
[Parameter(Mandatory=$True)][string]$domainController,
[Parameter(Mandatory=$True)][string]$orgName
)

C:\PSTools\PsExec.exe -accepteula -i -u $username -p $password powershell.exe -executionpolicy bypass $installerPath -exchangeZip $exchangeZip -domainController $domainController -orgName $orgName

Exit 0
