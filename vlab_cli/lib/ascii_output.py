# -*- coding: UTF-8 -*-
"""This module formats common CLI output in a consistent format"""
import copy

from tabulate import tabulate


def format_machine_info(vlab_api, info):
    """Convert the deserialized JSON API response into a CLI friendly format

    :Returns: String

    :param vlab_api: An instantiated connection to the vLab server
    :type vlab_api: vlab_cli.lib.api.vLabApi

    :param info: The deserialized JSON API response from the vLab server
    :type info: Dictionary
    """
    shorter_link = vlab_api.post('/api/1/link',
                                 json={'url': info['console']}).json()['content']['url']
    rows = []
    kind, version = info['note'].split('=')
    rows.append(['Type', ':', kind])
    rows.append(['Version', ':', version])
    rows.append(['State', ':', info['state']])
    rows.append(['IPs', ':', ' '.join(info['ips'])])
    rows.append(['Console', ':', shorter_link])
    return tabulate(rows, tablefmt='plain')


def vm_table_view(vlab_api, info):
    """Create an ASCII table displaying information about virtual machines

    :Returns: String

    :param vlab_api: An instantiated connection to the vLab server
    :type vlab_api: vlab_cli.lib.api.vLabApi

    :param info: The mapping of VM name to general information about the VM
    :type info: Dictionary
    """
    vm_body = []
    vm_header = ['Name', 'IPs', 'Type', 'Version', 'Powered', 'Console']
    for vm, data in info.items():
        body = {'url': data['console']}
        shorter_link = vlab_api.post('/api/1/link', json=body).json()['content']['url']
        kind = data['meta']['component']
        version = data['meta']['version']
        power = data['state'].replace('powered', '')
        row = [vm, '\n'.join(data['ips']), kind, version, power, shorter_link]
        vm_body.append(row)
    table = tabulate(vm_body, headers=vm_header, tablefmt='presto')
    return table


def columned_table(header, columns):
    """Create an ASCII table by supplying a header and columns

    :Returns: String

    :param header: The headers of the table
    :type header: List

    :param columns: The different columns under each header
    :type columns: List
    """
    if not len(header) == len(columns):
        error = 'the number of columns must match the number of headers'
        raise ValueError(error)

    # Add extra elements so all columns are the same depth
    local_columns = copy.deepcopy(columns) # avoid side effects
    max_depth = len(max(columns, key=len))
    for idx, column in enumerate(local_columns):
        missing = max_depth - len(column)
        tmp = ['' for x in range(missing)]
        local_columns[idx] = column + tmp

    # Now transposing the columns to rows is easy!
    as_rows = zip(*local_columns)
    return tabulate(as_rows, headers=header, tablefmt='presto', numalign="center")
