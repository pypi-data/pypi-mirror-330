if(Test-Path "state_file") {
     exit
}

cscript /B C:\Windows\system32\slmgr.vbs /rearm

$ecode = $?

start-sleep 1

# NOTE: Technically, rearming Windows requires a reboot for
# it to take effect. This script makes an assumption that some reboot
# will occur later in the schedule. This was done to improve experiment
# launch time. To ensure a reboot happens every time please uncomment the
# below code.

#Add-Content -Path "state_file" -Value "ran once"
#Add-Content -Path "reboot" -Value "reboot"
#
#while(!(Test-Path "reboot")) {
#    start-sleep 1
#}

Exit $ecode
