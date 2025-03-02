#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- CLI Methods for Paths & Drives
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse

import json
import os
import sys

from quickcolor.color_def import color
from showexception.showexception import exception_details

from media_mgr.paths_and_drives import show_drive_info, get_drive_paths, get_full_search_paths_all_drives
from media_mgr.paths_and_drives import get_all_media_paths, get_filtered_media_paths, get_lsblk_mountable_partitions
from media_mgr.paths_and_drives import show_dev_partitions, mount_dev_partitions

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def cli():
    try:
        parser = argparse.ArgumentParser(
                    description=f'{"-." * 3}  {color.CBLUE2}Paths {color.CYELLOW2}and Drives {color.CEND}for media manager',
                    epilog='-.' * 40)

        parser.add_argument('-v', '--verbose', action="store_true",
                            help='run with verbosity hooks enabled')

        parser.add_argument('--version', action="store_true", help='top-level package version')

        subparsers = parser.add_subparsers(dest='cmd')

        p_showDriveInfo = subparsers.add_parser('drive.info', help='show drive info on a given server')
        p_showDriveInfo.add_argument('--ipv4', default=None, metavar='<ipv4.addr>', help='Server IPV4')

        p_getDrivePaths = subparsers.add_parser('drive.paths', help='show drive paths on a server')
        p_getDrivePaths.add_argument('--ipv4', default=None, metavar='<ipv4.addr>', help='Server IPV4')
        p_getDrivePaths.add_argument('--type', default='plex',
                metavar='<srvType>', choices=['plex', 'worker'], help='Server types')

        p_getFullSearchPathsAllDrives = subparsers.add_parser('get.full.search.paths.all.drives',
                help='get full search paths from all drives')
        p_getFullSearchPathsAllDrives.add_argument('--ipv4', default=None, metavar='<ipv4.addr>', help='Server IPV4')
        p_getFullSearchPathsAllDrives.add_argument('--type', default='plex',
                metavar='<srvType>', choices=['plex', 'worker'], help='Server types')

        p_getAllMediaPaths = subparsers.add_parser('get.all.media.paths', help='get all media paths')
        p_getAllMediaPaths.add_argument('--ipv4', default=None, metavar='<ipv4.addr>', help='Server IPV4')
        p_getAllMediaPaths.add_argument('--type', default='plex',
                metavar='<srvType>', choices=['plex', 'worker'], help='Server types')

        p_getFilteredMediaPaths = subparsers.add_parser('get.filtered.paths', help='get filtered local  media paths')
        p_getFilteredMediaPaths.add_argument('--ipv4', default=None, metavar='<ipv4.addr>', help='Server IPV4')
        p_getFilteredMediaPaths.add_argument('--type', default='plex',
                metavar='<srvType>', choices=['plex', 'worker'], help='Server types')
        p_getFilteredMediaPaths.add_argument('lookfor', default=None, nargs='*',
                metavar='<lookingFor>', help='Supported path terminations')

        p_getLsblkDevicesAndMounts = subparsers.add_parser('get.lsblk.mounts', help='get lsblk devices and mount paths')
        p_getLsblkDevicesAndMounts.add_argument('--ipv4', default=None, metavar='<ipv4.addr>', help='Server IPV4')

        p_showDevicePartitions = subparsers.add_parser('show.dev.partitions', help='display device partitions (mounted and unmounted)')
        p_showDevicePartitions.add_argument('--ipv4', default=None, metavar='<ipv4.addr>', help='Server IPV4')

        p_mountDevicePartitions = subparsers.add_parser('mount.dev.partitions', help='mount any mountable device partitions')
        p_mountDevicePartitions.add_argument('--ipv4', default=None, metavar='<ipv4.addr>', help='Server IPV4')

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        # print(args)

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        if args.version:
            from importlib.metadata import version
            import media_mgr
            print(f'{color.CGREEN}{os.path.basename(sys.argv[0])}{color.CEND} resides in package ' + \
                    f'{color.CBLUE2}{media_mgr.__package__}{color.CEND} ' + \
                    f'version {color.CVIOLET2}{version("media_mgr")}{color.CEND} ...')
            sys.exit(0)

        if args.cmd == 'drive.info':
            show_drive_info(ipv4=args.ipv4)

        elif args.cmd == 'drive.paths':
            print('-' * 100)
            print(f'{color.CYELLOW}Drive Paths ({args.ipv4 if args.ipv4 else "Local"})!{color.CEND}')
            print('-' * 100)
            paths = get_drive_paths(ipv4 = args.ipv4, serverType = args.type)
            for idx, path in enumerate(paths):
                print(f'{color.CGREEN2}{idx+1:>3}. {color.CEND}{color.CGREEN}{path}{color.CEND}')
                if idx % 20 == 19:
                    print('-' * 100)
            print('-' * 100)

        elif args.cmd == 'get.full.search.paths.all.drives':
            print('-' * 100)
            print(f'{color.CYELLOW}Get Full Search Paths All Drives from {args.ipv4 if args.ipv4 else "Local"}!{color.CEND}')
            print('-' * 100)
            paths = get_full_search_paths_all_drives(ipv4 = args.ipv4, serverType = args.type)
            for idx, path in enumerate(paths):
                print(f'{color.CBLUE}{idx+1:>3}. {color.CCYAN}{path}{color.CEND}')
                if idx % 20 == 19:
                    print('-' * 100)
            print('-' * 100)

        elif args.cmd == 'get.all.media.paths':
            print('-' * 100)
            print(f'{color.CYELLOW}Get All Media Paths ({args.ipv4 if args.ipv4 else "Local"})!{color.CEND}')
            print('-' * 100)
            paths = get_all_media_paths(ipv4 = args.ipv4, serverType = args.type)
            for idx, path in enumerate(paths):
                print(f'{color.CGREEN2}{idx+1:>3}. {color.CGREEN}{path}{color.CEND}')
                if idx % 20 == 19:
                    print('-' * 100)
            print('-' * 100)

        elif args.cmd == 'get.filtered.paths':
            print('-' * 100)
            print(f'{color.CYELLOW}Get Filtered Media Paths ({args.ipv4 if args.ipv4 else "Local"})!{color.CEND}')
            print('-' * 100)
            paths = get_filtered_media_paths(ipv4 = args.ipv4, serverType = args.type, lookingFor = args.lookfor)
            for idx, path in enumerate(paths):
                print(f'{color.CBLUE}{idx+1:>3}. {color.CBLUE2}{path}{color.CEND}')
                if idx % 20 == 19:
                    print('-' * 100)
            print('-' * 100)

        elif args.cmd == 'get.lsblk.mounts':
            print('-' * 100)
            print(f'{color.CYELLOW}Get <lsblk> Devices & Mount Paths ({args.ipv4 if args.ipv4 else "Local"})!{color.CEND}')
            print('-' * 100)
            mountablePartitions = get_lsblk_mountable_partitions(ipv4=args.ipv4)
            for idx, partition in enumerate(mountablePartitions):
                print(f'{color.CBLUE}{idx+1:>3}. {color.CBLUE2}{json.dumps(partition, indent=4)}{color.CEND}')
                if idx % 20 == 19:
                    print('-' * 100)
            print('-' * 100)

        elif args.cmd == 'show.dev.partitions':
            show_dev_partitions(ipv4 = args.ipv4)

        elif args.cmd == 'mount.dev.partitions':
            mount_dev_partitions(ipv4 = args.ipv4)

    except Exception as e:
        exception_details(e, "Paths & Drives CLI")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def cli_mount_drives():
    try:
        parser = argparse.ArgumentParser(
                    description=f'{"-." * 3}  {color.CBLUE2}Mount Drives {color.CYELLOW2}on Server {color.CEND}utility',
                    epilog='-.' * 40)

        parser.add_argument('-v', '--verbose', action="store_true",
                            help='run with verbosity hooks enabled')

        parser.add_argument('--ipv4', default=None, metavar='<ipv4.addr>', help='Server IPV4')

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        # print(args)

        mount_dev_partitions(ipv4 = args.ipv4)

    except Exception as e:
        exception_details(e, "Mount Drives CLI")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

