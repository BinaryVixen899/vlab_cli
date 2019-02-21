# -*- coding: UTF-8 -*-
"""Defines the CLI for destroying a port mapping/forwarding rule"""
import click


from vlab_cli.lib.api import consume_task
from vlab_cli.lib.widgets import Spinner, typewriter
from vlab_cli.lib.click_extras import MandatoryOption
from vlab_cli.lib.clippy import invoke_portmap_clippy
from vlab_cli.lib.portmap_helpers import (get_component_protocols, get_protocol_port,
                                          validate_ip, determine_which_ip, validate_ip)


@click.command()
@click.option('-a', '--ip-address',
              help='Explicitly supply the IP of the target VM')
@click.option('-p', '--protocol', type=click.Choice(['ssh', 'https', 'rdp']),
              help='The protocol of the mapping rule to destory')
@click.option('-n', '--name', cls=MandatoryOption,
              help='The name of the VM that owns the rule')
@click.pass_context
def portmap(ctx, name, protocol, ip_address):
    """Destroy a port mapping rule"""
    info = consume_task(ctx.obj.vlab_api,
                        endpoint='/api/1/inf/inventory',
                        message='Collecting information about your inventory',
                        method='GET').json()
    the_vm = info['content'].get(name, None)
    if the_vm is None:
        error = "You own no machine named {}. See 'vlab status' for help".format(name)
        raise click.ClickException(error)

    vm_type = the_vm['meta']['component']
    validate_ip(name, vm_type, the_vm['ips'], ip_address, the_vm['state'])
    target_addr = determine_which_ip(the_vm['ips'], ip_address)
    valid_protocols = get_component_protocols(vm_type)
    if not protocol or protocol not in valid_protocols:
        protocol = invoke_portmap_clippy(ctx.obj.username, vm_type, valid_protocols)
    target_port = get_protocol_port(vm_type, protocol)

    with Spinner('Deleting port mapping rule to {} for {}'.format(name, protocol)):
        resp = ctx.obj.vlab_api.get('/api/1/ipam/portmap', params={'name': name, 'target_port' : target_port})
        try:
            conn_port = list(resp.json()['content'].keys())[0]
        except IndexError:
            # No such rule, but who cares? The target state (i.e. no rule) is true
            pass
        else:
            ctx.obj.vlab_api.delete('/api/1/ipam/portmap', json={'conn_port': int(conn_port)})
    click.echo('OK!')
