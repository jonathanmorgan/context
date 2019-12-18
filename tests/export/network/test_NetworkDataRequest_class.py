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
    TEST_OUTPUT_SPEC_LEN = 5
    TEST_OUTPUT_TYPE = "file"
    TEST_OUTPUT_FILE_PATH = "./NetworkDataRequest_test_output.txt"
    TEST_OUTPUT_FORMAT = "TSV_matrix"
    TEST_OUTPUT_STRUCTURE = "both_trait_columns"
    TEST_OUTPUT_INCLUDE_COLUMN_HEADERS = True
    
    # test - relation_selection (RS)
    TEST_RS_RELATION_SELECTION_ITEM_COUNT = 8
    TEST_RS_RELATION_TYPE_SLUG_FILTER_COMBINE_TYPE = FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_AND
    TEST_RS_RELATION_TYPE_SLUG_FILTERS_COUNT = 1
    TEST_RS_RELATION_TRAIT_FILTER_COMBINE_TYPE = FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_AND
    TEST_RS_RELATION_TRAIT_FILTERS_COUNT = 3
    TEST_RS_ENTITY_TYPE_SLUG_FILTER_COMBINE_TYPE = FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_AND
    TEST_RS_ENTITY_TYPE_SLUG_FILTERS_COUNT = 3
    TEST_RS_ENTITY_TRAIT_FILTER_COMBINE_TYPE = FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_AND
    TEST_RS_ENTITY_TRAIT_FILTERS_COUNT = 1
    TEST_RS_ENTITY_ID_FILTER_COMBINE_TYPE = FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_AND
    TEST_RS_ENTITY_ID_FILTERS_COUNT = 1

    # test - entity_selection (ES)
    TEST_ES_RELATION_SELECTION_ITEM_COUNT = 8
    TEST_ES_RELATION_TYPE_SLUG_FILTER_COMBINE_TYPE = FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_AND
    TEST_ES_RELATION_TYPE_SLUG_FILTERS_COUNT = 1
    TEST_ES_RELATION_TRAIT_FILTER_COMBINE_TYPE = FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_AND
    TEST_ES_RELATION_TRAIT_FILTERS_COUNT = 3
    TEST_ES_ENTITY_TYPE_SLUG_FILTER_COMBINE_TYPE = FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_AND
    TEST_ES_ENTITY_TYPE_SLUG_FILTERS_COUNT = 3
    TEST_ES_ENTITY_TRAIT_FILTER_COMBINE_TYPE = FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_AND
    TEST_ES_ENTITY_TRAIT_FILTERS_COUNT = 1
    TEST_ES_ENTITY_ID_FILTER_COMBINE_TYPE = FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_AND
    TEST_ES_ENTITY_ID_FILTERS_COUNT = 1

    # map of JSON file paths to associated validate functions
    JSON_FILE_TO_VALIDATE_FUNCTION_MAP = {}
    JSON_FILE_TO_VALIDATE_FUNCTION_MAP[ TestHelper.FILE_PATH_NETWORK_DATA_REQUEST_BASIC ] = "validate_instance_basic"
    JSON_FILE_TO_VALIDATE_FUNCTION_MAP[ TestHelper.FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_ID_FILTER ] = "validate_instance_id_filter"
    JSON_FILE_TO_VALIDATE_FUNCTION_MAP[ TestHelper.FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_SELECTION ] = "validate_instance_entity_selection"
    
    # test - get()/set()
    TEST_SET_ENTITY_SELECTION = "test_set_entity_selection"
    TEST_SET_IS_REQUEST_OK = "false"
    TEST_SET_OUTPUT_FILE_PATH = "test_set_output_file_path"
    TEST_SET_OUTPUT_FORMAT = "test_set_output_format"
    TEST_SET_OUTPUT_INCLUDE_COLUMN_HEADERS = "test_set_output_include_column_headers"
    TEST_SET_OUTPUT_SPECIFICATION = "test_set_output_specification"
    TEST_SET_OUTPUT_SPEC_PROPERTY_NAME = "test_set_output_spec_property_name"
    TEST_SET_OUTPUT_SPEC_PROPERTY = "test_set_output_spec_property"
    TEST_SET_OUTPUT_SPEC_PROPERTY_AGAIN = "test_set_output_spec_property_again"
    TEST_SET_OUTPUT_STRUCTURE = "test_set_output_structure"
    TEST_SET_OUTPUT_TYPE = "test_set_output_type"
    TEST_SET_RELATION_SELECTION = "test_set_relation_selection"

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
            self.validate_output_spec( test_instance_IN )
            
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
            self.validate_output_spec( test_instance_IN )

            # ! ----> validate same as basic, plus entity id filter
            self.validate_relation_selection( test_instance_IN )

        else:
        
            # no instance passed in.  Assert Not None here, so we raise Error.
            test_value = test_instance_IN
            error_string = "None passed in, should be a NetworkDataRequest instance."
            self.assertIsNotNone( test_value, msg = error_string )
            
        #-- END check to see if instance passed in. --#
        
    #-- END method validate_instance_id_filter() --#
    

    def validate_output_spec( self, test_instance_IN ):
        
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

        # got test instance?
        if ( test_instance_IN is not None ):
        
            # is there an output_specification?
            output_spec = test_instance_IN.get_output_specification()
            
            # should not be None
            test_value = output_spec
            error_string = "No output_specification found, should be a dictionary instance."
            self.assertIsNotNone( test_value, msg = error_string )
            
            # should be 5 things in the output_specification
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
            output_file_path = test_instance_IN.get_output_file_path()
            test_value = output_file_path
            should_be = self.TEST_OUTPUT_FILE_PATH
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
        
        print( "\n\n------------------------------\nsimple - 1 level - entity type slug\n------------------------------" )
        test_filter_type = NetworkDataRequest.FILTER_TYPE_ENTITY_TYPE_SLUG
        test_filter_list = []
        
        #----------------------------------------------------------------------#
        # --------> filter 1 - FROM entity type slug = "person"
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
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        #----------------------------------------------------------------------#
        # --------> filter 2 - TO entity type slug = "person"
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
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        #----------------------------------------------------------------------#
        # --------> filter 3 - THROUGH entity type slug = "article"
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
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
       
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        # ! --------> AND
        
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND )
        test_filter_spec.set_value_list( test_filter_list )
        should_be = 2320
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # and, store for later.
        simple_1_filter_spec = test_filter_spec
        nested_test_filter_list.append( test_filter_spec )

        # ! --------> OR

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
        
        print( "\n\n------------------------------\nmore complex - 1 level - relation_trait\n------------------------------" )
        test_filter_type = NetworkDataRequest.FILTER_TYPE_RELATION_TRAIT
        test_filter_list = []
        test_q_list = []
        
        #----------------------------------------------------------------------#
        # --------> filter 1 - pub_date in range 2009-12-01 to 2009-12-31
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "pub_date" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_IN_RANGE )
        test_filter_spec.set_value_from( "2009-12-01" )
        test_filter_spec.set_value_to( "2009-12-31" )
        should_be = 1703
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # add to list
        test_q_list.append( test_filter_spec.get_my_q() )
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        #----------------------------------------------------------------------#
        # --------> filter 2 - coder user in "automated"
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "sourcenet-coder-User-username" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "automated" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 2739
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # add to list
        test_q_list.append( test_filter_spec.get_my_q() )
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        #----------------------------------------------------------------------#
        # --------> filter 3 - coder type in "OpenCalais_REST_API_v2"
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_name( "coder_type" )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES )
        test_value_list = []
        test_value_list.append( "OpenCalais_REST_API_v2" )
        test_filter_spec.set_value_list( test_value_list )
        should_be = 2739
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # add to list
        test_q_list.append( test_filter_spec.get_my_q() )
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )
        
        # ! --------> base test
        
        test_qs = Entity_Relation.objects.all()
        for current_q in test_q_list:
        
            test_qs = test_qs.filter( current_q )
            
        #-- END loop over Q instances --#
        test_count = test_qs.count()

        # should be value passed in.
        test_value = test_count
        should_be = 1433
        error_string = "Processing complex single-level filter spec by hand, found {} relations, should_be: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )        

        # ! --------> AND
        
        test_filter_spec = FilterSpec()
        test_filter_spec.set_filter_type( test_filter_type )
        test_filter_spec.set_comparison_type( FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND )
        test_filter_spec.set_value_list( test_filter_list )
        should_be = 1433
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # and, store for later.
        complex_1_filter_spec = test_filter_spec
        nested_test_filter_list.append( test_filter_spec )
        
        #----------------------------------------------------------------------#
        # ! ----> 2 level - relation type slug, relation trait, entity type slug, entity trait
        #----------------------------------------------------------------------#
        
        print( "\n\n------------------------------\n2 level - relation type slug, relation trait, entity type slug, entity trait\n------------------------------" )
        test_filter_list = []
        
        #----------------------------------------------------------------------#
        # --------> filter 1 - relation_type_slug in "mentioned", "quoted", "shared_byline"
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
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )
        
        #----------------------------------------------------------------------#
        # --------> filter 2 - simple_1_filter_spec
        
        # validate
        test_filter_spec = simple_1_filter_spec
        should_be = 2320
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )

        #----------------------------------------------------------------------#
        # --------> filter 3 - complex_1_filter_spec
        
        # validate
        test_filter_spec = complex_1_filter_spec
        should_be = 1433
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
        # add to list
        test_filter_json_dict = test_filter_spec.get_filter_spec()
        test_filter_list.append( test_filter_json_dict )
        
        #----------------------------------------------------------------------#
        # --------> filter 4 - entity trait "sourcenet-Newspaper-ID" IN 1
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
        
        # validate
        self.validate_filter_spec( test_instance, test_filter_spec, should_be )
        
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
        # ! TODO ----> AND
        #----------------------------------------------------------------------#
        
        #----------------------------------------------------------------------#
        # ! TODO ----> OR
        #----------------------------------------------------------------------#
        
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

        # ! ----> test set()-ers
        
        # for each (using last loaded test instance):
        # - get original value and store
        # - set new value
        # - get value.
        # - assertEquals( get value, new value )
        # - assertNotEqual( get value, original value )
        
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


#-- END test class NetworkDataRequestTest --#
