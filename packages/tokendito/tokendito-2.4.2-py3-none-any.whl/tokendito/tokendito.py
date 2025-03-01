#!/usr/bin/env python
# vim: set filetype=python ts=4 sw=4
# -*- coding: utf-8 -*-
"""tokendito entry point."""
import sys


def main(args=None):  # needed for console script
    """Packge entry point."""
    if not __package__:
        import os.path

        path = os.path.dirname(os.path.dirname(__file__))
        sys.path[0:0] = [path]
    from tokendito.user import cmd_interface

    return cmd_interface(args)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(1)
