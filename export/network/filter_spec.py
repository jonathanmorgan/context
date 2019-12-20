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
from python_utilities.json.json_helper import JSONHelper
from python_utilities.parameters.param_container import ParamContainer
from python_utilities.status.status_container import StatusContainer

# Import context shared classes.
from context.shared.context_base import ContextBase


#===============================================================================
# ! > classes (in alphabetical order by name)
#===============================================================================

class FilterSpec( ContextBase ):


    #---------------------------------------------------------------------------
    # ! ==> CONSTANTS-ish
    #---------------------------------------------------------------------------


    # LOGGING
    DEBUG_FLAG = True
    LOGGER_NAME = "context.export.network.filter_spec.FilterSpec"
    ME = LOGGER_NAME

    #--------------------------------------------------------------------------#
    # !----> filter spec
    
    # value comparison
    PROP_NAME_NAME = "name"
    PROP_NAME_TYPE_ID = "type_id"
    PROP_NAME_TYPE_LABEL = "type_label"
    PROP_NAME_DATA_TYPE = "data_type"
    PROP_NAME_COMPARISON_TYPE = "comparison_type"
    PROP_NAME_FILTER_TYPE = "filter_type"
    PROP_NAME_VALUE = "value"
    PROP_NAME_VALUE_LIST = "value_list"
    PROP_NAME_VALUE_FROM = "value_from"
    PROP_NAME_VALUE_TO = "value_to"
    PROP_NAME_RELATION_ROLES_LIST = "relation_roles_list"

    # reserved trait values
    VALUE_EMPTY = ContextBase.STRING_EMPTY
    
    # data_type values
    PROP_VALUE_DATA_TYPE_STRING = ContextBase.DATA_TYPE_STRING
    PROP_VALUE_DATA_TYPE_INT = ContextBase.DATA_TYPE_INT
    PROP_VALUE_DATA_TYPE_DATE = ContextBase.DATA_TYPE_DATE
    PROP_VALUE_DATA_TYPE_DATETIME = ContextBase.DATA_TYPE_DATETIME
    PROP_VALUE_DATA_TYPE_FILTER = ContextBase.DATA_TYPE_FILTER
    PROP_VALUE_DATA_TYPE_DEFAULT = PROP_VALUE_DATA_TYPE_STRING
    DATA_TYPE_VALUES = ContextBase.DATA_TYPE_VALUES

    # trait_comparison_type values
    PROP_VALUE_COMPARISON_TYPE_EQUALS = ContextBase.COMPARISON_TYPE_EQUALS
    PROP_VALUE_COMPARISON_TYPE_INCLUDES = ContextBase.COMPARISON_TYPE_INCLUDES
    PROP_VALUE_COMPARISON_TYPE_EXCLUDES = ContextBase.COMPARISON_TYPE_EXCLUDES
    PROP_VALUE_COMPARISON_TYPE_IN_RANGE = ContextBase.COMPARISON_TYPE_IN_RANGE
    PROP_VALUE_COMPARISON_TYPE_AND = ContextBase.COMPARISON_TYPE_AND
    PROP_VALUE_COMPARISON_TYPE_AND_FILTER = ContextBase.COMPARISON_TYPE_AND_FILTER
    PROP_VALUE_COMPARISON_TYPE_AND_AMPERSAND = ContextBase.COMPARISON_TYPE_AND_AMPERSAND
    PROP_VALUE_COMPARISON_TYPE_OR = ContextBase.COMPARISON_TYPE_OR
    PROP_VALUE_COMPARISON_TYPE_DEFAULT = PROP_VALUE_COMPARISON_TYPE_INCLUDES
    COMPARISON_TYPE_VALUES = ContextBase.COMPARISON_TYPE_VALUES
    
    # relation_roles_list values
    PROP_VALUE_RELATION_ROLES_LIST_FROM = ContextBase.RELATION_ROLES_FROM
    PROP_VALUE_RELATION_ROLES_LIST_TO = ContextBase.RELATION_ROLES_TO
    PROP_VALUE_RELATION_ROLES_LIST_THROUGH = ContextBase.RELATION_ROLES_THROUGH
    PROP_VALUE_RELATION_ROLES_LIST_ALL = ContextBase.RELATION_ROLES_ALL
    PROP_VALUE_RELATION_ROLES_LIST_DEFAULT = PROP_VALUE_RELATION_ROLES_LIST_ALL
    RELATION_ROLES_LIST_VALUES = ContextBase.RELATION_ROLES_VALUES

    # reserved trait values
    TRAIT_VALUE_EMPTY = ContextBase.STRING_EMPTY
    
    # ! ----> JSON output defaults
    JSON_OUTPUT_DEFAULT_DO_SORT_KEYS = True
    JSON_OUTPUT_DEFAULT_INDENT_SIZE = 4
    JSON_OUTPUT_DEFAULT_SEPARATORS = ( ',', ': ' )


    #---------------------------------------------------------------------------
    # ! ==> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self ):

        # call parent's __init__()
        super( FilterSpec, self ).__init__()

        # declare variables - moved to parent
        #self.request = None
        #self.parameters = ParamContainer()

        # define parameters - moved to parent
        #self.define_parameters( NetworkOutput.PARAM_NAME_TO_TYPE_MAP )
        
        # store raw JSON string, if JSON
        self.m_json_string = None
        
        # and store parsed JSON
        self.m_json = None
        
        # store children converted to FilterSpecs, if present.
        self.m_child_filter_spec_list = []
        
        # store self converted to Q() instance (if not an aggregate).
        self.m_my_q = None
                        
        # set logger name (for LoggingHelper parent class: (LoggingHelper --> BasicRateLimited --> ContextTextBase --> ArticleCoding).
        self.set_logger_name( self.LOGGER_NAME )
        
    #-- END method __init__() --#


    #---------------------------------------------------------------------------
    # ! ==> instance methods
    #---------------------------------------------------------------------------


    def add_to_child_filter_spec_list( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        filter_spec_list = None
        
        # get list
        filter_spec_list = self.get_child_filter_spec_list()

        # append value
        filter_spec_list.append( value_IN )
        
        # return it
        value_OUT = value_IN
        
        return value_OUT
    
    #-- END method add_to_child_filter_spec_list() --#


    def get_child_filter_spec_list( self ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        filter_spec_list = None
        
        # see if already stored.
        filter_spec_list = self.m_child_filter_spec_list
        
        # anything stored?
        if ( filter_spec_list is None ):
        
            # no.  Create list, store it, and return it.
            filter_spec_list = []
            
            # store it.
            self.set_child_filter_spec_list( filter_spec_list )
            
            # return it.
            value_OUT = self.get_child_filter_spec_list()
            
        else:
        
            # found something.  Return it.
            value_OUT = filter_spec_list
            
        #-- END see if initialized --#
        
        return value_OUT
    
    #-- END method get_child_filter_spec_list() --#


    def get_comparison_type( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_filter_spec_property( self.PROP_NAME_COMPARISON_TYPE )
        
        return value_OUT
    
    #-- END method get_comparison_type() --#


    def get_data_type( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_filter_spec_property( self.PROP_NAME_DATA_TYPE )
        
        return value_OUT
    
    #-- END method get_data_type() --#


    def get_filter_spec( self ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        prop_dict = None
        
        # see if already stored.
        prop_dict = self.m_json
        
        # anything stored?
        if ( prop_dict is None ):
        
            # no.  Create a dictionary, store it, and return it.
            prop_dict = {}
            
            # store it.
            self.set_filter_spec( prop_dict )
            
            # return it.
            value_OUT = self.get_filter_spec()
            
        else:
        
            # found something.  Return it.
            value_OUT = prop_dict
            
        #-- END see if initialized --#
        
        return value_OUT
    
    #-- END method get_filter_spec() --#


    def get_filter_spec_property( self, name_IN, default_IN = None ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        prop_dict = None
        
        # get output spec
        prop_dict = self.get_filter_spec()
        
        # retrieve the output_type value.
        value_OUT = prop_dict.get( name_IN, default_IN )
        
        return value_OUT
    
    #-- END method get_filter_spec_property() --#


    def get_filter_type( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_filter_spec_property( self.PROP_NAME_FILTER_TYPE )
        
        return value_OUT
    
    #-- END method get_filter_type() --#


    def get_my_q( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the value.
        value_OUT = self.m_my_q
        
        return value_OUT
        
    #-- END method get_my_q() --#


    def get_name( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_filter_spec_property( self.PROP_NAME_NAME )
        
        return value_OUT
    
    #-- END method get_name() --#


    def get_relation_roles_list( self ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        temp_list = None
        
        # retrieve the output_type value.
        value_OUT = self.get_filter_spec_property( self.PROP_NAME_RELATION_ROLES_LIST )
        
        # check if empty.  If so, set it to default (all).
        if ( ( value_OUT is None ) or ( value_OUT == "" ) or ( len( value_OUT ) == 0 ) ):
        
            # not set, or empty.  Set to default.
            temp_list = []
            temp_list.append( self.PROP_VALUE_RELATION_ROLES_LIST_DEFAULT )
            
            # store it.
            self.set_relation_roles_list( temp_list )

            # retrieve and return it.
            value_OUT = self.get_relation_roles_list()
        
        #-- END check if empty. --#

        return value_OUT
    
    #-- END method get_relation_roles_list() --#


    def get_type_id( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_filter_spec_property( self.PROP_NAME_TYPE_ID )
        
        return value_OUT
    
    #-- END method get_type_id() --#


    def get_type_label( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_filter_spec_property( self.PROP_NAME_TYPE_LABEL )
        
        return value_OUT
    
    #-- END method get_type_label() --#


    def get_value( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_filter_spec_property( self.PROP_NAME_VALUE )
        
        return value_OUT
    
    #-- END method get_value() --#


    def get_value_from( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_filter_spec_property( self.PROP_NAME_VALUE_FROM )
        
        return value_OUT
    
    #-- END method get_value_from() --#


    def get_value_list( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_filter_spec_property( self.PROP_NAME_VALUE_LIST )
        
        return value_OUT
    
    #-- END method get_value_list() --#


    def get_value_to( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_type value.
        value_OUT = self.get_filter_spec_property( self.PROP_NAME_VALUE_TO )
        
        return value_OUT
    
    #-- END method get_value_to() --#


    def output_filter_spec_as_json_string( self,
                                           sort_keys_IN = JSON_OUTPUT_DEFAULT_DO_SORT_KEYS,
                                           indent_IN = JSON_OUTPUT_DEFAULT_INDENT_SIZE,
                                           separators_IN = JSON_OUTPUT_DEFAULT_SEPARATORS ):
    
        # return reference
        value_OUT = None
        
        # declare variable
        filter_spec_dict = None
        
        # get filter spec dictionary
        filter_spec_dict = self.get_filter_spec()
        
        # use JSONHelper to render.
        value_OUT = JSONHelper.pretty_print_json( filter_spec_dict,
                                                  sort_keys_IN = sort_keys_IN,
                                                  indent_IN = indent_IN,
                                                  separators_IN = separators_IN )
        
        return value_OUT
        
    #-- END method output_filter_spec_as_json_string() --#


    def set_child_filter_spec_list( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_child_filter_spec_list = value_IN
        
        # return it
        value_OUT = self.get_child_filter_spec_list()
        
        return value_OUT
    
    #-- END method set_child_filter_spec_list() --#


    def set_comparison_type( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_filter_spec_property( self.PROP_NAME_COMPARISON_TYPE, value_IN )
        
        return value_OUT
    
    #-- END method set_comparison_type() --#


    def set_data_type( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_filter_spec_property( self.PROP_NAME_DATA_TYPE, value_IN )
        
        return value_OUT
    
    #-- END method set_data_type() --#


    def set_filter_spec( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_json = value_IN
        
        # return it
        value_OUT = self.get_filter_spec()
        
        return value_OUT
    
    #-- END method set_filter_spec() --#


    def set_filter_spec_property( self, name_IN, value_IN ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        output_spec = None
        
        # get output spec
        output_spec = self.get_filter_spec()

        # store value
        output_spec[ name_IN ] = value_IN
        
        # return it
        value_OUT = self.get_filter_spec_property( name_IN )
        
        return value_OUT
    
    #-- END method set_filter_spec_property() --#


    def set_filter_type( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_filter_spec_property( self.PROP_NAME_FILTER_TYPE, value_IN )
        
        return value_OUT
    
    #-- END method set_filter_type() --#


    def set_my_q( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_my_q = value_IN
        
        # return it
        value_OUT = self.get_my_q()
        
        return value_OUT
        
    #-- END method set_my_q() --#


    def set_name( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_filter_spec_property( self.PROP_NAME_NAME, value_IN )
        
        return value_OUT
    
    #-- END method set_name() --#


    def set_relation_roles_list( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_filter_spec_property( self.PROP_NAME_RELATION_ROLES_LIST, value_IN )
        
        return value_OUT
    
    #-- END method set_relation_roles_list() --#


    def set_type_id( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_filter_spec_property( self.PROP_NAME_TYPE_ID, value_IN )
        
        return value_OUT
    
    #-- END method set_type_id() --#


    def set_type_label( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_filter_spec_property( self.PROP_NAME_TYPE_LABEL, value_IN )
        
        return value_OUT
    
    #-- END method set_type_label() --#


    def set_value( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_filter_spec_property( self.PROP_NAME_VALUE, value_IN )
        
        return value_OUT
    
    #-- END method set_value() --#


    def set_value_from( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_filter_spec_property( self.PROP_NAME_VALUE_FROM, value_IN )
        
        return value_OUT
    
    #-- END method set_value_from() --#


    def set_value_list( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_filter_spec_property( self.PROP_NAME_VALUE_LIST, value_IN )
        
        return value_OUT
    
    #-- END method set_value_list() --#


    def set_value_to( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_filter_spec_property( self.PROP_NAME_VALUE_TO, value_IN )
        
        return value_OUT
    
    #-- END method set_value_to() --#


    def to_json_string( self,
                        sort_keys_IN = JSON_OUTPUT_DEFAULT_DO_SORT_KEYS,
                        indent_IN = JSON_OUTPUT_DEFAULT_INDENT_SIZE,
                        separators_IN = JSON_OUTPUT_DEFAULT_SEPARATORS ):
    
        # return reference
        value_OUT = None
        
        # call output method.
        value_OUT = self.output_filter_spec_as_json_string( sort_keys_IN = sort_keys_IN,
                                                            indent_IN = indent_IN,
                                                            separators_IN = separators_IN )
        
        return value_OUT
        
    #-- END method to_json_string() --#


#-- END class FilterSpec --#