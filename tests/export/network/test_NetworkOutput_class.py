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
    TEST_SET_RELATION_QUERY_SET = "test_set_relation_query_set"

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


    def test_add_entities_to_dict( self ):

        # def add_entities_to_dict( self, relation_qs_IN, dictionary_IN, include_through_IN = False, store_entity_IN = False ):
        
        # declare variables
        me = "test_add_entities_to_dict"
        debug_flag = None
        test_instance = None
        relation_id_list = None
        relation_qs = None
        entity_dict = None
        entity_dict_count = None
        entity_id = None
        entity_instance = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # create instance
        test_instance = NetworkOutput()
        
        # relation QuerySet
        relation_id_list = TestHelper.TEST_RELATION_IDS_WITH_THROUGH
        relation_qs = Entity_Relation.objects.filter( pk__in = relation_id_list )
        
        # ! ----> call method - defaults
        entity_dict = {}
        entity_dict = test_instance.add_entities_to_dict( relation_qs, entity_dict )
        entity_dict_count = len( entity_dict )
        
        # should have 10 things in it.
        test_value = entity_dict_count
        should_be = 15
        error_string = "Entity dictionary length = {}, should = {}, for relation IDs: {}.".format( test_value, should_be, relation_id_list )
        self.assertEqual( test_value, should_be, msg = error_string )

        # make sure all have value of None
        for entity_id, entity_instance in six.iteritems( entity_dict ):
        
            # all should be None.
            test_value = entity_instance
            error_string = "Entity instance should be None, instead is: {}.".format( entity_instance )
            self.assertIsNone( test_value, msg = error_string )
            
        #-- END loop over entity dictionary --#
        
        # ! ----> call method - load instancees
        entity_dict = {}
        entity_dict = test_instance.add_entities_to_dict( relation_qs, entity_dict, store_entity_IN = True )
        entity_dict_count = len( entity_dict )
        
        # should have 10 things in it.
        test_value = entity_dict_count
        should_be = 15
        error_string = "Entity dictionary length = {}, should = {}, for relation IDs: {}.".format( test_value, should_be, relation_id_list )
        self.assertEqual( test_value, should_be, msg = error_string )        
        
        # make sure all are not None, and are Entity instances with same ID as
        #     key.
        for entity_id, entity_instance in six.iteritems( entity_dict ):
        
            # all should not be None.
            test_value = entity_instance
            error_string = "Entity instance should not be None."
            self.assertIsNotNone( test_value, msg = error_string )
            
            # should be an Entity.
            should_be = Entity
            error_string = "nested instance: {} for ID {} is not of class {}.".format( test_value, entity_id, should_be )
            self.assertIsInstance( test_value, should_be, msg = error_string )
        
            # Entity instance ID should equal key.
            test_value = entity_instance.id
            should_be = entity_id
            error_string = "nested instance ID = {}, should = {}; instance: {}.".format( test_value, should_be, entity_instance )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        #-- END loop over entity dictionary --#
        
        # ! ----> call method - include THROUGH
        entity_dict = {}
        entity_dict = test_instance.add_entities_to_dict( relation_qs, entity_dict, include_through_IN = True )
        entity_dict_count = len( entity_dict )
        
        # should have 21 things in it.
        test_value = entity_dict_count
        should_be = 21
        error_string = "when including THROUGH, Entity dictionary length = {}, should = {}, for relation IDs: {}.".format( test_value, should_be, relation_id_list )
        self.assertEqual( test_value, should_be, msg = error_string )

    #-- END test method test_add_entities_to_dict() --#
        
        
    def test_add_entity_to_dict( self ):

        # def add_entity_to_dict( self, entity_IN, dictionary_IN, store_entity_IN = False ):
        
        # declare variables
        me = "test_add_entity_to_dict"
        debug_flag = None
        test_instance = None
        relation_id_list = None
        relation_instance = None
        relation_qs = None
        from_to_entity_dict = None
        all_entity_dict = None
        relation_index = None
        relation_counter = None
        from_to_count = None
        all_count = None
        from_entity = None
        to_entity = None
        through_entity = None
        entity_dict_count = None
        entity_id = None
        entity_instance = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # create instance
        test_instance = NetworkOutput()
        
        # relation QuerySet
        relation_id_list = TestHelper.TEST_RELATION_IDS_WITH_THROUGH
        relation_qs = Entity_Relation.objects.filter( pk__in = relation_id_list )
                
        # ! ----> loop over relations - (default - don't store Entity instances)

        # initialize
        from_to_entity_dict = {}
        all_entity_dict = {}
        relation_index = -1
        relation_counter = 0
        
        # loop
        for relation_instance in relation_qs:
        
            # increment counters
            relation_index += 1
            relation_counter = relation_index + 1
            
            # retrieve entities
            from_entity = relation_instance.relation_from
            to_entity = relation_instance.relation_to
            through_entity = relation_instance.relation_through
            
            # add entities to dictionaries.
            
            # ! --------> FROM/TO
            from_to_entity_dict = test_instance.add_entity_to_dict( from_entity, from_to_entity_dict )
            from_to_entity_dict = test_instance.add_entity_to_dict( to_entity, from_to_entity_dict )
            entity_dict_count = len( from_to_entity_dict )
            
            # test entity count
            test_value = entity_dict_count
            should_be = TestHelper.TEST_FROM_TO_ENTITY_COUNT_AT_INDEX[ relation_index ]
            error_string = "FROM/TO Entity dictionary length = {}, should = {}, relation_index: {}.".format( test_value, should_be, relation_index )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! --------> ALL - FROM/TO/THROUGH
            all_entity_dict = test_instance.add_entity_to_dict( from_entity, all_entity_dict )
            all_entity_dict = test_instance.add_entity_to_dict( to_entity, all_entity_dict )
            all_entity_dict = test_instance.add_entity_to_dict( through_entity, all_entity_dict )
            entity_dict_count = len( all_entity_dict )
            
            # test entity count
            test_value = entity_dict_count
            should_be = TestHelper.TEST_ALL_ENTITY_COUNT_AT_INDEX[ relation_index ]
            error_string = "FROM/TO Entity dictionary length = {}, should = {}, relation_index: {}.".format( test_value, should_be, relation_index )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        #-- END loop over Relations --#
            
        # make sure all have value of None
        for entity_id, entity_instance in six.iteritems( from_to_entity_dict ):
        
            # all should be None.
            test_value = entity_instance
            error_string = "Entity instance should be None, instead is: {}.".format( entity_instance )
            self.assertIsNone( test_value, msg = error_string )
            
        #-- END loop over entity dictionary --#
        
        # ! ----> loop over relations - (don't store Entity instances)

        # initialize
        from_to_entity_dict = {}
        all_entity_dict = {}
        relation_index = -1
        relation_counter = 0
        do_store_entities = False
        
        # loop
        for relation_instance in relation_qs:
        
            # increment counters
            relation_index += 1
            relation_counter = relation_index + 1
            
            # retrieve entities
            from_entity = relation_instance.relation_from
            to_entity = relation_instance.relation_to
            through_entity = relation_instance.relation_through
            
            # add entities to dictionaries.
            
            # ! --------> FROM/TO
            from_to_entity_dict = test_instance.add_entity_to_dict( from_entity, from_to_entity_dict, store_entity_IN = do_store_entities )
            from_to_entity_dict = test_instance.add_entity_to_dict( to_entity, from_to_entity_dict, store_entity_IN = do_store_entities )
            entity_dict_count = len( from_to_entity_dict )
            
            # test entity count
            test_value = entity_dict_count
            should_be = TestHelper.TEST_FROM_TO_ENTITY_COUNT_AT_INDEX[ relation_index ]
            error_string = "FROM/TO Entity dictionary length = {}, should = {}, relation_index: {}.".format( test_value, should_be, relation_index )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! --------> ALL - FROM/TO/THROUGH
            all_entity_dict = test_instance.add_entity_to_dict( from_entity, all_entity_dict, store_entity_IN = do_store_entities )
            all_entity_dict = test_instance.add_entity_to_dict( to_entity, all_entity_dict, store_entity_IN = do_store_entities )
            all_entity_dict = test_instance.add_entity_to_dict( through_entity, all_entity_dict, store_entity_IN = do_store_entities )
            entity_dict_count = len( all_entity_dict )
            
            # test entity count
            test_value = entity_dict_count
            should_be = TestHelper.TEST_ALL_ENTITY_COUNT_AT_INDEX[ relation_index ]
            error_string = "FROM/TO Entity dictionary length = {}, should = {}, relation_index: {}.".format( test_value, should_be, relation_index )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        #-- END loop over Relations --#
            
        # make sure all have value of None
        for entity_id, entity_instance in six.iteritems( from_to_entity_dict ):
        
            # all should be None.
            test_value = entity_instance
            error_string = "Entity instance should be None, instead is: {}.".format( entity_instance )
            self.assertIsNone( test_value, msg = error_string )
            
        #-- END loop over entity dictionary --#
        
        # ! ----> loop over relations - store Entity instances

        # initialize
        from_to_entity_dict = {}
        all_entity_dict = {}
        relation_index = -1
        relation_counter = 0
        do_store_entities = True
        
        # loop
        for relation_instance in relation_qs:
        
            # increment counters
            relation_index += 1
            relation_counter = relation_index + 1
            
            # retrieve entities
            from_entity = relation_instance.relation_from
            to_entity = relation_instance.relation_to
            through_entity = relation_instance.relation_through
            
            # add entities to dictionaries.
            
            # ! --------> FROM/TO
            from_to_entity_dict = test_instance.add_entity_to_dict( from_entity, from_to_entity_dict, store_entity_IN = do_store_entities )
            from_to_entity_dict = test_instance.add_entity_to_dict( to_entity, from_to_entity_dict, store_entity_IN = do_store_entities )
            entity_dict_count = len( from_to_entity_dict )
            
            # test entity count
            test_value = entity_dict_count
            should_be = TestHelper.TEST_FROM_TO_ENTITY_COUNT_AT_INDEX[ relation_index ]
            error_string = "FROM/TO Entity dictionary length = {}, should = {}, relation_index: {}.".format( test_value, should_be, relation_index )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! --------> ALL - FROM/TO/THROUGH
            all_entity_dict = test_instance.add_entity_to_dict( from_entity, all_entity_dict, store_entity_IN = do_store_entities )
            all_entity_dict = test_instance.add_entity_to_dict( to_entity, all_entity_dict, store_entity_IN = do_store_entities )
            all_entity_dict = test_instance.add_entity_to_dict( through_entity, all_entity_dict, store_entity_IN = do_store_entities )
            entity_dict_count = len( all_entity_dict )
            
            # test entity count
            test_value = entity_dict_count
            should_be = TestHelper.TEST_ALL_ENTITY_COUNT_AT_INDEX[ relation_index ]
            error_string = "FROM/TO Entity dictionary length = {}, should = {}, relation_index: {}.".format( test_value, should_be, relation_index )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        #-- END loop over Relations --#
            
        # make sure all are not None, and are Entity instances with same ID as
        #     key.
        for entity_id, entity_instance in six.iteritems( from_to_entity_dict ):
        
            # all should not be None.
            test_value = entity_instance
            error_string = "Entity instance should not be None."
            self.assertIsNotNone( test_value, msg = error_string )
            
            # should be an Entity.
            should_be = Entity
            error_string = "nested instance: {} for ID {} is not of class {}.".format( test_value, entity_id, should_be )
            self.assertIsInstance( test_value, should_be, msg = error_string )
        
            # Entity instance ID should equal key.
            test_value = entity_instance.id
            should_be = entity_id
            error_string = "nested instance ID = {}, should = {}; instance: {}.".format( test_value, should_be, entity_instance )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        #-- END loop over entity dictionary --#
        
        # make sure all are not None, and are Entity instances with same ID as
        #     key.
        for entity_id, entity_instance in six.iteritems( all_entity_dict ):
        
            # all should not be None.
            test_value = entity_instance
            error_string = "Entity instance should not be None."
            self.assertIsNotNone( test_value, msg = error_string )
            
            # should be an Entity.
            should_be = Entity
            error_string = "nested instance: {} for ID {} is not of class {}.".format( test_value, entity_id, should_be )
            self.assertIsInstance( test_value, should_be, msg = error_string )
        
            # Entity instance ID should equal key.
            test_value = entity_instance.id
            should_be = entity_id
            error_string = "nested instance ID = {}, should = {}; instance: {}.".format( test_value, should_be, entity_instance )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        #-- END loop over entity dictionary --#
        
    #-- END test method test_add_entity_to_dict() --#
        
        
    def test_create_entity_dict( self ):

        # declare variables
        me = "test_create_entity_dict"
        debug_flag = None
        test_instance = None
        test_request = None
        entity_dict = None
        entity_dict_count = None
        entity_id = None
        entity_instance = None
        
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
        
        # call method
        entity_dict = test_instance.create_entity_dict()
        entity_dict_count = len( entity_dict )
        
        # should have 72 things in it.
        test_value = entity_dict_count
        should_be = 72
        error_string = "Entity dictionary length = {}, should = {}, for request: {}.".format( test_value, should_be, test_request )
        self.assertEqual( test_value, should_be, msg = error_string )

        # make sure all have value of None
        for entity_id, entity_instance in six.iteritems( entity_dict ):
        
            # all should be None.
            test_value = entity_instance
            error_string = "Entity instance should be None, instead is: {}.".format( entity_instance )
            self.assertIsNone( test_value, msg = error_string )
            
        #-- END loop over entity dictionary --#
        
        # call method
        entity_dict = test_instance.create_entity_dict( load_instance_IN = True )
        entity_dict_count = len( entity_dict )
        
        # should have 72 things in it.
        test_value = entity_dict_count
        should_be = 72
        error_string = "Entity dictionary length = {}, should = {}, for request: {}.".format( test_value, should_be, test_request )
        self.assertEqual( test_value, should_be, msg = error_string )        
        
        # make sure all are not None, and are Entity instances with same ID as
        #     key.
        for entity_id, entity_instance in six.iteritems( entity_dict ):
        
            # all should not be None.
            test_value = entity_instance
            error_string = "Entity instance should not be None."
            self.assertIsNotNone( test_value, msg = error_string )
            
            # should be an Entity.
            should_be = Entity
            error_string = "nested instance: {} for ID {} is not of class {}.".format( test_value, entity_id, should_be )
            self.assertIsInstance( test_value, should_be, msg = error_string )
        
            # Entity instance ID should equal key.
            test_value = entity_instance.id
            should_be = entity_id
            error_string = "nested instance ID = {}, should = {}; instance: {}.".format( test_value, should_be, entity_instance )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        #-- END loop over entity dictionary --#
        
        # call method
        entity_dict = test_instance.create_entity_dict( include_through_IN = True )
        entity_dict_count = len( entity_dict )
        
        # should have 84 things in it.
        test_value = entity_dict_count
        should_be = 84
        error_string = "when including THROUGH, Entity dictionary length = {}, should = {}, for request: {}.".format( test_value, should_be, test_request )
        self.assertEqual( test_value, should_be, msg = error_string )

    #-- END test method test_create_entity_dict() --#
        
        
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

        # ! --------> get/set_relation_query_set()
        test_method = "set_relation_query_set"
        original_value = test_instance.get_relation_query_set()
        new_value = self.TEST_SET_RELATION_QUERY_SET
        test_instance.set_relation_query_set( new_value )
        test_value = test_instance.get_relation_query_set()

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
