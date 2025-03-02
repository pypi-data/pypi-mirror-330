# Copyright (C) 2024, 2025 Jaromir Hradilek

# MIT License
#
# Permission  is hereby granted,  free of charge,  to any person  obtaining
# a copy of  this software  and associated documentation files  (the "Soft-
# ware"),  to deal in the Software  without restriction,  including without
# limitation the rights to use,  copy, modify, merge,  publish, distribute,
# sublicense, and/or sell copies of the Software,  and to permit persons to
# whom the Software is furnished to do so,  subject to the following condi-
# tions:
#
# The above copyright notice  and this permission notice  shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS",  WITHOUT WARRANTY OF ANY KIND,  EXPRESS
# OR IMPLIED,  INCLUDING BUT NOT LIMITED TO  THE WARRANTIES OF MERCHANTABI-
# LITY,  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT
# SHALL THE AUTHORS OR COPYRIGHT HOLDERS  BE LIABLE FOR ANY CLAIM,  DAMAGES
# OR OTHER LIABILITY,  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM,  OUT OF OR IN CONNECTION WITH  THE SOFTWARE  OR  THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import argparse
import errno
import sys

from lxml import etree
from . import NAME, VERSION, DESCRIPTION
from .transform import to_concept, to_reference, to_task, \
                       to_concept_generated, to_reference_generated, \
                       to_task_generated

# Print a message to standard error output and terminate the script:
def exit_with_error(error_message, exit_status=errno.EPERM):
    # Print the supplied message to standard error output:
    print(f'{NAME}: {error_message}', file=sys.stderr)

    # Terminate the script with the supplied exit status:
    sys.exit(exit_status)

# Convert the selected file:
def convert(source_file, target_type):
    # Select the appropriate XSLT transformer:
    transform = {
        'concept':       to_concept,
        'reference':     to_reference,
        'task':          to_task,
        'concept-gen':   to_concept_generated,
        'reference-gen': to_reference_generated,
        'task-gen':      to_task_generated,
    }[target_type]

    # Run the transformation:
    try:
        xml = transform(etree.parse(source_file))
    except etree.XSLTApplyError as message:
        exit_with_error(f'{source_file}: {message}')
    except etree.XMLSyntaxError as message:
        exit_with_error(f'{source_file}: ERROR: {message}')

    # Print any warning messages to standard error output:
    for error in transform.error_log:
        print(f'{source_file}: {error.message}', file=sys.stderr)

    # Return the result:
    return xml

# Parse supplied command-line options:
def parse_args():
    # Configure the option parser:
    parser = argparse.ArgumentParser(prog=NAME,
        description=DESCRIPTION,
        add_help=False)

    # Redefine section titles for the main command:
    parser._optionals.title = 'Options'
    parser._positionals.title = 'Arguments'

    # Add supported command-line options:
    info = parser.add_mutually_exclusive_group()
    info.add_argument('-h', '--help',
        action='help',
        help='display this help and exit')
    info.add_argument('-v', '--version',
        action='version',
        version=f'{NAME} {VERSION}',
        help='display version information and exit')
    parser.add_argument('-t', '--type',
        choices=('concept', 'reference', 'task', 'concept-gen', 'reference-gen', 'task-gen'),
        required=True,
        help='target DITA content type')
    parser.add_argument('-o', '--output',
        default=sys.stdout,
        help='write output to the selected file instead of stdout')

    # Add supported command-line arguments:
    parser.add_argument('file', metavar='FILE',
        default=sys.stdin,
        nargs='?',
        help='specify the DITA topic file to convert')

    # Parse the command-line options:
    args = parser.parse_args()

    # Recognize the instruction to read from standard input:
    if args.file == '-':
        args.file = sys.stdin

    # Convert the selected file:
    try:
        xml = convert(args.file, args.type)
    except OSError as message:
        exit_with_error(message)

    # Determine whether to write to standard output:
    if args.output == sys.stdout or args.output == '-':
        # Print to standard output:
        sys.stdout.write(str(xml))

        # Terminate the script:
        sys.exit(0)

    # Write to the selected file:
    try:
        with open(args.output, 'w') as f:
            f.write(str(xml))
    except Exception as ex:
        exit_with_error(f'{args.output}: {ex}')
