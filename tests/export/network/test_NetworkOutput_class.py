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
import difflib
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
from context.export.network.ndo_simple_matrix import NDO_SimpleMatrix
from context.export.network.ndo_csv_matrix import NDO_CSVMatrix
from context.export.network.ndo_tab_delimited_matrix import NDO_TabDelimitedMatrix
from context.export.network.network_data_request import NetworkDataRequest
from context.export.network.network_output import NetworkOutput
from context.models import Entity
from context.models import Entity_Relation
from context.tests.export.network.test_helper import TestHelper

# python_utilities
from python_utilities.booleans.boolean_helper import BooleanHelper
from python_utilities.django_utils.django_test_case_helper import DjangoTestCaseHelper
from python_utilities.exceptions.exception_helper import ExceptionHelper


class NetworkOutputTest( DjangoTestCaseHelper ):
    

    #----------------------------------------------------------------------------
    # ! ==> Constants-ish
    #----------------------------------------------------------------------------


    # DEBUG
    DEBUG = False
    LOGGER_NAME = "context.tests.export.network.test_NetworkOutput_class.py.NetworkOutputTest"

    # CLASS NAME
    CLASS_NAME = "NetworkOutputTest"
    
    # test - get()/set()
    TEST_SET_NDO_INSTANCE = "test_set_NDO_instance"
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
        #TestHelper.standardSetUp( self )
        TestHelper.standardSetUp( self, fixture_list_IN = TestHelper.FIXTURE_LIST_DATA )

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


    #----------------------------------------------------------------------------
    # ! ==> instance methods - shared methods
    #----------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # ! ==> instance methods - tests
    #----------------------------------------------------------------------------


    def test_create_NDO_instance( self ):

        # declare variables
        me = "test_create_NDO_instance"
        debug_flag = None
        test_instance = None
        test_request = None
        test_NDO_instance = None
        output_format = None
        test_value = None
        should_be = None
        error_string = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # create instance
        test_instance = NetworkOutput()
        
        # initialize request
        test_request = TestHelper.load_basic()
        test_instance.set_network_data_request( test_request )
        
        #----------------------------------------------------------------------#
        # ! ----> retrieve NDO instance - default (TSV_matrix)
        output_format = test_request.get_output_format()
        test_NDO_instance = test_instance.create_NDO_instance()
        
        # output_format of instance should match format from request.
        test_value = test_NDO_instance.get_output_format()
        should_be = output_format
        error_string = "NDO output format = {}, should = {} for NDO instance: {}.".format( test_value, should_be, test_NDO_instance )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # instance should be of expected class.
        test_value = test_NDO_instance
        should_be = NDO_TabDelimitedMatrix
        error_string = "NDO instance: {} is not of class {}.".format( test_value, should_be )
        self.assertIsInstance( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> retrieve NDO instance - TSV_matrix
        test_request.set_output_format( NetworkDataRequest.PROP_VALUE_OUTPUT_FORMAT_TSV_MATRIX )
        output_format = test_request.get_output_format()
        test_NDO_instance = test_instance.create_NDO_instance()
        
        # output_format of instance should match format from request.
        test_value = test_NDO_instance.get_output_format()
        should_be = output_format
        error_string = "NDO output format = {}, should = {} for NDO instance: {}.".format( test_value, should_be, test_NDO_instance )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # instance should be of expected class.
        test_value = test_NDO_instance
        should_be = NDO_TabDelimitedMatrix
        error_string = "NDO instance: {} is not of class {}.".format( test_value, should_be )
        self.assertIsInstance( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> retrieve NDO instance - default (CSV_matrix)
        test_request.set_output_format( NetworkDataRequest.PROP_VALUE_OUTPUT_FORMAT_CSV_MATRIX )
        output_format = test_request.get_output_format()
        test_NDO_instance = test_instance.create_NDO_instance()
        
        # output_format of instance should match format from request.
        test_value = test_NDO_instance.get_output_format()
        should_be = output_format
        error_string = "NDO output format = {}, should = {} for NDO instance: {}.".format( test_value, should_be, test_NDO_instance )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # instance should be of expected class.
        test_value = test_NDO_instance
        should_be = NDO_CSVMatrix
        error_string = "NDO instance: {} is not of class {}.".format( test_value, should_be )
        self.assertIsInstance( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> retrieve NDO instance - default (simple_matrix)
        test_request.set_output_format( NetworkDataRequest.PROP_VALUE_OUTPUT_FORMAT_SIMPLE_MATRIX )
        output_format = test_request.get_output_format()
        test_NDO_instance = test_instance.create_NDO_instance()
        
        # output_format of instance should match format from request.
        test_value = test_NDO_instance.get_output_format()
        should_be = output_format
        error_string = "NDO output format = {}, should = {} for NDO instance: {}.".format( test_value, should_be, test_NDO_instance )
        self.assertEqual( test_value, should_be, msg = error_string )
    
        # instance should be of expected class.
        test_value = test_NDO_instance
        should_be = NDO_SimpleMatrix
        error_string = "NDO instance: {} is not of class {}.".format( test_value, should_be )
        self.assertIsInstance( test_value, should_be, msg = error_string )
        
    #-- END test method test_create_NDO_instance() --#


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
        
        # initialize request
        test_request = TestHelper.load_basic()
        test_instance.set_network_data_request( test_request )
        
        # ! ----> test get() using set()
        
        # for each (using last loaded test instance):
        # - get original value and store
        # - set new value
        # - get value.
        # - assertEquals( get value, new value )
        # - assertNotEqual( get value, original value )
        
        # ! --------> get/set_NDO_instance()
        test_method = "set_NDO_instance"
        output_format = test_request.get_output_format()
        test_NDO_instance = test_instance.get_NDO_instance()
        original_value = test_NDO_instance

        # output_format of instance should match format from request.
        test_value = test_NDO_instance.get_output_format()
        should_be = output_format
        error_string = "NDO output format = {}, should = {} for NDO instance: {}.".format( test_value, should_be, test_NDO_instance )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # instance should be of expected class.
        test_value = test_NDO_instance
        should_be = NDO_TabDelimitedMatrix
        error_string = "NDO instance: {} is not of class {}.".format( test_value, should_be )
        self.assertIsInstance( test_value, should_be, msg = error_string )
        
        # set a new value
        new_value = self.TEST_SET_NDO_INSTANCE
        test_instance.set_NDO_instance( new_value )
        test_value = test_instance.get_NDO_instance()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_network_data_request()
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


    def test_render_network_data( self ):

        # declare variables
        me = "test_render_network_data"
        debug_flag = None
        test_instance = None
        test_request = None
        network_data = None
        network_data_char_count = None
        reference_data_file_path = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # create instance
        test_instance = NetworkOutput()
        
        # initialize request
        test_request = TestHelper.load_basic()
        
        # remove output type and file path, so no output
        test_request.set_output_type( None )
        test_request.set_output_file_path( None )
        #test_request.set_output_file_path( TestHelper.TEST_BASIC_TSV_OUTPUT )
        
        # place request in instance.
        test_instance.set_network_data_request( test_request )
        
        # call render
        network_data = test_instance.render_network_data()
        network_data_char_count = len( network_data )
        
        # validate against test file.
        reference_data_file_path = TestHelper.FILE_PATH_NETWORK_DATA_REQUEST_BASIC_TSV_OUTPUT
        self.validate_string_against_file_contents( network_data, reference_data_file_path )
        
    #-- END test method test_render_network_data() --#
        
        
#-- END test class NetworkOutputTest --#
