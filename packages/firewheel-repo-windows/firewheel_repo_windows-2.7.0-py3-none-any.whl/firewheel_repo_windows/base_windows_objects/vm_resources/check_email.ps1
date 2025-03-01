param(
[Parameter(Mandatory=$True)][string]$username,
[Parameter(Mandatory=$True)][string]$password,
[Parameter(Mandatory=$True)][string]$domain,
[Parameter(Mandatory=$True)][string]$mailbox,
[Parameter(Mandatory=$True)][string]$smtp,
[Parameter(Mandatory=$True)][int]$clickRate,
[Parameter(Mandatory=$True)][string]$trusted
)

$Provider=New-Object Microsoft.CSharp.CSharpCodeProvider
$Compiler=$Provider.CreateCompiler()
$Params=New-Object System.CodeDom.Compiler.CompilerParameters
$Params.GenerateExecutable=$False
$Params.GenerateInMemory=$True
$Params.IncludeDebugInformation=$False
$Params.ReferencedAssemblies.Add("System.DLL") | Out-Null

$TASource=@'
  namespace Local.ToolkitExtensions.Net.CertificatePolicy{
    public class TrustAll : System.Net.ICertificatePolicy {
      public TrustAll() { 
      }
      public bool CheckValidationResult(System.Net.ServicePoint sp,
        System.Security.Cryptography.X509Certificates.X509Certificate cert, 
        System.Net.WebRequest req, int problem) {
        return true;
      }
    }
  }
'@ 
$TAResults=$Provider.CompileAssemblyFromSource($Params,$TASource)
$TAAssembly=$TAResults.CompiledAssembly

$TrustAll=$TAAssembly.CreateInstance("Local.ToolkitExtensions.Net.CertificatePolicy.TrustAll")
[System.Net.ServicePointManager]::CertificatePolicy=$TrustAll

$dllpath = "C:\Program Files\Microsoft\Exchange\Web Services\2.2\Microsoft.Exchange.WebServices.dll"
[void][Reflection.Assembly]::LoadFile($dllpath)

$exchangeservice = New-Object Microsoft.Exchange.WebServices.Data.ExchangeService([Microsoft.Exchange.WebServices.Data.ExchangeVersion]::Exchange2007_SP1)
$exchangeservice.Credentials = new-object Microsoft.Exchange.WebServices.Data.WebCredentials($username,$password,$domain)
$mail_uri = new-object System.UriBuilder -ArgumentList "https://$($smtp)/EWS/Exchange.asmx"
$exchangeservice.Url = $mail_uri.Uri

$inboxfolderid = New-Object Microsoft.Exchange.WebServices.Data.FolderId([Microsoft.Exchange.WebServices.Data.WellKnownFolderName]::Inbox,$mailbox)
$inboxfolder = [Microsoft.Exchange.WebServices.Data.Folder]::Bind($exchangeservice,$inboxfolderid)

$sfunread = New-Object Microsoft.Exchange.WebServices.Data.SearchFilter+IsEqualTo([Microsoft.Exchange.WebServices.Data.EmailMessageSchema]::IsRead, $false)
$sfattachment = New-Object Microsoft.Exchange.WebServices.Data.SearchFilter+IsEqualTo([Microsoft.Exchange.WebServices.Data.EmailMessageSchema]::HasAttachments, $true)

$sfcollection = New-Object Microsoft.Exchange.WebServices.Data.SearchFilter+SearchFilterCollection([Microsoft.Exchange.WebServices.Data.LogicalOperator]::And);
$sfcollection.add($sfunread)
$view = New-Object -TypeName Microsoft.Exchange.WebServices.Data.ItemView -ArgumentList 100

while($true) {
    $foundemails = $inboxfolder.FindItems($sfcollection, $view)
    foreach ($email in $foundemails.Items){
        $email.Load()
        Write-Output "Got an email from: $email.from.name"
        $attachments = $email.Attachments
    
        foreach ($attachment in $attachments){
            $attachment.Load()
            $attachmentname = $attachment.Name.ToString()
            $click = get-random -Maximum 100
            if($email.From.Address -eq $trusted -or $click -le $clickRate) { 
                $save_path = "C:\Users\$($username)\Desktop\$($attachmentname)"
                $file = New-Object System.IO.FileStream(($save_path), [System.IO.FileMode]::Create)
                $file.Write($attachment.Content, 0, $attachment.Content.Length)
                $file.close()
                Write-Output "Clicking attachment"
                start-process -filepath $save_path
                start-sleep 1
            }
        }
        $email.IsRead = $true
        $email.Update([Microsoft.Exchange.WebServices.Data.ConflictResolutionMode]::AlwaysOverwrite)
    }
    $sleep_time = Get-Random -Minimum 120 -Maximum 360
    start-sleep $sleep_time
}
