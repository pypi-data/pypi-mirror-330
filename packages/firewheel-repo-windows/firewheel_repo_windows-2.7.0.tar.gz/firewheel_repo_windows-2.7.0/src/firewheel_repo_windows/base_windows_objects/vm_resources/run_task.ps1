param(
[Parameter(Mandatory=$True)][string]$name
)

Start-ScheduledTask -TaskName $name
