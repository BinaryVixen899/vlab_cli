import os, winshell

VMdictionary = {'A' : 'RandomIsilon', 'B': 'RandomIsilon2', 'C' : 'RandomIsilon3'}
for vm in sorted(VMdictionary.keys()):
            desktop = winshell.desktop()
            params = {'name' : vm}
            path = os.path.join(desktop, "{}.lnk".format(vm))
            target = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe" 
            print(vm)
            winshell.CreateShortcut(path,target,Arguments="gci", StartIn=r"C:\Windows\System32\WindowsPowerShell\v1.0", Icon=("", 0), Description="")
print("done")