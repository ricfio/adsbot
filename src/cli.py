"""
Command Line Interface
"""

import os
import sys
import getopt

from src.exceptions.application_exception import ApplicationException
from src.kernel import Kernel

class CLI:
    """Command Line Interface"""

    kernel: Kernel

    def __init__(self, kernel) -> None:
        self.kernel = kernel

    def execute_command(self, argv):
        """execute command"""
        # parse CLI request
        _, args = getopt.getopt(argv,"h",["help"])
        if len(args)==0:
            self.print_usage()
        else:
            # execute CLI command
            controller = self.kernel.get_controller()
            commands = {
                'list': controller.list_ads,
                'publish': controller.publish,
            }
            callback = commands.get(args[0], self.print_usage)
            callback()

    @classmethod
    def process(cls,argv):
        """process CLI request"""
        try:
            kernel = Kernel()
            cli = cls(kernel)
            cli.execute_command(argv)
        except getopt.GetoptError:
            __class__.print_usage()
            sys.exit(1)
        except ApplicationException as exception:
            print('error: ' + str(exception))
            if kernel:
                __class__.print_debug(kernel)
            sys.exit(1)

    @staticmethod
    def print_debug(kernel: Kernel):
        """print debug information"""
        dotenv_list = "\n".join(list(map(lambda path: f'- {path}', kernel.dotenv_list)))
        print()
        print(f'environment {kernel.environment}')
        print(dotenv_list)
        print()
        print('configuration')
        print(f'- {kernel.config_path}')
        print()

    @staticmethod
    def print_usage():
        """print usage information"""
        name = os.path.basename(sys.argv[0])
        print()
        print(f'usage: {name} [--help] <command>')
        print()
        print('<command>')
        print(' - list               List ads')
        print(' - publish            Publish ads')
        print()
