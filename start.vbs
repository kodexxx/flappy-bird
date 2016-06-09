Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c python game.py"
oShell.Run strArgs, 0, false