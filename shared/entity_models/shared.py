'''
Copyright 2021 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context.

context is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context. If not, see http://www.gnu.org/licenses/.
'''

#================================================================================
# Imports
#================================================================================

# python imports
import logging

# python_utilities
from python_utilities.logging.logging_helper import LoggingHelper

#================================================================================
# Shared variables and functions
#================================================================================


'''
Debugging code, shared across all models.
'''

DEBUG = False
DEFAULT_LOGGER_NAME = "context.shared.entity_models"

def output_log_message( message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = DEFAULT_LOGGER_NAME, log_level_code_IN = logging.DEBUG, do_print_IN = False ):

    '''
    Accepts message string.  If debug is on, logs it.  If not,
       does nothing for now.
    '''

    # declare variables
    do_print = False

    # got a message?
    if ( message_IN ):

        # only print if debug is on.
        do_print = DEBUG

        # call LoggingHelper method
        LoggingHelper.log_message( message_IN,
                                   method_IN = method_IN,
                                   indent_with_IN = indent_with_IN,
                                   logger_name_IN = logger_name_IN,
                                   log_level_code_IN = log_level_code_IN,
                                   do_print_IN = do_print_IN )

    #-- END check to see if message. --#

#-- END method output_log_message() --#


def output_debug( message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = DEFAULT_LOGGER_NAME ):

    '''
    Accepts message string.  If debug is on, logs it.  If not,
       does nothing for now.
    '''

    # declare variables
    do_print = False

    # got a message?
    if ( message_IN ):

        # only print if debug is on.
        do_print = DEBUG

        # call LoggingHelper method
        LoggingHelper.output_debug( message_IN,
                                    method_IN = method_IN,
                                    indent_with_IN = indent_with_IN,
                                    logger_name_IN = logger_name_IN,
                                    do_print_IN = do_print )

    #-- END check to see if message. --#

#-- END method output_debug() --#
