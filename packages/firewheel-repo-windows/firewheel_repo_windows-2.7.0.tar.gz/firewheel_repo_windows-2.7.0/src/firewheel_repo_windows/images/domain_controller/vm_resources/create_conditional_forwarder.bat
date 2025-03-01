:: The first argument is expected to be the name of the zone to add (i.e. acme.com)
:: The second parameter is the IP address to forward all acme.com DNS requests to (generally the acme.com domain controller)

dnscmd.exe /zoneadd %1 /dsforwarder %2

timeout /t 2
exit /b 0
