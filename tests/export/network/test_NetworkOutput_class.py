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
from context.export.network.network_output import NetworkOutput
from context.tests.test_helper import TestHelper

# python_utilities
from python_utilities.booleans.boolean_helper import BooleanHelper
from python_utilities.exceptions.exception_helper import ExceptionHelper


class NetworkOutputTest( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ==> Constants-ish
    #----------------------------------------------------------------------------


    # DEBUG
    DEBUG = False

    # CLASS NAME
    CLASS_NAME = "NetworkOutputTest"
    
    # test - get()/set()
    TEST_SET_NETWORK_DATA_REQUEST = "test_set_network_data_request"

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
        
        # create instance
        test_instance = NetworkOutput()
        
        # ! ----> test get() using set()
        
        # for each (using last loaded test instance):
        # - get original value and store
        # - set new value
        # - get value.
        # - assertEquals( get value, new value )
        # - assertNotEqual( get value, original value )
        
        # ! --------> set_network_data_request()
        test_method = "set_network_data_request"
        original_value = test_instance.get_network_data_request()
        new_value = self.TEST_SET_NETWORK_DATA_REQUEST
        test_instance.set_network_data_request( new_value )
        test_value = test_instance.get_network_data_request()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

    #-- END test method test_getters_and_setters() --#


#-- END test class NetworkOutputTest --#
