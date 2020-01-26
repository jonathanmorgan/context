"""
This file contains tests of the context NetworkDataRequestTest class.
"""

# base Python imports
import json
import logging
import os
import sys

# import six
import six

# django imports
from django.db.models import Q
import django.test

# context imports
from context.export.network.filter_spec import FilterSpec
from context.export.network.network_data_request import NetworkDataRequest
from context.models import Entity
from context.models import Entity_Relation
from context.tests.export.network.test_helper import TestHelper

# python_utilities
from python_utilities.booleans.boolean_helper import BooleanHelper
from python_utilities.exceptions.exception_helper import ExceptionHelper


class NetworkDataRequestTest( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ==> Constants-ish
    #----------------------------------------------------------------------------


    # DEBUG
    DEBUG = False

    # CLASS NAME
    CLASS_NAME = "NetworkDataRequestTest"
    
    # JSON files details are in network-specific TestHelper now.

    # test values
    TEST_OUTPUT_SPEC_LEN = 7
    TEST_OUTPUT_TYPE = "file"
    TEST_OUTPUT_FILE_PATH_BASIC = "./NetworkDataRequest_basic_test_output.tsv"
    TEST_OUTPUT_FILE_PATH_ENTITY_ID = "./NetworkDataRequest_entity_id_test_output.tsv"
    TEST_OUTPUT_FILE_PATH_ENTITY_SELECT = "./NetworkDataRequest_entity_select_test_output.tsv"
    TEST_OUTPUT_FORMAT = "TSV_matrix"
    TEST_OUTPUT_STRUCTURE = "both_trait_columns"
    TEST_OUTPUT_INCLUDE_COLUMN_HEADERS = True
    
    # map of JSON file paths to associated validate functions
    JSON_FILE_TO_VALIDATE_FUNCTION_MAP = {}
    JSON_FILE_TO_VALIDATE_FUNCTION_MAP[ TestHelper.FILE_PATH_NETWORK_DATA_REQUEST_BASIC ] = "validate_instance_basic"
    JSON_FILE_TO_VALIDATE_FUNCTION_MAP[ TestHelper.FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_ID_FILTER ] = "validate_instance_id_filter"
    JSON_FILE_TO_VALIDATE_FUNCTION_MAP[ TestHelper.FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_SELECTION ] = "validate_instance_entity_selection"
    
    # test - get()/set()
    TEST_SET_ENTITY_ID_TO_INSTANCE_MAP = { 1 : None, 2 : None, 3 : None }
    TEST_SET_ENTITY_ID_TO_TRAITS_MAP = { 1 : {}, 2 : {}, 3 : {} }
    TEST_SET_ENTITY_IDS_AND_TRAITS_HEADER_LIST = [ "id_1", "id_2", "id_3", "trait1", "trait_2", "trait_3", "trait_4" ]
    TEST_SET_ENTITY_SELECTION = "test_set_entity_selection"
    TEST_SET_IS_REQUEST_OK = "false"
    TEST_SET_OUTPUT_ENTITY_IDENTIFIERS_LIST = [ { "name" : "identifier_name_1", "source" : "source_1" }, { "name" : "identifier_name_2", "source" : "source_2" } ]
    TEST_SET_OUTPUT_ENTITY_TRAITS_LIST = [ { "name" : "trait_1" }, { "name" : "trait_2" } ]
    TEST_SET_OUTPUT_FILE_PATH = "test_set_output_file_path"
    TEST_SET_OUTPUT_FORMAT = "test_set_output_format"
    TEST_SET_OUTPUT_INCLUDE_COLUMN_HEADERS = "test_set_output_include_column_headers"
    TEST_SET_OUTPUT_SPECIFICATION = "test_set_output_specification"
    TEST_SET_OUTPUT_SPEC_PROPERTY_NAME = "test_set_output_spec_property_name"
    TEST_SET_OUTPUT_SPEC_PROPERTY = "test_set_output_spec_property"
    TEST_SET_OUTPUT_SPEC_PROPERTY_AGAIN = "test_set_output_spec_property_again"
    TEST_SET_OUTPUT_STRUCTURE = "test_set_output_structure"
    TEST_SET_OUTPUT_TYPE = "test_set_output_type"
    TEST_SET_RELATION_QUERY_SET = "test_set_relation_query_set"
    TEST_SET_RELATION_SELECTION = "test_set_relation_selection"
    
    # ! ----> goal values
    GOAL_ENTITY_IDS_AND_TRAITS_HEADER_LIST = []
    GOAL_ENTITY_IDS_AND_TRAITS_HEADER_LIST.append( "id_person_sourcenet_id" )
    GOAL_ENTITY_IDS_AND_TRAITS_HEADER_LIST.append( "id_person_open_calais_uuid" )
    GOAL_ENTITY_IDS_AND_TRAITS_HEADER_LIST.append( "trait_first_name" )
    GOAL_ENTITY_IDS_AND_TRAITS_HEADER_LIST.append( "trait_middle_name" )
    GOAL_ENTITY_IDS_AND_TRAITS_HEADER_LIST.append( "trait_last_name" )
    
    # ! ----> test values for identifier labels
    
    # identifiers
    TEST_ID_NAME = "test_id_name"
    TEST_ID_ID_TYPE = "test_id_type"
    TEST_ID_SOURCE = "test_source"
    TEST_ID_IDENTIFIER_TYPE_ID = "test_identifier_type_id"
    TEST_ID_HEADER = "test_header"
    
    # traits
    TEST_TRAIT_NAME = "test_trait_name"
    TEST_TRAIT_SLUG = "test_trait_slug"
    TEST_TRAIT_ENTITY_TYPE_TRAIT_ID = "test_entity_trait_type_id"
    TEST_TRAIT_HEADER = "test_header"


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
        TestHelper.standardSetUp( self, fixture_list_IN = TestHelper.FIXTURE_LIST_DATA )
        
        # debug flag
        #NetworkDataRequest.DEBUG_FLAG = True

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


    def create_2_level_aggregate( self, test_instance_IN = None ):
        
        # return reference
        filter_OUT = None
        
        # declare variables
        me = "create_2_level_aggregate"
        test_instance = None
        test_filter_type = None
        test_filter_list = None
        test_filter_spec = None
        test_filter_json_dict = None
        test_value_list = None
        test_role_list = None
        should_be = None
        test_q_list = None
        current_q = None
        test_qs = None
        test_count = None
        
        # do we have a test instance?
        if ( test_instance_IN is not None ):
        
            # yes - test as we go.
            test_instance = test_instance_IN
            
        #-- END check to see if test instance. --#
        
        print( "\n\n------------------------------\n2 level - relation type slug, relation trait, entity type slug, entity trait\n------------------------------" )
        test_filter_list = []
        
        #----------------------------------------------------------------------#
        # ! ----> filter 1 - relation_type_slug in "mentioned", "quoted", "shared_byline"
        test_filter_type = NetworkDataRequest.FILTER_TYPE_RELATION_TYPE_SLUG
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "mentioned" )
        test_value_list.append( "quoted" )
        test_value_list.append( "shared_byline" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 437
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )
        
        #----------------------------------------------------------------------#
        # ! ----> filter 2 - entity type slug
        
        # validate
        test_filter_spec = self.create_simple_1_level_aggregate( test_instance_IN = test_instance )
        should_be = 2320

        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        #----------------------------------------------------------------------#
        # ! ----> filter 3 - relation traits
                
        # validate
        test_filter_spec = self.create_complex_1_level_aggregate( test_instance_IN = test_instance )
        should_be = 1433

        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )
        
        #----------------------------------------------------------------------#
        # ! ----> filter 4 - entity trait "sourcenet-Newspaper-ID" IN 1
        test_filter_type = NetworkDataRequest.FILTER_TYPE_ENTITY_TRAIT
        test_filter_spec = FilterSpec()
        test_filter_spec.set_name( "sourcenet-Newspaper-ID" )
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_filter_spec.set_value_list( [ 1 ] )
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = 945
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )
        
        # ! --------> AND
        
        test_filter_type = NetworkDataRequest.FILTER_TYPE_AND
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND )
        test_filter_spec.set_value_list( test_filter_list )
        should_be = 112
        
        # print the JSON
        test_filter_spec_json_string = test_filter_spec.output_filter_spec_as_json_string()
        print( "\n\n2-level filter spec test - JSON:\n{}".format( test_filter_spec_json_string ) )
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            #self.validate_filter_spec( test_instance, test_filter_spec, should_be, do_compact_queryset_IN = False )
            #self.validate_filter_spec( test_instance, test_filter_spec, should_be, do_compact_queryset_IN = True )
            
        #-- END check to see if we validate --#
       
        filter_OUT = test_filter_spec
        
        return filter_OUT
        
    #-- END method create_2_level_aggregate() --#


    def create_2_level_aggregate_test( self, test_instance_IN = None ):
        
        # return reference
        filter_OUT = None
        
        # declare variables
        me = "create_2_level_aggregate_test"
        test_instance = None
        test_filter_type = None
        test_filter_list = None
        test_filter_spec = None
        test_filter_json_dict = None
        test_value_list = None
        test_role_list = None
        should_be = None
        test_q_list = None
        current_q = None
        test_qs = None
        test_count = None
        
        # do we have a test instance?
        if ( test_instance_IN is not None ):
        
            # yes - test as we go.
            test_instance = test_instance_IN
            
        #-- END check to see if test instance. --#
        
        print( "\n\n------------------------------\n2 level - relation type slug, relation trait, entity type slug, entity trait\n------------------------------" )
        test_filter_list = []
        
        #----------------------------------------------------------------------#
        # ! ----> filter 1 - relation_type_slug in "mentioned", "quoted", "shared_byline"
        test_filter_type = NetworkDataRequest.FILTER_TYPE_RELATION_TYPE_SLUG
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "mentioned" )
        test_value_list.append( "quoted" )
        test_value_list.append( "shared_byline" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 437
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )
        
        #----------------------------------------------------------------------#
        # ! ----> filter 2 - relation traits
        
        # validate
        test_filter_spec = self.create_complex_1_level_aggregate( test_instance_IN = test_instance )
        should_be = 1433

        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )
        
        #----------------------------------------------------------------------#
        # ! ----> filter 3 - entity type slug        

        # validate
        test_filter_spec = self.create_simple_1_level_aggregate( test_instance_IN = test_instance )
        should_be = 2320

        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        #----------------------------------------------------------------------#
        # ! ----> filter 4 - entity trait "sourcenet-Newspaper-ID" IN 1
        test_filter_type = NetworkDataRequest.FILTER_TYPE_ENTITY_TRAIT
        test_filter_spec = FilterSpec()
        test_filter_spec.set_name( "sourcenet-Newspaper-ID" )
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_filter_spec.set_value_list( [ 1 ] )
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = 945
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )
        
        # ! --------> AND
        
        test_filter_type = NetworkDataRequest.FILTER_TYPE_AND
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND )
        test_filter_spec.set_value_list( test_filter_list )
        should_be = 112
        
        # print the JSON
        test_filter_spec_json_string = test_filter_spec.output_filter_spec_as_json_string()
        print( "\n\n2-level filter spec test - JSON:\n{}".format( test_filter_spec_json_string ) )
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            #self.validate_filter_spec( test_instance, test_filter_spec, should_be, do_compact_queryset_IN = False )
            #self.validate_filter_spec( test_instance, test_filter_spec, should_be, do_compact_queryset_IN = True )
            
        #-- END check to see if we validate --#
       
        filter_OUT = test_filter_spec
        
        return filter_OUT
        
    #-- END method create_2_level_aggregate_test() --#


    def create_complex_1_level_aggregate( self,
                                          test_instance_IN = None ):
        
        # return reference
        filter_OUT = None
        
        # declare variables
        me = "create_complex_1_level_aggregate"
        test_instance = None
        test_filter_type = None
        test_filter_list = None
        test_filter_spec = None
        test_filter_json_dict = None
        test_value_list = None
        test_role_list = None
        should_be = None
        test_q_list = None
        current_q = None
        test_qs = None
        test_count = None
        
        # do we have a test instance?
        if ( test_instance_IN is not None ):
        
            # yes - test as we go.
            test_instance = test_instance_IN
            
        #-- END check to see if test instance. --#
        
        print( "\n\n------------------------------\nmore complex - 1 level - relation_trait\n------------------------------" )
        test_filter_type = NetworkDataRequest.FILTER_TYPE_RELATION_TRAIT
        test_filter_list = []
        test_q_list = []
        
        #----------------------------------------------------------------------#
        # ! ----> filter 1 - pub_date in range 2009-12-01 to 2009-12-31
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "pub_date" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_IN_RANGE )
        test_filter_spec.set_value_from( "2009-12-01" )
        test_filter_spec.set_value_to( "2009-12-31" )
        should_be = 1703
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_q_list.append( test_filter_spec.get_my_q() )
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        #----------------------------------------------------------------------#
        # ! ----> filter 2 - coder user in "automated"
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "sourcenet-coder-User-username" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "automated" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 2739
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_q_list.append( test_filter_spec.get_my_q() )
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        #----------------------------------------------------------------------#
        # ! ----> filter 3 - coder type in "OpenCalais_REST_API_v2"
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "coder_type" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "OpenCalais_REST_API_v2" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 2739
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_q_list.append( test_filter_spec.get_my_q() )
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        # ! ----> base test
        
        test_qs = Entity_Relation.objects.all()
        for current_q in test_q_list:
        
            test_qs = test_qs.filter( current_q )
            
        #-- END loop over Q instances --#
        test_count = test_qs.count()
        
        # sanity check
        test_value = test_count
        should_be = 1433
        error_string = "Processing complex single-level filter spec by hand, found {} relations, should_be: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )        
        
        # ! ----> aggregate        
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND )
        test_filter_spec.set_value_list( test_filter_list )
        should_be = 1433
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
        
        filter_OUT = test_filter_spec
        
        return filter_OUT

    #-- END method create_complex_1_level_aggregate() --#


    def create_simple_1_level_aggregate( self,
                                         comparison_type_IN = FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND,
                                         test_instance_IN = None ):
        
        # return reference
        filter_OUT = None
        
        # declare variables
        me = "create_simple_1_level_aggregate"
        test_instance = None
        test_filter_type = None
        test_filter_list = None
        test_filter_spec = None
        test_filter_json_dict = None
        test_role_list = None
        should_be = None
        
        # do we have a test instance?
        if ( test_instance_IN is not None ):
        
            # yes - test as we go.
            test_instance = test_instance_IN
            
        #-- END check to see if test instance. --#
        
        print( "\n\n------------------------------\nsimple - 1 level - entity type slug\n------------------------------" )
        test_filter_type = NetworkDataRequest.FILTER_TYPE_ENTITY_TYPE_SLUG
        test_filter_list = []
        
        #----------------------------------------------------------------------#
        # ! ----> filter 1 - FROM entity type slug = "person"
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        test_filter_spec.set_value( "person" )
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = 2320
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        #----------------------------------------------------------------------#
        # ! ----> filter 2 - TO entity type slug = "person"
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        test_filter_spec.set_value( "person" )
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = 3169
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        #----------------------------------------------------------------------#
        # ! ----> filter 3 - THROUGH entity type slug = "article"
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        test_filter_spec.set_value( "article" )
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = 2743
        
        # validate?
        if ( test_instance is not None ):
        
            # validate
            self.validate_filter_spec( test_instance, test_filter_spec, should_be )
            
        #-- END check to see if we validate --#
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( comparison_type_IN )
        test_filter_spec.set_value_list( test_filter_list )
        
        # validate?
        if ( test_instance is not None ):
        
            if ( ( comparison_type_IN == FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND )
                or ( comparison_type_IN == FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND_FILTER ) ):

                # AND
                should_be = 2320

                # validate
                self.validate_filter_spec( test_instance, test_filter_spec, should_be )
                    
            elif ( comparison_type_IN == FilterSpec.PROP_VALUE_COMPARISON_TYPE_OR ):
                
                # OR
                should_be = 3169

                # validate
                self.validate_filter_spec( test_instance, test_filter_spec, should_be )
                
            #-- END check to see if known comparison type --#
            
        #-- END check to see if we are testing. --#
        
        filter_OUT = test_filter_spec
        
        return filter_OUT
    
    #-- END method create_simple_1_level_aggregate() --#
    

    def validate_entity_selection( self, test_instance_IN ):        

        # declare variables
        me = "validate_entity_selection"
        test_temp = None
        test_value = None
        should_be = None
        error_message = None
        properties_count = None
        entity_selection_dict = None
        entity_selection_count = None

        # got test instance?
        if ( test_instance_IN is not None ):
        
            # there is just one property.
            properties_count = 1
        
            # ! ----> validate entity_selection
            entity_selection_dict = test_instance_IN.get_entity_selection()
            
            # count the items
            entity_selection_count = len( entity_selection_dict )
            test_value = entity_selection_count
            should_be = properties_count
            error_string = "entity_selection has {} items, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        else:
        
            # no instance passed in.  Assert Not None here, so we raise Error.
            test_value = test_instance_IN
            error_string = "None passed in, should be a NetworkDataRequest instance."
            self.assertIsNotNone( test_value, msg = error_string )
            
        #-- END check to see if instance passed in. --#
        
    #-- END method validate_entity_selection() --#
    

    def validate_filter_spec( self,
                              test_instance_IN,
                              filter_spec_IN,
                              result_count_IN,
                              do_compact_queryset_IN = False ):
        
        # declare variables
        me = "validate_filter_spec"
        test_instance = None
        test_filter_spec = None
        result_count = None
        relation_qs = None
        filter_comparison_type = None
        test_q = None
        test_value = None
        should_be = None
        error_string = None
        result_status = None
        result_status_is_error = None
        test_qs = None
        test_count = None
        
        # init
        test_instance = test_instance_IN
        test_filter_spec = filter_spec_IN
        result_count = result_count_IN
        relation_qs = Entity_Relation.objects.all()
        
        # call the appropriate build method.
        result_status = test_instance.build_filter_spec_q( test_filter_spec )
        
        # assert no error
        result_status_is_error = result_status.is_error()
        test_value = result_status_is_error
        should_be = False
        error_string = "Processing filter spec {}, got error status ( {}, should be {} ) from build_filter_spec_q(): {}.".format( test_filter_spec, test_value, should_be, result_status )
        self.assertEqual( test_value, should_be, msg = error_string )        
        
        # let filter_relations_by_filter_spec() figure out what to do based on
        #     type - aggregate or not...
        test_qs = test_instance.filter_relations_by_filter_spec( relation_qs,
                                                                 test_filter_spec,
                                                                 do_compact_queryset_IN = do_compact_queryset_IN )
        test_count = test_qs.count()
    
        # should be value passed in.
        test_value = test_count
        should_be = result_count
        error_string = "Processing filter spec {}, found {} relations, should_be: {}.".format( test_filter_spec, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )        
    
    #-- END method validate_filter_spec() --#


    def validate_instance_basic( self, test_instance_IN ):        

        # declare variables
        me = "validate_instance_basic"
        test_temp = None
        test_value = None
        should_be = None
        error_message = None

        # got test instance?
        if ( test_instance_IN is not None ):
        
            # ! ----> validate output_specification
            self.validate_output_spec( test_instance_IN )
            
            # ! ----> validate relation_selection
            self.validate_relation_selection( test_instance_IN )

        else:
        
            # no instance passed in.  Assert Not None here, so we raise Error.
            test_value = test_instance_IN
            error_string = "None passed in, should be a NetworkDataRequest instance."
            self.assertIsNotNone( test_value, msg = error_string )
            
        #-- END check to see if instance passed in. --#
        
    #-- END method validate_instance_basic() --#
    

    def validate_instance_empty( self, test_instance_IN ):
        
        # declare variables
        me = "validate_instance_empty"
        test_value = None
        should_be = None
        error_message = None

        # got test instance?
        if ( test_instance_IN is not None ):
            
            pass
            
        #-- END check if instance --#
        
    #-- END method validate_instance_empty() --#
    

    def validate_instance_entity_selection( self, test_instance_IN ):
        
        # declare variables
        me = "validate_instance_entity_selection"
        test_value = None
        should_be = None
        error_message = None

        # got test instance?
        if ( test_instance_IN is not None ):
        
            # ! ----> validate output_specification
            self.validate_output_spec( test_instance_IN, output_file_path_IN = self.TEST_OUTPUT_FILE_PATH_ENTITY_SELECT )
            
            # ! ----> validate relation_selection
            self.validate_relation_selection( test_instance_IN )

            # ! ----> validate entity_selection
            self.validate_entity_selection( test_instance_IN )

        else:
        
            # no instance passed in.  Assert Not None here, so we raise Error.
            test_value = test_instance_IN
            error_string = "None passed in, should be a NetworkDataRequest instance."
            self.assertIsNotNone( test_value, msg = error_string )
            
        #-- END check to see if instance passed in. --#
        
    #-- END method validate_instance_entity_selection() --#
    

    def validate_instance_id_filter( self, test_instance_IN ):
        
        # declare variables
        me = "validate_instance_id_filter"
        test_value = None
        should_be = None
        error_message = None

        # got test instance?
        if ( test_instance_IN is not None ):
        
            # ! ----> validate output_specification
            self.validate_output_spec( test_instance_IN, output_file_path_IN = self.TEST_OUTPUT_FILE_PATH_ENTITY_ID )

            # ! ----> validate same as basic, plus entity id filter
            self.validate_relation_selection( test_instance_IN )

        else:
        
            # no instance passed in.  Assert Not None here, so we raise Error.
            test_value = test_instance_IN
            error_string = "None passed in, should be a NetworkDataRequest instance."
            self.assertIsNotNone( test_value, msg = error_string )
            
        #-- END check to see if instance passed in. --#
        
    #-- END method validate_instance_id_filter() --#
    

    def validate_output_spec( self, test_instance_IN, output_file_path_IN = None ):
        
        # declare variables
        me = "validate_output_spec"
        test_value = None
        should_be = None
        error_message = None
        output_spec = None
        output_spec_length = None
        output_type = None
        output_file_path = None
        output_format = None
        output_structure = None
        output_include_column_headers = None
        should_be_output_file_path = None

        # got test instance?
        if ( test_instance_IN is not None ):
        
            # is there an output_specification?
            output_spec = test_instance_IN.get_output_specification()
            
            # should not be None
            test_value = output_spec
            error_string = "No output_specification found, should be a dictionary instance."
            self.assertIsNotNone( test_value, msg = error_string )
            
            # should be 7 things in the output_specification
            test_value = len( output_spec )
            should_be = self.TEST_OUTPUT_SPEC_LEN
            error_string = "nested output_specification dictionary has {} items, should have {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )

            # get output information.

            # output_type
            output_type = test_instance_IN.get_output_type()
            test_value = output_type
            should_be = self.TEST_OUTPUT_TYPE
            error_string = "nested output_type is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # output_file_path
            
            # init
            should_be_output_file_path = self.TEST_OUTPUT_FILE_PATH_BASIC
            if ( output_file_path_IN is not None ):
            
                # use path passed in.
                should_be_output_file_path = output_file_path_IN
                
            #-- END check to see if should be file path passed in --#
            
            output_file_path = test_instance_IN.get_output_file_path()
            test_value = output_file_path
            should_be = should_be_output_file_path
            error_string = "nested output_file_path is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )

            # output_format
            output_format = test_instance_IN.get_output_format()
            test_value = output_format
            should_be = self.TEST_OUTPUT_FORMAT
            error_string = "nested output_format is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )

            # output_structure
            output_structure = test_instance_IN.get_output_structure()
            test_value = output_structure
            should_be = self.TEST_OUTPUT_STRUCTURE
            error_string = "nested output_structure is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )

            # output_include_column_headers
            output_include_column_headers = test_instance_IN.get_output_include_column_headers()
            test_value = output_include_column_headers
            should_be = self.TEST_OUTPUT_INCLUDE_COLUMN_HEADERS
            error_string = "nested output_include_column_headers is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )            

        else:
        
            # no instance passed in.  Assert Not None here, so we raise Error.
            test_value = test_instance_IN
            error_string = "None passed in, should be a NetworkDataRequest instance."
            self.assertIsNotNone( test_value, msg = error_string )
            
        #-- END check to see if instance passed in. --#
        
    #-- END method validate_output_spec() --#


    def validate_relation_selection( self, test_instance_IN ):        

        # declare variables
        me = "validate_relation_selection"
        test_temp = None
        test_value = None
        should_be = None
        error_message = None
        properties_count = None
        relation_selection_dict = None
        relation_selection_count = None

        # got test instance?
        if ( test_instance_IN is not None ):
        
            # should just be 1 property, for now, the filter_specification.
            properties_count = 1
                
            # ! ----> validate relation_selection
            relation_selection_dict = test_instance_IN.get_relation_selection()
            
            # count the items
            relation_selection_count = len( relation_selection_dict )
            test_value = relation_selection_count
            should_be = properties_count
            error_string = "relation_selection has {} items, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        else:
        
            # no instance passed in.  Assert Not None here, so we raise Error.
            test_value = test_instance_IN
            error_string = "None passed in, should be a NetworkDataRequest instance."
            self.assertIsNotNone( test_value, msg = error_string )
            
        #-- END check to see if instance passed in. --#
        
    #-- END method validate_relation_selection() --#
    

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
        test_instance = NetworkDataRequest()
        
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
        test_instance = NetworkDataRequest()
        
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
        
        
    def test_build_filter_spec_aggregate_q( self ):

        # declare variables
        me = "test_build_filter_spec_aggregate_q"
        debug_flag = None
        test_filter_list = None
        test_instance = None
        test_q = None
        test_value = None
        relation_qs = None
        should_be = None
        error_string = None
        test_filter_spec = None
        test_filter_type = None
        test_role_list = None
        test_value_list = None
        test_filter_json_dict = None
        nested_test_filter_list = None
        simple_1_filter_spec = None
        complex_1_filter_spec = None
        test_q_list = None
        test_filter_spec_json_string = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_instance = TestHelper.load_with_entity_id_filter()
        nested_test_filter_list = []
        
        #----------------------------------------------------------------------#
        # ! ----> simple - 1 level - entity type slug
        #----------------------------------------------------------------------#
        
        # ! --------> AND

        # create simple aggregate
        test_filter_spec = self.create_simple_1_level_aggregate( comparison_type_IN = FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND,
                                                                 test_instance_IN = test_instance )
        should_be = 2320
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # and, store for later.
        simple_1_filter_spec = test_filter_spec
        nested_test_filter_list.append( test_filter_spec )

        # ! --------> OR

        test_filter_list = test_filter_spec.get_value_list()
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_OR )
        test_filter_spec.set_value_list( test_filter_list )
        should_be = 3169
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        #----------------------------------------------------------------------#
        # ! ----> more complex - 1 level - relation_trait
        #----------------------------------------------------------------------#
        
        # create more complex aggregate
        test_filter_spec = self.create_complex_1_level_aggregate( test_instance )
        
        # ! --------> AND
        
        should_be = 1433
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # and, store for later.
        complex_1_filter_spec = test_filter_spec
        nested_test_filter_list.append( test_filter_spec )
        
        #----------------------------------------------------------------------#
        # ! ----> 2 level - relation type slug, relation trait, entity type slug, entity trait
        #----------------------------------------------------------------------#
        
        # create test_filter_spec
        test_filter_spec = self.create_2_level_aggregate_test( test_instance )

        # test
        should_be = 112
        
        # print the JSON
        if ( debug_flag == True ):

            test_filter_spec_json_string = test_filter_spec.output_filter_spec_as_json_string()
            print( "\n\n2-level filter spec test - JSON:\n{}".format( test_filter_spec_json_string ) )
            
        #-- END DEBUG --#
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        #self.validate_filter_spec( test_instance, test_filter_spec, should_be, do_compact_queryset_IN = False )
        #self.validate_filter_spec( test_instance, test_filter_spec, should_be, do_compact_queryset_IN = True )
        
    #-- END test method build_filter_spec_aggregate_q() --#


    def test_build_filter_spec_entity_id_q( self ):

        # declare variables
        me = "test_build_filter_spec_entity_id_q"
        debug_flag = None
        test_instance = None
        test_value = None
        relation_qs = None
        should_be = None
        error_string = None
        test_filter_spec = None
        test_filter_type = None
        test_role_list = None
        test_qs = None
        test_count = None
        test_value_list = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_instance = TestHelper.load_with_entity_id_filter()
        test_filter_type = NetworkDataRequest.FILTER_TYPE_ENTITY_ID
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "equals"
        #----------------------------------------------------------------------#
        
        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "person_sourcenet_id" )
        test_filter_spec.set_value( "2020202" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # counts for good match.
        match_all = 28
        match_from_to = match_all
        match_from = 11
        match_to = 17
        match_through = 0
        
        # --------> single match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "person_sourcenet_id" )
        test_filter_spec.set_value( "202" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> single match - roles = "ALL".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO", "THROUGH" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM"
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "TO"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "THROUGH"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_through
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "includes"
        #----------------------------------------------------------------------#
        
        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "person_sourcenet_id" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "20202020" )
        test_value_list.append( "20202021" )
        test_value_list.append( "20202022" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # counts for good match.
        match_all = 135
        match_from_to = match_all
        match_from = 88
        match_to = 63
        match_through = 0
        
        # --------> default roles = "ALL".
        test_value_list = []
        test_value_list.append( "46" )
        test_value_list.append( "163" )
        test_value_list.append( "161" )
        test_value_list.append( "164" )
        test_value_list.append( "30" )
        test_value_list.append( "175" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> single match - roles = "ALL".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO", "THROUGH" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM"
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "TO"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "THROUGH"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_through
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "excludes"
        #----------------------------------------------------------------------#
        
        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "person_sourcenet_id" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EXCLUDES )
        test_value_list = []
        test_value_list.append( "20202020" )
        test_value_list.append( "20202021" )
        test_value_list.append( "20202022" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 3162
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # counts for good match.
        match_all = 3124
        match_from_to = match_all
        match_from = 2228
        match_to = 3099
        match_through = 0
        
        # --------> default roles = "ALL".
        test_value_list = []
        test_value_list.append( "46" )
        test_value_list.append( "163" )
        test_value_list.append( "161" )
        test_value_list.append( "164" )
        test_value_list.append( "30" )
        test_value_list.append( "175" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> single match - roles = "ALL".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO", "THROUGH" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM"
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "TO"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "THROUGH"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_through
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
    #-- END test method test_build_filter_spec_entity_id_q() --#


    def test_build_filter_spec_entity_q_target_roles( self ):
        
        # declare variables
        me = "test_build_filter_spec_entity_trait_q"
        debug_flag = None
        test_instance = None
        test_filter_type = None
        entity_qs = None
        entity_filter_q = None
        test_q = None
        relation_qs = None

        test_value = None
        relation_qs = None
        should_be = None
        error_string = None
        test_filter_spec = None
        test_role_list = None
        test_qs = None
        test_count = None
        test_value_list = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_instance = TestHelper.load_with_entity_id_filter()
        test_filter_type = NetworkDataRequest.FILTER_TYPE_ENTITY_TYPE_SLUG

        # ! ----> type slugs "person" or "article"
        
        # make QuerySet of entities (to start, entity types person and article)
        entity_qs = Entity.objects.all()
        test_value_list = []
        test_value_list.append( "person" )
        test_value_list.append( "article" )
        entity_filter_q = Q( entity_types__entity_type__slug__in = test_value_list )
        entity_qs = entity_qs.filter( entity_filter_q )
        
        # make sure we have right entity count
        test_value = entity_qs.count()
        should_be = 315
        error_string = "Filtered entities: count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # start with Entity_Relation QS
        relation_qs = Entity_Relation.objects.all()

        # make sure we have right starting relation count
        test_value = relation_qs.count()
        should_be = 3215
        error_string = "Total relations: count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> ALL
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 3215
        error_string = "ALL count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> FROM | TO | THROUGH
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 3215
        error_string = "FROM | TO | THROUGH count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> FROM | TO
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 3215
        error_string = "FROM | TO count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> FROM | THROUGH
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 3169
        error_string = "FROM | THROUGH count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> TO | THROUGH
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 3215
        error_string = "TO | THROUGH count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> FROM
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 2746
        error_string = "FROM count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> TO
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 3215
        error_string = "TO count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> THROUGH
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 2743
        error_string = "THROUGH count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! ----> type slugs "newspaper" or "article"
        
        # make QuerySet of entities (to start, entity types person and article)
        entity_qs = Entity.objects.all()
        test_value_list = []
        test_value_list.append( "newspaper" )
        test_value_list.append( "article" )
        entity_filter_q = Q( entity_types__entity_type__slug__in = test_value_list )
        entity_qs = entity_qs.filter( entity_filter_q )
        
        # make sure we have right entity count
        test_value = entity_qs.count()
        should_be = 49
        error_string = "Filtered entities: count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # start with Entity_Relation QS
        relation_qs = Entity_Relation.objects.all()

        # make sure we have right starting relation count
        test_value = relation_qs.count()
        should_be = 3215
        error_string = "Total relations: count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> ALL
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 3215
        error_string = "ALL count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> FROM | TO | THROUGH
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 3215
        error_string = "FROM | TO | THROUGH count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> FROM | TO
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 895
        error_string = "FROM | TO count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> FROM | THROUGH
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 3215
        error_string = "FROM | THROUGH count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> TO | THROUGH
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 2789
        error_string = "TO | THROUGH count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> FROM
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 895
        error_string = "FROM count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> TO
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 46
        error_string = "TO count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> THROUGH
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )

        # call method build_filter_spec_entity_id_q
        test_q = test_instance.build_filter_spec_entity_q_target_roles( entity_qs, test_role_list )

        # run query and test count.
        test_qs = relation_qs.filter( test_q )
        test_value = test_qs.count()
        should_be = 2743
        error_string = "THROUGH count = {}, should = {} ( SQL: {} ).".format( test_value, should_be, entity_qs.query )
        self.assertEqual( test_value, should_be, msg = error_string )

    #-- END test method test_build_filter_spec_entity_q_target_roles() --#
    
    
    def test_build_filter_spec_entity_trait_q( self ):

        # declare variables
        me = "test_build_filter_spec_entity_trait_q"
        debug_flag = None
        test_instance = None
        test_value = None
        relation_qs = None
        should_be = None
        error_string = None
        test_filter_spec = None
        test_filter_type = None
        test_role_list = None
        test_qs = None
        test_count = None
        test_value_list = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_instance = TestHelper.load_with_entity_id_filter()
        test_filter_type = NetworkDataRequest.FILTER_TYPE_ENTITY_TRAIT
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "equals"
        #----------------------------------------------------------------------#
        
        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "first_name" )
        test_filter_spec.set_value( "needboxestakeplenty" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # counts for good match.
        match_all = 175
        match_from_to = match_all
        match_from = 68
        match_to = 107
        match_through = 0
        
        # --------> single match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "first_name" )
        test_filter_spec.set_value( "John" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> single match - roles = "ALL".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO", "THROUGH" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM"
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "TO"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "THROUGH"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_through
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "includes"
        #----------------------------------------------------------------------#
        
        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "first_name" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "20202020" )
        test_value_list.append( "20202021" )
        test_value_list.append( "20202022" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # counts for good match.
        match_all = 353
        match_from_to = match_all
        match_from = 139
        match_to = 218
        match_through = 0
        
        # --------> default roles = "ALL".
        test_value_list = []
        test_value_list.append( "John" )
        test_value_list.append( "Michael" )
        test_value_list.append( "Robert" )
        test_value_list.append( "Steve" )
        test_value_list.append( "Larry" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> single match - roles = "ALL".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO", "THROUGH" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM"
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "TO"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "THROUGH"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_through
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "excludes"
        #----------------------------------------------------------------------#
        
        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "first_name" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EXCLUDES )
        test_value_list = []
        test_value_list.append( "20202020" )
        test_value_list.append( "20202021" )
        test_value_list.append( "20202022" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 3162
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # counts for good match.
        match_all = 3094
        match_from_to = match_all
        match_from = 2177
        match_to = 2944
        match_through = 0
        
        # --------> default roles = "ALL".
        test_value_list = []
        test_value_list.append( "John" )
        test_value_list.append( "Michael" )
        test_value_list.append( "Robert" )
        test_value_list.append( "Steve" )
        test_value_list.append( "Larry" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> single match - roles = "ALL".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO", "THROUGH" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM"
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "TO"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "THROUGH"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_through
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "in_range"
        #----------------------------------------------------------------------#
        
        # --------> no match.
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "pub_date" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_IN_RANGE )
        test_filter_spec.set_value_from( "2019-12-01" )
        test_filter_spec.set_value_to( "2019-12-31" )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # counts for good match.
        match_all = 1443
        match_from_to = 188
        match_from = 170
        match_to = 18
        match_through = 1255
        
        # --------> match.
        test_filter_spec.set_value_from( "2010-02-08" )
        test_filter_spec.set_value_to( "2010-02-13" )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> single match - roles = "ALL".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO", "THROUGH" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM"
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "TO"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "THROUGH"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_through
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

    #-- END test method test_build_filter_spec_entity_trait_q() --#


    def test_build_filter_spec_entity_type_slug_q( self ):

        # declare variables
        me = "test_build_filter_spec_entity_type_slug_q"
        debug_flag = None
        test_instance = None
        test_value = None
        relation_qs = None
        should_be = None
        error_string = None
        test_filter_spec = None
        test_filter_type = None
        test_role_list = None
        test_qs = None
        test_count = None
        test_value_list = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_instance = TestHelper.load_with_entity_id_filter()
        test_filter_type = NetworkDataRequest.FILTER_TYPE_ENTITY_TYPE_SLUG
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "equals"
        #----------------------------------------------------------------------#
        
        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_value( "peregrine" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # counts for good match.
        match_all = 3169
        match_from_to = match_all
        match_from = 2320
        match_to = match_all
        match_through = 0
        
        # --------> single match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_value( "person" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> single match - roles = "ALL".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO", "THROUGH" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM"
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "TO"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "THROUGH"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_through
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "includes"
        #----------------------------------------------------------------------#
        
        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "peregrine" )
        test_value_list.append( "chartreuse" )
        test_value_list.append( "bumblebee" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 0
        
        # counts for good match.
        match_all = 3215
        match_from_to = match_all
        match_from = 2746
        match_to = 3215
        match_through = 2743
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> default roles = "ALL".
        test_value_list = []
        test_value_list.append( "person" )
        test_value_list.append( "article" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> single match - roles = "ALL".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO", "THROUGH" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM"
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "TO"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "THROUGH"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_through
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "excludes"
        #----------------------------------------------------------------------#
        
        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EXCLUDES )
        test_value_list = []
        test_value_list.append( "peregrine" )
        test_value_list.append( "chartreuse" )
        test_value_list.append( "bumblebee" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 3215
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # counts for good match.
        match_all = 3215
        match_from_to = match_all
        match_from = 2789
        match_to = 3169
        match_through = 0
        
        # --------> default roles = "ALL".
        test_value_list = []
        test_value_list.append( "article" )
        test_value_list.append( "peregrine" )
        test_value_list.append( "chartreuse" )
        test_value_list.append( "bumblebee" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> single match - roles = "ALL".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO", "THROUGH" (should be same as all).
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_all
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM", "TO".
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "FROM"
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_from
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "TO"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_to
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # --------> single match - roles = "THROUGH"
        test_role_list = []
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = match_through
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
    #-- END test method test_build_filter_spec_entity_type_slug_q() --#


    def test_build_filter_spec_q( self ):

        # declare variables
        me = "test_build_filter_spec_q"
        debug_flag = None
        test_filter_type = None
        test_instance = None
        test_value = None
        relation_qs = None
        should_be = None
        error_string = None
        test_filter_spec = None
        test_filter_type = None
        test_role_list = None
        test_qs = None
        test_count = None
        test_value_list = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_instance = TestHelper.load_with_entity_id_filter()
        
        #----------------------------------------------------------------------#
        # ! ----> entity ID
        #----------------------------------------------------------------------#
        
        test_filter_type = NetworkDataRequest.FILTER_TYPE_ENTITY_ID
        
        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "person_sourcenet_id" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "20202020" )
        test_value_list.append( "20202021" )
        test_value_list.append( "20202022" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> "ALL".
        test_value_list = []
        test_value_list.append( "46" )
        test_value_list.append( "163" )
        test_value_list.append( "161" )
        test_value_list.append( "164" )
        test_value_list.append( "30" )
        test_value_list.append( "175" )
        test_filter_spec.set_value_list( test_value_list )
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = 135
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        #----------------------------------------------------------------------#
        # ! ----> entity trait
        #----------------------------------------------------------------------#
        
        test_filter_type = NetworkDataRequest.FILTER_TYPE_ENTITY_TRAIT
        
        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "first_name" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "20202020" )
        test_value_list.append( "20202021" )
        test_value_list.append( "20202022" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> roles = "FROM", "TO"
        test_value_list = []
        test_value_list.append( "John" )
        test_value_list.append( "Michael" )
        test_value_list.append( "Robert" )
        test_value_list.append( "Steve" )
        test_value_list.append( "Larry" )
        test_filter_spec.set_value_list( test_value_list )
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM )
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO )
        #test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = 353
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        #----------------------------------------------------------------------#
        # ! ----> entity type slug
        #----------------------------------------------------------------------#

        test_filter_type = NetworkDataRequest.FILTER_TYPE_ENTITY_TYPE_SLUG

        # --------> no match - default roles = "ALL".
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "peregrine" )
        test_value_list.append( "chartreuse" )
        test_value_list.append( "bumblebee" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> default roles = "ALL".
        test_value_list = []
        test_value_list.append( "person" )
        test_value_list.append( "article" )
        test_filter_spec.set_value_list( test_value_list )
        test_role_list = []
        test_role_list.append( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL )
        test_filter_spec.set_relation_roles_list( test_role_list )
        should_be = 3215        

        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        #----------------------------------------------------------------------#
        # ! ----> relation trait
        #----------------------------------------------------------------------#
        
        test_filter_type = NetworkDataRequest.FILTER_TYPE_RELATION_TRAIT

        # --------> no match.
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "pub_date" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_IN_RANGE )
        test_filter_spec.set_value_from( "2019-12-01" )
        test_filter_spec.set_value_to( "2019-12-31" )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> match.
        test_filter_spec.set_value_from( "2010-02-08" )
        test_filter_spec.set_value_to( "2010-02-13" )
        should_be = 1443
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        #----------------------------------------------------------------------#
        # ! ----> relation type slug
        #----------------------------------------------------------------------#
        
        test_filter_type = NetworkDataRequest.FILTER_TYPE_RELATION_TYPE_SLUG

        # --------> no match.
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EXCLUDES )
        test_value_list = []
        test_value_list.append( "peregrine" )
        test_value_list.append( "chartreuse" )
        test_value_list.append( "bumblebee" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 3215
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> match.
        test_value_list = []
        test_value_list.append( "quoted" )
        test_value_list.append( "mentioned" )
        test_value_list.append( "shared_byline" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 2778
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        #----------------------------------------------------------------------#
        # ! ----> AND
        #----------------------------------------------------------------------#
        
        # create test_filter_spec
        test_filter_spec = self.create_2_level_aggregate( test_instance )

        # test
        should_be = 112
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        #----------------------------------------------------------------------#
        # ! ----> OR
        #----------------------------------------------------------------------#
        
        # create simple aggregate
        test_filter_spec = self.create_simple_1_level_aggregate( comparison_type_IN = FilterSpec.PROP_VALUE_COMPARISON_TYPE_OR,
                                                                 test_instance_IN = test_instance )
        # test
        should_be = 3169
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

    #-- END test method test_build_filter_spec_q() --#


    def test_build_filter_spec_relation_trait_q( self ):

        # declare variables
        me = "test_build_filter_spec_relation_trait_q"
        debug_flag = None
        test_instance = None
        test_value = None
        relation_qs = None
        should_be = None
        error_string = None
        test_filter_spec = None
        test_filter_type = None
        test_role_list = None
        test_qs = None
        test_count = None
        test_value_list = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_instance = TestHelper.load_with_entity_id_filter()
        test_filter_type = NetworkDataRequest.FILTER_TYPE_RELATION_TRAIT
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "equals"
        #----------------------------------------------------------------------#
        
        # --------> no match.
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "pub_date" )
        test_filter_spec.set_value( "2019-12-13" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> match.
        test_filter_spec.set_value( "2009-12-07" )
        should_be = 167
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "includes"
        #----------------------------------------------------------------------#
        
        # --------> no match.
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "pub_date" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "20202020" )
        test_value_list.append( "20202021" )
        test_value_list.append( "20202022" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> match.
        test_value_list = []
        test_value_list.append( "2009-12-07" )
        test_value_list.append( "2010-02-13" )
        test_value_list.append( "2010-02-08" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 793
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "excludes"
        #----------------------------------------------------------------------#
        
        # --------> no match.
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "pub_date" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EXCLUDES )
        test_value_list = []
        test_value_list.append( "20202020" )
        test_value_list.append( "20202021" )
        test_value_list.append( "20202022" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 3211
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> match.
        test_value_list = []
        test_value_list.append( "2009-12-07" )
        test_value_list.append( "2010-02-13" )
        test_value_list.append( "2010-02-08" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 2418
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        #----------------------------------------------------------------------#
        # ! ----> comparison type "in_range"
        #----------------------------------------------------------------------#
        
        # --------> no match.
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "pub_date" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_IN_RANGE )
        test_filter_spec.set_value_from( "2019-12-01" )
        test_filter_spec.set_value_to( "2019-12-31" )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> match.
        test_filter_spec.set_value_from( "2010-02-08" )
        test_filter_spec.set_value_to( "2010-02-13" )
        should_be = 1443
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

    #-- END test method test_build_filter_spec_relation_trait_q() --#


    def test_build_filter_spec_relation_type_slug_q( self ):

        # declare variables
        me = "test_build_filter_spec_relation_type_slug_q"
        debug_flag = None
        test_instance = None
        test_value = None
        relation_qs = None
        should_be = None
        error_string = None
        test_filter_spec = None
        test_filter_type = None
        test_role_list = None
        test_qs = None
        test_count = None
        test_value_list = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init
        test_instance = TestHelper.load_with_entity_id_filter()
        test_filter_type = NetworkDataRequest.FILTER_TYPE_RELATION_TYPE_SLUG
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "equals"
        #----------------------------------------------------------------------#
        
        # --------> no match.
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_value( "peregrine" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> match.
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_value( "quoted" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS )
        should_be = 155
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        #----------------------------------------------------------------------#
        # ! ----> comparison type "includes"
        #----------------------------------------------------------------------#
        
        # --------> no match.
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "peregrine" )
        test_value_list.append( "chartreuse" )
        test_value_list.append( "bumblebee" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 0
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> match.
        test_value_list = []
        test_value_list.append( "quoted" )
        test_value_list.append( "mentioned" )
        test_value_list.append( "shared_byline" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 437
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        #----------------------------------------------------------------------#
        # ! ----> comparison type "excludes"
        #----------------------------------------------------------------------#
        
        # --------> no match.
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_EXCLUDES )
        test_value_list = []
        test_value_list.append( "peregrine" )
        test_value_list.append( "chartreuse" )
        test_value_list.append( "bumblebee" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 3215
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

        # --------> match.
        test_value_list = []
        test_value_list.append( "quoted" )
        test_value_list.append( "mentioned" )
        test_value_list.append( "shared_byline" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 2778
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )

    #-- END test method test_build_filter_spec_relation_type_slug_q() --#


    def test_create_entity_id_header_label( self ):

        # declare variables
        me = "test_create_entity_id_header_label"
        debug_flag = None
        test_instance = None
        id_dict = None
        test_value = None
        should_be = None
        error_string = None
        original_ids_list = None

        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        #----------------------------------------------------------------------#
        # ! ----> test basic instance.
        test_instance = TestHelper.load_basic()
        
        # get identifier list
        original_ids_list = test_instance.get_output_entity_identifiers_list()
                
        # ! --------> #1 original_ids_list[ 0 ]
        id_dict = original_ids_list[ 0 ]
        
        # call the method
        test_value = NetworkDataRequest.create_entity_id_header_label( id_dict )
        
        # should be "id_person_sourcenet_id"
        should_be = "id_person_sourcenet_id"
        error_string = "BASIC - got {} as label for id 1 ( original_ids_list[ 0 ] ), should = {}.  Dict: {}".format( test_value, should_be, id_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> #2 original_ids_list[ 1 ]
        id_dict = original_ids_list[ 1 ]
        
        # call the method
        test_value = NetworkDataRequest.create_entity_id_header_label( id_dict )
        
        # should be "id_person_open_calais_uuid"
        should_be = "id_person_open_calais_uuid"
        error_string = "BASIC - got {} as label for id 2 ( original_ids_list[ 1 ] ), should = {}.  Dict: {}".format( test_value, should_be, id_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> more tests

        # ! --------> no name, no type, no source
        id_dict = {}
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_NAME ] = None  # self.TEST_ID_NAME
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_ID_TYPE ] = None  # self.TEST_ID_ID_TYPE
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_SOURCE ] = None  # self.TEST_ID_SOURCE
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_IDENTIFIER_TYPE_ID ] = self.TEST_ID_IDENTIFIER_TYPE_ID
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_OUTPUT_HEADER ] = None  # self.TEST_ID_HEADER

        # call the method
        test_value = NetworkDataRequest.create_entity_id_header_label( id_dict )
        
        # should be None - name is required.
        should_be = None
        error_string = "BASIC - got {} as label, should = {}.  Dict: {}".format( test_value, should_be, id_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> name, no type, no source
        id_dict = {}
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_NAME ] = self.TEST_ID_NAME
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_ID_TYPE ] = None  # self.TEST_ID_ID_TYPE
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_SOURCE ] = None  # self.TEST_ID_SOURCE
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_IDENTIFIER_TYPE_ID ] = self.TEST_ID_IDENTIFIER_TYPE_ID
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_OUTPUT_HEADER ] = None  # self.TEST_ID_HEADER

        # call the method
        test_value = NetworkDataRequest.create_entity_id_header_label( id_dict )
        
        # should be "id_person_open_calais_uuid"
        should_be = "{}{}".format( NetworkDataRequest.OUTPUT_ENTITY_IDENTIFIERS_LABEL_PREFIX, self.TEST_ID_NAME )
        error_string = "BASIC - got {} as label, should = {}.  Dict: {}".format( test_value, should_be, id_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> name, type, no source
        id_dict = {}
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_NAME ] = self.TEST_ID_NAME
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_ID_TYPE ] = self.TEST_ID_ID_TYPE
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_SOURCE ] = None  # self.TEST_ID_SOURCE
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_IDENTIFIER_TYPE_ID ] = self.TEST_ID_IDENTIFIER_TYPE_ID
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_OUTPUT_HEADER ] = None  # self.TEST_ID_HEADER

        # call the method
        test_value = NetworkDataRequest.create_entity_id_header_label( id_dict )
        
        # should be "id_person_open_calais_uuid"
        should_be = "{}{}{}{}".format( NetworkDataRequest.OUTPUT_ENTITY_IDENTIFIERS_LABEL_PREFIX,
                                       self.TEST_ID_NAME,
                                       NetworkDataRequest.OUTPUT_ENTITY_LABEL_SEPARATOR,
                                       self.TEST_ID_ID_TYPE )
        error_string = "BASIC - got {} as label, should = {}.  Dict: {}".format( test_value, should_be, id_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> name, no type, source
        id_dict = {}
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_NAME ] = self.TEST_ID_NAME
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_ID_TYPE ] = None  # self.TEST_ID_ID_TYPE
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_SOURCE ] = self.TEST_ID_SOURCE
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_IDENTIFIER_TYPE_ID ] = self.TEST_ID_IDENTIFIER_TYPE_ID
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_OUTPUT_HEADER ] = None  # self.TEST_ID_HEADER

        # call the method
        test_value = NetworkDataRequest.create_entity_id_header_label( id_dict )
        
        # should be "id_person_open_calais_uuid"
        should_be = "{}{}{}{}".format( NetworkDataRequest.OUTPUT_ENTITY_IDENTIFIERS_LABEL_PREFIX,
                                       self.TEST_ID_NAME,
                                       NetworkDataRequest.OUTPUT_ENTITY_LABEL_SEPARATOR,
                                       self.TEST_ID_SOURCE )
        error_string = "BASIC - got {} as label, should = {}.  Dict: {}".format( test_value, should_be, id_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> name, type, source
        id_dict = {}
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_NAME ] = self.TEST_ID_NAME
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_ID_TYPE ] = self.TEST_ID_ID_TYPE
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_SOURCE ] = self.TEST_ID_SOURCE
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_IDENTIFIER_TYPE_ID ] = self.TEST_ID_IDENTIFIER_TYPE_ID
        id_dict[ NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_OUTPUT_HEADER ] = None  # self.TEST_ID_HEADER

        # call the method
        test_value = NetworkDataRequest.create_entity_id_header_label( id_dict )
        
        # should be "id_person_open_calais_uuid"
        should_be = "{}{}{}{}{}{}".format( NetworkDataRequest.OUTPUT_ENTITY_IDENTIFIERS_LABEL_PREFIX,
                                           self.TEST_ID_NAME,
                                           NetworkDataRequest.OUTPUT_ENTITY_LABEL_SEPARATOR,
                                           self.TEST_ID_ID_TYPE,
                                           NetworkDataRequest.OUTPUT_ENTITY_LABEL_SEPARATOR,
                                           self.TEST_ID_SOURCE )
        error_string = "BASIC - got {} as label, should = {}.  Dict: {}".format( test_value, should_be, id_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

    #-- END test method test_create_entity_id_header_label --#


    def test_create_entity_ids_and_traits_header_list( self ):
        
        # declare variables
        me = "test_create_entity_ids_and_traits_header_list"
        debug_flag = None
        test_instance = None
        header_list = None
        header_list_count = None
        goal_header_list = None
        goal_header_list_count = None
        goal_value = None
        test_index = None
        test_value = None
        should_be = None
        error_string = None
        original_header_list = None
        original_header_list_count = None
        test_list = None
        test_list_count = None
        should_not_be = None

        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        #----------------------------------------------------------------------#
        # ! ----> test basic instance.
        test_instance = TestHelper.load_basic()
        
        # call the method
        header_list = test_instance.create_entity_ids_and_traits_header_list()
        header_list_count = len( header_list )
        
        # initialize verification
        goal_header_list = self.GOAL_ENTITY_IDS_AND_TRAITS_HEADER_LIST
        goal_header_list_count = len( goal_header_list )
        test_index = -1
        
        # should be same length
        test_value = header_list_count
        should_be = goal_header_list_count
        error_string = "BASIC - header list count: {} - should be {} ( header_list = {}; goal_header_list: {} )".format( test_value, should_be, header_list, goal_header_list )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # loop - validate same values and position
        for goal_value in goal_header_list:
        
            # increment index
            test_index += 1
            
            # goal value should be in the list
            test_value = goal_value in header_list
            should_be = True
            error_string = "BASIC - header \"{}\" in header_list? {} - should be {} ( header_list = {}; goal_header_list: {} )".format( goal_value, test_value, should_be, header_list, goal_header_list )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # item at index should be goal value
            test_value = header_list[ test_index ]
            should_be = goal_value
            error_string = "BASIC - item at index {} = {}, should be {} ( header_list = {}; goal_header_list: {} )".format( test_index, test_value, should_be, header_list, goal_header_list )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        #-- END loop over goal list --#
        
        # ! ----> save original, swap in a different list, then make sure the new list is returned.
        original_header_list = test_instance.get_entity_ids_and_traits_header_list()
        original_header_list_count = len( original_header_list )
        test_list = self.TEST_SET_ENTITY_IDS_AND_TRAITS_HEADER_LIST
        test_list_count = len( test_list )
        test_instance.set_entity_ids_and_traits_header_list( test_list )
        
        # call the method
        header_list = test_instance.create_entity_ids_and_traits_header_list()
        header_list_count = len( header_list )
        
        # count should = test.
        test_value = header_list_count
        should_be = test_list_count
        error_string = "BASIC - header list count: {} - should be {} ( header_list = {}; test_list: {} )".format( test_value, should_be, header_list, test_list )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # count should not = original.
        test_value = header_list_count
        should_not_be = original_header_list_count
        error_string = "BASIC - header list count: {} - should not be {} ( header_list = {}; original_header_list: {} )".format( test_value, should_not_be, header_list, original_header_list )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )
        
        # retrieved list should equal test list.
        test_value = header_list
        should_be = test_list
        error_string = "BASIC - header list: {} - should = {}".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # retrieved list should not equal original list.
        test_value = header_list
        should_not_be = original_header_list
        error_string = "BASIC - header list: {} - should not = {}".format( test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

    #-- END test method test_create_entity_ids_and_traits_header_list --#    


    def test_create_entity_trait_header_label( self ):

        # declare variables
        me = "test_create_entity_trait_header_label"
        debug_flag = None
        test_instance = None
        trait_dict = None
        test_value = None
        should_be = None
        error_string = None
        original_traits_list = None

        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        #----------------------------------------------------------------------#
        # ! ----> test basic instance.
        test_instance = TestHelper.load_basic()
        
        # get traits list
        original_traits_list = test_instance.get_output_entity_traits_list()
                
        # ! --------> #1 original_traits_list[ 0 ]
        trait_dict = original_traits_list[ 0 ]
        
        # call the method
        test_value = NetworkDataRequest.create_entity_trait_header_label( trait_dict )
        
        # should be "trait_first_name"
        should_be = "trait_first_name"
        error_string = "BASIC - got {} as label for trait 1 ( original_traits_list[ 0 ] ), should = {}.  Dict: {}".format( test_value, should_be, trait_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> #2 original_traits_list[ 1 ]
        trait_dict = original_traits_list[ 1 ]
        
        # call the method
        test_value = NetworkDataRequest.create_entity_trait_header_label( trait_dict )
        
        # should be "trait_middle_name"
        should_be = "trait_middle_name"
        error_string = "BASIC - got {} as label for trait 2 ( original_traits_list[ 1 ] ), should = {}.  Dict: {}".format( test_value, should_be, trait_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> #3 original_traits_list[ 2 ]
        trait_dict = original_traits_list[ 2 ]
        
        # call the method
        test_value = NetworkDataRequest.create_entity_trait_header_label( trait_dict )
        
        # should be "trait_last_name"
        should_be = "trait_last_name"
        error_string = "BASIC - got {} as label for trait 1 ( original_traits_list[ 0 ] ), should = {}.  Dict: {}".format( test_value, should_be, trait_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> more tests

        # ! --------> no name, no slug
        trait_dict = {}
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_NAME ] = None  # self.TEST_TRAIT_NAME
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_SLUG ] = None  # self.TEST_TRAIT_SLUG
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_ENTITY_TYPE_TRAIT_ID ] = self.TEST_TRAIT_ENTITY_TYPE_TRAIT_ID
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_OUTPUT_HEADER ] = None  # self.TEST_TRAIT_HEADER

        # call the method
        test_value = NetworkDataRequest.create_entity_trait_header_label( trait_dict )
        
        # should be None - name is required.
        should_be = None
        error_string = "BASIC - got {} as label, should = {}.  Dict: {}".format( test_value, should_be, trait_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> name, no slug
        trait_dict = {}
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_NAME ] = self.TEST_TRAIT_NAME
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_SLUG ] = None  # self.TEST_TRAIT_SLUG
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_ENTITY_TYPE_TRAIT_ID ] = self.TEST_TRAIT_ENTITY_TYPE_TRAIT_ID
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_OUTPUT_HEADER ] = None  # self.TEST_TRAIT_HEADER

        # call the method
        test_value = NetworkDataRequest.create_entity_trait_header_label( trait_dict )
        
        # should be "id_person_open_calais_uuid"
        should_be = "{}{}".format( NetworkDataRequest.OUTPUT_ENTITY_TRAITS_LABEL_PREFIX,
                                   self.TEST_TRAIT_NAME )
        error_string = "BASIC - got {} as label, should = {}.  Dict: {}".format( test_value, should_be, trait_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> name, slug
        trait_dict = {}
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_NAME ] = self.TEST_TRAIT_NAME
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_SLUG ] = self.TEST_TRAIT_SLUG
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_ENTITY_TYPE_TRAIT_ID ] = self.TEST_TRAIT_ENTITY_TYPE_TRAIT_ID
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_OUTPUT_HEADER ] = None  # self.TEST_TRAIT_HEADER

        # call the method
        test_value = NetworkDataRequest.create_entity_trait_header_label( trait_dict )
        
        # should be prefix, then name, then slug
        should_be = "{}{}{}{}".format( NetworkDataRequest.OUTPUT_ENTITY_TRAITS_LABEL_PREFIX,
                                       self.TEST_TRAIT_NAME,
                                       NetworkDataRequest.OUTPUT_ENTITY_LABEL_SEPARATOR,
                                       self.TEST_TRAIT_SLUG )
        error_string = "BASIC - got {} as label, should = {}.  Dict: {}".format( test_value, should_be, trait_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> name, slug, header
        trait_dict = {}
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_NAME ] = self.TEST_TRAIT_NAME
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_SLUG ] = self.TEST_TRAIT_SLUG
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_ENTITY_TYPE_TRAIT_ID ] = self.TEST_TRAIT_ENTITY_TYPE_TRAIT_ID
        trait_dict[ NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_OUTPUT_HEADER ] = self.TEST_TRAIT_HEADER

        # call the method
        test_value = NetworkDataRequest.create_entity_trait_header_label( trait_dict )
        
        # should be just header
        should_be = "{}{}".format( NetworkDataRequest.OUTPUT_ENTITY_TRAITS_LABEL_PREFIX,
                                   self.TEST_TRAIT_HEADER )
        error_string = "BASIC - got {} as label, should = {}.  Dict: {}".format( test_value, should_be, trait_dict )
        self.assertEqual( test_value, should_be, msg = error_string )

    #-- END test method test_create_entity_trait_header_label --#


    def test_do_output_entity_traits_or_ids( self ):

        # declare variables
        me = "test_do_output_entity_traits_or_ids"
        debug_flag = None
        test_instance = None
        test_value = None
        should_be = None
        error_string = None
        original_ids_list = None
        original_traits_list = None

        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        #----------------------------------------------------------------------#
        # ! ----> test basic instance.
        test_instance = TestHelper.load_basic()
        
        # store off the original lists.
        original_ids_list = test_instance.get_output_entity_identifiers_list()
        original_traits_list = test_instance.get_output_entity_traits_list()
                
        # call the method
        test_value = test_instance.do_output_entity_ids_or_traits()
        
        # should be True...
        should_be = True
        error_string = "BASIC - output ids and traits?  got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> set both to None.
        test_instance.set_output_entity_identifiers_list( None )
        test_instance.set_output_entity_traits_list( None )
                
        # call the method
        test_value = test_instance.do_output_entity_ids_or_traits()
        
        # should be False...
        should_be = False
        error_string = "BASIC - output ids and traits?  got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> set both to empty lists.
        test_instance.set_output_entity_identifiers_list( [] )
        test_instance.set_output_entity_traits_list( [] )
                
        # call the method
        test_value = test_instance.do_output_entity_ids_or_traits()
        
        # should be False...
        should_be = False
        error_string = "BASIC - output ids and traits?  got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> just identifiers.
        test_instance.set_output_entity_identifiers_list( original_ids_list )
        test_instance.set_output_entity_traits_list( [] )
                
        # call the method
        test_value = test_instance.do_output_entity_ids_or_traits()
        
        # should be True...
        should_be = True
        error_string = "BASIC - output ids and traits?  got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> just traits.
        test_instance.set_output_entity_identifiers_list( [] )
        test_instance.set_output_entity_traits_list( original_traits_list )
                
        # call the method
        test_value = test_instance.do_output_entity_ids_or_traits()
        
        # should be True...
        should_be = True
        error_string = "BASIC - output ids and traits?  got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

    #-- END test method test_do_output_entity_traits_or_ids --#


    def test_filter_relation_query_set( self ):

        # declare variables
        me = "test_filter_relation_query_set"
        debug_flag = None
        test_instance = None
        test_qs = None
        test_value = None
        should_be = None
        error_string = None

        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        #----------------------------------------------------------------------#
        # ! ----> test basic instance.
        test_instance = TestHelper.load_basic()
                
        # call the method - no QS passed in, so makes its own, and doesn't use
        #     entity_selection.
        test_qs = test_instance.filter_relation_query_set()
        
        # QuerySet should not be None
        test_value = test_qs
        error_string = "Retrieving QuerySet filtered based on nested basic spec, returned None"
        self.assertIsNotNone( test_value, msg = error_string )
        
        # and should match count...
        test_value = test_qs.count()
        should_be = 112
        error_string = "BASIC - got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> test basic 2 instance.
        test_instance = TestHelper.load_basic_2()
                
        # call the method - no QS passed in, so makes its own, and doesn't use
        #     entity_selection.
        test_qs = test_instance.filter_relation_query_set()
        
        # QuerySet should not be None
        test_value = test_qs
        error_string = "Retrieving QuerySet filtered based on nested basic 2 spec, returned None"
        self.assertIsNotNone( test_value, msg = error_string )
        
        # and should match count...
        test_value = test_qs.count()
        should_be = 112
        error_string = "BASIC 2 - got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> test entity select instance - use_entity_selection_IN = default (False)
        test_instance = TestHelper.load_with_entity_selection()
                
        # call the method - no QS passed in, so makes its own, and doesn't use
        #     entity_selection.
        test_qs = test_instance.filter_relation_query_set()
        
        # QuerySet should not be None
        test_value = test_qs
        error_string = "Retrieving QuerySet filtered based on nested with entity selection spec, returned None"
        self.assertIsNotNone( test_value, msg = error_string )
        
        # and should match count...
        test_value = test_qs.count()
        should_be = 112
        error_string = "with_entity_selection - default - got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> test entity select instance - use_entity_selection_IN = False
        test_instance = TestHelper.load_with_entity_selection()
                
        # call the method - no QS passed in, so makes its own, and doesn't use
        #     entity_selection.
        test_qs = test_instance.filter_relation_query_set( use_entity_selection_IN = False )
        
        # QuerySet should not be None
        test_value = test_qs
        error_string = "Retrieving QuerySet filtered based on nested with entity selection spec, returned None"
        self.assertIsNotNone( test_value, msg = error_string )
        
        # and should match count...
        test_value = test_qs.count()
        should_be = 112
        error_string = "with_entity_selection - False - got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> test entity select instance - use_entity_selection_IN = True
        test_instance = TestHelper.load_with_entity_selection()
                
        # call the method - no QS passed in, so makes its own, and doesn't use
        #     entity_selection.
        test_qs = test_instance.filter_relation_query_set( use_entity_selection_IN = True )
        
        # QuerySet should not be None
        test_value = test_qs
        error_string = "Retrieving QuerySet filtered based on nested with entity selection spec, returned None"
        self.assertIsNotNone( test_value, msg = error_string )
        
        # and should match count...
        test_value = test_qs.count()
        should_be = 248
        error_string = "with_entity_selection - True - got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # ! TODO - test with a QuerySet passed in.
        
    #-- END test method test_filter_relation_query_set()


    def test_filter_relations( self ):

        # declare variables
        me = "test_filter_relations"
        debug_flag = None
        test_instance = None
        test_filters = None
        test_qs = None
        test_value = None
        should_be = None
        error_string = None

        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )

        # load basic for first few tests.
        test_instance = TestHelper.load_basic()

        #----------------------------------------------------------------------#
        # ! ----> no filter spec.
        test_filters = None
        test_qs = test_instance.filter_relations( selection_filters_IN = test_filters )

        # QuerySet should be None
        test_value = test_qs
        error_string = "Retrieving QuerySet filtered based on no filter spec, should be None, instead got: {}".format( test_qs )
        self.assertIsNone( test_value, msg = error_string )
                
        #----------------------------------------------------------------------#
        # ! ----> test basic relation filters.
                
        # call the method - no QS passed in, so makes its own, and doesn't use
        #     entity_selection.
        test_filters = test_instance.get_selection_filters( use_entity_selection_IN = True )
        test_qs = test_instance.filter_relations( selection_filters_IN = test_filters )
        
        # QuerySet should not be None
        test_value = test_qs
        error_string = "Retrieving QuerySet filtered based on nested basic relation spec, returned None"
        self.assertIsNotNone( test_value, msg = error_string )
        
        # and should match count...
        test_value = test_qs.count()
        should_be = 112
        error_string = "BASIC - got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> test basic 2 instance.
        test_instance = TestHelper.load_basic_2()
                
        # call the method - no QS passed in, so makes its own, and doesn't use
        #     entity_selection.
        test_filters = test_instance.get_selection_filters( use_entity_selection_IN = True )
        test_qs = test_instance.filter_relations( selection_filters_IN = test_filters )
        
        # QuerySet should not be None
        test_value = test_qs
        error_string = "Retrieving QuerySet filtered based on nested basic 2 spec, returned None"
        self.assertIsNotNone( test_value, msg = error_string )
        
        # and should match count...
        test_value = test_qs.count()
        should_be = 112
        error_string = "BASIC 2 - got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> test entity select instance - use_entity_selection_IN = default (False)
        test_instance = TestHelper.load_with_entity_selection()
                
        # call the method - no QS passed in, so makes its own, and doesn't use
        #     entity_selection.
        test_filters = test_instance.get_selection_filters()
        test_qs = test_instance.filter_relations( selection_filters_IN = test_filters )
        
        # QuerySet should not be None
        test_value = test_qs
        error_string = "Retrieving QuerySet filtered based on nested with entity selection spec, returned None"
        self.assertIsNotNone( test_value, msg = error_string )
        
        # and should match count...
        test_value = test_qs.count()
        should_be = 112
        error_string = "with_entity_selection - default - got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> test entity select instance - use_entity_selection_IN = False
        test_instance = TestHelper.load_with_entity_selection()
                
        # call the method - no QS passed in, so makes its own, and doesn't use
        #     entity_selection.
        test_filters = test_instance.get_selection_filters( use_entity_selection_IN = False )
        test_qs = test_instance.filter_relations( selection_filters_IN = test_filters )
        
        # QuerySet should not be None
        test_value = test_qs
        error_string = "Retrieving QuerySet filtered based on nested with entity selection spec, returned None"
        self.assertIsNotNone( test_value, msg = error_string )
        
        # and should match count...
        test_value = test_qs.count()
        should_be = 112
        error_string = "with_entity_selection - False - got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> test entity select instance - use_entity_selection_IN = True
        test_instance = TestHelper.load_with_entity_selection()
                
        # call the method - no QS passed in, so makes its own, and doesn't use
        #     entity_selection.
        test_filters = test_instance.get_selection_filters( use_entity_selection_IN = True )
        test_qs = test_instance.filter_relations( selection_filters_IN = test_filters )
        
        # QuerySet should not be None
        test_value = test_qs
        error_string = "Retrieving QuerySet filtered based on nested with entity selection spec, returned None"
        self.assertIsNotNone( test_value, msg = error_string )
        
        # and should match count...
        test_value = test_qs.count()
        should_be = 248
        error_string = "with_entity_selection - True - got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # ! TODO - test with a QuerySet passed in.
        
    #-- END test method test_filter_relations()


    def test_get_selection_filters( self ):

        # declare variables
        me = "test_get_selection_filters"
        debug_flag = None
        test_instance = None
        relation_selection = None
        entity_selection = None
        test_value = None
        should_be = None
        should_not_be = None
        error_string = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        #----------------------------------------------------------------------#
        # ! ----> test one without entity selection
        
        # load "with_entity_selection" to use as test instance.
        test_instance = TestHelper.load_basic()
        
        # retrieve the relation_selection directly.
        relation_selection = test_instance.get_relation_selection()
        entity_selection = test_instance.get_entity_selection()
        
        # relation should not be empty
        test_value = relation_selection
        should_not_be = 0
        error_string = "BASIC - relation_selection count = {}, should not be {}.".format( test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )
                
        # entity should be empty dict
        test_value = len( entity_selection )
        should_be = 0
        error_string = "BASIC - entity_selection count = {}, should be {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # ! --------> load, passing no argument (entity_relation = False)
        test_value = test_instance.get_selection_filters()

        # relation_selection should equal test
        should_be = relation_selection
        error_string = "BASIC - get_selection_filters(): got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # ! --------> load, use_entity_selection_IN = False
        test_value = test_instance.get_selection_filters( use_entity_selection_IN = False )

        # relation_selection should equal test
        should_be = relation_selection
        error_string = "BASIC - get_selection_filters(): got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> load, use_entity_selection_IN = True
        test_value = test_instance.get_selection_filters( use_entity_selection_IN = True )

        # relation_selection should equal test
        should_be = relation_selection
        error_string = "BASIC - get_selection_filters(): got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> test one with entity selection
        
        # load "with_entity_selection" to use as test instance.
        test_instance = TestHelper.load_with_entity_selection()
        
        # retrieve the relation_selection directly.
        relation_selection = test_instance.get_relation_selection()
        entity_selection = test_instance.get_entity_selection()
        
        # relation should not be empty
        test_value = relation_selection
        should_not_be = 0
        error_string = "W/ENTITY - relation_selection count = {}, should not be {}.".format( test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )
                
        # entity should not be empty
        test_value = len( entity_selection )
        should_not_be = 0
        error_string = "W/ENTITY - entity_selection, count = {}, should not be {}.".format( test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )
                
        # ! --------> load, passing no argument (entity_relation = False)
        test_value = test_instance.get_selection_filters()

        # relation_selection should equal test
        should_be = relation_selection
        error_string = "W/ENTITY - get_selection_filters(): got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # ! --------> load, use_entity_selection_IN = False
        test_value = test_instance.get_selection_filters( use_entity_selection_IN = False )

        # relation_selection should equal test
        should_be = relation_selection
        error_string = "W/ENTITY - get_selection_filters(): got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # ! --------> load, use_entity_selection_IN = True
        test_value = test_instance.get_selection_filters( use_entity_selection_IN = True )

        # entity_selection should equal test
        should_be = entity_selection
        error_string = "W/ENTITY - get_selection_filters(): got {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

    #-- END test method test_get_selection_filters() --#


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
        
        # ! ----> test get()-ers
        
        # load "with_entity_id_filter" to use as test instance.
        test_instance = TestHelper.load_with_entity_id_filter()
        
        # first, test getters by calling the validate method
        self.validate_instance_id_filter( test_instance )
        
        # load "with_entity_selection" to use as test instance.
        test_instance = TestHelper.load_with_entity_selection()
        
        # first, test getters by calling the validate method
        self.validate_instance_entity_selection( test_instance )

        # ! ----> test get/set()-ers
        
        # for each (using last loaded test instance):
        # - get original value and store
        # - set new value
        # - get value.
        # - assertEquals( get value, new value )
        # - assertNotEqual( get value, original value )

        # ! --------> get/set_entity_ids_and_traits_header_list()
        test_method = "set_entity_ids_and_traits_header_list"
        original_value = test_instance.get_entity_ids_and_traits_header_list()
        new_value = self.TEST_SET_ENTITY_IDS_AND_TRAITS_HEADER_LIST
        test_instance.set_entity_ids_and_traits_header_list( new_value )
        test_value = test_instance.get_entity_ids_and_traits_header_list()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )
        
        # ! --------> get/set_entity_id_to_instance_map()
        test_method = "set_entity_id_to_instance_map"
        original_value = test_instance.get_entity_id_to_instance_map()
        new_value = self.TEST_SET_ENTITY_ID_TO_INSTANCE_MAP
        test_instance.set_entity_id_to_instance_map( new_value )
        test_value = test_instance.get_entity_id_to_instance_map()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_entity_id_to_traits_map()
        test_method = "set_entity_id_to_traits_map"
        original_value = test_instance.get_entity_id_to_traits_map()
        new_value = self.TEST_SET_ENTITY_ID_TO_TRAITS_MAP
        test_instance.set_entity_id_to_traits_map( new_value )
        test_value = test_instance.get_entity_id_to_traits_map()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> set_entity_selection()
        test_method = "set_entity_selection"
        original_value = test_instance.get_entity_selection()
        new_value = self.TEST_SET_ENTITY_SELECTION
        test_instance.set_entity_selection( new_value )
        test_value = test_instance.get_entity_selection()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> set_is_request_ok()
        test_method = "set_is_request_ok"
        original_value = test_instance.is_request_ok()
        new_value = self.TEST_SET_IS_REQUEST_OK
        test_instance.set_is_request_ok( new_value )
        test_value = test_instance.is_request_ok()

        # setter converts strings to boolean values, so convert this value to
        #     boolean.
        new_value = BooleanHelper.convert_value_to_boolean( new_value )

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_output_entity_identifiers_list()
        test_method = "set_output_entity_identifiers_list"
        original_value = test_instance.get_output_entity_identifiers_list()
        new_value = self.TEST_SET_OUTPUT_ENTITY_IDENTIFIERS_LIST
        test_instance.set_output_entity_identifiers_list( new_value )
        test_value = test_instance.get_output_entity_identifiers_list()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_output_entity_traits_list()
        test_method = "set_output_entity_traits_list"
        original_value = test_instance.get_output_entity_traits_list()
        new_value = self.TEST_SET_OUTPUT_ENTITY_TRAITS_LIST
        test_instance.set_output_entity_traits_list( new_value )
        test_value = test_instance.get_output_entity_traits_list()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> set_output_file_path()
        test_method = "set_output_file_path"
        original_value = test_instance.get_output_file_path()
        new_value = self.TEST_SET_OUTPUT_FILE_PATH
        test_instance.set_output_file_path( new_value )
        test_value = test_instance.get_output_file_path()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> set_output_format()
        test_method = "set_output_format"
        original_value = test_instance.get_output_format()
        new_value = self.TEST_SET_OUTPUT_FORMAT
        test_instance.set_output_format( new_value )
        test_value = test_instance.get_output_format()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> set_output_include_column_headers()
        test_method = "set_output_include_column_headers"
        original_value = test_instance.get_output_include_column_headers()
        new_value = self.TEST_SET_OUTPUT_INCLUDE_COLUMN_HEADERS
        test_instance.set_output_include_column_headers( new_value )
        test_value = test_instance.get_output_include_column_headers()

        # setter converts strings to boolean values, so convert this value to
        #     boolean.
        new_value = BooleanHelper.convert_value_to_boolean( new_value )

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> set_output_specification()
        test_method = "set_output_specification"
        original_value = test_instance.get_output_specification()
        new_value = self.TEST_SET_OUTPUT_SPECIFICATION
        test_instance.set_output_specification( new_value )
        test_value = test_instance.get_output_specification()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )
        
        # put back the original so we have a dictionary there.
        test_instance.set_output_specification( original_value )

        # ! --------> set_output_spec_property()
        test_method = "set_output_spec_property"
        test_name = self.TEST_SET_OUTPUT_SPEC_PROPERTY_NAME
        original_value = test_instance.get_output_spec_property( test_name )
        new_value = self.TEST_SET_OUTPUT_SPEC_PROPERTY
        test_instance.set_output_spec_property( test_name, new_value )
        test_value = test_instance.get_output_spec_property( test_name )

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set it again.
        original_value = test_instance.get_output_spec_property( test_name )
        new_value = self.TEST_SET_OUTPUT_SPEC_PROPERTY_AGAIN
        test_instance.set_output_spec_property( test_name, new_value )
        test_value = test_instance.get_output_spec_property( test_name )

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # set to None.
        original_value = test_instance.get_output_spec_property( test_name )
        new_value = None
        test_instance.set_output_spec_property( test_name, new_value )
        test_value = test_instance.get_output_spec_property( test_name )

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> set_output_structure()
        test_method = "set_output_structure"
        original_value = test_instance.get_output_structure()
        new_value = self.TEST_SET_OUTPUT_STRUCTURE
        test_instance.set_output_structure( new_value )
        test_value = test_instance.get_output_structure()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> set_output_type()
        test_method = "set_output_type"
        original_value = test_instance.get_output_type()
        new_value = self.TEST_SET_OUTPUT_TYPE
        test_instance.set_output_type( new_value )
        test_value = test_instance.get_output_type()

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

        # ! --------> set_relation_selection
        test_method = "set_relation_selection"
        original_value = test_instance.get_relation_selection()
        new_value = self.TEST_SET_RELATION_SELECTION
        test_instance.set_relation_selection( new_value )
        test_value = test_instance.get_relation_selection()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

    #-- END test method test_getters_and_setters() --#


    def test_load_network_data_request_json( self ):
        
        # declare variables
        me = "test_load_network_data_request_json"
        debug_flag = None
        test_instance = None
        test_value = None
        should_be = None
        error_string = None
        json_file_path_list = None
        json_file_path = None
        json_file = None
        parsed_json = None
        result_status = None
        result_status_is_error = None
        validate_function = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init instance.
        test_instance = NetworkDataRequest()
        
        # loop over the JSON files.
        json_file_path_list = TestHelper.FILE_PATH_LIST
        for json_file_path in json_file_path_list:
        
            try:
        
                # try to open json file for reading
                with open( json_file_path ) as json_file:  
                
                    # parse the JSON
                    parsed_json = json.load( json_file )
                
                #-- END open of JSON file to read it into memory. --#
                
                # call the load_network_data_request_json() method
                result_status = test_instance.load_network_data_request_json( parsed_json )
                
                # errors?
                result_status_is_error = result_status.is_error()

                # should not be an error
                test_value = result_status_is_error
                should_be = False
                error_string = "Processing JSON {}, got error, status = {}.".format( parsed_json, result_status )
                self.assertEqual( test_value, should_be, msg = error_string )
                
                # get validate function for JSON file path
                validate_function = self.JSON_FILE_TO_VALIDATE_FUNCTION_MAP.get( json_file_path )
                
                # Should be a function, not None.
                test_value = validate_function
                error_string = "Retrieving validate function for JSON file path {} returned None ( map = {} )".format( json_file_path, validate_function )
                self.assertIsNotNone( test_value, msg = error_string )
            
                # call the function.
                getattr( self, validate_function )( test_instance )

            except: # catch *any* exceptions
            
                # get, log, and return exception
                e = sys.exc_info()[0]
                
                # if debug, log the exception details
                if ( debug_flag == True ):

                    # log the exception
                    status_message = "In {}(): ERROR - exception caught while processing JSON file {}, JSON = {}.".format( me, json_file_path, parsed_json )
                    ExceptionHelper.log_exception( e, message_IN = status_message, print_details_IN = debug_flag )
                    
                #-- END DEBUG --#
                
                # throw the exception on
                raise
                
            #-- try...except. --#

        
        #-- END loop over file paths. --#
        
        
    #-- END method test_load_network_data_request_json() --#


    def test_load_network_data_request_json_file( self ):
        
        # declare variables
        me = "test_load_network_data_request_json_file"
        debug_flag = None
        test_instance = None
        test_value = None
        should_be = None
        error_string = None
        json_file_path_list = None
        json_file_path = None
        json_file = None
        result_status = None
        result_status_is_error = None
        validate_function = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init instance.
        test_instance = NetworkDataRequest()
        
        # loop over the JSON files.
        json_file_path_list = TestHelper.FILE_PATH_LIST
        for json_file_path in json_file_path_list:
        
            # call the load_network_data_request_json() method
            result_status = test_instance.load_network_data_request_json_file( json_file_path )
            
            # errors?
            result_status_is_error = result_status.is_error()

            # should not be an error
            test_value = result_status_is_error
            should_be = False
            error_string = "Processing JSON file {}, got error, status = {}.".format( json_file_path, result_status )
            self.assertEqual( test_value, should_be, msg = error_string )
        
            # get validate function for JSON file path
            validate_function = self.JSON_FILE_TO_VALIDATE_FUNCTION_MAP.get( json_file_path )
            
            # Should be a function, not None.
            test_value = validate_function
            error_string = "Retrieving validate function for JSON file path {} returned None ( map = {} )".format( json_file_path, validate_function )
            self.assertIsNotNone( test_value, msg = error_string )
        
            # call the function.
            getattr( self, validate_function )( test_instance )

        #-- END loop over file paths. --#
        
    #-- END method test_load_network_data_request_json_file() --#


    def test_load_network_data_request_json_string( self ):
        
        # declare variables
        me = "test_load_network_data_request_json_string"
        debug_flag = None
        test_instance = None
        test_value = None
        should_be = None
        error_string = None
        json_file_path_list = None
        json_file_path = None
        json_file = None
        json_string = None
        result_status = None
        result_status_is_error = None
        validate_function = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # init instance.
        test_instance = NetworkDataRequest()
        
        # loop over the JSON files.
        json_file_path_list = TestHelper.FILE_PATH_LIST
        for json_file_path in json_file_path_list:
        
            try:
        
                # try to open json file for reading
                with open( json_file_path ) as json_file:  
                
                    # parse the JSON
                    json_string = json_file.read()
                
                #-- END open of JSON file to read it into memory. --#
                
                # call the load_network_data_request_json() method
                result_status = test_instance.load_network_data_request_json_string( json_string )
                
                # errors?
                result_status_is_error = result_status.is_error()

                # should not be an error
                test_value = result_status_is_error
                should_be = False
                error_string = "Processing JSON file {} ( {} ), got error, status = {}.".format( json_file_path, json_string, result_status )
                self.assertEqual( test_value, should_be, msg = error_string )

                # get validate function for JSON file path
                validate_function = self.JSON_FILE_TO_VALIDATE_FUNCTION_MAP.get( json_file_path )
                
                # Should be a function, not None.
                test_value = validate_function
                error_string = "Retrieving validate function for JSON file path {} returned None ( map = {} )".format( json_file_path, validate_function )
                self.assertIsNotNone( test_value, msg = error_string )
            
                # call the function.
                getattr( self, validate_function )( test_instance )
    
            except: # catch *any* exceptions
            
                # get, log, and return exception
                e = sys.exc_info()[0]
                
                # if debug, log the exception details
                if ( debug_flag == True ):

                    status_message = "In {}(): ERROR - exception caught while processing JSON file {}, JSON = {}.".format( me, json_file_path, json_string )
                    ExceptionHelper.log_exception( e, message_IN = status_message, print_details_IN = debug_flag )
                    
                #-- END DEBUG --#

                # throw the exception again.                
                raise
                
            #-- try...except. --#

        
        #-- END loop over file paths. --#
        
        
    #-- END method test_load_network_data_request_json_string() --#


    def test_process_entities( self ):

        # declare variables
        me = "test_process_entities"
        debug_flag = None
        test_instance = None
        entity_dict = None
        entity_dict_count = None
        entity_id = None
        entity_instance = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # initialize request
        test_instance = TestHelper.load_basic()
        
        # remove output type and file path, so no output
        test_instance.set_output_type( None )
        test_instance.set_output_file_path( None )
        #test_instance.set_output_file_path( TestHelper.TEST_BASIC_TSV_OUTPUT )
        
        # call method
        entity_dict = test_instance.process_entities()
        entity_dict_count = len( entity_dict )
        
        # should have 72 things in it.
        test_value = entity_dict_count
        should_be = 72
        error_string = "Entity dictionary length = {}, should = {}, for request: {}.".format( test_value, should_be, test_instance )
        self.assertEqual( test_value, should_be, msg = error_string )

        # make sure all have value of None
        for entity_id, entity_instance in six.iteritems( entity_dict ):
        
            # all should be None.
            test_value = entity_instance
            error_string = "Entity instance should be None, instead is: {}.".format( entity_instance )
            self.assertIsNone( test_value, msg = error_string )
            
        #-- END loop over entity dictionary --#
        
        # call method
        entity_dict = test_instance.process_entities( load_instance_IN = True )
        entity_dict_count = len( entity_dict )
        
        # should have 72 things in it.
        test_value = entity_dict_count
        should_be = 72
        error_string = "Entity dictionary length = {}, should = {}, for request: {}.".format( test_value, should_be, test_instance )
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
        entity_dict = test_instance.process_entities( include_through_IN = True )
        entity_dict_count = len( entity_dict )
        
        # should have 84 things in it.
        test_value = entity_dict_count
        should_be = 84
        error_string = "when including THROUGH, Entity dictionary length = {}, should = {}, for request: {}.".format( test_value, should_be, test_instance )
        self.assertEqual( test_value, should_be, msg = error_string )

    #-- END test method test_process_entities() --#
        
        
#-- END test class NetworkDataRequestTest --#
