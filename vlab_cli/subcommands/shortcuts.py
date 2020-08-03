#Work In progress, the idea is to have shortcuts here for every VM in the machine 
#This script is not ready yet
#this script does not have a way to handle if there are already shortcuts
#This script does not have a way to handle if things are removed from the list
import os, winshell
import click

from vlab_cli.lib.api import consume_task
from vlab_cli.lib import api
from vlab_cli.lib.portmap_helpers import get_component_protocols
@click.command()
@click.option('--shortcutscreate', is_flag=True, help='Create shorcuts for your VMs')
@click.pass_context



def ShortcutsCreate(ctx):
    """Creates Shorcuts for your virtual lab machines"""
    resp = consume_task(ctx.obj.vlab_api,
        endpoint='/api/1/inf/inventory',
        message='Collecting information about your inventory',
        method='GET',
        timeout=120)
    vm_info = resp.json()['content']
    desktop = winshell.desktop()
    target = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
    # gateway = vm_info.pop('defaultGateway', None)
    # if gateway:
    #     try:
    #         # if the gateway is off, it wont have an IP
    #         gateway_ip = [x for x in gateway['ips'] if ':' not in x and not x.startswith('192.168')][0]
    #     except IndexError:
    #         gateway_ip = gateway['state']
    # else:
    #     gateway_ip = 'None' # so users see the literal word
    
    for vm in sorted(vm_info.keys()):
            params = {'name' : vm}
            kind = vm_info[vm]['meta']['component']
            protocollist = get_component_protocols(kind)
            resp = ctx.obj.vlab_api.get('/api/1/ipam/addr', params=params, auto_check=False)
            if resp.json()['error'] == None:
                addr_info = resp.json()['content']
            else:
                addr_info = {}
            ips = '\n'.join(vm_info[vm]['ips'])
            if not ips: 
                # fall back to port map rule
                addrs = addr_info.get(vm, {}).get('addr', '')
                ips = '\n'.join(addrs)
            path = os.path.join(desktop, "{}.lnk".format(vm))
             
            if (ssh in protocollist) and (gui in protocollist)
                arguments="vlab connect {} -p ssh".format(vm))
                winshell.CreateShortcut(path,target,Arguments="", StartIn=r"C:\Windows\System32\WindowsPowerShell\v1.0", Icon=("", 0), Description="")
                winshell.CreateShortcut(path,target,Arguments="gci", StartIn=r"C:\Windows\System32\WindowsPowerShell\v1.0", Icon=("", 0), Description="")

            elif kind in []

            else: 
                

            print(vm)
          

   


