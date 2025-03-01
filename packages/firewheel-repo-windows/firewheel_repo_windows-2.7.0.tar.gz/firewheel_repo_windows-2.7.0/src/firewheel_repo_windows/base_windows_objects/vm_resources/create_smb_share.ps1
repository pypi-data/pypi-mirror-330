Param(
[Parameter(Mandatory=$True)][string]$name,
[Parameter(Mandatory=$True)][string]$path,
[Parameter(Mandatory=$True)][string]$fullaccess,
[Parameter(Mandatory=$True)][string]$folderenumerationmode,
[Parameter(Mandatory=$True)][string]$cachingmode
)

# "name": "Exercise",                       # Name of the SMB Share
# "path": "C:\Shares\Exercise",
# "caching_mode": "Documents",              # None, Manual, Programs, Documents, or Branch Cache
# "folder_enumeration_mode": "AccessBased", # AccessBased or Unrestricted
# "full_access": "ACME\Domain Users"        # Accounts or groups to grant full access to

if( -not (Test-Path -path $path)) {
    try {
        New-Item -Path $path -ItemType Directory -ErrorAction stop
    } catch {
        Write-Output "Unable to create path: $path"
    }
}

while($true) {
    try {
        New-SMBShare -Name $name -Path $path -CachingMode $cachingmode -FolderEnumerationMode $folderenumerationmode -FullAccess "$fullaccess"
        break
    } catch {
        Write-Output $_.Exception.Message
        start-sleep 3
    }
}

$ecode = $?

start-sleep 1

Exit $ecode
