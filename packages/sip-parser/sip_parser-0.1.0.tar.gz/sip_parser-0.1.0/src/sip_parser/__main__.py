"""
__main__.py

Scenario Instance Parser
"""

import logging
import logging.config
import sys
import argparse
from pathlib import Path
from sip_parser import version
from sip_parser.parser import SIParser

_logpath = Path("si_parser.log")

def get_logger():
    """Initiate the logger"""
    log_conf_path = Path(__file__).parent / 'log.conf'  # Logging configuration is in this file
    logging.config.fileConfig(fname=log_conf_path, disable_existing_loggers=False)
    return logging.getLogger(__name__)  # Create a logger for this module

# Configure the expected parameters and actions for the argparse module
def parse(cl_input):
    """
    The command line interface is for diagnostic purposes

    :param cl_input:
    :return:
    """
    parser = argparse.ArgumentParser(description='Scenario instance parser')
    parser.add_argument('sifile', nargs='?', action='store',
                        help='Scenario instance file name with .sip extension')
    parser.add_argument('-D', '--debug', action='store_true',
                        help='Debug mode'),
    parser.add_argument('-V', '--version', action='store_true',
                        help='Print the current version of parser')
    return parser.parse_args(cl_input)


def main():
    # Start logging
    logger = get_logger()
    logger.info(f'Class model parser version: {version}')

    # Parse the command line args
    args = parse(sys.argv[1:])

    if args.version:
        # Just print the version and quit
        print(f'Scenario instance parser version: {version}')
        sys.exit(0)

    if args.sifile:
        fpath = Path(args.sifile)
        d = args.debug
        result = SIParser.parse_file(file_input=fpath, debug=d)

    logger.info("No problemo")  # We didn't die on an exception, basically
    print("\nNo problemo")


if __name__ == "__main__":
    main()
