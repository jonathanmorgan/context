"""
This file contains tests of the context NetworkDataRequestTest class.

Functions tested:
- add_entity_type()
- get_entity_for_identifier()
- get_entity_trait()
- get_identifier()
- set_entity_trait()
- set_identifier()

"""

# base Python imports
import json
import logging
import os
import sys

# import six
import six

# django imports
import django.test

# context imports
from context.export.network.filter_spec import FilterSpec
from context.export.network.network_data_request import NetworkDataRequest
from context.tests.export.network.test_helper import TestHelper

# python_utilities
from python_utilities.booleans.boolean_helper import BooleanHelper
from python_utilities.exceptions.exception_helper import ExceptionHelper


class FilterSpecTest( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ==> Constants-ish
    #----------------------------------------------------------------------------


    # DEBUG
    DEBUG = False

    # CLASS NAME
    CLASS_NAME = "FilterSpecTest"
    
    # test - get()/set()
    TEST_SET_COMPARISON_TYPE = "test_set_comparison_type"
    TEST_SET_DATA_TYPE = "test_set_data_type"
    TEST_SET_FILTER_SPEC = "test_set_filter_spec"
    TEST_SET_FILTER_SPEC_PROPERTY_NAME = "test_set_filter_spec_property_name"
    TEST_SET_FILTER_SPEC_PROPERTY = "test_set_filter_spec_property"
    TEST_SET_FILTER_TYPE = "test_set_filter_type"
    TEST_SET_MY_Q = "test_set_my_q"
    TEST_SET_NAME = "test_set_name"
    TEST_SET_RELATION_ROLES_LIST = [ FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM, FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO ]
    TEST_SET_TYPE_ID = "test_set_type_id"
    TEST_SET_TYPE_LABEL = "test_set_type_label"
    TEST_SET_VALUE = "test_set_value"
    TEST_SET_VALUE_FROM = "test_set_value_from"
    TEST_SET_VALUE_LIST = "test_set_value_list"
    TEST_SET_VALUE_TO = "test_set_value_to"
    TEST_AGAIN = "_again"

    #----------------------------------------------------------------------
    # ! ==> class methods
    #----------------------------------------------------------------------


    #---------------------------------------------------------------------------
    # ! ==> overridden built-in methods
    #---------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # ! ==> instance methods - setup
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
        
        print( '\n====> In {}.{}'.format( self.CLASS_NAME, me ) )
        
        # get setup error count
        setup_error_count = self.setup_error_count
        
        # should be 0
        error_message = ";".join( self.setup_error_list )
        self.assertEqual( setup_error_count, 0, msg = error_message )
        
    #-- END test method test_django_config_installed() --#


    #----------------------------------------------------------------------------
    # ! ==> instance methods - shared methods
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # ! ==> instance methods - tests
    #----------------------------------------------------------------------------


    def test_child_filter_set_list( self ):

        # declare variables
        me = "test_child_filter_set_list"
        debug_flag = None
        test_instance = None
        test_method = None
        original_value = None
        new_value = None
        test_value = None
        should_be = None
        error_string = None
        test_list = None
        test_list_count = None
        test_filter_spec = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # create a test instance    
        test_instance = FilterSpec()
        
        # Test:
        # - get original value and store (should be empty list)
        # - set new value (new list, with something in it)
        # - get value.
        # - assertEquals( get value, new value )
        # - assertNotEqual( get value, original value )
        
        # get
        test_list = test_instance.get_child_filter_spec_list()
        original_value = test_list
        
        # list should not be none...
        test_value = test_list
        error_string = "Retrieving initial child filter spec list for filter spec {}, returned None".format( test_instance )
        self.assertIsNotNone( test_value, msg = error_string )

        # ...should have length 0.
        test_value = len( test_list )
        should_be = 0
        error_string = "new list length = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # add an item
        test_filter_spec = FilterSpec()
        test_instance.add_to_child_filter_spec_list( test_filter_spec )

        # previously retrieved list should now have length 1
        test_value = len( test_list )
        should_be = 1
        error_string = "new list length = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # add an item
        test_filter_spec = FilterSpec()
        test_instance.add_to_child_filter_spec_list( test_filter_spec )

        # previously retrieved list should now have length 2
        test_value = len( test_list )
        should_be = 2
        error_string = "new list length = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # get
        test_list = test_instance.get_child_filter_spec_list()
        
        # should have length 2
        test_value = len( test_list )
        should_be = 2
        error_string = "new list length = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # should be equal to original_list
        test_value = test_list
        should_be = original_value
        error_string = "list retrieved from instance = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # make totally new list.
        new_list = []
        new_list.append( FilterSpec() )
        new_list.append( FilterSpec() )
        new_list.append( FilterSpec() )
        
        # set list in instance.
        test_instance.set_child_filter_spec_list( new_list )
        
        # get list
        test_list = test_instance.get_child_filter_spec_list()
        
        # should not be equal to original list
        test_value = test_list
        should_not_be = original_value
        error_string = "new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # should be equal to new_list
        test_value = test_list
        should_be = new_list
        error_string = "list retrieved from instance = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # should have length 3
        test_value = len( test_list )
        should_be = 3
        error_string = "new list length = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

    #-- END test method test_child_filter_set_list() --#


    def test_getters_and_setters( self ):

        # declare variables
        me = "test_getters_and_setters"
        debug_flag = None
        test_instance = None
        test_method = None
        original_value = None
        new_value = None
        test_value = None
        should_be = None
        error_string = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # create a test instance    
        test_instance = FilterSpec()
        
        # ! ----> test get()-ers and set()-ers together
        
        # for each (using last loaded test instance):
        # - get original value and store
        # - set new value
        # - get value.
        # - assertEquals( get value, new value )
        # - assertNotEqual( get value, original value )
        
        #----------------------------------------------------------------------#
        # ! --------> set_comparison_type()
        test_method = "set_comparison_type"
        original_value = test_instance.get_comparison_type()
        new_value = self.TEST_SET_COMPARISON_TYPE
        test_instance.set_comparison_type( new_value )
        test_value = test_instance.get_comparison_type()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_comparison_type()
        new_value = "{}{}".format( self.TEST_SET_COMPARISON_TYPE, self.TEST_AGAIN )
        test_instance.set_comparison_type( new_value )
        test_value = test_instance.get_comparison_type()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! --------> set_data_type()
        test_method = "set_data_type"
        original_value = test_instance.get_data_type()
        new_value = self.TEST_SET_DATA_TYPE
        test_instance.set_data_type( new_value )
        test_value = test_instance.get_data_type()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_data_type()
        new_value = "{}{}".format( self.TEST_SET_DATA_TYPE, self.TEST_AGAIN )
        test_instance.set_data_type( new_value )
        test_value = test_instance.get_data_type()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! --------> set_filter_spec()
        test_method = "set_filter_spec"
        original_value = test_instance.get_filter_spec()
        new_value = self.TEST_SET_FILTER_SPEC
        test_instance.set_filter_spec( new_value )
        test_value = test_instance.get_filter_spec()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )
        
        # put back the original so we have a dictionary there.
        test_instance.set_filter_spec( original_value )

        #----------------------------------------------------------------------#
        # ! --------> set_filter_spec_property()
        test_method = "set_filter_spec_property"
        test_name = self.TEST_SET_FILTER_SPEC_PROPERTY_NAME
        original_value = test_instance.get_filter_spec_property( test_name )
        new_value = self.TEST_SET_FILTER_SPEC_PROPERTY
        test_instance.set_filter_spec_property( test_name, new_value )
        test_value = test_instance.get_filter_spec_property( test_name )

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_filter_spec_property( test_name )
        new_value = "{}{}".format( self.TEST_SET_FILTER_SPEC_PROPERTY_NAME, self.TEST_AGAIN )
        test_instance.set_filter_spec_property( test_name, new_value )
        test_value = test_instance.get_filter_spec_property( test_name )

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set to None.
        original_value = test_instance.get_filter_spec_property( test_name )
        new_value = None
        test_instance.set_filter_spec_property( test_name, new_value )
        test_value = test_instance.get_filter_spec_property( test_name )

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! --------> set_filter_type()
        test_method = "set_filter_type"
        original_value = test_instance.get_filter_type()
        new_value = self.TEST_SET_FILTER_TYPE
        test_instance.set_filter_type( new_value )
        test_value = test_instance.get_filter_type()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_filter_type()
        new_value = "{}{}".format( self.TEST_SET_FILTER_TYPE, self.TEST_AGAIN )
        test_instance.set_filter_type( new_value )
        test_value = test_instance.get_filter_type()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! --------> set_my_q()
        test_method = "set_my_q"
        original_value = test_instance.get_my_q()
        new_value = self.TEST_SET_MY_Q
        test_instance.set_my_q( new_value )
        test_value = test_instance.get_my_q()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_my_q()
        new_value = "{}{}".format( self.TEST_SET_MY_Q, self.TEST_AGAIN )
        test_instance.set_my_q( new_value )
        test_value = test_instance.get_my_q()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! --------> set_name()
        test_method = "set_name"
        original_value = test_instance.get_name()
        new_value = self.TEST_SET_NAME
        test_instance.set_name( new_value )
        test_value = test_instance.get_name()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_name()
        new_value = "{}{}".format( self.TEST_SET_NAME, self.TEST_AGAIN )
        test_instance.set_name( new_value )
        test_value = test_instance.get_name()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! --------> set_relation_roles_list()
        test_method = "set_relation_roles_list"
        original_value = list( test_instance.get_relation_roles_list() )
        new_value = self.TEST_SET_RELATION_ROLES_LIST
        test_instance.set_relation_roles_list( new_value )
        test_value = test_instance.get_relation_roles_list()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = list ( test_instance.get_relation_roles_list() )
        new_value.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_instance.set_relation_roles_list( new_value )
        test_value = test_instance.get_relation_roles_list()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, retrieved {}, should = {}.".format( test_method, new_value, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! TODO set_type_id()
        test_method = "set_type_id"
        original_value = test_instance.get_type_id()
        new_value = self.TEST_SET_TYPE_ID
        test_instance.set_type_id( new_value )
        test_value = test_instance.get_type_id()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_type_id()
        new_value = "{}{}".format( self.TEST_SET_TYPE_ID, self.TEST_AGAIN )
        test_instance.set_type_id( new_value )
        test_value = test_instance.get_type_id()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! TODO set_type_label()
        test_method = "set_type_label"
        original_value = test_instance.get_type_label()
        new_value = self.TEST_SET_TYPE_LABEL
        test_instance.set_type_label( new_value )
        test_value = test_instance.get_type_label()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_type_label()
        new_value = "{}{}".format( self.TEST_SET_TYPE_LABEL, self.TEST_AGAIN )
        test_instance.set_type_label( new_value )
        test_value = test_instance.get_type_label()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! TODO set_value()
        test_method = "set_value"
        original_value = test_instance.get_value()
        new_value = self.TEST_SET_VALUE
        test_instance.set_value( new_value )
        test_value = test_instance.get_value()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_value()
        new_value = "{}{}".format( self.TEST_SET_VALUE, self.TEST_AGAIN )
        test_instance.set_value( new_value )
        test_value = test_instance.get_value()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! TODO set_value_from()
        test_method = "set_value_from"
        original_value = test_instance.get_value_from()
        new_value = self.TEST_SET_VALUE_FROM
        test_instance.set_value_from( new_value )
        test_value = test_instance.get_value_from()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_value_from()
        new_value = "{}{}".format( self.TEST_SET_VALUE_FROM, self.TEST_AGAIN )
        test_instance.set_value_from( new_value )
        test_value = test_instance.get_value_from()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! TODO set_value_list()
        test_method = "set_value_list"
        original_value = test_instance.get_value_list()
        new_value = self.TEST_SET_VALUE_LIST
        test_instance.set_value_list( new_value )
        test_value = test_instance.get_value_list()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_value_list()
        new_value = "{}{}".format( self.TEST_SET_VALUE_LIST, self.TEST_AGAIN )
        test_instance.set_value_list( new_value )
        test_value = test_instance.get_value_list()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! TODO set_value_to()
        test_method = "set_value_to"
        original_value = test_instance.get_value_to()
        new_value = self.TEST_SET_VALUE_TO
        test_instance.set_value_to( new_value )
        test_value = test_instance.get_value_to()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_value_to()
        new_value = "{}{}".format( self.TEST_SET_VALUE_TO, self.TEST_AGAIN )
        test_instance.set_value_to( new_value )
        test_value = test_instance.get_value_to()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

    #-- END test method test_getters_and_setters() --#


#-- END test class FilterSpecTest --#
