# cadvance/__main__.py
import argparse
from .automation import Cadvance
from colorama import Fore

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="CadVance - A professional AutoCAD automation package"
    )

    # Command to open AutoCAD
    parser.add_argument(
        '--open',
        action='store_true',
        help='Open AutoCAD if it is not running.'
    )

    # Command to close AutoCAD
    parser.add_argument(
        '--close',
        action='store_true',
        help='Close AutoCAD if it is running.'
    )

    # Command to check AutoCAD version
    parser.add_argument(
        '--version',
        action='store_true',
        help='Check the installed version of AutoCAD.'
    )

    # Command to check if AutoCAD is running
    parser.add_argument(
        '--status',
        action='store_true',
        help='Check if AutoCAD is running.'
    )

    # Add a flag for debug mode
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode for detailed logging.'
    )

    return parser.parse_args()

def main():
    """Main entry point for the CadVance CLI tool."""
    args = parse_arguments()
    cad = Cadvance(debug=args.debug)

    # Open AutoCAD if the --open argument is provided
    if args.open:
        cad.open_cad()

    # Close AutoCAD if the --close argument is provided
    elif args.close:
        cad.close_cad()

    # Show AutoCAD version if the --version argument is provided
    elif args.version:
        cad.cad_version()

    # Check if AutoCAD is running if the --status argument is provided
    elif args.status:
        if Cadvance.is_cad_running():
            print(Fore.GREEN + "[ CadVance ] Info: AutoCAD is running." + Fore.RESET)
        else:
            print(Fore.YELLOW + "[ CadVance ] Info: AutoCAD is not running." + Fore.RESET)

    else:
        # If no arguments are provided, show a simple usage message
        print(Fore.CYAN + "[ CadVance ] Info: No command provided. Use --help for options." + Fore.RESET)

if __name__ == "__main__":
    main()
