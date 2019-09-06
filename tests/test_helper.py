from __future__ import unicode_literals

'''
Copyright 2010-2019 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context.

context is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context. If not, see http://www.gnu.org/licenses/.
'''


#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================

# python libraries

# Django imports
from django.contrib.auth.models import User
from django.core.management import call_command

# import basic django configuration application.
from django_config.models import Config_Property

# python_utilities - logging
from python_utilities.logging.logging_helper import LoggingHelper


#================================================================================
# Shared variables and functions
#================================================================================


#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class TestHelper( object ):

    
    #----------------------------------------------------------------------------
    # CONSTANTS-ish
    #----------------------------------------------------------------------------


    # fixtures paths, in order they should be loaded.
    FIXTURE_UNIT_TEST_CONTEXT_METADATA = "context/fixtures/context-sourcenet_entities_and_relations.json"
    FIXTURE_LIST = []
    FIXTURE_LIST.append( FIXTURE_UNIT_TEST_CONTEXT_METADATA )
    
    # Test user
    TEST_USER_NAME = "test_user"
    TEST_USER_EMAIL = "test@email.com"
    TEST_USER_PASSWORD = "calliope"


    #----------------------------------------------------------------------------
    # Class variables - overriden by __init__() per instance if same names, but
    #    if not set there, shared!
    #----------------------------------------------------------------------------

    
    DEBUG = True


    #-----------------------------------------------------------------------------
    # class methods
    #-----------------------------------------------------------------------------


    @classmethod
    def create_test_user( cls, username_IN = "" ):

        # return reference
        user_OUT = None

        # declare variables
        test_user = None
        test_username = ""

        # do we want non-standard username?
        if ( ( username_IN is not None ) and ( username_IN != "" ) ):

            test_username = username_IN

        else:

            test_username = cls.TEST_USER_NAME

        #-- END check to see if special user name. --#

        # create new test user
        test_user = User.objects.create_user( username = test_username,
                                              email = cls.TEST_USER_EMAIL,
                                              password = cls.TEST_USER_PASSWORD )
        test_user.save()

        user_OUT = test_user

        return user_OUT

    #-- END class method create_test_user() --#


    @classmethod
    def get_test_user( cls, username_IN = "" ):

        # return reference
        user_OUT = None

        # declare variables
        test_user = None
        test_username = ""

        # do we want non-standard username?
        if ( ( username_IN is not None ) and ( username_IN != "" ) ):

            test_username = username_IN

        else:

            test_username = cls.TEST_USER_NAME

        #-- END check to see if special user name. --#

        # try a lookup
        try:

            # by username
            user_OUT = User.objects.get( username = test_username )
        
        except Exception as e:
        
            # create new test user
            user_OUT = cls.create_test_user()

        #-- END try to get existing test user. --#

        return user_OUT

    #-- END class method get_test_user() --#


    @classmethod
    def load_fixture( cls, fixture_path_IN = "", verbosity_IN = 0 ):
        
        # declare variables
        
        # got a fixture path?
        if ( ( fixture_path_IN is not None ) and ( fixture_path_IN != "" ) ):
        
            # got a path - try to load it.
            call_command( 'loaddata', fixture_path_IN, verbosity = verbosity_IN )
            
        #-- END check to make sure we have a path --#
        
    #-- END function load_fixture() --#
    
    
    @classmethod
    def output_debug( cls, message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = "" ):
        
        '''
        Accepts message string.  If debug is on, logs it.  If not,
           does nothing for now.
        '''
        
        # declare variables
    
        # got a message?
        if ( message_IN ):
        
            # only print if debug is on.
            if ( cls.DEBUG == True ):
            
                # use Logging Helper to log messages.
                LoggingHelper.output_debug( message_IN, method_IN, indent_with_IN, logger_name_IN )
            
            #-- END check to see if debug is on --#
        
        #-- END check to see if message. --#
    
    #-- END method output_debug() --#
        

    @classmethod
    def standardSetUp( cls, test_case_IN = None ):
        
        """
        setup tasks.  Call function that we'll re-use.
        """
        
        # return reference
        status_OUT = None

        # declare variables
        me = "standardSetUp"
        status_instance = None
        current_fixture = ""
        
        print( "\nIn TestHelper." + me + "(): starting standardSetUp." )
        
        # see if test case passed in.  If so, set status variables on it.
        if ( test_case_IN is not None ):
        
            # not None, set status variables on it.
            status_instance = test_case_IN
            
        else:
        
            # no test case passed in.  Just set on self...?  This shouldn't
            #     work.
            status_instance = self
        
        #-- END check to see if test case --#
        
        # janky way to add variables to instance since you can't override init.
        status_instance.setup_error_count = 0
        status_instance.setup_error_list = []
        
        # loop over fixtures in cls.FIXTURE_LIST
        for current_fixture in cls.FIXTURE_LIST:
        
            try:
            
                cls.load_fixture( current_fixture )
    
            except Exception as e:
            
                # looks like there was a problem.
                status_instance.setup_error_count += 1
                status_instance.setup_error_list.append( current_fixture )
                
            #-- END try/except --#
            
        #-- END loop over cls.FIXTURE_LIST --#
                
        print( "In context.TestHelper.{}(): standardSetUp complete.".format( me ) )
        
        return status_OUT

    #-- END function standardSetUp() --#
        

    #----------------------------------------------------------------------------
    # __init__() method
    #----------------------------------------------------------------------------


    def __init__( self ):

        # call parent's __init__()
        super( TestHelper, self ).__init__()

    #-- END method __init__() --#


    #----------------------------------------------------------------------------
    # instance methods, in alphabetical order
    #----------------------------------------------------------------------------


#-- END class TestHelper --#