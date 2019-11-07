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
from python_utilities.exceptions.exception_helper import ExceptionHelper
from python_utilities.logging.logging_helper import LoggingHelper

# context_text imports
from context.models import Entity
from context.models import Entity_Identifier
from context.models import Entity_Trait

#================================================================================
# Shared variables and functions
#================================================================================


#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class TestHelper( object ):

    
    #----------------------------------------------------------------------------
    # ! ==> CONSTANTS-ish
    #----------------------------------------------------------------------------


    # fixtures paths, in order they should be loaded.
    FIXTURE_UNIT_TEST_CONTEXT_METADATA = "context-sourcenet_entities_and_relations.json"
    FIXTURE_LIST = []
    FIXTURE_LIST.append( FIXTURE_UNIT_TEST_CONTEXT_METADATA )
    
    # Test user
    TEST_USER_NAME = "test_user"
    TEST_USER_EMAIL = "test@email.com"
    TEST_USER_PASSWORD = "calliope"

    # Test Entity information
    TEST_ENTITY_NAME = "calliope"
    
    # Test Entity_Identifier default information
    TEST_ENTITY_IDENTIFIER_NAME = "calliope_type"
    TEST_ENTITY_IDENTIFIER_UUID = "123456"
    TEST_ENTITY_IDENTIFIER_ID_TYPE = "made-up"
    TEST_ENTITY_IDENTIFIER_SOURCE = "my_brain"
    TEST_ENTITY_IDENTIFIER_NOTE = "default initialization notes"
    
    # Test Entity_Trait default information
    TEST_ENTITY_TRAIT_NAME = "calliope_status"
    TEST_ENTITY_TRAIT_SLUG = TEST_ENTITY_TRAIT_NAME
    TEST_ENTITY_TRAIT_VALUE = "calliope_status_value"
    TEST_ENTITY_TRAIT_VALUE_JSON = '{ "calliope_status": "calliope_status_value" }'
    TEST_ENTITY_TRAIT_LABEL = "important"
    TEST_ENTITY_TRAIT_DESCRIPTION = "The calliope status for this important thing."    


    #----------------------------------------------------------------------------
    # ! ==> Class variables
    # - overriden by __init__() per instance if same names, but if not set
    #     there, shared!
    #----------------------------------------------------------------------------

    
    DEBUG = True


    #-----------------------------------------------------------------------------
    # class methods
    #-----------------------------------------------------------------------------


    @classmethod
    def create_test_entity( cls, entity_type_slug_IN = None ):
        
        # return reference
        instance_OUT = None
        
        # declare variables
        entity_instance = None
        
        # create entity
        entity_instance = Entity()
        
        # set some values
        entity_instance.name = cls.TEST_ENTITY_NAME
        entity_instance.save()
        
        if ( ( entity_type_slug_IN is not None ) and ( entity_type_slug_IN != "" ) ):
        
            # we do.  Add entity type.
            entity_instance.add_entity_type( entity_type_slug_IN )
        
        #-- END check to see if we assign an entity type --#
        
        # return it
        instance_OUT = entity_instance
        return instance_OUT

    #-- END method create_test_entity() --#


    @classmethod
    def create_test_entity_identifier( cls, entity_instance_IN ):
        
        # return reference
        instance_OUT = None
        
        # declare variables
        identifier_instance = None
        
        # create entity
        identifier_instance = Entity_Identifier()
        
        # set some values
        identifier_instance.name = cls.TEST_ENTITY_IDENTIFIER_NAME
        identifier_instance.uuid = cls.TEST_ENTITY_IDENTIFIER_UUID
        identifier_instance.id_type = cls.TEST_ENTITY_IDENTIFIER_ID_TYPE
        identifier_instance.source = cls.TEST_ENTITY_IDENTIFIER_SOURCE
        identifier_instance.note = cls.TEST_ENTITY_IDENTIFIER_NOTE
        identifier_instance.entity = entity_instance_IN
        identifier_instance.save()
        
        # return it
        instance_OUT = identifier_instance
        return instance_OUT

    #-- END method create_test_entity_identifier() --#


    @classmethod
    def create_test_entity_trait( cls, entity_instance_IN ):
        
        '''
        Contents:
        
        #entity = models.ForeignKey( "Entity", on_delete = models.CASCADE )
        name = models.CharField( max_length = 255 )
        slug = models.SlugField( blank = True, null = True )
        value = models.CharField( max_length = 255, blank = True, null = True )
        value_json = JSONField( blank = True, null = True )
        label = models.CharField( max_length = 255, blank = True, null = True )
        description = models.TextField( blank = True )
    
        # context
        trait_type = models.ForeignKey( "Trait_Type", on_delete = models.SET_NULL, blank = True, null = True )
        term = models.ForeignKey( "Term", on_delete = models.SET_NULL, blank = True, null = True )
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        trait_instance = None
        
        # create entity
        trait_instance = Entity_Trait()
        
        # set some values
        trait_instance.name = cls.TEST_ENTITY_TRAIT_NAME
        trait_instance.slug = cls.TEST_ENTITY_TRAIT_SLUG
        trait_instance.value = cls.TEST_ENTITY_TRAIT_VALUE
        trait_instance.value_json = cls.TEST_ENTITY_TRAIT_VALUE_JSON
        trait_instance.label = cls.TEST_ENTITY_TRAIT_LABEL
        trait_instance.description = cls.TEST_ENTITY_TRAIT_DESCRIPTION
        trait_instance.entity = entity_instance_IN
        trait_instance.save()
        
        # return it
        instance_OUT = trait_instance
        return instance_OUT

    #-- END method create_test_entity_trait() --#


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
    def output_debug( cls, message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = "", do_print_IN = False ):
        
        '''
        Accepts message string and other optional logging things.  Logs the
            debug message.
        '''
        
        # declare variables
    
        # got a message?
        if ( message_IN ):
        
            # use Logging Helper to log messages.
            LoggingHelper.output_debug( message_IN, method_IN, indent_with_IN, logger_name_IN, do_print_IN = do_print_IN )
        
        #-- END check to see if message. --#
    
    #-- END method output_debug() --#
        

    @classmethod
    def standardSetUp( cls, test_case_IN = None, fixture_list_IN = FIXTURE_LIST ):
        
        """
        setup tasks.  Call function that we'll re-use.
        """
        
        # return reference
        status_OUT = None

        # declare variables
        me = "standardSetUp"
        status_instance = None
        fixture_list = None
        current_fixture = ""
        exception_message = None
        
        print( "\nIn context.TestHelper." + me + "(): starting standardSetUp." )
        
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
        
        # get fixture list
        fixture_list = fixture_list_IN
        if ( ( fixture_list is None ) or ( len( fixture_list ) <= 0 ) ):
        
            # no list passed in.  Use default.
            fixture_list = cls.FIXTURE_LIST
            
        #-- END check to see if list passed in --#
        
        if ( cls.DEBUG == True ):
            print( "----> Fixture list: {}".format( fixture_list ) )
        #-- END DEBUG --#

        # loop over fixtures in fixture_list
        for current_fixture in fixture_list:
        
            try:
            
                cls.load_fixture( current_fixture )
    
            except Exception as e:
            
                # looks like there was a problem.
                status_instance.setup_error_count += 1
                status_instance.setup_error_list.append( current_fixture )
                
                # log Exception
                exception_message = "Exception thrown loading fixture {}".format( current_fixture )
                ExceptionHelper.log_exception( e,
                                               message_IN = exception_message,
                                               method_IN = me,
                                               do_print_IN = True )
                
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