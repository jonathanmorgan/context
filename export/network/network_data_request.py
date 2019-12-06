from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2019 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context.

context is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context. If not, see http://www.gnu.org/licenses/.
'''

'''
This object is used to store a request for network data, made up of two parallel
    sets of filter criteria, one to select the nodes (Entities) to include as
    rows and columns in the graph (this creates symmetric matrices, so same
    number of rows and columns, and entities are in the same order from top to
    bottom and left to right).
    
It can be initialized directly in the instance, or it can be initialized from a
    JSON file.
'''

__author__ = "jonathanmorgan"
__date__ = "$December, 4 2019 10:44:50 AM$"

if __name__ == "__main__":
    print( "Hello World" )

#===============================================================================
# ! > imports (in alphabetical order by package, then by name)
#===============================================================================

# python base imports
#from datetime import date
from datetime import datetime
import json
import logging
import operator
import sys

# django database classes
from django.db.models import Q

# python_utilities
from python_utilities.booleans.boolean_helper import BooleanHelper
from python_utilities.parameters.param_container import ParamContainer
from python_utilities.status.status_container import StatusContainer

# Import context shared classes.
from context.shared.context_base import ContextBase


#===============================================================================
# ! > classes (in alphabetical order by name)
#===============================================================================

class NetworkDataRequest( ContextBase ):


    #---------------------------------------------------------------------------
    # ! ==> CONSTANTS-ish
    #---------------------------------------------------------------------------


    # LOGGING
    DEBUG_FLAG = True
    LOGGER_NAME = "context.export.network.network_data_request.NetworkDataRequest"
    ME = LOGGER_NAME

    # a network data request will have a set of "output_specification" info, a 
    #     set of "relation_selection" filter criteria, and an optional set of
    #     additional "entity_selection" filter criteria.  Each can contain the
    #     same set of relation filter criteria, used to select relations, then
    #     for the entity selection, entities are selected from all the FROMs and
    #     TOs of the matching relations.

    # root-level properties
    PROP_NAME_OUTPUT_SPECIFICATION = "output_specification"
    PROP_NAME_RELATION_SELECT = "relation_selection"
    PROP_NAME_ENTITY_SELECT = "entity_selection"
    
    #--------------------------------------------------------------------------#
    # ! ----> output_details
    PROP_NAME_OUTPUT_TYPE = "output_type"
    PROP_NAME_OUTPUT_FILE_PATH = "output_file_path"
    PROP_NAME_OUTPUT_FORMAT = "output_format"
    PROP_NAME_OUTPUT_STRUCTURE = "output_structure"
    PROP_NAME_OUTPUT_INCLUDE_COLUMN_HEADERS = "output_include_column_headers"
    
    # output_type values
    PROP_VALUE_OUTPUT_TYPE_FILE = "file"
    PROP_VALUE_OUTPUT_TYPE_DOWNLOAD = "download"
    PROP_VALUE_OUTPUT_TYPE_DEFAULT = PROP_VALUE_OUTPUT_TYPE_FILE
    OUTPUT_TYPE_VALUES = []
    OUTPUT_TYPE_VALUES.append( PROP_VALUE_OUTPUT_TYPE_FILE )
    OUTPUT_TYPE_VALUES.append( PROP_VALUE_OUTPUT_TYPE_DOWNLOAD )
    
    # output_format values
    PROP_VALUE_OUTPUT_FORMAT_SIMPLE_MATRIX = "simple_matrix"
    PROP_VALUE_OUTPUT_FORMAT_CSV_MATRIX = "CSV_matrix"
    PROP_VALUE_OUTPUT_FORMAT_TSV_MATRIX = "TSV_matrix"
    PROP_VALUE_OUTPUT_FORMAT_NODE_AND_EDGE_LISTS = "node_and_edge_lists"
    PROP_VALUE_OUTPUT_FORMAT_DEFAULT = PROP_VALUE_OUTPUT_FORMAT_TSV_MATRIX
    OUTPUT_FORMAT_VALUES = []
    OUTPUT_FORMAT_VALUES.append( PROP_VALUE_OUTPUT_FORMAT_SIMPLE_MATRIX )
    OUTPUT_FORMAT_VALUES.append( PROP_VALUE_OUTPUT_FORMAT_CSV_MATRIX )
    OUTPUT_FORMAT_VALUES.append( PROP_VALUE_OUTPUT_FORMAT_TSV_MATRIX )
    OUTPUT_FORMAT_VALUES.append( PROP_VALUE_OUTPUT_FORMAT_NODE_AND_EDGE_LISTS )
    
    # output_structure values
    PROP_VALUE_OUTPUT_STRUCTURE_JUST_TIES = "just_ties"
    PROP_VALUE_OUTPUT_STRUCTURE_JUST_TRAITS = "just_traits"
    PROP_VALUE_OUTPUT_STRUCTURE_BOTH_TRAIT_COLUMNS = "both_trait_columns"
    PROP_VALUE_OUTPUT_STRUCTURE_BOTH_TRAIT_ROWS = "both_trait_rows"
    PROP_VALUE_OUTPUT_STRUCTURE_DEFAULT = PROP_VALUE_OUTPUT_STRUCTURE_JUST_TIES
    OUTPUT_STRUCTURE_VALUES = []
    OUTPUT_STRUCTURE_VALUES.append( PROP_VALUE_OUTPUT_STRUCTURE_JUST_TIES )
    OUTPUT_STRUCTURE_VALUES.append( PROP_VALUE_OUTPUT_STRUCTURE_JUST_TRAITS )
    OUTPUT_STRUCTURE_VALUES.append( PROP_VALUE_OUTPUT_STRUCTURE_BOTH_TRAIT_COLUMNS )
    OUTPUT_STRUCTURE_VALUES.append( PROP_VALUE_OUTPUT_STRUCTURE_BOTH_TRAIT_ROWS )
    
    #--------------------------------------------------------------------------#
    # ! ----> filter criteria - relations
    PROP_NAME_RELATION_TYPE_SLUG_FILTER_COMBINE_TYPE = "relation_type_slug_filter_combine_type"
    PROP_NAME_RELATION_TYPE_SLUG_FILTERS = "relation_type_slug_filters"
    PROP_NAME_RELATION_TRAIT_FILTER_COMBINE_TYPE = "relation_trait_filter_combine_type"
    PROP_NAME_RELATION_TRAIT_FILTERS = "relation_trait_filters"
    
    #--------------------------------------------------------------------------#
    # ! ----> filter criteria - entities
    PROP_NAME_ENTITY_TYPE_SLUG_FILTER_COMBINE_TYPE = "entity_type_slug_filter_combine_type"
    PROP_NAME_ENTITY_TYPE_SLUG_FILTERS = "entity_type_slug_filters"
    PROP_NAME_ENTITY_TRAIT_FILTER_COMBINE_TYPE = "entity_trait_filter_combine_type"
    PROP_NAME_ENTITY_TRAIT_FILTERS = "entity_trait_filters"
    PROP_NAME_ENTITY_ID_FILTER_COMBINE_TYPE = "entity_id_filter_combine_type"
    PROP_NAME_ENTITY_ID_FILTERS = "entity_id_filters"
    
    #--------------------------------------------------------------------------#
    # !----> filter criteria - shared
    
    # value comparison
    PROP_NAME_NAME = "name"
    PROP_NAME_TYPE_ID = "type_id"
    PROP_NAME_TYPE_LABEL = "type_label"
    PROP_NAME_DATA_TYPE = "data_type"
    PROP_NAME_COMPARISON_TYPE = "comparison_type"
    PROP_NAME_VALUE = "value"
    PROP_NAME_VALUE_LIST = "value_list"
    PROP_NAME_VALUE_FROM = "value_from"
    PROP_NAME_VALUE_TO = "value_to"
    PROP_NAME_RELATION_ROLES_LIST = "relation_roles_list"

    # filter_combine_type values
    PROP_VALUE_FILTER_COMBINE_TYPE_AND = "AND"
    PROP_VALUE_FILTER_COMBINE_TYPE_OR = "OR"
    PROP_VALUE_FILTER_COMBINE_TYPE_DEFAULT = PROP_VALUE_FILTER_COMBINE_TYPE_AND
    FILTER_COMBINE_TYPE_VALUES = []
    FILTER_COMBINE_TYPE_VALUES.append( PROP_VALUE_FILTER_COMBINE_TYPE_AND )
    FILTER_COMBINE_TYPE_VALUES.append( PROP_VALUE_FILTER_COMBINE_TYPE_OR )

    # reserved trait values
    VALUE_EMPTY = "EMPTY_VALUE"
    
    # data_type values
    PROP_VALUE_DATA_TYPE_STRING = "string"
    PROP_VALUE_DATA_TYPE_INT = "int"
    PROP_VALUE_DATA_TYPE_DATE = "date"
    PROP_VALUE_DATA_TYPE_DATETIME = "datetime"
    PROP_VALUE_DATA_TYPE_FILTER = "filter"
    PROP_VALUE_DATA_TYPE_DEFAULT = PROP_VALUE_DATA_TYPE_STRING
    DATA_TYPE_VALUES = []
    DATA_TYPE_VALUES.append( PROP_VALUE_DATA_TYPE_STRING )
    DATA_TYPE_VALUES.append( PROP_VALUE_DATA_TYPE_INT )
    DATA_TYPE_VALUES.append( PROP_VALUE_DATA_TYPE_DATE )
    DATA_TYPE_VALUES.append( PROP_VALUE_DATA_TYPE_DATETIME )
    DATA_TYPE_VALUES.append( PROP_VALUE_DATA_TYPE_FILTER )

    # trait_comparison_type values
    PROP_VALUE_COMPARISON_TYPE_EQUALS = "equals"
    PROP_VALUE_COMPARISON_TYPE_INCLUDES = "includes"
    PROP_VALUE_COMPARISON_TYPE_EXCLUDES = "excludes"
    PROP_VALUE_COMPARISON_TYPE_IN_RANGE = "in_range"
    PROP_VALUE_COMPARISON_TYPE_AND = PROP_VALUE_FILTER_COMBINE_TYPE_AND
    PROP_VALUE_COMPARISON_TYPE_OR = PROP_VALUE_FILTER_COMBINE_TYPE_OR    
    PROP_VALUE_COMPARISON_TYPE_DEFAULT = PROP_VALUE_COMPARISON_TYPE_EQUALS
    COMPARISON_TYPE_VALUES = []
    COMPARISON_TYPE_VALUES.append( PROP_VALUE_COMPARISON_TYPE_EQUALS )
    COMPARISON_TYPE_VALUES.append( PROP_VALUE_COMPARISON_TYPE_INCLUDES )
    COMPARISON_TYPE_VALUES.append( PROP_VALUE_COMPARISON_TYPE_EXCLUDES )
    COMPARISON_TYPE_VALUES.append( PROP_VALUE_COMPARISON_TYPE_IN_RANGE )
    COMPARISON_TYPE_VALUES.append( PROP_VALUE_COMPARISON_TYPE_AND )
    COMPARISON_TYPE_VALUES.append( PROP_VALUE_COMPARISON_TYPE_OR )
    
    # relation_roles_list values
    PROP_VALUE_RELATION_ROLES_LIST_FROM = "FROM"
    PROP_VALUE_RELATION_ROLES_LIST_TO = "TO"
    PROP_VALUE_RELATION_ROLES_LIST_THROUGH = "THROUGH"
    PROP_VALUE_RELATION_ROLES_LIST_ALL = "ALL"
    PROP_VALUE_RELATION_ROLES_LIST_EMPTY = ""
    PROP_VALUE_RELATION_ROLES_LIST_NONE = None
    PROP_VALUE_RELATION_ROLES_LIST_DEFAULT = PROP_VALUE_RELATION_ROLES_LIST_ALL
    RELATION_ROLES_LIST_VALUES = []
    RELATION_ROLES_LIST_VALUES.append( PROP_VALUE_RELATION_ROLES_LIST_FROM )
    RELATION_ROLES_LIST_VALUES.append( PROP_VALUE_RELATION_ROLES_LIST_TO )
    RELATION_ROLES_LIST_VALUES.append( PROP_VALUE_RELATION_ROLES_LIST_THROUGH )
    RELATION_ROLES_LIST_VALUES.append( PROP_VALUE_RELATION_ROLES_LIST_ALL )
    RELATION_ROLES_LIST_VALUES.append( PROP_VALUE_RELATION_ROLES_LIST_EMPTY )    
    RELATION_ROLES_LIST_VALUES.append( PROP_VALUE_RELATION_ROLES_LIST_NONE )

    #--------------------------------------------------------------------------#
    # ! ----> filter criteria - traits
    PROP_NAME_TRAIT_NAME = "trait_name"
    PROP_NAME_TRAIT_TYPE_ID = "trait_type_id"
    PROP_NAME_TRAIT_TYPE_SLUG = "trait_type_slug"
    PROP_NAME_TRAIT_DATA_TYPE = PROP_NAME_DATA_TYPE
    PROP_NAME_TRAIT_COMPARISON_TYPE = PROP_NAME_COMPARISON_TYPE
    PROP_NAME_TRAIT_VALUE = PROP_NAME_VALUE
    PROP_NAME_TRAIT_VALUE_LIST = PROP_NAME_VALUE_LIST
    PROP_NAME_TRAIT_VALUE_FROM = PROP_NAME_VALUE_FROM
    PROP_NAME_TRAIT_VALUE_TO = PROP_NAME_VALUE_TO
    
    # trait_filter_combine_type values
    PROP_VALUE_TRAIT_FILTER_COMBINE_TYPE_AND = PROP_VALUE_FILTER_COMBINE_TYPE_AND
    PROP_VALUE_TRAIT_FILTER_COMBINE_TYPE_OR = PROP_VALUE_FILTER_COMBINE_TYPE_OR
    PROP_VALUE_TRAIT_FILTER_COMBINE_TYPE_DEFAULT = PROP_VALUE_TRAIT_FILTER_COMBINE_TYPE_AND
    TRAIT_FILTER_COMBINE_TYPE_VALUES = FILTER_COMBINE_TYPE_VALUES

    # trait_data_type values
    PROP_VALUE_TRAIT_DATA_TYPE_STRING = PROP_VALUE_DATA_TYPE_STRING
    PROP_VALUE_TRAIT_DATA_TYPE_INT = PROP_VALUE_DATA_TYPE_INT
    PROP_VALUE_TRAIT_DATA_TYPE_DATE = PROP_VALUE_DATA_TYPE_DATE
    PROP_VALUE_TRAIT_DATA_TYPE_DATETIME = PROP_VALUE_DATA_TYPE_DATETIME
    PROP_VALUE_TRAIT_DATA_TYPE_TRAIT_FILTER = PROP_VALUE_DATA_TYPE_FILTER
    PROP_VALUE_TRAIT_DATA_TYPE_DEFAULT = PROP_VALUE_TRAIT_DATA_TYPE_STRING
    TRAIT_DATA_TYPE_VALUES = DATA_TYPE_VALUES

    # trait_comparison_type values
    PROP_VALUE_TRAIT_COMPARISON_TYPE_EQUALS = PROP_VALUE_COMPARISON_TYPE_EQUALS
    PROP_VALUE_TRAIT_COMPARISON_TYPE_INCLUDES = PROP_VALUE_COMPARISON_TYPE_INCLUDES
    PROP_VALUE_TRAIT_COMPARISON_TYPE_EXCLUDES = PROP_VALUE_COMPARISON_TYPE_EXCLUDES
    PROP_VALUE_TRAIT_COMPARISON_TYPE_IN_RANGE = PROP_VALUE_COMPARISON_TYPE_IN_RANGE
    PROP_VALUE_TRAIT_COMPARISON_TYPE_AND = PROP_VALUE_COMPARISON_TYPE_AND
    PROP_VALUE_TRAIT_COMPARISON_TYPE_OR = PROP_VALUE_COMPARISON_TYPE_OR    
    PROP_VALUE_TRAIT_COMPARISON_TYPE_DEFAULT = PROP_VALUE_TRAIT_COMPARISON_TYPE_EQUALS
    TRAIT_COMPARISON_TYPE_VALUES = COMPARISON_TYPE_VALUES
    
    # reserved trait values
    TRAIT_VALUE_EMPTY = VALUE_EMPTY

    #--------------------------------------------------------------------------#
    # ! ----> filter criteria - entity identifiers
    PROP_NAME_ID_NAME = "id_name"
    PROP_NAME_ID_TYPE_ID = "id_type_id"
    PROP_NAME_ID_TYPE_NAME = "id_type_name"
    PROP_NAME_ID_DATA_TYPE = PROP_NAME_DATA_TYPE
    PROP_NAME_ID_COMPARISON_TYPE = PROP_NAME_COMPARISON_TYPE
    PROP_NAME_ID_VALUE = PROP_NAME_VALUE
    PROP_NAME_ID_VALUE_LIST = PROP_NAME_VALUE_LIST

    # id_filter_combine_type values
    PROP_VALUE_ID_FILTER_COMBINE_TYPE_AND = PROP_VALUE_FILTER_COMBINE_TYPE_AND
    PROP_VALUE_ID_FILTER_COMBINE_TYPE_OR = PROP_VALUE_FILTER_COMBINE_TYPE_OR
    PROP_VALUE_ID_FILTER_COMBINE_TYPE_DEFAULT = PROP_VALUE_ID_FILTER_COMBINE_TYPE_AND
    ID_FILTER_COMBINE_TYPE_VALUES = FILTER_COMBINE_TYPE_VALUES

    # id_data_type values
    PROP_VALUE_ID_DATA_TYPE_STRING = PROP_VALUE_DATA_TYPE_STRING
    PROP_VALUE_ID_DATA_TYPE_INT = PROP_VALUE_DATA_TYPE_INT
    PROP_VALUE_ID_DATA_TYPE_FILTER = PROP_VALUE_DATA_TYPE_FILTER
    PROP_VALUE_ID_DATA_TYPE_DEFAULT = PROP_VALUE_TRAIT_DATA_TYPE_STRING
    ID_DATA_TYPE_VALUES = []
    ID_DATA_TYPE_VALUES.append( PROP_VALUE_ID_DATA_TYPE_STRING )
    ID_DATA_TYPE_VALUES.append( PROP_VALUE_ID_DATA_TYPE_INT )
    ID_DATA_TYPE_VALUES.append( PROP_VALUE_ID_DATA_TYPE_FILTER )

    # id_comparison_type values
    PROP_VALUE_ID_COMPARISON_TYPE_EQUALS = PROP_VALUE_COMPARISON_TYPE_EQUALS
    PROP_VALUE_ID_COMPARISON_TYPE_INCLUDES = PROP_VALUE_COMPARISON_TYPE_INCLUDES
    PROP_VALUE_ID_COMPARISON_TYPE_EXCLUDES = PROP_VALUE_COMPARISON_TYPE_EXCLUDES
    PROP_VALUE_ID_COMPARISON_TYPE_AND = PROP_VALUE_COMPARISON_TYPE_AND
    PROP_VALUE_ID_COMPARISON_TYPE_OR = PROP_VALUE_COMPARISON_TYPE_OR    
    PROP_VALUE_ID_COMPARISON_TYPE_DEFAULT = PROP_VALUE_ID_COMPARISON_TYPE_EQUALS
    ID_COMPARISON_TYPE_VALUES = []
    ID_COMPARISON_TYPE_VALUES.append( PROP_VALUE_ID_COMPARISON_TYPE_EQUALS )
    ID_COMPARISON_TYPE_VALUES.append( PROP_VALUE_ID_COMPARISON_TYPE_INCLUDES )
    ID_COMPARISON_TYPE_VALUES.append( PROP_VALUE_ID_COMPARISON_TYPE_EXCLUDES )
    ID_COMPARISON_TYPE_VALUES.append( PROP_VALUE_ID_COMPARISON_TYPE_AND )
    ID_COMPARISON_TYPE_VALUES.append( PROP_VALUE_ID_COMPARISON_TYPE_OR )

    #---------------------------------------------------------------------------
    # ! ==> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self ):

        # call parent's __init__()
        super( NetworkDataRequest, self ).__init__()

        # declare variables - moved to parent
        #self.request = None
        #self.parameters = ParamContainer()

        # define parameters - moved to parent
        #self.define_parameters( NetworkOutput.PARAM_NAME_TO_TYPE_MAP )
        
        # store raw JSON string, if JSON
        self.m_request_json_string = None
        
        # and store parsed JSON
        self.m_request_json = None
        
        # output specification details
        self.m_output_specification = None
        self.m_output_type = None
        self.m_output_file_path = None
        self.m_output_format = None
        self.m_output_structure = None
        self.m_output_include_column_headers = None

        # variables for outputting result as file
        self.mime_type = ""
        self.file_extension = ""
        
        # variables to hold node and tie filter criteria.
        self.m_relation_selection_dict = None
        self.m_entity_selection_dict = None
                
        # set logger name (for LoggingHelper parent class: (LoggingHelper --> BasicRateLimited --> ContextTextBase --> ArticleCoding).
        self.set_logger_name( self.LOGGER_NAME )
        
        # status
        self.m_is_request_ok = True
        
    #-- END method __init__() --#


    #---------------------------------------------------------------------------
    # ! ==> instance methods
    #---------------------------------------------------------------------------


    def is_request_ok( self ):
        
        # return reference
        value_OUT = None
        
        value_OUT = self.m_is_request_ok
        
        return value_OUT
    
    #-- END method is_request_ok() --#


    def get_entity_select( self ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        prop_dict = None
        
        # see if already stored.
        prop_dict = self.m_entity_selection_dict
        
        # anything stored?
        if ( prop_dict is None ):
        
            # no.  Create a dictionary, store it, and return it.
            prop_dict = {}
            
            # store it.
            self.set_entity_select( prop_dict )
            
            # return it.
            value_OUT = self.get_entity_select()
            
        else:
        
            # found something.  Return it.
            value_OUT = prop_dict
            
        #-- END see if initialized --#
        
        return value_OUT
    
    #-- END method get_entity_select() --#


    def get_entity_selection_property( self, name_IN, default_IN = None ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        prop_dict = None
        
        # get output spec
        prop_dict = self.get_entity_select()
        
        # retrieve the output_type value.
        value_OUT = prop_dict.get( name_IN, default_IN )
        
        return value_OUT
    
    #-- END method get_entity_selection_property() --#


    def get_output_file_path( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_output_spec_property( self.PROP_NAME_OUTPUT_FILE_PATH )
        
        return value_OUT
    
    #-- END method get_output_file_path() --#


    def get_output_format( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_output_spec_property( self.PROP_NAME_OUTPUT_FORMAT )
        
        return value_OUT
    
    #-- END method get_output_format() --#


    def get_output_include_column_headers( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_output_spec_property( self.PROP_NAME_OUTPUT_INCLUDE_COLUMN_HEADERS )
        
        return value_OUT
    
    #-- END method get_output_include_column_headers() --#


    def get_output_specification( self ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        prop_dict = None
        
        # see if already stored.
        prop_dict = self.m_output_specification
        
        # anything stored?
        if ( prop_dict is None ):
        
            # no.  Create a dictionary, store it, and return it.
            prop_dict = {}
            
            # store it.
            self.set_output_specification( prop_dict )
            
            # return it.
            value_OUT = self.get_output_specification()
            
        else:
        
            # found something.  Return it.
            value_OUT = prop_dict
            
        #-- END see if initialized --#
        
        return value_OUT
    
    #-- END method get_output_specification() --#


    def get_output_spec_property( self, name_IN, default_IN = None ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        output_spec = None
        
        # get output spec
        output_spec = self.get_output_specification()
        
        # retrieve the output_type value.
        value_OUT = output_spec.get( name_IN, default_IN )
        
        return value_OUT
    
    #-- END method get_output_spec_property() --#


    def get_output_structure( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_output_spec_property( self.PROP_NAME_OUTPUT_STRUCTURE )
        
        return value_OUT
    
    #-- END method get_output_format() --#


    def get_output_type( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_output_spec_property( self.PROP_NAME_OUTPUT_TYPE )
        
        return value_OUT
    
    #-- END method get_output_type() --#


    def get_relation_select( self ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        prop_dict = None
        
        # see if already stored.
        prop_dict = self.m_relation_selection_dict
        
        # anything stored?
        if ( prop_dict is None ):
        
            # no.  Create a dictionary, store it, and return it.
            prop_dict = {}
            
            # store it.
            self.set_relation_select( prop_dict )
            
            # return it.
            value_OUT = self.get_relation_select()
            
        else:
        
            # found something.  Return it.
            value_OUT = prop_dict
            
        #-- END see if initialized --#
        
        return value_OUT
    
    #-- END method get_relation_select() --#


    def get_relation_selection_property( self, name_IN, default_IN = None ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        prop_dict = None
        
        # get output spec
        prop_dict = self.get_relation_select()
        
        # retrieve the output_type value.
        value_OUT = prop_dict.get( name_IN, default_IN )
        
        return value_OUT
    
    #-- END method get_relation_selection_property() --#


    def load_network_data_request_json( self, json_IN ):
        
        '''
        Accepts JSON string - stores it, parses it, then passes it on to method
            for initializing this instance using the parsed JSON dictionary.
        '''
        
        # return reference
        status_OUT = None
        
        # declare variables
        me = "load_network_data_request_json"
        status_message = None
        status_code = None
        result_status = None
        result_status_is_error = None
        
        # declare variables - output information
        output_spec_dict = None
        relation_select_dict = None
        entity_select_dict = None

        # init status container
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )

        # make sure we have a JSON instance
        if ( json_IN is not None ):
        
            # try to retrieve output information
            output_spec_dict = json_IN.get( self.PROP_NAME_OUTPUT_SPECIFICATION, None )
            
            # got something?  "output_specification" is required.
            if ( output_spec_dict is not None ):
            
                # got one.  Store the output specification.
                self.set_output_specification( output_spec_dict )
                            
            else:
            
                # ERROR - no output spec passed in.
                status_message = "In {}(): ERROR - no output spec in JSON, so nothing to do.".format( me )
                self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.ERROR )
                status_code = StatusContainer.STATUS_CODE_ERROR
                status_OUT.set_status_code( status_code )
                status_OUT.add_message( status_message )
                
                # and set is_request_ok to False.
                self.set_is_request_ok( False )
                
            #-- END check to see if output spec --#
            
            # retrieve and store relation_select
            relation_select_dict = json_IN.get( self.PROP_NAME_RELATION_SELECT, None )
            
            # got something?  "relation_select" is required.
            if ( relation_select_dict is not None ):
            
                # got one.  Store the output specification.
                self.set_relation_select( relation_select_dict )
                            
            else:
            
                # ERROR - no rleation select spec passed in.
                status_message = "In {}(): ERROR - no relation select criteria, so nothing to do.".format( me )
                self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.ERROR )
                status_code = StatusContainer.STATUS_CODE_ERROR
                status_OUT.set_status_code( status_code )
                status_OUT.add_message( status_message )
                
                # and set is_request_ok to False.
                self.set_is_request_ok( False )
                
            #-- END check to see if relation select spec --#
            
            # retrieve and store entity_selection
            entity_select_dict = json_IN.get( self.PROP_NAME_ENTITY_SELECT, None )
            
            # got something?  "entity_select" is required.
            if ( entity_select_dict is not None ):
            
                # got one.  Store the output specification.
                self.set_entity_select( entity_select_dict )
                            
            #-- END check to see if entity select spec --#
        
        else:
        
            # ERROR - no JSON passed in.
            status_message = "In {}(): ERROR - no JSON string passed in, so nothing to do.".format( me )
            self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.ERROR )
            status_code = StatusContainer.STATUS_CODE_ERROR
            status_OUT.set_status_code( status_code )
            status_OUT.add_message( status_message )
        
        #-- END check to see if JSON string passed in --#        
        
        return status_OUT

    #-- END method load_network_data_request_json_string() --#
    

    def load_network_data_request_json_file( self, path_to_json_file_IN ):
        
        '''
        Accepts path to network data request JSON file.  Opens the file, reads
            the JSON into a string, then passes the string on to method for
            loading JSON from string.
            
        Returns StatusContainer. 
        '''
        
        # return reference
        status_OUT = None
        
        # declare variables
        me = "load_network_data_request_json_file"
        status_message = None
        status_code = None
        result_status = None
        result_status_is_error = None
        json_file = None
        json_string = None

        # init status container
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )

        # make sure we have a path
        if ( ( path_to_json_file_IN is not None ) and ( path_to_json_file_IN != "" ) ):
        
            # try to open json file for reading
            with open( path_to_json_file_IN ) as json_file:  
            
                # read the JSON text.
                json_string = json_file.read()
                
            #-- END open of JSON file to read it into memory. --#
            
            # call the method to load from JSON string.
            result_status = self.load_network_data_request_json_string( json_string )
    	                
            # errors?
            result_status_is_error = result_status.is_error()
            if ( result_status_is_error == True ):
            
                # set status to error, add a message, then nest the
                #     StatusContainer instance.
                status_message = "In {}(): ERROR - errors loading JSON from string after reading it from file ( path = {} ).  See nested StatusContainer for more details.".format( me, path_to_json_file_IN )
                self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.ERROR )
                status_code = StatusContainer.STATUS_CODE_ERROR
                status_OUT.set_status_code( status_code )
                status_OUT.add_message( status_message )
                status_OUT.add_status_container( result_status )
            
            #-- END check to see if errors. --#
                    
        else:
        
            # ERROR - no path passed in.  Why bother?
            status_message = "In {}(): ERROR - no file path passed in, so nothing to do.".format( me )
            self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.ERROR )
            status_code = StatusContainer.STATUS_CODE_ERROR
            status_OUT.set_status_code( status_code )
            status_OUT.add_message( status_message )
        
        #-- END check to see if JSON file path passed in --#
        
        return status_OUT

    #-- END method load_network_data_request_json_file() --#
    

    def load_network_data_request_json_string( self, json_string_IN ):
        
        '''
        Accepts JSON string - stores it, parses it, then passes it on to method
            for initializing this instance using the parsed JSON dictionary.
        '''
        
        # return reference
        status_OUT = None
        
        # declare variables
        me = "load_network_data_request_json_string"
        status_message = None
        status_code = None
        result_status = None
        result_status_is_error = None
        json_instance = None

        # init status container
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # make sure we have a JSON string
        if ( ( json_string_IN is not None ) and ( json_string_IN != "" ) ):
        
            # store the raw JSON string.
            self.m_request_json_string = json_string_IN
        
            # try to parse JSON
            try:

                # read the JSON text.
                json_instance = json.loads( json_string_IN )

                # call the method to load from JSON string.
                result_status = self.load_network_data_request_json( json_instance )
                
                # errors?
                result_status_is_error = result_status.is_error()
                if ( result_status_is_error == True ):
                
                    # set status to error, add a message, then nest the
                    #     StatusContainer instance.
                    status_message = "In {}(): ERROR - errors loading JSON from string ( {} ).  See nested StatusContainer for more details.".format( me, json_string_IN )
                    self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.ERROR )
                    status_code = StatusContainer.STATUS_CODE_ERROR
                    status_OUT.set_status_code( status_code )
                    status_OUT.add_message( status_message )
                    status_OUT.add_status_container( result_status )
                
                #-- END check to see if errors. --#
    
            except: # catch *any* exceptions
            
                # get, log, and return exception
                e = sys.exc_info()[0]
                
                # update status
                status_code = StatusContainer.STATUS_CODE_ERROR
                status_message = "In {}(): ERROR - exception caught while parsing JSON string ( {} ).".format( me, json_string_IN )
                status_OUT.set_status_code( status_code )
                status_OUT.add_message( status_message )
                
                # process the exception
                self.process_exception( e, message_IN = status_message, print_details_IN = self.DEBUG_FLAG )
                
                # get the details
                status_message = self.last_exception_details
                status_OUT.add_message( status_message )
                status_OUT.set_detail_value( "exception", e )

            #-- try...except. --#
            
        else:
        
            # ERROR - no string passed in.
            status_message = "In {}(): ERROR - no JSON string passed in, so nothing to do.".format( me )
            self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.ERROR )
            status_code = StatusContainer.STATUS_CODE_ERROR
            status_OUT.set_status_code( status_code )
            status_OUT.add_message( status_message )
        
        #-- END check to see if JSON string passed in --#

        return status_OUT

    #-- END method load_network_data_request_json_string() --#
    

    def set_entity_select( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_entity_selection_dict = value_IN
        
        # return it
        value_OUT = self.get_entity_select()
        
        return value_OUT
    
    #-- END method set_entity_select() --#


    def set_is_request_ok( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        boolean_value = None
        
        if ( value_IN is not None ):
            
            # convert to boolean
            boolean_value = BooleanHelper.convert_value_to_boolean( value_IN )
            
            # store it
            self.m_is_request_ok = boolean_value
            
            # return it
            value_OUT = self.is_request_ok()
            
        #-- END check to see if value is non-empty. --#
        
        return value_OUT
    
    #-- END method set_is_request_ok() --#


    def set_output_file_path( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_output_spec_value( self.PROP_NAME_OUTPUT_FILE_PATH, value_IN )
        
        return value_OUT
    
    #-- END method set_output_file_path() --#


    def set_output_format( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_output_spec_value( self.PROP_NAME_OUTPUT_FORMAT, value_IN )
        
        return value_OUT
    
    #-- END method set_output_format() --#


    def set_output_include_column_headers( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        boolean_value = None
        
        if ( value_IN is not None ):
            
            # convert to boolean
            boolean_value = BooleanHelper.convert_value_to_boolean( value_IN )
            
            # store and return it
            value_OUT = self.set_output_spec_value( self.PROP_NAME_OUTPUT_INCLUDE_COLUMN_HEADERS, boolean_value )
            
        #-- END check to see if value is non-empty. --#
        
        return value_OUT
    
    #-- END method set_output_include_column_headers() --#


    def set_output_specification( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_output_specification = value_IN
        
        # return it
        value_OUT = self.get_output_specification()
        
        return value_OUT
    
    #-- END method set_output_specification() --#


    def set_output_spec_property( self, name_IN, value_IN ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        output_spec = None
        
        # get output spec
        output_spec = self.get_output_specification()

        # store value
        output_spec[ name_IN ] = value_IN
        
        # return it
        value_OUT = self.get_output_spec_property( name_IN )
        
        return value_OUT
    
    #-- END method set_output_spec_value() --#


    def set_output_structure( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_output_spec_value( self.PROP_NAME_OUTPUT_STRUCTURE, value_IN )
        
        return value_OUT
    
    #-- END method set_output_structure() --#


    def set_output_type( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_output_spec_value( self.PROP_NAME_OUTPUT_TYPE, value_IN )
        
        return value_OUT
    
    #-- END method set_output_type() --#


    def set_relation_select( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_relation_selection_dict = value_IN
        
        # return it
        value_OUT = self.get_relation_select()
        
        return value_OUT
    
    #-- END method set_relation_select() --#


#-- END class NetworkDataRequest --#