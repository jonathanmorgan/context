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
from context.tests.test_helper import TestHelper

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
    
    # JSON files
    FILE_PATH_BASE_FOLDER = "{}/".format( os.path.dirname( os.path.realpath( __file__ ) ) )
    FILE_PATH_NETWORK_DATA_REQUEST_BASIC = "{}network_data_request_basic.json".format( FILE_PATH_BASE_FOLDER )
    FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_ID_FILTER = "{}network_data_request_with_entity_id_filter.json".format( FILE_PATH_BASE_FOLDER )
    FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_SELECTION = "{}network_data_request_with_entity_select.json".format( FILE_PATH_BASE_FOLDER )
    FILE_PATH_LIST = []
    FILE_PATH_LIST.append( FILE_PATH_NETWORK_DATA_REQUEST_BASIC )
    FILE_PATH_LIST.append( FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_ID_FILTER )
    FILE_PATH_LIST.append( FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_SELECTION )
    
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
    JSON_FILE_TO_VALIDATE_FUNCTION_MAP[ FILE_PATH_NETWORK_DATA_REQUEST_BASIC ] = "validate_instance_basic"
    JSON_FILE_TO_VALIDATE_FUNCTION_MAP[ FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_ID_FILTER ] = "validate_instance_id_filter"
    JSON_FILE_TO_VALIDATE_FUNCTION_MAP[ FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_SELECTION ] = "validate_instance_entity_selection"
    
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


    @classmethod
    def load_basic( cls ):
        
        # return reference
        instance_OUT = None
        
        # create instance
        instance_OUT = NetworkDataRequest()
        
        # load basic.
        instance_OUT.load_network_data_request_json_file( cls.FILE_PATH_NETWORK_DATA_REQUEST_BASIC )
        
        return instance_OUT
        
    #-- END class method load_basic() --#


    @classmethod
    def load_with_entity_id_filter( cls ):
        
        # return reference
        instance_OUT = None
        
        # create instance
        instance_OUT = NetworkDataRequest()
        
        # load basic.
        instance_OUT.load_network_data_request_json_file( cls.FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_ID_FILTER )
        
        return instance_OUT
        
    #-- END class method load_with_entity_id_filter() --#


    @classmethod
    def load_with_entity_selection( cls ):
        
        # return reference
        instance_OUT = None
        
        # create instance
        instance_OUT = NetworkDataRequest()
        
        # load basic.
        instance_OUT.load_network_data_request_json_file( cls.FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_SELECTION )
        
        return instance_OUT
        
    #-- END class method load_with_entity_selection() --#


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


    def validate_entity_selection( self,
                                   test_instance_IN,
                                   include_entity_id_filter_IN = False ):        

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
        
            # testing entity ID filter?
            if ( include_entity_id_filter_IN == True ):
        
                # testing entity ID filter - 10 properties, not 8
                properties_count = 10
                
            else:
            
                # not testing entity ID filter - 8 properties
                properties_count = 8
                
            #-- END check to see if testing entity ID filter. --#
        
            # ! ----> validate entity_selection
            entity_selection_dict = test_instance_IN.get_entity_selection()
            
            # count the items
            entity_selection_count = len( entity_selection_dict )
            test_value = entity_selection_count
            should_be = properties_count
            error_string = "entity_selection has {} items, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! ----> try retrieving entity_selection properties
            
            # ! --------> relation_type_slug_filter_combine_type
            test_prop_name = NetworkDataRequest.PROP_NAME_RELATION_TYPE_SLUG_FILTER_COMBINE_TYPE
            test_value = test_instance_IN.get_entity_selection_property( test_prop_name )
            should_be = self.TEST_ES_RELATION_TYPE_SLUG_FILTER_COMBINE_TYPE
            error_string = "relation_type_slug_filter_combine_type is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! --------> relation_type_slug_filters
            test_prop_name = NetworkDataRequest.PROP_NAME_RELATION_TYPE_SLUG_FILTERS
            test_temp = test_instance_IN.get_entity_selection_property( test_prop_name )
            test_value = len( test_temp )
            should_be = self.TEST_ES_RELATION_TYPE_SLUG_FILTERS_COUNT
            error_string = "relation_type_slug_filters count is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! --------> relation_trait_filter_combine_type
            test_prop_name = NetworkDataRequest.PROP_NAME_RELATION_TRAIT_FILTER_COMBINE_TYPE
            test_value = test_instance_IN.get_entity_selection_property( test_prop_name )
            should_be = self.TEST_ES_RELATION_TRAIT_FILTER_COMBINE_TYPE
            error_string = "relation_trait_filter_combine_type is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! --------> relation_trait_filters
            test_prop_name = NetworkDataRequest.PROP_NAME_RELATION_TRAIT_FILTERS
            test_temp = test_instance_IN.get_entity_selection_property( test_prop_name )
            test_value = len( test_temp )
            should_be = self.TEST_ES_RELATION_TRAIT_FILTERS_COUNT
            error_string = "relation_trait_filters count is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
                        
            # ! --------> entity_type_slug_filter_combine_type
            test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_TYPE_SLUG_FILTER_COMBINE_TYPE
            test_value = test_instance_IN.get_entity_selection_property( test_prop_name )
            should_be = self.TEST_ES_ENTITY_TYPE_SLUG_FILTER_COMBINE_TYPE
            error_string = "entity_type_slug_filter_combine_type is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )

            # ! --------> entity_type_slug_filters
            test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_TYPE_SLUG_FILTERS
            test_temp = test_instance_IN.get_entity_selection_property( test_prop_name )
            test_value = len( test_temp )
            should_be = self.TEST_ES_ENTITY_TYPE_SLUG_FILTERS_COUNT
            error_string = "entity_type_slug_filters count is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! --------> entity_trait_filter_combine_type
            test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_TRAIT_FILTER_COMBINE_TYPE
            test_value = test_instance_IN.get_entity_selection_property( test_prop_name )
            should_be = self.TEST_ES_ENTITY_TRAIT_FILTER_COMBINE_TYPE
            error_string = "entity_trait_filter_combine_type is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )            
            
            # ! --------> entity_trait_filters
            test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_TRAIT_FILTERS
            test_temp = test_instance_IN.get_entity_selection_property( test_prop_name )
            test_value = len( test_temp )
            should_be = self.TEST_ES_ENTITY_TRAIT_FILTERS_COUNT
            error_string = "entity_trait_filters count is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # testing entity ID filter?
            if ( include_entity_id_filter_IN == True ):
        
                # ! --------> entity_id_filter_combine_type
                test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_ID_FILTER_COMBINE_TYPE
                test_value = test_instance_IN.get_entity_selection_property( test_prop_name )
                should_be = self.TEST_ES_ENTITY_ID_FILTER_COMBINE_TYPE
                error_string = "entity_trait_filter_combine_type is {}, should be {}.".format( test_value, should_be )
                self.assertEqual( test_value, should_be, msg = error_string )            
                
                # ! --------> entity_id_filters
                test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_ID_FILTERS
                test_temp = test_instance_IN.get_entity_selection_property( test_prop_name )
                test_value = len( test_temp )
                should_be = self.TEST_ES_ENTITY_ID_FILTERS_COUNT
                error_string = "entity_id_filters count is {}, should be {}.".format( test_value, should_be )
                self.assertEqual( test_value, should_be, msg = error_string )
                
            #-- END check to see if testing entity ID filter. --#

        else:
        
            # no instance passed in.  Assert Not None here, so we raise Error.
            test_value = test_instance_IN
            error_string = "None passed in, should be a NetworkDataRequest instance."
            self.assertIsNotNone( test_value, msg = error_string )
            
        #-- END check to see if instance passed in. --#
        
    #-- END method validate_entity_selection() --#
    

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
            self.validate_relation_selection( test_instance_IN,
                                              include_entity_id_filter_IN = True )

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


    def validate_relation_selection( self,
                                     test_instance_IN,
                                     include_entity_id_filter_IN = False ):        

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
        
            # testing entity ID filter?
            if ( include_entity_id_filter_IN == True ):
        
                # testing entity ID filter - 10 properties, not 8
                properties_count = 10
                
            else:
            
                # not testing entity ID filter - 8 properties
                properties_count = 8
                
            #-- END check to see if testing entity ID filter. --#
        
            # ! ----> validate relation_selection
            relation_selection_dict = test_instance_IN.get_relation_selection()
            
            # count the items
            relation_selection_count = len( relation_selection_dict )
            test_value = relation_selection_count
            should_be = properties_count
            error_string = "relation_selection has {} items, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! ----> try retrieving relation_selection properties
            
            # ! --------> relation_type_slug_filter_combine_type
            test_prop_name = NetworkDataRequest.PROP_NAME_RELATION_TYPE_SLUG_FILTER_COMBINE_TYPE
            test_value = test_instance_IN.get_relation_selection_property( test_prop_name )
            should_be = self.TEST_RS_RELATION_TYPE_SLUG_FILTER_COMBINE_TYPE
            error_string = "relation_type_slug_filter_combine_type is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! --------> relation_type_slug_filters
            test_prop_name = NetworkDataRequest.PROP_NAME_RELATION_TYPE_SLUG_FILTERS
            test_temp = test_instance_IN.get_relation_selection_property( test_prop_name )
            test_value = len( test_temp )
            should_be = self.TEST_RS_RELATION_TYPE_SLUG_FILTERS_COUNT
            error_string = "relation_type_slug_filters count is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! --------> relation_trait_filter_combine_type
            test_prop_name = NetworkDataRequest.PROP_NAME_RELATION_TRAIT_FILTER_COMBINE_TYPE
            test_value = test_instance_IN.get_relation_selection_property( test_prop_name )
            should_be = self.TEST_RS_RELATION_TRAIT_FILTER_COMBINE_TYPE
            error_string = "relation_trait_filter_combine_type is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! --------> relation_trait_filters
            test_prop_name = NetworkDataRequest.PROP_NAME_RELATION_TRAIT_FILTERS
            test_temp = test_instance_IN.get_relation_selection_property( test_prop_name )
            test_value = len( test_temp )
            should_be = self.TEST_RS_RELATION_TRAIT_FILTERS_COUNT
            error_string = "relation_trait_filters count is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
                        
            # ! --------> entity_type_slug_filter_combine_type
            test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_TYPE_SLUG_FILTER_COMBINE_TYPE
            test_value = test_instance_IN.get_relation_selection_property( test_prop_name )
            should_be = self.TEST_RS_ENTITY_TYPE_SLUG_FILTER_COMBINE_TYPE
            error_string = "entity_type_slug_filter_combine_type is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )

            # ! --------> entity_type_slug_filters
            test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_TYPE_SLUG_FILTERS
            test_temp = test_instance_IN.get_relation_selection_property( test_prop_name )
            test_value = len( test_temp )
            should_be = self.TEST_RS_ENTITY_TYPE_SLUG_FILTERS_COUNT
            error_string = "entity_type_slug_filters count is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # ! --------> entity_trait_filter_combine_type
            test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_TRAIT_FILTER_COMBINE_TYPE
            test_value = test_instance_IN.get_relation_selection_property( test_prop_name )
            should_be = self.TEST_RS_ENTITY_TRAIT_FILTER_COMBINE_TYPE
            error_string = "entity_trait_filter_combine_type is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )            
            
            # ! --------> entity_trait_filters
            test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_TRAIT_FILTERS
            test_temp = test_instance_IN.get_relation_selection_property( test_prop_name )
            test_value = len( test_temp )
            should_be = self.TEST_RS_ENTITY_TRAIT_FILTERS_COUNT
            error_string = "entity_trait_filters count is {}, should be {}.".format( test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )
            
            # testing entity ID filter?
            if ( include_entity_id_filter_IN == True ):
        
                # ! --------> entity_id_filter_combine_type
                test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_ID_FILTER_COMBINE_TYPE
                test_value = test_instance_IN.get_relation_selection_property( test_prop_name )
                should_be = self.TEST_RS_ENTITY_ID_FILTER_COMBINE_TYPE
                error_string = "entity_trait_filter_combine_type is {}, should be {}.".format( test_value, should_be )
                self.assertEqual( test_value, should_be, msg = error_string )            
                
                # ! --------> entity_id_filters
                test_prop_name = NetworkDataRequest.PROP_NAME_ENTITY_ID_FILTERS
                test_temp = test_instance_IN.get_relation_selection_property( test_prop_name )
                test_value = len( test_temp )
                should_be = self.TEST_RS_ENTITY_ID_FILTERS_COUNT
                error_string = "entity_id_filters count is {}, should be {}.".format( test_value, should_be )
                self.assertEqual( test_value, should_be, msg = error_string )
                
            #-- END check to see if testing entity ID filter. --#

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
        
        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )
        
        # ! ----> test get()-ers
        
        # load "with_entity_id_filter" to use as test instance.
        test_instance = self.load_with_entity_id_filter()
        
        # first, test getters by calling the validate method
        self.validate_instance_id_filter( test_instance )
        
        # load "with_entity_selection" to use as test instance.
        test_instance = self.load_with_entity_selection()
        
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

    #-- END test method test_getters() --#


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
        
        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )
        
        # init instance.
        test_instance = NetworkDataRequest()
        
        # loop over the JSON files.
        json_file_path_list = self.FILE_PATH_LIST
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
        
        
    #-- END method load_network_data_request_json() --#


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
        
        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )
        
        # init instance.
        test_instance = NetworkDataRequest()
        
        # loop over the JSON files.
        json_file_path_list = self.FILE_PATH_LIST
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
        
    #-- END method load_network_data_request_json_file() --#


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
        
        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )
        
        # init instance.
        test_instance = NetworkDataRequest()
        
        # loop over the JSON files.
        json_file_path_list = self.FILE_PATH_LIST
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
        
        
    #-- END method load_network_data_request_json_string() --#


#-- END test class NetworkDataRequestTest --#
