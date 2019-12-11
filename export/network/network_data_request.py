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

# Import the classes for our context application
from context.models import Entity_Relation

# Import context shared classes.
from context.shared.context_base import ContextBase

# other context export network classes
from context.export.network.filter_spec import FilterSpec


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
    # ! ----> filter types - name prefixes/types and variable name suffixes.
    FILTER_TYPE_RELATION_TYPE_SLUG = "relation_type_slug"
    FILTER_TYPE_RELATION_TRAIT = "relation_trait"
    FILTER_TYPE_ENTITY_TYPE_SLUG = "entity_type_slug"
    FILTER_TYPE_ENTITY_TRAIT = "entity_trait"
    FILTER_TYPE_ENTITY_ID = "entity_id"
    FILTER_TYPE_LIST = []
    FILTER_TYPE_LIST.append( FILTER_TYPE_RELATION_TYPE_SLUG )
    FILTER_TYPE_LIST.append( FILTER_TYPE_RELATION_TRAIT )
    FILTER_TYPE_LIST.append( FILTER_TYPE_ENTITY_TYPE_SLUG )
    FILTER_TYPE_LIST.append( FILTER_TYPE_ENTITY_TRAIT )
    FILTER_TYPE_LIST.append( FILTER_TYPE_ENTITY_ID )
    
    # variable name suffixes
    SUFFIX_FILTER_COMBINE_TYPE = "_filter_combine_type"
    SUFFIX_FILTERS = "_filters"
    
    # map of type to build function name.
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP = {}
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP[ FILTER_TYPE_RELATION_TYPE_SLUG ] = "build_filter_spec_{}_q".format( FILTER_TYPE_RELATION_TYPE_SLUG )
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP[ FILTER_TYPE_RELATION_TRAIT ] = "build_filter_spec_{}_q".format( FILTER_TYPE_RELATION_TRAIT )
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP[ FILTER_TYPE_ENTITY_TYPE_SLUG ] = "build_filter_spec_{}_q".format( FILTER_TYPE_ENTITY_TYPE_SLUG )
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP[ FILTER_TYPE_ENTITY_TRAIT ] = "build_filter_spec_{}_q".format( FILTER_TYPE_ENTITY_TRAIT )
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP[ FILTER_TYPE_ENTITY_ID ] = "build_filter_spec_{}_q".format( FILTER_TYPE_ENTITY_ID )
    
    #--------------------------------------------------------------------------#
    # ! ----> filter spec - comparison types
    RECURSIVE_COMPARISON_TYPE_LIST = []
    RECURSIVE_COMPARISON_TYPE_LIST.append( FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND )
    RECURSIVE_COMPARISON_TYPE_LIST.append( FilterSpec.PROP_VALUE_COMPARISON_TYPE_OR )
    
    
    #--------------------------------------------------------------------------#
    # ! ----> filter criteria - relations
    PROP_NAME_RELATION_TYPE_SLUG_FILTER_COMBINE_TYPE = "{}{}".format( FILTER_TYPE_RELATION_TYPE_SLUG, SUFFIX_FILTER_COMBINE_TYPE )
    PROP_NAME_RELATION_TYPE_SLUG_FILTERS = "{}{}".format( FILTER_TYPE_RELATION_TYPE_SLUG, SUFFIX_FILTERS )
    PROP_NAME_RELATION_TRAIT_FILTER_COMBINE_TYPE = "{}{}".format( FILTER_TYPE_RELATION_TRAIT, SUFFIX_FILTER_COMBINE_TYPE )
    PROP_NAME_RELATION_TRAIT_FILTERS = "{}{}".format( FILTER_TYPE_RELATION_TRAIT, SUFFIX_FILTERS )
    
    #--------------------------------------------------------------------------#
    # ! ----> filter criteria - entities
    PROP_NAME_ENTITY_TYPE_SLUG_FILTER_COMBINE_TYPE = "{}{}".format( FILTER_TYPE_ENTITY_TYPE_SLUG, SUFFIX_FILTER_COMBINE_TYPE )
    PROP_NAME_ENTITY_TYPE_SLUG_FILTERS = "{}{}".format( FILTER_TYPE_ENTITY_TYPE_SLUG, SUFFIX_FILTERS )
    PROP_NAME_ENTITY_TRAIT_FILTER_COMBINE_TYPE = "{}{}".format( FILTER_TYPE_ENTITY_TRAIT, SUFFIX_FILTER_COMBINE_TYPE )
    PROP_NAME_ENTITY_TRAIT_FILTERS = "{}{}".format( FILTER_TYPE_ENTITY_TRAIT, SUFFIX_FILTERS )
    PROP_NAME_ENTITY_ID_FILTER_COMBINE_TYPE = "{}{}".format( FILTER_TYPE_ENTITY_ID, SUFFIX_FILTER_COMBINE_TYPE )
    PROP_NAME_ENTITY_ID_FILTERS = "{}{}".format( FILTER_TYPE_ENTITY_ID, SUFFIX_FILTERS )
    
    #--------------------------------------------------------------------------#
    # !----> filter criteria - shared
    
    # reserved trait values
    VALUE_EMPTY = ContextBase.STRING_EMPTY
        
    #--------------------------------------------------------------------------#
    # ! ----> filter criteria - traits
    
    # trait_filter_combine_type values
    PROP_VALUE_TRAIT_FILTER_COMBINE_TYPE_AND = ContextBase.STRING_AND
    PROP_VALUE_TRAIT_FILTER_COMBINE_TYPE_OR = ContextBase.STRING_OR
    PROP_VALUE_TRAIT_FILTER_COMBINE_TYPE_DEFAULT = PROP_VALUE_TRAIT_FILTER_COMBINE_TYPE_AND
    TRAIT_FILTER_COMBINE_TYPE_VALUES = FilterSpec.FILTER_COMBINE_TYPE_VALUES

    # reserved trait values
    TRAIT_VALUE_EMPTY = ContextBase.STRING_EMPTY

    #--------------------------------------------------------------------------#
    # ! ----> filter criteria - entity identifiers

    # id_filter_combine_type values
    PROP_VALUE_ID_FILTER_COMBINE_TYPE_AND = ContextBase.STRING_AND
    PROP_VALUE_ID_FILTER_COMBINE_TYPE_OR = ContextBase.STRING_OR
    PROP_VALUE_ID_FILTER_COMBINE_TYPE_DEFAULT = PROP_VALUE_ID_FILTER_COMBINE_TYPE_AND
    ID_FILTER_COMBINE_TYPE_VALUES = FilterSpec.FILTER_COMBINE_TYPE_VALUES


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


    def build_filter_spec_aggregate_q( self, filter_spec_IN = None, filter_type_IN = None ):
        
        # return reference
        q_OUT = None
        
        # declare variables
        me = "build_filter_spec_aggregate_q"
        debug_flag = False
        status_message = None
        filter_spec_list = None
        filter_combine_type = None
        filter_q_list = None
        filter_spec_dict = None
        filter_spec = None
        filter_q = None
        collected_q = None
        filter_q_count = None
        filter_q_counter = None
        
        # init debug_flag
        debug_flag = self.DEBUG_FLAG
        
        # make sure we have filter spec
        if ( filter_spec_IN is not None ):
        
            # filter spec list OK?
            filter_spec_list = filter_spec_IN.get_value_list()
            if ( ( filter_spec_list is not None ) and ( len( filter_spec_list ) > 0 ) ):
            
                # make sure we have a type
                filter_combine_type = filter_spec_IN.get_comparison_type()
                if ( ( filter_combine_type is None ) or ( filter_combine_type != "" ) ):
                
                    # use default.
                    filter_combine_type = FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_DEFAULT
                    
                #-- END check to see if combine type passed in. --#
                    
                # make sure combine type is valid.
                if ( filter_combine_type in FilterSpec.FILTER_COMBINE_TYPE_VALUES ):
                                
                    # loop over filters, build a Q() list.
                    filter_q_list = []
                    for filter_spec_dict in filter_spec_list:
                    
                        # load into FilterSpec instance.
                        filter_spec = FilterSpec()
                        filter_spec.set_filter_spec( filter_spec_dict )
                        
                        # call the method to create a Q() filter based on type.
                        filter_q = self.build_filter_spec_q( filter_spec_IN = filter_spec,
                                                             filter_type_IN = filter_type_IN )
                        
                        # add to list?
                        if ( filter_q is not None ):
                        
                            # add to list.
                            filter_q_list.append( filter_q )
                            
                        #-- END check to see if anything returned --#
                        
                    #-- END loop over filter specs. --#
                    
                    # now, based on the combine type, combine Qs and filter QuerySet
                    #     with the result.
                    collected_q = None
                    
                    # how many Qs?
                    filter_q_count = len( filter_q_list )
                    if ( filter_q_count == 1 ):
    
                        # just one thing.  Get it, store it in collected_q.
                        collected_q = filter_q_list[ 0 ]
                        
                    elif ( filter_q_count > 1 ):
                    
                        # loop over list
                        filter_q_counter = 0
                        for filter_q in filter_q_list:
                        
                            # increment counter
                            filter_q_counter += 1
                            
                            # what position in list?
                            if ( filter_q_counter == 1 ):
                            
                                # first - seed collected_q with first thing.
                                collected_q = filter_q
                                
                            else:
                            
                                # second+ - combine based on combine type.                        
                                if ( filter_combine_type == FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_AND ):
                                
                                    # AND ( "&" ) the current Q to the collected.
                                    collected_q = collected_q & filter_q
                                
                                elif ( filter_combine_type == FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_OR ):
                                
                                    # OR ( "|" ) the Qs together.
                                    collected_q = collected_q | filter_q
                
                                else:
                                
                                    # ERROR - valid but unknown combine type...
                                    status_message = "In {}(): ERROR (and strange) - valid but unknown combine type {}, nothing to do.  Valid types: {}".format( me, filter_combine_type, FilterSpec.FILTER_COMBINE_TYPE_VALUES )
                                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                                    
                                #-- END check of combine type. --#
                                
                            #-- END check of index of current filter --#
                        
                        #-- END loop over filter Qs --#
                        
                    elif ( filter_q_count == 0 ):
                    
                        # WARNING - no Qs.
                        status_message = "In {}(): WARNING - No Qs resulted from processing.  filters: {}".format( me, selection_filters )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.WARNING )
                    
                    else:
                    
                        # ERROR - unexpected value.
                        status_message = "In {}(): ERROR - filter count not 0, 1, or > 1. filters: {}".format( me, selection_filters )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                    
                    #-- END check of count of filter Qs. --#
                                    
                else:
                
                    # ERROR - unknown combine type.
                    status_message = "In {}(): ERROR - unknown combine type {}, nothing to do.  Valid types: {}".format( me, filter_combine_type, FilterSpec.FILTER_COMBINE_TYPE_VALUES )
                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                    
                #-- END check to make sure combine type is known and valid --#    
                    
            else:
            
                # ERROR - no filter list passed in.
                status_message = "In {}(): ERROR - no filter list passed in ( {} ), nothing to do.".format( me, filter_spec_list )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                
            #-- END check to make sure combine type is known and valid --#
            
        else:
        
            # ERROR - no filter spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in ( {} ), nothing to do.".format( me, filter_spec_IN )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
        #-- END check to make sure combine type is known and valid --#
        
        # set return reference.
        q_OUT = collected_q

        return q_OUT

    #-- END method build_filter_spec_aggregate_q() --#
                    

    def build_filter_spec_entity_id_q( self, filter_spec_IN, filter_type_IN ):
        
        # return reference
        q_OUT = None
        
        # declare variables
        me = "build_filter_spec_entity_id_q"
        debug_flag = None
        status_message = None
        filter_spec = None
        filter_comparison_type = None
        filter_name = None
        filter_type_id = None
        filter_type_label = None
        filter_data_type = None
        filter_value = None
        filter_value_list = None
        filter_value_from = None
        filter_value_to = None
        filter_relation_roles_list = None
        is_ok = None
        entity_qs = None
        current_q = None
        
        # init
        is_ok = True
        debug_flag = self.DEBUG_FLAG
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # retrieve comparison type
            filter_comparison_type = filter_spec.get_comparison_type()
            
            # valid type?
            if ( filter_comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - recursive or not?
                if ( filter_comparison_type in recursive_comparison_type_list ):
                
                    # call method to build aggregate Q from filter spec.
                    q_OUT = self.build_filter_spec_aggregate_q( filter_spec_IN = filter_spec,
                                                                filter_type_IN = filter_type_IN )
                    
                else:
                
                    # not recursive, retrieve values
                    filter_name = filter_spec.get_name()  # name of identifier
                    filter_type_id = filter_spec.get_type_id()
                    filter_type_label = filter_spec.get_type_label()
                    filter_data_type = filter_spec.get_data_type()
                    filter_value = filter_spec.get_value()
                    filter_value_list = filter_spec.get_value_list()
                    filter_value_from = filter_spec.get_value_from()
                    filter_value_to = filter_spec.get_value_to()
                    filter_relation_roles_list = filter_spec.get_relation_roles_list()
                    
                    # ! ----> check for required fields

                    # name
                    if ( ( filter_name is None ) or ( filter_name == "" ) ):
                    
                        # filter name is required.  not OK.
                        is_ok = False
                        
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - name is required type \"{}\", is missing from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                    
                    #-- END check to see if name set. --#
                    
                    # OK to proceed?
                    if ( is_ok == True ):
                    
                        # first, use filter values to match entity or entities.
                        entity_qs = Entity.objects.all()
                        
                        # filter on requested identifier name...
                        entity_qs = entity_qs.filter( entity_identifier__name = filter_name )
                    
                        # ! ----> comparison type will tell us what to do.
                        if ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS ):
                        
                            # ...and ID equal to "value".
                            entity_qs = entity_qs.filter( entity_identifier__uuid = filter_value )
                        
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES ):
                        
                            # ...and ID among values in "value_list"
                            entity_qs = entity_qs.filter( entity_identifier__uuid__in = filter_value_list )
                        
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_EXCLUDES ):
                        
                            # ...and ID NOT among values in "value_list"
                            entity_qs = entity_qs.exclude( entity_identifier__uuid__in = filter_value_list )
                                                
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_IN_RANGE ):
                        
                            # ERROR - invalid comparison type for this filter type.
                            status_message = "In {}(): ERROR - comparison type {} is not valid for filter type {} ( from filter spec: {} _.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            is_ok = False
                                                    
                        else:
                        
                            # ERROR - unknown comparison type.
                            status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            is_ok = False
                        
                        #-- END check to see what comparison type. --#
                        
                        # everything still OK?
                        if ( is_ok == True ):
                        
                            # ! ----> call method to then apply this to requested roles.
                            q_OUT = self.build_filter_spec_entity_q_target_roles( entity_qs, filter_relation_roles_list )
                            
                        #-- END check to see if everything OK after finding matching entities --#
                        
                    else:
                    
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - required elements of filter spec missing for this type: {}, from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                    
                    #-- END check to see if OK --#
                    
                #-- END check to see if recursive type, or atomic. --#
                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )

        #-- END check to make sure spec passed in. --#
        
        return q_OUT
        
    #-- END method build_filter_spec_entity_id_q() --#


    def build_filter_spec_entity_q_target_roles( self, entity_qs_IN, filter_relation_roles_list_IN, q_IN = None ):

        '''
        Accepts entity QuerySet and list of roles whose entities should be
            filtered to match the contents of the entity QuerySet.  Returns Q()
            instance that filters appropriately.
        '''

        # return reference
        q_OUT = None
        
        # declare variables
        me = "build_filter_spec_entity_q_target_roles"
        debug_flag = None
        status_message = None
        filter_relation_roles_list = None
        entity_qs = None
        current_q = None
        
        # init
        is_ok = True
        
        # init q_OUT
        if ( q_IN is not None ):
        
            # use the Q() passed in.
            q_OUT = q_IN
        
        #-- END check to see if Q() passed in.
        
        # got roles list?
        if ( ( filter_relation_roles_list_IN is not None ) and ( len( filter_relation_roles_list_IN > 0 ) ) ):
        
            # got a QuerySet?
            if ( entity_qs_IN is not None ):

                # yes - set up variables
                filter_relation_roles_list = filter_relation_roles_list_IN
                entity_qs = entity_qs_IN
                
                # ! ----> which relation roles?
                
                # ! --------> FROM
                if ( ( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_FROM in filter_relation_roles_list )
                    or ( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL in filter_relation_roles_list ) ):
                    
                    # create Q()
                    current_q = Q( relation_from__in = entity_qs )
                    
                    # is Q() populated?
                    if ( q_OUT is None ):
                    
                        # no - start with this Q().
                        q_OUT = current_q
                    
                    else:
                    
                        # yes - OR new Q() on the end.
                        q_OUT = q_OUT | current_q
                    
                    #-- END check to see if Q() populated --#
                    
                #-- END check to see if FROM included. --#

                # ! --------> TO
                if ( ( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_TO in filter_relation_roles_list )
                    or ( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL in filter_relation_roles_list ) ):
                    
                    # create Q()
                    current_q = Q( relation_to__in = entity_qs )
                    
                    # is Q() populated?
                    if ( q_OUT is None ):
                    
                        # no - start with this Q().
                        q_OUT = current_q
                    
                    else:
                    
                        # yes - OR new Q() on the end.
                        q_OUT = q_OUT | current_q
                    
                    #-- END check to see if Q() populated --#
                    
                #-- END check to see if TO included. --#

                # ! --------> THROUGH
                if ( ( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_THROUGH in filter_relation_roles_list )
                    or ( FilterSpec.PROP_VALUE_RELATION_ROLES_LIST_ALL in filter_relation_roles_list ) ):
                    
                    # create Q()
                    current_q = Q( relation_through__in = entity_qs )
                    
                    # is Q() populated?
                    if ( q_OUT is None ):
                    
                        # no.  Make a Q().
                        q_OUT = current_q
                    
                    else:
                    
                        # yes - this should never happen, but OR it on the end.
                        q_OUT = q_OUT | current_q
                    
                    #-- END check to see if Q() populated --#
                    
                #-- END check to see if THROUGH included. --#
                
            else:
            
                # ERROR - No entity QuerySet passed in
                status_message = "In {}(): ERROR - no Entity QuerySet passed in. Doing nothing.".format( me )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no roles list passed in.
            status_message = "In {}(): ERROR - no roles list passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )

        #-- END check to make sure spec passed in. --#
        
        return q_OUT
        
    #-- END method build_filter_spec_entity_q_target_roles() --#


    def build_filter_spec_entity_trait_q( self, filter_spec_IN, filter_type_IN ):        
        
        # return reference
        q_OUT = None
        
        # declare variables
        me = "build_filter_spec_entity_trait_q"
        debug_flag = None
        status_message = None
        filter_spec = None
        filter_comparison_type = None
        filter_name = None
        filter_type_id = None
        filter_type_label = None
        filter_data_type = None
        filter_value = None
        filter_value_list = None
        filter_value_from = None
        filter_value_to = None
        filter_relation_roles_list = None
        is_ok = None
        entity_qs = None
        current_q = None
        
        # init
        is_ok = True
        debug_flag = self.DEBUG_FLAG
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # retrieve comparison type
            filter_comparison_type = filter_spec.get_comparison_type()
            
            # valid type?
            if ( filter_comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - recursive or not?
                if ( filter_comparison_type in recursive_comparison_type_list ):
                
                    # call method to build aggregate Q from filter spec.
                    q_OUT = self.build_filter_spec_aggregate_q( filter_spec_IN = filter_spec,
                                                                filter_type_IN = filter_type_IN )
                    
                else:
                
                    # not recursive, retrieve values
                    filter_name = filter_spec.get_name()  # name of identifier
                    filter_type_id = filter_spec.get_type_id()
                    filter_type_label = filter_spec.get_type_label()
                    filter_data_type = filter_spec.get_data_type()
                    filter_value = filter_spec.get_value()
                    filter_value_list = filter_spec.get_value_list()
                    filter_value_from = filter_spec.get_value_from()
                    filter_value_to = filter_spec.get_value_to()
                    filter_relation_roles_list = filter_spec.get_relation_roles_list()
                    
                    # ! ----> check for required fields

                    # name
                    if ( ( filter_name is None ) or ( filter_name == "" ) ):
                    
                        # filter name is required.  not OK.
                        is_ok = False
                        
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - name is required type \"{}\", is missing from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                    
                    #-- END check to see if name set. --#
                    
                    # OK to proceed?
                    if ( is_ok == True ):
                    
                        # first, use filter values to match entity or entities.
                        entity_qs = Entity.objects.all()
                        
                        # filter on requested identifier name...
                        entity_qs = entity_qs.filter( entity_trait__name = filter_name )
                    
                        # ! ----> comparison type will tell us what to do.
                        if ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS ):
                        
                            # ...and value equal to "value".
                            entity_qs = entity_qs.filter( entity_trait__value = filter_value )
                        
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES ):
                        
                            # ...and value among values in "value_list"
                            entity_qs = entity_qs.filter( entity_trait__value__in = filter_value_list )
                        
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_EXCLUDES ):
                        
                            # ...and value NOT among values in "value_list"
                            entity_qs = entity_qs.exclude( entity_trait__value__in = filter_value_list )
                                                
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_IN_RANGE ):

                            # ...and value > "value_from" and < "value_to"
                            entity_qs = entity_qs.filter( entity_trait__value__gte = filter_value_from )
                            entity_qs = entity_qs.filter( entity_trait__value__lte = filter_value_to )
                                                    
                        else:
                        
                            # ERROR - unknown comparison type.
                            status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            is_ok = False
                        
                        #-- END check to see what comparison type. --#
                        
                        # everything still OK?
                        if ( is_ok == True ):
                        
                            # ! ----> call method to then apply this to requested roles.
                            q_OUT = self.build_filter_spec_entity_q_target_roles( entity_qs, filter_relation_roles_list )
                                                        
                        #-- END check to see if everything OK after finding matching entities --#
                        
                    else:
                    
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - required elements of filter spec missing for this type: {}, from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                    
                    #-- END check to see if OK --#
                    
                #-- END check to see if recursive type, or atomic. --#
                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )

        #-- END check to make sure spec passed in. --#
        
        return q_OUT
        
    #-- END method build_filter_spec_entity_trait_q() --#


    def build_filter_spec_entity_type_slug_q( self, filter_spec_IN, filter_type_IN ):

        # return reference
        q_OUT = None
        
        # declare variables
        me = "build_filter_spec_entity_type_slug_q"
        debug_flag = None
        status_message = None
        filter_spec = None
        filter_comparison_type = None
        filter_name = None
        filter_type_id = None
        filter_type_label = None
        filter_data_type = None
        filter_value = None
        filter_value_list = None
        filter_value_from = None
        filter_value_to = None
        filter_relation_roles_list = None
        is_ok = None
        entity_qs = None
        current_q = None
        
        # init
        is_ok = True
        debug_flag = self.DEBUG_FLAG
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # retrieve comparison type
            filter_comparison_type = filter_spec.get_comparison_type()
            
            # valid type?
            if ( filter_comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - recursive or not?
                if ( filter_comparison_type in recursive_comparison_type_list ):
                
                    # call method to build aggregate Q from filter spec.
                    q_OUT = self.build_filter_spec_aggregate_q( filter_spec_IN = filter_spec,
                                                                filter_type_IN = filter_type_IN )
                    
                else:
                
                    # not recursive, retrieve values
                    filter_name = filter_spec.get_name()  # name of identifier
                    filter_type_id = filter_spec.get_type_id()
                    filter_type_label = filter_spec.get_type_label()
                    filter_data_type = filter_spec.get_data_type()
                    filter_value = filter_spec.get_value()
                    filter_value_list = filter_spec.get_value_list()
                    filter_value_from = filter_spec.get_value_from()
                    filter_value_to = filter_spec.get_value_to()
                    filter_relation_roles_list = filter_spec.get_relation_roles_list()
                    
                    # ! ----> check for required fields

                    # name
                    if ( ( filter_name is None ) or ( filter_name == "" ) ):
                    
                        # filter name is required.  not OK.
                        is_ok = False
                        
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - name is required type \"{}\", is missing from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                    
                    #-- END check to see if name set. --#
                    
                    # OK to proceed?
                    if ( is_ok == True ):
                    
                        # first, use filter values to match entity or entities.
                        entity_qs = Entity.objects.all()
                        
                        # ! ----> comparison type will tell us what to do.
                        
                        # EQUALS
                        if ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS ):
                        
                            # ...and value equal to "value".
                            entity_qs = entity_qs.filter( entity_types__entity_type__slug = filter_value )
                        
                        # INCLUDES
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES ):
                        
                            # ...and value among values in "value_list"
                            entity_qs = entity_qs.filter( entity_types__entity_type__slug__in = filter_value_list )
                        
                        # EXCLUDES
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_EXCLUDES ):
                        
                            # ...and value NOT among values in "value_list"
                            entity_qs = entity_qs.exclude( entity_types__entity_type__slug__in = filter_value_list )

                        # IN RANGE
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_IN_RANGE ):

                            # ERROR - invalid comparison type for this filter type.
                            status_message = "In {}(): ERROR - comparison type {} is not valid for filter type {} ( from filter spec: {} _.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            is_ok = False
                                                    
                        else:
                        
                            # ERROR - unknown comparison type.
                            status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            is_ok = False
                        
                        #-- END check to see what comparison type. --#
                        
                        # everything still OK?
                        if ( is_ok == True ):
                        
                            # ! ----> call method to then apply this to requested roles.
                            q_OUT = self.build_filter_spec_entity_q_target_roles( entity_qs, filter_relation_roles_list )
                            
                        #-- END check to see if everything OK after finding matching entities --#
                        
                    else:
                    
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - required elements of filter spec missing for this type: {}, from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                    
                    #-- END check to see if OK --#
                    
                #-- END check to see if recursive type, or atomic. --#
                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )

        #-- END check to make sure spec passed in. --#
        
        return q_OUT
        
    #-- END method build_filter_spec_entity_type_slug_q() --#


    def build_filter_spec_q( self, filter_spec_IN, filter_type_IN ):
        
        '''
        Accepts filter spec and filter type, returns a Q that filters
            appropriately to match the filters specified in the spec passed in.
            If the filter type is AND or OR, hands off processing to method
            build_filter_spec_aggregate_q(), which then recursively calls this
            method for each item in the list being ANDed or ORed together.  If
            not an aggregating type, passes processing off to a type-specific
            processing method to be correctly handled for the particular type.
        '''
        
        # return reference
        q_OUT = None
        
        # declare variables
        me = "build_filter_spec_q"
        recursive_comparison_type_list = None
        filter_spec = None
        comparison_type = None
        method_name = None
        method_pointer = None        
        
        # init
        recursive_comparison_type_list = self.RECURSIVE_COMPARISON_TYPE_LIST
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # retrieve comparison type
            comparison_type = filter_spec.get_comparison_type()
            
            # valid type?
            if ( comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - recursive or not?
                if ( comparison_type in recursive_comparison_type_list ):
                
                    # call method to build aggregate Q from filter spec.
                    q_OUT = self.build_filter_spec_aggregate_q( filter_spec_IN = filter_spec,
                                                                filter_type_IN = filter_type_IN )
                    
                else:
                
                    # not recursive - call appropriate method based on filter
                    #     type, then let it implement the different comparisons.
                    
                    # get method name
                    method_name = self.FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP.get( filter_type_IN )
                    
                    # get method pointer
                    method_pointer = getattr( self, method_name )
                    
                    # call method, passing spec.
                    q_OUT = method_pointer( filter_spec )
                
                #-- END check to see what to do based on filter type. --#
                                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )

        #-- END check to make sure spec passed in. --#
        
    #-- END method build_filter_spec_q() --#


    def build_filter_spec_relation_trait_q( self, filter_spec_IN, filter_type_IN ):
        
        # return reference
        q_OUT = None
        
        # declare variables
        me = "build_filter_spec_relation_trait_q"
        debug_flag = None
        status_message = None
        filter_spec = None
        filter_comparison_type = None
        filter_name = None
        filter_type_id = None
        filter_type_label = None
        filter_data_type = None
        filter_value = None
        filter_value_list = None
        filter_value_from = None
        filter_value_to = None
        filter_relation_roles_list = None
        is_ok = None
        current_q = None
        
        # init
        is_ok = True
        debug_flag = self.DEBUG_FLAG
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # retrieve comparison type
            filter_comparison_type = filter_spec.get_comparison_type()
            
            # valid type?
            if ( filter_comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - recursive or not?
                if ( filter_comparison_type in recursive_comparison_type_list ):
                
                    # call method to build aggregate Q from filter spec.
                    q_OUT = self.build_filter_spec_aggregate_q( filter_spec_IN = filter_spec,
                                                                filter_type_IN = filter_type_IN )
                    
                else:
                
                    # not recursive, retrieve values
                    filter_name = filter_spec.get_name()  # name of identifier
                    filter_type_id = filter_spec.get_type_id()
                    filter_type_label = filter_spec.get_type_label()
                    filter_data_type = filter_spec.get_data_type()
                    filter_value = filter_spec.get_value()
                    filter_value_list = filter_spec.get_value_list()
                    filter_value_from = filter_spec.get_value_from()
                    filter_value_to = filter_spec.get_value_to()
                    filter_relation_roles_list = filter_spec.get_relation_roles_list()
                    
                    # ! ----> check for required fields

                    # name
                    if ( ( filter_name is None ) or ( filter_name == "" ) ):
                    
                        # filter name is required.  not OK.
                        is_ok = False
                        
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - name is required type \"{}\", is missing from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                    
                    #-- END check to see if name set. --#
                    
                    # OK to proceed?
                    if ( is_ok == True ):
                    
                        # filter on requested trait name...
                        current_q = Q( entity_relation_trait__name = filter_name )
                    
                        # ! ----> comparison type will tell us what to do.
                        if ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS ):
                        
                            # ...and value equal to "value".
                            current_q = current_q & Q( entity_relation_trait__value = filter_value )
                        
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES ):
                        
                            # ...and value among values in "value_list"
                            current_q = current_q & Q( entity_relation_trait__value__in = filter_value_list )
                        
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_EXCLUDES ):
                        
                            # ...and value NOT among values in "value_list"
                            current_q = current_q & ( ~ Q( entity_relation_trait__value__in = filter_value_list ) )
                                                
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_IN_RANGE ):

                            # ...and value > "value_from" and < "value_to"
                            current_q = current_q & Q( entity_relation_trait__value__gte = filter_value_from )
                            current_q = current_q & Q( entity_relation_trait__value__lte = filter_value_to )
                                                    
                        else:
                        
                            # ERROR - unknown comparison type.
                            status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            is_ok = False
                        
                        #-- END check to see what comparison type. --#
                        
                        # everything still OK?
                        if ( is_ok == True ):
                        
                            # OK!  Return current_q.
                            q_OUT = current_q
                                                        
                        #-- END check to see if everything OK after finding matching entities --#
                        
                    else:
                    
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - required elements of filter spec missing for this type: {}, from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                    
                    #-- END check to see if OK --#
                    
                #-- END check to see if recursive type, or atomic. --#
                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )

        #-- END check to make sure spec passed in. --#
        
        return q_OUT
        
    #-- END method build_filter_spec_relation_trait_q() --#


    def build_filter_spec_relation_type_slug_q( self, filter_spec_IN, filter_type_IN ):
        
        # return reference
        q_OUT = None
        
        # declare variables
        me = "build_filter_spec_relation_type_slug_q"
        debug_flag = None
        status_message = None
        filter_spec = None
        filter_comparison_type = None
        filter_name = None
        filter_type_id = None
        filter_type_label = None
        filter_data_type = None
        filter_value = None
        filter_value_list = None
        filter_value_from = None
        filter_value_to = None
        filter_relation_roles_list = None
        is_ok = None
        current_q = None
        
        # init
        is_ok = True
        debug_flag = self.DEBUG_FLAG
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # retrieve comparison type
            filter_comparison_type = filter_spec.get_comparison_type()
            
            # valid type?
            if ( filter_comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - recursive or not?
                if ( filter_comparison_type in recursive_comparison_type_list ):
                
                    # call method to build aggregate Q from filter spec.
                    q_OUT = self.build_filter_spec_aggregate_q( filter_spec_IN = filter_spec,
                                                                filter_type_IN = filter_type_IN )
                    
                else:
                
                    # not recursive, retrieve values
                    filter_name = filter_spec.get_name()  # name of identifier
                    filter_type_id = filter_spec.get_type_id()
                    filter_type_label = filter_spec.get_type_label()
                    filter_data_type = filter_spec.get_data_type()
                    filter_value = filter_spec.get_value()
                    filter_value_list = filter_spec.get_value_list()
                    filter_value_from = filter_spec.get_value_from()
                    filter_value_to = filter_spec.get_value_to()
                    filter_relation_roles_list = filter_spec.get_relation_roles_list()
                    
                    # ! ----> check for required fields

                    # name
                    if ( ( filter_name is None ) or ( filter_name == "" ) ):
                    
                        # filter name is required.  not OK.
                        is_ok = False
                        
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - name is required type \"{}\", is missing from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                    
                    #-- END check to see if name set. --#
                    
                    # OK to proceed?
                    if ( is_ok == True ):
                    
                        # ! ----> comparison type will tell us what to do.
                        if ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_EQUALS ):
                        
                            # ...and value equal to "value".
                            current_q = Q( relation_type__slug = filter_value )
                        
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_INCLUDES ):
                        
                            # ...and value among values in "value_list"
                            current_q = Q( relation_type__slug__in = filter_value_list )
                        
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_EXCLUDES ):
                        
                            # ...and value NOT among values in "value_list"
                            current_q = ~ Q( relation_type__slug__in = filter_value_list )
                                                
                        elif ( filter_comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_IN_RANGE ):

                            # ERROR - invalid comparison type for this filter type.
                            status_message = "In {}(): ERROR - comparison type {} is not valid for filter type {} ( from filter spec: {} ).  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            is_ok = False
                                                    
                        else:
                        
                            # ERROR - unknown comparison type.
                            status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            is_ok = False
                        
                        #-- END check to see what comparison type. --#
                        
                        # everything still OK?
                        if ( is_ok == True ):
                        
                            # OK!  Return current_q.
                            q_OUT = current_q
                                                        
                        #-- END check to see if everything OK after finding matching entities --#
                        
                    else:
                    
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - required elements of filter spec missing for this type: {}, from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                    
                    #-- END check to see if OK --#
                    
                #-- END check to see if recursive type, or atomic. --#
                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )

        #-- END check to make sure spec passed in. --#
        
        return q_OUT
        
    #-- END method build_filter_spec_relation_type_slug_q() --#


    def filter_relation_query_set( self, qs_IN = None, use_entity_selection_IN = False ):
        
        '''
        Uses nested selection filters to it to build up an Entity_Relation
            QuerySet that filters as requested.
        '''

        # return reference
        qs_OUT = None

        # declare variables
        me = "filter_relation_query_set"
        debug_flag = None
        my_logger = None
        selection_filters = None
        filter_type_list = None
        filter_type = None
        
        # initialize.
        debug_flag = self.DEBUG_FLAG

        # get selection_filters
        slection_filters = self.get_selection_filters( use_entity_selection_IN )
        
        # got filters?
        if ( selection_filters is not None ):
        
            # set up QuerySet - QuerySet passed in?
            if ( qs_IN is not None ):
            
                # use QuerySet passed in.
                qs_OUT = qs_IN
                
            else:
            
                # start with all relations.
                qs_OUT = Entity_Relation.objects.all()
                
            #-- END initialize QuerySet --#
        
            # ! ----> process the different types of filters.

            # loop over filter types.
            filter_type_list = self.FILTER_TYPE_LIST
            for filter_type in filter_type_list:
            
                # call filter_relations() with the selected filters and
                #     current filter type.
                qs_OUT = self.filter_relations( qs_IN = qs_OUT,
                                                selection_filters_IN = selection_filters,
                                                filter_type_IN = filter_type )
            
            #-- END loop over filter types. --#
            
        else:

            # ERROR - no selection filters, can't process.
            status_message = "In {}(): ERROR - no selection filters found in NetworkDataRequest, so nothing to do.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
        
        #-- END check to see if we have selection filters --#

        return qs_OUT

    #-- end method filter_relation_query_set() ---------------------------#


    def filter_relations( self, qs_IN = None, selection_filters_IN = None, filter_type_IN = None ):
        
        '''
        Uses nested selection filters to it to build up an Entity_Relation
            QuerySet that filters as requested.

        Accepts QuerySet, filters JSON, and filter type.  Uses the type to
            retrieve combine type and filter specs, then bundles them together
            into a FilterSpec instance of type AND or OR to match the combine
            type and hands off the actual filtering to
            build_filter_spec_aggregate_q().  Takes the resulting Q() instance
            and uses it to filter the QuerySet passed in (or created from
            scratch, if none passed in).
        '''

        # return reference
        qs_OUT = None

        # declare variables
        me = "filter_relations"
        debug_flag = None
        my_logger = None
        is_filter_type_valid = None
        selection_filters = None
        filter_combine_type_property_name = None
        filter_combine_type = None
        filter_spec_list_property_name = None
        filter_spec_list = None
        filter_spec = None
        result_q = None
        
        # initialize.
        debug_flag = self.DEBUG_FLAG
        qs_OUT = qs_IN
        selection_filters = selection_filters_IN
        
        # got filters?
        if ( selection_filters is not None ):
        
            # valid filter type?
            if ( ( filter_type_IN is not None ) and ( filter_type_IN in self.FILTER_TYPE_LIST ) ):
            
                # valid filter type - set up QuerySet - QuerySet passed in?
                if ( qs_IN is not None ):
                
                    # use QuerySet passed in.
                    qs_OUT = qs_IN
                    
                else:
                
                    # start with all relations.
                    qs_OUT = Entity_Relation.objects.all()
                    
                #-- END initialize QuerySet --#
            
                # get combine type...
                filter_combine_type_property_name = "{}{}".format( filter_type_IN, self.SUFFIX_FILTER_COMBINE_TYPE )
                filter_combine_type = selection_filters.get( filter_combine_type_property_name, FilterSpec.PROP_VALUE_FILTER_COMBINE_TYPE_DEFAULT )
    
                # ...and filter specs based on type.
                filter_spec_list_property_name = "{}{}".format( filter_type_IN, self.SUFFIX_FILTERS )
                filter_spec_list = selection_filters.get( filter_spec_list_property_name )
                
                # make sure combine type is valid.
                if ( filter_combine_type in FilterSpec.FILTER_COMBINE_TYPE_VALUES ):
                
                    # create filter_spec for list, with comparison type =
                    #     combine type.
                    filter_spec = FilterSpec()
                    filter_spec.set_comparison_type( filter_combine_type )
                    filter_spec.set_value_list( filter_spec_list )
                    filter_spec.set_data_type( FilterSpec.PROP_VALUE_DATA_TYPE_FILTER )
                    
                    # call method build_filter_spec_q()
                    result_q = self.build_filter_spec_q( filter_spec_IN = filter_spec,
                                                         filter_type_IN = filter_type_IN )
                
                    # if result_q is not None, filter.
                    if ( result_q is not None ):
                    
                        # got something.  Filter and return.
                        qs_OUT = qs_OUT.filter( result_q )
                    
                    #-- END check to see if result_q has anything in it. --#
                
                else:
                
                    # ERROR - unknown combine type.
                    status_message = "In {}(): ERROR - unknown combine type {}, nothing to do.  Valid types: {}".format( me, filter_combine_type, FilterSpec.FILTER_COMBINE_TYPE_VALUES )
                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                    
                #-- END check to make sure combine type is known and valid --#            
                
            else:
    
                # ERROR - invalid filter type.
                status_message = "In {}(): ERROR - unknown filter type {}, nothing to do.  Valid types: {}".format( me, filter_type_IN, self.FILTER_TYPE_LIST )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
            #-- END check to see if we have selection filters --#
    
        else:

            # ERROR - no selection filters, can't process.
            status_message = "In {}(): ERROR - no selection filters passed in, so nothing to do.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
        
        #-- END check to see if we have selection filters --#

        return qs_OUT

    #-- end method filter_relations() ---------------------------#


    def get_entity_selection( self ):
        
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
            self.set_entity_selection( prop_dict )
            
            # return it.
            value_OUT = self.get_entity_selection()
            
        else:
        
            # found something.  Return it.
            value_OUT = prop_dict
            
        #-- END see if initialized --#
        
        return value_OUT
    
    #-- END method get_entity_selection() --#


    def get_entity_selection_property( self, name_IN, default_IN = None ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        prop_dict = None
        
        # get output spec
        prop_dict = self.get_entity_selection()
        
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


    def get_relation_selection( self ):
        
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
            self.set_relation_selection( prop_dict )
            
            # return it.
            value_OUT = self.get_relation_selection()
            
        else:
        
            # found something.  Return it.
            value_OUT = prop_dict
            
        #-- END see if initialized --#
        
        return value_OUT
    
    #-- END method get_relation_selection() --#


    def get_relation_selection_property( self, name_IN, default_IN = None ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        prop_dict = None
        
        # get output spec
        prop_dict = self.get_relation_selection()
        
        # retrieve the output_type value.
        value_OUT = prop_dict.get( name_IN, default_IN )
        
        return value_OUT
    
    #-- END method get_relation_selection_property() --#


    def get_selection_filters( self, use_entity_selection_IN = False ):
        
        '''
        Uses nested selection filters to it to build up an Entity_Relation
            QuerySet that filters as requested.
        '''

        # return reference
        filters_OUT = None

        # declare variables
        me = "get_selection_filters"
        debug_flag = None
        status_message = None
        selection_filters = None
        
        # initialize.
        debug_flag = self.DEBUG_FLAG
        
        # which selection criteria do we use?
        if ( use_entity_selection_IN == True ):

            status_message = "In {}(): use_entity_selection_IN is True".format( me )
            self.output_message( status_message, do_print_IN = True, log_level_code_IN = logging.DEBUG )
                
            # try to retrieve entity selection.
            selection_filters = self.get_entity_selection()
            
            # got something?
            if ( ( selection_filters is None ) or ( len( selection_filters ) == 0 ) ):
            
                # no.  Output info message, default to relation_selection.
                status_message = "In {}(): \"entity_selection\" filtering was requested, but not specified in the request.  Defaulting to \"relation_selection\".".format( me )
                self.output_message( status_message, do_print_IN = True, log_level_code_IN = logging.INFO )
                selection_filters = self.get_relation_selection()
                
            #-- END check to see if "entity_selection" is missing --#
            
        else:
        
            status_message = "In {}(): use_entity_selection_IN is False".format( me )
            self.output_message( status_message, do_print_IN = True, log_level_code_IN = logging.DEBUG )
                
            # use relation_selection.
            selection_filters = self.get_relation_selection()
            
        #-- END check to ee if we use "entity_selection" --#
        
        filters_OUT = selection_filters
        
        return filters_OUT

    #-- end method get_selection_filters() ---------------------------#


    def is_request_ok( self ):
        
        # return reference
        value_OUT = None
        
        value_OUT = self.m_is_request_ok
        
        return value_OUT
    
    #-- END method is_request_ok() --#


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
                self.set_relation_selection( relation_select_dict )
                            
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
                self.set_entity_selection( entity_select_dict )
                            
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
    
    
    def set_entity_selection( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_entity_selection_dict = value_IN
        
        # return it
        value_OUT = self.get_entity_selection()
        
        return value_OUT
    
    #-- END method set_entity_selection() --#


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
        value_OUT = self.set_output_spec_property( self.PROP_NAME_OUTPUT_FILE_PATH, value_IN )
        
        return value_OUT
    
    #-- END method set_output_file_path() --#


    def set_output_format( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_output_spec_property( self.PROP_NAME_OUTPUT_FORMAT, value_IN )
        
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
            value_OUT = self.set_output_spec_property( self.PROP_NAME_OUTPUT_INCLUDE_COLUMN_HEADERS, boolean_value )
            
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
    
    #-- END method set_output_spec_property() --#


    def set_output_structure( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_output_spec_property( self.PROP_NAME_OUTPUT_STRUCTURE, value_IN )
        
        return value_OUT
    
    #-- END method set_output_structure() --#


    def set_output_type( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_output_spec_property( self.PROP_NAME_OUTPUT_TYPE, value_IN )
        
        return value_OUT
    
    #-- END method set_output_type() --#


    def set_relation_selection( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_relation_selection_dict = value_IN
        
        # return it
        value_OUT = self.get_relation_selection()
        
        return value_OUT
    
    #-- END method set_relation_selection() --#


#-- END class NetworkDataRequest --#