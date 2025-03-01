Param(
[Parameter(Mandatory=$True)][string]$hostname, 
[Parameter(Mandatory=$True)][string]$Users
)

Add-PSSnapin *Microsoft.Exchange*

foreach($username in Get-Content $Users) {
   try {
       Enable-Mailbox -Identity $username
   } catch {
       $ErrorMessage = $_.Exception.Message
       $ItemName = $_.Exception.GetType().fullname
       Write-Output "Error: $ItemName -- $ErrorMessage"
   }
   start-sleep 1
}
