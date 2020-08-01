#Work In pgoress, the idea is to have shortcuts here for every VM in the machine 
import os, winshell
import click

from vlab_cli.lib import api, consume,task

@click.command()
@click.option('--create', is_flag=True, help='Create shorcuts for your VMs')
@click.pass_context

# def getMachines(vlab_api, info):
#     vm_body =[]
#     vm_header = ['Name', 'IPs','Type']
#     for vm, data in info.items():
#         body = {}


def CreateShortcuts(ctx):
    """Display general information about your virtual lab"""
    resp = consume_task(ctx.obj.vlab_api,
                        endpoint='/api/1/inf/inventory',
                        message='Collecting information about your inventory',
                        method='GET',
                        timeout=120)
    vm_info = resp.json()['content']
    gateway = vm_info.pop('defaultGateway', None)
    
    if gateway:
        try:
            # if the gateway is off, it wont have an IP
            gateway_ip = [x for x in gateway['ips'] if ':' not in x and not x.startswith('192.168')][0]
        except IndexError:
            gateway_ip = gateway['state']
    else:
        gateway_ip = 'None' # so users see the literal word
        vm_body = []
        vm_header = ['Name', 'IPs', 'Connectable', 'Type', 'Version', 'Powered', 'Networks']
        for vm in sorted(vm_info.keys()):
            path = os.path.join(desktop, 'Name'}
            target = 
            shortcut = file(path, 'w')
            shortcut.write('[InternetShortcut]\n')
            shortcut.write('URL=%s' % target)
            shortcut.close()
            params = {'name' : vm}
            resp = ctx.obj.vlab_api.get('/api/1/ipam/addr', params=params, auto_check=False)
            if resp.json()['error'] == None:
                addr_info = resp.json()['content']
            else:
                addr_info = {}
            connectable = addr_info.get(vm, {}).get('routable', 'initializing')
            networks = ','.join(vm_info[vm].get('networks', ['?']))
            kind = vm_info[vm]['meta']['component']
            version = vm_info[vm]['meta']['version']
            power = vm_info[vm]['state'].replace('powered', '')
            ips = '\n'.join(vm_info[vm]['ips'])
            if not ips:
                # fall back to port map rule
                addrs = addr_info.get(vm, {}).get('addr', '')
                ips = '\n'.join(addrs)
            row = [vm, ips, connectable, kind, version, power, networks]

        quota_info = ctx.obj.vlab_api.get('/api/1/quota').json()['content']


    heading = '\nUsername: {}\nGateway : {}\nVM Quota: {}\nVM Count: {}'.format(ctx.obj.username,
                                                                                  gateway_ip,
                                                                                  quota_info['soft-limit'],
                                                                                  len(vm_info.keys()))

def shortcuts(create):
    if create:
        desktop = winshell.desktop()
        path = os.path.join(desktop, ""
        target =

