Set COUNTER=0
:try_again
    net localgroup "Remote Desktop Users" "%1" /add
    if %errorlevel% neq 0 (

        if %COUNTER%==6 ( Exit 1 )

        set /A COUNTER=COUNTER+1
        timeout /t 30
        goto :try_again
    )
