"""
This file contains tests of the context_text Person model (and by extension
   Abstract_Person).

Functions tested:
- Person.look_up_person_from_name()
"""

# python imports
import datetime
import json

# import six
import six

# django imports
import django.test

# context_text imports
from context.models import Entity_Trait
from context.tests.test_helper import TestHelper


class Entity_TraitModelTest( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ----> Constants-ish
    #----------------------------------------------------------------------------


    # DEBUG
    DEBUG = False

    # CLASS NAME
    CLASS_NAME = "Entity_TraitModelTest"

    # Entity Type slugs
    ENTITY_TYPE_SLUG_PERSON = "person"
    
    # test values
    TEST_ENTITY_TRAIT_VALUE_INT = "1234567"
    TEST_ENTITY_TRAIT_VALUE_DATETIME = "2019-10-08"
    TEST_DATETIME_FORMAT_STRING = "%Y-%m-%d"
    

    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------------


    def setUp( self ):
        
        """
        setup tasks.  Call function that we'll re-use.
        """

        # call TestHelper.standardSetUp()
        TestHelper.standardSetUp( self )

    #-- END function setUp() --#
        

    def test_setup( self ):

        """
        Tests whether there were errors in setup.
        """
        
        # declare variables
        me = "test_setup"
        error_count = -1
        error_message = ""
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # get setup error count
        setup_error_count = self.setup_error_count
        
        # should be 0
        error_message = ";".join( self.setup_error_list )
        self.assertEqual( setup_error_count, 0, msg = error_message )
        
    #-- END test method test_django_config_installed() --#


    def test_get_trait_value( self ):

        '''
        Things to test passing to the method:

            get_trait_value( self ):
        '''

        # declare variables
        me = "test_get_trait_value"
        entity_instance = None
        entity_type = None
        trait_name = None
        trait_instance = None
        entity_type_trait = None
        my_trait_id = None
        my_trait_name = None
        my_trait_slug = None
        my_trait_label = None
        my_trait_value = None
        
        # declare variables - test values
        test_trait_value = None
        
        # debug
        debug_flag = self.DEBUG

        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_trait_value = TestHelper.TEST_ENTITY_TRAIT_VALUE

        # build a "person" entity.
        entity_instance = TestHelper.create_test_entity()
        entity_type = entity_instance.add_entity_type( self.ENTITY_TYPE_SLUG_PERSON )
        
        # add a test trait
        trait_instance = TestHelper.create_test_entity_trait( entity_instance )
        
        # trait details
        my_trait_id = trait_instance.id
        my_trait_name = trait_instance.name
        my_trait_slug = trait_instance.slug
        my_trait_label = trait_instance.label
        my_trait_value = trait_instance.get_trait_value()
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        print( "trait_instance: {}".format( trait_instance ) )

        #======================================================================#
        # ! make sure value is what we expect.
        #======================================================================#
        
        should_be = test_trait_value
        error_string = "trait value: {} --> should be = {}".format( my_trait_value, should_be )
        self.assertEqual( my_trait_value, should_be, msg = error_string )
                
    #-- END test method test_get_entity_trait_value() --#


    def test_get_trait_value_as_int( self ):

        '''
        Things to test passing to the method:

            get_trait_value_as_int( self ):
        '''

        # declare variables
        me = "test_get_trait_value_as_int"
        entity_instance = None
        entity_type = None
        trait_name = None
        trait_instance = None
        entity_type_trait = None
        my_trait_id = None
        my_trait_name = None
        my_trait_slug = None
        my_trait_label = None
        my_trait_value = None
        
        # declare variables - test values
        test_trait_value = None
        test_trait_value_string = None
        
        # debug
        debug_flag = self.DEBUG

        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_trait_value_string = self.TEST_ENTITY_TRAIT_VALUE_INT
        test_trait_value = int( test_trait_value_string )

        # build a "person" entity.
        entity_instance = TestHelper.create_test_entity()
        entity_type = entity_instance.add_entity_type( self.ENTITY_TYPE_SLUG_PERSON )
        
        # add a test trait
        trait_instance = TestHelper.create_test_entity_trait( entity_instance )
        
        # set value to int
        trait_instance.value = test_trait_value_string
        trait_instance.save()
        
        # trait details
        my_trait_id = trait_instance.id
        my_trait_name = trait_instance.name
        my_trait_slug = trait_instance.slug
        my_trait_label = trait_instance.label
        my_trait_value = trait_instance.get_trait_value_as_int()
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        print( "trait_instance: {}".format( trait_instance ) )

        #======================================================================#
        # ! make sure value is what we expect.
        #======================================================================#
        
        should_be = test_trait_value
        error_string = "trait value: {} --> should be = {}".format( my_trait_value, should_be )
        self.assertEqual( my_trait_value, should_be, msg = error_string )
                
    #-- END test method test_get_trait_value_as_int() --#


    def test_get_trait_value_as_datetime( self ):

        '''
        Things to test passing to the method:

            get_trait_value_as_datetime( self ):
        '''

        # declare variables
        me = "test_get_trait_value_as_datetime"
        entity_instance = None
        entity_type = None
        trait_name = None
        trait_instance = None
        entity_type_trait = None
        my_trait_id = None
        my_trait_name = None
        my_trait_slug = None
        my_trait_label = None
        my_trait_value = None
        
        # declare variables - test values
        test_trait_value = None
        test_trait_value_string = None
        test_format_string = None
        
        # debug
        debug_flag = self.DEBUG

        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_trait_value_string = self.TEST_ENTITY_TRAIT_VALUE_DATETIME
        test_format_string = self.TEST_DATETIME_FORMAT_STRING
        test_trait_value = datetime.datetime.strptime( test_trait_value_string, test_format_string )

        # build a "person" entity.
        entity_instance = TestHelper.create_test_entity()
        entity_type = entity_instance.add_entity_type( self.ENTITY_TYPE_SLUG_PERSON )
        
        # add a test trait
        trait_instance = TestHelper.create_test_entity_trait( entity_instance )
        
        # set value to int
        trait_instance.value = test_trait_value_string
        trait_instance.save()
        
        # trait details
        my_trait_id = trait_instance.id
        my_trait_name = trait_instance.name
        my_trait_slug = trait_instance.slug
        my_trait_label = trait_instance.label
        my_trait_value = trait_instance.get_trait_value_as_datetime( test_format_string )
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        print( "trait_instance: {}".format( trait_instance ) )

        #======================================================================#
        # ! make sure value is what we expect.
        #======================================================================#
        
        should_be = test_trait_value
        error_string = "trait value: {} --> should be = {}".format( my_trait_value, should_be )
        self.assertEqual( my_trait_value, should_be, msg = error_string )
                
    #-- END test method test_get_trait_value_as_datetime() --#


    def test_get_trait_value_as_json( self ):

        '''
        Things to test passing to the method:

            get_trait_value_as_json( self ):
        '''

        # declare variables
        me = "test_get_trait_value_as_json"
        entity_instance = None
        entity_type = None
        trait_name = None
        trait_instance = None
        entity_type_trait = None
        my_trait_id = None
        my_trait_name = None
        my_trait_slug = None
        my_trait_label = None
        my_trait_value = None
        
        # declare variables - test values
        test_trait_value = None
        test_trait_value_string = None
        test_format_string = None
        
        # debug
        debug_flag = self.DEBUG

        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_trait_value_string = TestHelper.TEST_ENTITY_TRAIT_VALUE_JSON
        test_trait_value = json.loads( test_trait_value_string )

        # build a "person" entity.
        entity_instance = TestHelper.create_test_entity()
        entity_type = entity_instance.add_entity_type( self.ENTITY_TYPE_SLUG_PERSON )
        
        # add a test trait
        trait_instance = TestHelper.create_test_entity_trait( entity_instance )
        
        # set value to None, so we get JSON value.
        trait_instance.value = None
        trait_instance.save()
        
        # trait details
        my_trait_id = trait_instance.id
        my_trait_name = trait_instance.name
        my_trait_slug = trait_instance.slug
        my_trait_label = trait_instance.label
        my_trait_value = trait_instance.get_trait_value_as_json()
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        print( "trait_instance: {}".format( trait_instance ) )

        #======================================================================#
        # ! make sure value is what we expect.
        #======================================================================#
        
        should_be = test_trait_value
        error_string = "trait value: {} --> should be = {}".format( my_trait_value, should_be )
        self.assertEqual( my_trait_value, should_be, msg = error_string )
                
    #-- END test method test_get_trait_value_as_json() --#


    def test_get_value_json( self ):

        '''
        Things to test passing to the method:

            get_trait_value_as_json( self ):
        '''

        # declare variables
        me = "test_get_value_json"
        entity_instance = None
        entity_type = None
        trait_name = None
        trait_instance = None
        entity_type_trait = None
        my_trait_id = None
        my_trait_name = None
        my_trait_slug = None
        my_trait_label = None
        my_trait_value = None
        
        # declare variables - test values
        test_trait_value = None
        test_trait_value_string = None
        test_format_string = None
        
        # debug
        debug_flag = self.DEBUG

        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_trait_value_string = TestHelper.TEST_ENTITY_TRAIT_VALUE_JSON
        test_trait_value = json.loads( test_trait_value_string )

        # build a "person" entity.
        entity_instance = TestHelper.create_test_entity()
        entity_type = entity_instance.add_entity_type( self.ENTITY_TYPE_SLUG_PERSON )
        
        # add a test trait
        trait_instance = TestHelper.create_test_entity_trait( entity_instance )
        
        # trait details
        my_trait_id = trait_instance.id
        my_trait_name = trait_instance.name
        my_trait_slug = trait_instance.slug
        my_trait_label = trait_instance.label
        my_trait_value = trait_instance.get_value_json()
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        print( "trait_instance: {}".format( trait_instance ) )

        #======================================================================#
        # ! make sure value is what we expect.
        #======================================================================#
        
        should_be = test_trait_value
        error_string = "trait value: {} --> should be = {}".format( my_trait_value, should_be )
        self.assertEqual( my_trait_value, should_be, msg = error_string )
        
        # try retrieving as string.
        my_trait_value = trait_instance.get_value_json( do_parse_IN = False )
        should_be = test_trait_value_string
        error_string = "trait value: {} --> should be = {}".format( my_trait_value, should_be )
        self.assertEqual( my_trait_value, should_be, msg = error_string )        
                
    #-- END test method test_get_value_json() --#


#-- END test class Entity_TraitModelTest --#
