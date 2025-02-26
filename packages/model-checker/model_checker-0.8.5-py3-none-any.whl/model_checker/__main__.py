'''
file specifies premises, conclusions, and settings.
running the file finds a model and prints the result.
to test from the Code/ directory, run: python -m src.model_checker 
'''

import sys
import subprocess
import argparse

# Try local imports first (for development)
try:
    from src.model_checker import __version__
    from src.model_checker.builder import (
        BuildProject,
        BuildModule,
    )
except ImportError:
    # Fall back to installed package imports
    from model_checker import __version__
    from model_checker.builder import (
        BuildProject,
        BuildModule,
    )


class ParseFileFlags:
    """Handles command line argument parsing and flag management."""

    def __init__(self):
        """Initialize parser with default configuration."""
        self.parser = self._create_parser()
        self.flags = None
        self.package_name = None

    def _create_parser(self):
        """Create and configure the argument parser."""
        parser = argparse.ArgumentParser(
            prog='model-checker',
            usage='%(prog)s [options] input',
            description="""
            Running '%(prog)s' without options or an input will prompt the user
            to generate a project. To run a test on an existing file, include
            the path to that file as the input.""",
            epilog="""
            More information can be found at:
            https://github.com/benbrastmckie/ModelChecker/""",
        )
        
        # Add arguments
        parser.add_argument(
            "file_path",
            nargs='?',
            default=None,
            type=str,
            help="Specifies the path to a Python file.",
        )
        parser.add_argument(
            '--contingent',
            '-c',
            action='store_true',
            help='Overrides to make all propositions contingent.'
        )
        parser.add_argument(
            '--disjoint',
            '-d',
            action='store_true',
            help='Overrides to make all propositions have disjoint subject-matters.'
        )
        parser.add_argument(
            '--non_empty',
            '-e',
            action='store_true',
            help='Overrides to make all propositions non_empty.'
        )
        parser.add_argument(
            '--load_theory',
            '-l',
            type=str,
            metavar='NAME',
            help='Load a specific theory by name.'
        )
        parser.add_argument(
            '--maximize',
            '-m',
            action='store_true',
            help='Overrides to compare semantic theories.'
        )
        parser.add_argument(
            '--non_null',
            '-n',
            action='store_true',
            help='Overrides to make all propositions non_null.'
        )
        parser.add_argument(
            '--print_constraints',
            '-p',
            action='store_true',
            help='Overrides to print the Z3 constraints or else the unsat_core constraints if there is no model.'
        )
        parser.add_argument(
            '--save_output',
            '-s',
            action='store_true',
            help='Overrides to prompt user to save output.'
        )
        parser.add_argument(
            '--print_impossible',
            '-i',
            action='store_true',
            help='Overrides to print impossible states.'
        )
        parser.add_argument(
            '--version',
            '-v',
            action='version',
            version=f"%(prog)s:  {__version__}",
            help='Prints the version number.'
        )
        parser.add_argument(
            '--upgrade',
            '-u',
            action='store_true',
            help='Upgrade the package.'
        )
        parser.add_argument(
            '--print_z3',
            '-z',
            action='store_true',
            help='Overrides to print Z3 model or unsat_core.'
        )
        return parser

    def parse(self):
        """Parse command line arguments and store results."""
        self.flags = self.parser.parse_args()
        self.package_name = self.parser.prog
        return self.flags, self.package_name

def main():
    if len(sys.argv) < 2:
        builder = BuildProject()
        builder.ask_generate()
        return
    parser = ParseFileFlags()
    module_flags, package_name = parser.parse()
    if module_flags.upgrade:
        print("Upgrading package")
        try:
            subprocess.run(['pip', 'install', '--upgrade', package_name], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to upgrade {package_name}: {e}")
        return
    if module_flags.load_theory:
        semantic_theory_name = module_flags.load_theory
        builder = BuildProject(semantic_theory_name)
        builder.ask_generate()
        return

    module = BuildModule(module_flags)

    # TODO: create print/save class
    if module.general_settings["maximize"]:
        module.run_comparison()
        return

    module.run_examples()

def run():
    """Entry point for the application."""
    main()

if __name__ == '__main__':
    run()
