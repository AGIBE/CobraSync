# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
from CobraSync import __version__
import CobraSync.CobraSync

def main():
    version_text = "CobraSync v" + __version__
    parser = argparse.ArgumentParser(description="Synchronisiert Kontakte aus Cobra nach GeoDBmeta und GeoDBProzess.", prog="CobraSync.exe", version=version_text)
    
    args = parser.parse_args()
    
    CobraSync.CobraSync.run_sync()
    
    
if __name__ == "__main__":
    main()