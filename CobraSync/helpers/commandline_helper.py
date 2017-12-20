# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import codecs
from CobraSync import __version__
import CobraSync.helpers.config_helper

def sync(args):
    config = CobraSync.helpers.config_helper.get_config()
    print("Es wird gesynct!!!")


def main():
    version_text = "CobraSync v" + __version__
    parser = argparse.ArgumentParser(description="Synchronisiert Kontakte aus Cobra nach GeoDBmeta und GeoDBProzess.", prog="CobraSync.exe", version=version_text)
    subparsers = parser.add_subparsers(help='Folgende Befehle sind verfuegbar:')
    
    # SYNC-Befehl
    sync_parser = subparsers.add_parser('sync', help='Führt die Synchronisation aus.')
    sync_parser.set_defaults(func=sync)
    
    args = parser.parse_args()
    args.func(args)
    
if __name__ == "__main__":
    main()