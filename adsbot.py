#!/usr/bin/env python3
"""
adsbot
"""

import sys

from src.cli import CLI

if __name__ == '__main__':
    CLI.process(sys.argv[1:])
