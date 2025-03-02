#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# Comms (and shell specific) utilities
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

import json
import subprocess

from quickcolor.color_def import color

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

# Note: this method of retrieving remote content is REALLY SLOW - zsh/bash kicks ass:
# -- show_drives_on_server 10.114.108.70 takes 250 msec
# -- running this python script takes
def run_ssh_send_cmd(ipv4: str, cmd: str = 'ls -als',
        timeout: int = 5, debug: bool = False):
    if debug:
        print(f'---- sending {color.CRED2}run_ssh_send_cmd{color.CEND} ' + \
                f'SEND CMD to {color.CBLUE2}{ipv4}:\n' + \
                f'{color.CBLUE}{cmd}{color.CEND}')

    session = subprocess.run(
            ["ssh", "%s" % ipv4, cmd],
            capture_output = True,
            text = True,
            timeout = timeout)

# ------------------------------------------------------------------------------------------------------

# Note: this method of retrieving remote content is REALLY SLOW - bash kicks ass:
# -- show_drives_on_server 10.114.108.70 takes 250 msec
# -- running this python script takes
def run_ssh_cmd(ipv4: str, cmd: str = 'ls -als',
        jsonOutput: bool = False, timeout: int = 5,
        debug: bool = False):
    if debug:
        print(f'---- sending {color.CYELLOW}run_ssh_cmd{color.CEND} ' + \
                f'CMD to {color.CBLUE2}{ipv4}:\n' + \
                f'{color.CYELLOW}{cmd}{color.CEND}')

    session = subprocess.run(
            ["ssh", "%s" % ipv4, cmd],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            # capture_output = True,
            text = True,
            timeout = timeout)

    try:
        if jsonOutput:
            returnResult = json.loads(session.stdout)
        else:
            result = session.stdout.strip("\n")
            returnResult = result.split('\n')

        if debug:
            print(f"{color.CRED}Received:{color.CEND}\n{str(returnResult)}")

        return returnResult

    except Exception as e:
        # error = session.stderr.readlines()
        error = session.stderr
        print(f'Error:\n{error}\n{str(e)}', file = sys.stderr)
        return None

# ------------------------------------------------------------------------------------------------------

def run_cmd(ipv4: str | None = None, cmd: str = 'ls -als',
            cmdGet: bool = True, jsonOutput: bool = False,
            timeout: int = 5, shell: bool = False,
            retCodeOnly: bool = False, debug: bool = False):

    if not ipv4:
        if debug:
            print(f'---- sending {color.CRED}run_cmd{color.CEND} ' + \
                    f'SEND CMD to {color.CBLUE2} the local system:\n' + \
                    f'{color.CBLUE}{cmd}{color.CEND}')

        cmdList = []
        cmdList.append(cmd)
        cmdResult = subprocess.run(
            cmdList,
            # stdout = subprocess.PIPE,
            # stderr = subprocess.PIPE,
            capture_output = True,
            text = True,
            shell = shell,
            timeout = timeout)

        if isinstance(cmdResult, subprocess.CompletedProcess) and cmdResult.returncode and debug:
            raise SystemError(f'Warning: Problem running local cmd ->{cmd}<- ' + \
                    f'... returncode: {cmdResult.returncode}\n... complete cmdREsult: {cmdResult}')

        if retCodeOnly:
            returnResult = cmdResult.returncode

        elif jsonOutput:
            returnResult = json.loads(cmdResult.stdout)
        else:
            result = cmdResult.stdout.strip("\n")
            returnResult = result.split('\n')

        if debug:
            print(f"{color.CRED}Received:{color.CEND}\n{str(returnResult)}")

        return returnResult

    else:
        if cmdGet:
            cmdResult = run_ssh_cmd(ipv4, cmd, jsonOutput, timeout, debug)
            if isinstance(cmdResult, subprocess.CompletedProcess) and cmdResult.returncode:
                raise SystemError(f'Warning: Problem running cmd ->{cmd}<- ' + \
                        f'on {ipv4} ... returncode: {cmdResult.returncode}')
        else:
            cmdResult = run_ssh_send_cmd(ipv4, cmd, timeout, debug)

    return cmdResult

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def is_server_active(ipv4: str = None):
    if not ipv4:
        raise ValueError(f"Need a valid IPV4 address!")

    retCode = run_cmd(ipv4 = None,
            cmd = f'ping -c 1 -W 1 -q {ipv4}',
            timeout = 2, shell = True, retCodeOnly = True)

    return retCode == 0

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def group_list(inputList = None, separator = None):
    group = []
    for item in inputList:
        if separator in item:
            yield group
            group = []
        group.append(item)
    yield group

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

