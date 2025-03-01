param(
[Parameter(Mandatory=$True)][string]$path,
[Parameter(Mandatory=$True)][string]$hostname,
[Parameter(Mandatory=$True)][string]$users,
[Parameter(Mandatory=$True)][string]$username,
[Parameter(Mandatory=$True)][string]$password,
[Parameter(Mandatory=$True)][string]$pstools
)

Add-Type -AssemblyName System.IO.Compression.FileSystem
$extractedDir = 'C:\PSTools'
[System.IO.Compression.ZipFile]::ExtractToDirectory($pstools, $extractedDir)

C:\PSTools\PsExec.exe \\$hostname -accepteula -i -u $username -p $password powershell.exe -executionpolicy bypass $path -hostname $hostname -users $users
