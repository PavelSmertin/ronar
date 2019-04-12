__author__ = 'pashtet'

"""
    ronarlistener.__main__
    ~~~~~~~~~~~~~~

    Alias for server.run for the command line, for when this module is directly executed as "python -m ronarlistener"
"""

if __name__ == '__main__':
    from .server import run
    run()
