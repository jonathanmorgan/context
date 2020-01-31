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
import six
import sys

# django database classes
from django.db.models import Q

# python_utilities
from python_utilities.booleans.boolean_helper import BooleanHelper
from python_utilities.parameters.param_container import ParamContainer
from python_utilities.status.status_container import StatusContainer

# Import the classes for our context application
from context.models import Entity
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
    DEBUG_FLAG = False
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
    PROP_NAME_OUTPUT_ENTITY_TRAITS_LIST = "output_entity_traits_list"
    PROP_NAME_OUTPUT_ENTITY_IDENTIFIERS_LIST = "output_entity_identifiers_list"    
    
    # entity identifier dictionary property names
    PROP_NAME_ENTITY_IDENTIFIERS_NAME = "name"
    PROP_NAME_ENTITY_IDENTIFIERS_ID_TYPE = "id_type"
    PROP_NAME_ENTITY_IDENTIFIERS_SOURCE = "source"
    PROP_NAME_ENTITY_IDENTIFIERS_SOURCE_IN_LIST = "source_in_list"
    PROP_NAME_ENTITY_IDENTIFIERS_IDENTIFIER_TYPE_ID = "identifier_type_id"
    PROP_NAME_ENTITY_IDENTIFIERS_OUTPUT_HEADER = "output_header"
    
    # entity trait dictionary property names
    PROP_NAME_ENTITY_TRAITS_NAME = "name"
    PROP_NAME_ENTITY_TRAITS_SLUG = "slug"
    PROP_NAME_ENTITY_TRAITS_ENTITY_TYPE_TRAIT_ID = "entity_type_trait_id"
    PROP_NAME_ENTITY_TRAITS_OUTPUT_HEADER = "output_header"
    
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
    
    # configuration for Trait and Identifier output.
    OUTPUT_ENTITY_LABEL_SEPARATOR = "_"
    OUTPUT_ENTITY_IDENTIFIERS_LABEL_PREFIX = "id{}".format( OUTPUT_ENTITY_LABEL_SEPARATOR )
    OUTPUT_ENTITY_TRAITS_LABEL_PREFIX = "trait{}".format( OUTPUT_ENTITY_LABEL_SEPARATOR )
    
    #--------------------------------------------------------------------------#
    # ! ----> filter types - name prefixes/types and variable name suffixes.
    FILTER_TYPE_RELATION_TYPE_SLUG = "relation_type_slug"
    FILTER_TYPE_RELATION_TRAIT = "relation_trait"
    FILTER_TYPE_ENTITY_TYPE_SLUG = "entity_type_slug"
    FILTER_TYPE_ENTITY_TRAIT = "entity_trait"
    FILTER_TYPE_ENTITY_ID = "entity_id"
    FILTER_TYPE_AND = ContextBase.STRING_AND
    FILTER_TYPE_OR = ContextBase.STRING_OR
    FILTER_TYPE_LIST = []
    FILTER_TYPE_LIST.append( FILTER_TYPE_RELATION_TYPE_SLUG )
    FILTER_TYPE_LIST.append( FILTER_TYPE_RELATION_TRAIT )
    FILTER_TYPE_LIST.append( FILTER_TYPE_ENTITY_TYPE_SLUG )
    FILTER_TYPE_LIST.append( FILTER_TYPE_ENTITY_TRAIT )
    FILTER_TYPE_LIST.append( FILTER_TYPE_ENTITY_ID )
    FILTER_TYPE_LIST.append( FILTER_TYPE_AND )
    FILTER_TYPE_LIST.append( FILTER_TYPE_OR )
    
    # map of type to build function name.
    BUILD_FUNCTION_NAME_PREFIX = "build_filter_spec_"
    BUILD_FUNCTION_NAME_SUFFIX = "_q"
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP = {}
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP[ FILTER_TYPE_RELATION_TYPE_SLUG ] = "{}{}{}".format( BUILD_FUNCTION_NAME_PREFIX, FILTER_TYPE_RELATION_TYPE_SLUG, BUILD_FUNCTION_NAME_SUFFIX )
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP[ FILTER_TYPE_RELATION_TRAIT ] = "{}{}{}".format( BUILD_FUNCTION_NAME_PREFIX, FILTER_TYPE_RELATION_TRAIT, BUILD_FUNCTION_NAME_SUFFIX )
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP[ FILTER_TYPE_ENTITY_TYPE_SLUG ] = "{}{}{}".format( BUILD_FUNCTION_NAME_PREFIX, FILTER_TYPE_ENTITY_TYPE_SLUG, BUILD_FUNCTION_NAME_SUFFIX )
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP[ FILTER_TYPE_ENTITY_TRAIT ] = "{}{}{}".format( BUILD_FUNCTION_NAME_PREFIX, FILTER_TYPE_ENTITY_TRAIT, BUILD_FUNCTION_NAME_SUFFIX )
    FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP[ FILTER_TYPE_ENTITY_ID ] = "{}{}{}".format( BUILD_FUNCTION_NAME_PREFIX, FILTER_TYPE_ENTITY_ID, BUILD_FUNCTION_NAME_SUFFIX )
    
    #--------------------------------------------------------------------------#
    # ! ----> filter spec - comparison types
    AGGREGATE_COMPARISON_TYPE_LIST = []
    AGGREGATE_COMPARISON_TYPE_LIST.append( FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND )
    AGGREGATE_COMPARISON_TYPE_LIST.append( FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND_FILTER )
    AGGREGATE_COMPARISON_TYPE_LIST.append( FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND_AMPERSAND )
    AGGREGATE_COMPARISON_TYPE_LIST.append( FilterSpec.PROP_VALUE_COMPARISON_TYPE_OR )
    
    
    #--------------------------------------------------------------------------#
    # ! ----> filter spec - property that holds spec
    PROP_NAME_FILTER_SPECIFICATION = "filter_specification"
    
    #--------------------------------------------------------------------------#
    # !----> filter criteria - shared
    
    # reserved trait values
    VALUE_EMPTY = ContextBase.STRING_EMPTY
        
    #--------------------------------------------------------------------------#
    # ! ----> filter criteria - traits
    
    # reserved trait values
    TRAIT_VALUE_EMPTY = ContextBase.STRING_EMPTY


    #-----------------------------------------------------------------------------
    # ! ==> class methods
    #-----------------------------------------------------------------------------


    @classmethod
    def compact_entity_relation_queryset( cls, qs_IN ):
    
        '''
        Accepts Emtity_Relation QuerySet.  Retrieves list of the IDs of the
            matching records, then creates a new QuerySet with IDs in the list
            of IDs from the QuerySet passed in.  Returns the new QuerySet.
        '''
        
        # return reference
        qs_OUT = None

        # declare variables
        me = "compact_entity_relation_queryset"
        debug_flag = None
        debug_flag_include_id_list = None
        status_message = None
        just_id_qs = None
        id_set = None
        id_list = None
        
        # init
        #debug_flag = cls.DEBUG_FLAG
        debug_flag = True
        debug_flag_include_id_list = False
        
        # make sure we have a QuerySet passed in.
        if ( qs_IN is not None ):
        
            # something passed in.  Try to get list of IDs.
            just_id_qs = qs_IN.values_list( 'id', flat = True )
            id_set = set( just_id_qs )
            id_list = list( id_set )
            
            # now, make a new QuerySet filtered for id in id_list
            qs_OUT = Entity_Relation.objects.all()
            qs_OUT = qs_OUT.filter( id__in = id_list )
            
            if ( debug_flag == True ):
            
                status_message = "\n\n**** Compacted Entity_Relation QuerySet."
                cls.output_debug( status_message, method_IN = me, do_print_IN = debug_flag )
                status_message = "\n\n- Query:\n{}".format( qs_IN.query )
                cls.output_debug( status_message, method_IN = me, do_print_IN = debug_flag )
                status_message = "\n\n- ID list count: {}".format( len( id_list ) )
                cls.output_debug( status_message, method_IN = me, do_print_IN = debug_flag )
                
                if ( debug_flag_include_id_list == True ):
                    status_message = "\n\n- ID list:\n{}".format( id_list )
                    cls.output_debug( status_message, method_IN = me, do_print_IN = debug_flag )
                #-- END check to see if include ID list --#
                
            #-- END DEBUG

        #-- END check to see if QuerySet passed in --#
        
        return qs_OUT
        
    #-- END class method compact_entity_relation_queryset() --#

        
    @classmethod
    def create_entity_id_header_label( cls,
                                       id_info_dict_IN,
                                       prefix_IN = OUTPUT_ENTITY_IDENTIFIERS_LABEL_PREFIX,
                                       separator_IN = OUTPUT_ENTITY_LABEL_SEPARATOR ):

        '''
        Assumes there is an output format property specified in the request
            stored in this instance.  Retrieves this output type, creates a
            NetworkDataOutput implementer instance to match the type, then
            returns the instance.  If no type or unknown type, returns None.
        '''
        
        # return reference
        value_OUT = None

        # declare variables
        me = "create_entity_id_header_label"
        id_info_dict = None
        id_name = None
        id_id_type = None
        id_source = None
        id_identifier_type_id = None
        id_header = None
        
        # for an info dictionary?
        id_info_dict = id_info_dict_IN
        if ( id_info_dict is not None ):

            # get values from the dict
            id_name = id_info_dict.get( cls.PROP_NAME_ENTITY_IDENTIFIERS_NAME, None )
            id_id_type = id_info_dict.get( cls.PROP_NAME_ENTITY_IDENTIFIERS_ID_TYPE, None )
            id_source = id_info_dict.get( cls.PROP_NAME_ENTITY_IDENTIFIERS_SOURCE, None )
            id_identifier_type_id = id_info_dict.get( cls.PROP_NAME_ENTITY_IDENTIFIERS_IDENTIFIER_TYPE_ID, None )
            id_header = id_info_dict.get( cls.PROP_NAME_ENTITY_IDENTIFIERS_OUTPUT_HEADER, None )
            
            # first, do we have a header?
            if ( ( id_header is not None ) and ( id_header != "" ) ):
            
                # yes.  Use it.
                value_OUT = id_header
                
            else:
            
                if ( ( id_name is not None ) and ( id_name != "" ) ):
                
                    # start with mandatory name.
                    value_OUT = id_name
                
                    # got an id type?
                    if ( ( id_id_type is not None ) and ( id_id_type != "" ) ):
                    
                        # yes.  Append
                        value_OUT = "{}{}{}".format( value_OUT, separator_IN, id_id_type )
                        
                    #-- END check to see if id_type --#
                        
                    # got a source?
                    if ( ( id_source is not None ) and ( id_source != "" ) ):
                    
                        # yes.  Append
                        value_OUT = "{}{}{}".format( value_OUT, separator_IN, id_source )
                        
                    #-- END check to see if id_source --#
                    
                else:
                
                    # no name.
                    value_OUT = None
                    
                #-- END check to see if name. --#
                
            #-- END check to see if pre-built header --#
                
        else:
        
            # no info dictionary passed in.  Nothing to see here.
            value_OUT = None
            
        #-- END check to make sure info passed in. --#
        
        # got a value?
        if ( ( value_OUT is not None ) and ( value_OUT != "" ) ):
        
            # prepend prefix if one set.
            if ( ( prefix_IN is not None ) and ( prefix_IN != "" ) ):
            
                # prepend prefix
                value_OUT = "{}{}".format( prefix_IN, value_OUT )
                
            #-- END check to see if prefix set. --#
            
        #-- END check to see if value set. --#

        return value_OUT

    #-- END create_entity_id_header_label() --#


    @classmethod
    def create_entity_trait_header_label( cls, trait_info_dict_IN, prefix_IN = OUTPUT_ENTITY_TRAITS_LABEL_PREFIX ):

        '''
        Assumes there is an output format property specified in the request
            stored in this instance.  Retrieves this output type, creates a
            NetworkDataOutput implementer instance to match the type, then
            returns the instance.  If no type or unknown type, returns None.
        '''
        
        # return reference
        value_OUT = None

        # declare variables
        me = "create_entity_trait_header_label"
        trait_info_dict = None
        trait_name = None
        trait_slug = None
        trait_entity_type_trait_id = None
        trait_header = None
        
        # for an info dictionary?
        trait_info_dict = trait_info_dict_IN
        if ( trait_info_dict is not None ):

            # get values from the dict
            trait_name = trait_info_dict.get( cls.PROP_NAME_ENTITY_TRAITS_NAME, None )
            trait_slug = trait_info_dict.get( cls.PROP_NAME_ENTITY_TRAITS_SLUG, None )
            trait_entity_type_trait_id = trait_info_dict.get( cls.PROP_NAME_ENTITY_TRAITS_ENTITY_TYPE_TRAIT_ID, None )
            trait_header = trait_info_dict.get( cls.PROP_NAME_ENTITY_TRAITS_OUTPUT_HEADER, None )
            
            # first, do we have a header?
            if ( ( trait_header is not None ) and ( trait_header != "" ) ):
            
                # yes.  Use it.
                value_OUT = trait_header
                
            else:
            
                if ( ( trait_name is not None ) and ( trait_name != "" ) ):
                
                    # start with mandatory name.
                    value_OUT = trait_name
                    
                    # got a slug?
                    if ( ( trait_slug is not None ) and ( trait_slug != "" ) ):
                    
                        # yes.  Append
                        value_OUT = "{}_{}".format( value_OUT, trait_slug )
                        
                    #-- END check to see if slug --#
                    
                else:
                
                    # no name.
                    value_OUT = None
                    
                #-- END check to see if name. --#
                
            #-- END check to see if pre-built header --#
                
        else:
        
            # no info dictionary passed in.  Nothing to see here.
            value_OUT = None
            
        #-- END check to make sure info passed in. --#

        # got a value?
        if ( ( value_OUT is not None ) and ( value_OUT != "" ) ):
        
            # prepend prefix if one set.
            if ( ( prefix_IN is not None ) and ( prefix_IN != "" ) ):
            
                # prepend prefix
                value_OUT = "{}{}".format( prefix_IN, value_OUT )
                
            #-- END check to see if prefix set. --#
            
        #-- END check to see if value set. --#

        return value_OUT

    #-- END create_entity_trait_header_label() --#


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
                
        # entity relation query set, for populating network ties.
        self.m_relation_query_set = None
        
        # entity dictionary and trait map
        self.m_entity_id_to_instance_map = {}
        self.m_entity_id_to_traits_map = {}
        self.m_entity_ids_and_traits_header_list = None
        self.m_entity_id_list = None
        
        # set logger name (for LoggingHelper parent class: (LoggingHelper --> BasicRateLimited --> ContextTextBase --> ArticleCoding).
        self.set_logger_name( self.LOGGER_NAME )
        
        # status
        self.m_is_request_ok = True
        
    #-- END method __init__() --#


    #---------------------------------------------------------------------------
    # ! ==> instance methods
    #---------------------------------------------------------------------------


    def add_entities_to_dict( self, relation_qs_IN, dictionary_IN, include_through_IN = False, store_entity_IN = False ):

        """
            Accepts a dictionary, a list of Entity_Relation instances, and flags
                that indicate if we want THROUGH in addition to FROM and TO; and
                if Entity model instances should be stored in the dictionary.
                Adds the entities from the FROM and TO of the relations in the Entity_Relation query set passed in to the
                dictionary, making the Entity ID the key and either None or the
                Entity instance the value, depending on the value in the
                store_entity_IN flag.  If include_through_IN == True, also adds
                Entities stored in relations as THROUGH to the map.

            Preconditions: request must have contained at least a valid filter
                specification, else this will likely be a list of all relations
                (or we won't even get to calling this method).

            Postconditions: uses a lot of memory if you choose a broad set of
                filter criteria. Returns the same dictionary passed in, but with
                the entities in relation_qs_IN added, and optionally adds the
                associated entities, if store_entity_IN == True.

            Parameters:
            - self - self instance variable.
            - relation_qs_IN - django query set object that contains the relations we
                want to add to our dictionary.
            - dictionary_IN - dictionary we want to add people to.  Returned
                with people added.
            - include_through_IN - boolean, defaults to False - If True,
                includes the entity in relation_through in the dictionary along
                with the FROM and TO.  If False, ignores THROUGH.
            - store_entity_IN - boolean, if False, doesn't load Entity model
                instances into dictionary while building the dictionary.  If
                True, loads Entity model instances and stores them in the
                dictionary as the value associated with each Entity's ID.

            Returns:
            - Dictionary - dictionary updated to include all entities from the
                FROM, TO, and optionally THROUGH references in the
                Entity_Relation QuerySet passed in, either mapped to None or to
                Entity model instances, depending on the store_entity_IN
                flag value.
        """

        # return reference
        entity_dict_OUT = {}

        # declare variables
        me = "add_entities_to_dict"
        current_relation = None
        current_entity = None
        current_entity_id = None
        current_value = None

        # set the output dictionary
        if ( dictionary_IN ):

            # yes, store in output parameter
            entity_dict_OUT = dictionary_IN

        #-- END check to see if dictionary passed in --#

        # loop over the articles
        for current_relation in relation_qs_IN:

            # ! ----> FROM

            # add FROM Entity ID to list.  If no Entity ID, don't add.
            current_entity = current_relation.relation_from
            
            # add to dictionary
            entity_dict_OUT = self.add_entity_to_dict( current_entity, entity_dict_OUT, store_entity_IN = store_entity_IN )

            # ! ----> TO

            # add TO Entity ID to list.  If no Entity ID, don't add.
            current_entity = current_relation.relation_to
            
            # add to dictionary
            entity_dict_OUT = self.add_entity_to_dict( current_entity, entity_dict_OUT, store_entity_IN = store_entity_IN )

            # ! ----> THROUGH?

            if ( include_through_IN == True ):

                # add THROUGH Entity ID to list.  If no Entity ID, don't add.
                current_entity = current_relation.relation_through
                
                # add to dictionary
                entity_dict_OUT = self.add_entity_to_dict( current_entity, entity_dict_OUT, store_entity_IN = store_entity_IN )
                
            #-- END check to see if we include THROUGH --#
    
        #-- END loop over Entities --#

        return entity_dict_OUT

    #-- END function add_entities_to_dict() --#


    def add_entity_to_dict( self, entity_IN, dictionary_IN, store_entity_IN = False ):

        """
            Accepts a dictionary, an Entity instance, and a flag that indicates
                if Entity model instances should be stored in the
                dictionary. Retrieves the Entity's ID and if it is not already
                in the dictionary, adds it, making the Entity ID the key and
                either None or the Entity instance the value, depending on the
                value in the store_entity_IN flag.

            Postconditions: Returns the same dictionary passed in, but with
                the Entity passed in added, and optionally adds the associated
                Entity instance, if store_entity_IN == True.

            Parameters:
            - self - self instance variable.
            - entity_IN - django Entity instance to be added to dictionary
                passed in.
            - dictionary_IN - dictionary we want to add entity to.  Returned
                with entity added.
            - store_entity_IN - boolean, defaults to False - if False, doesn't
                load Entity model instances into dictionary while building the
                dictionary.  If True, loads Entity model instances and stores
                them in the dictionary as the value associated with each
                Entity's ID.

            Returns:
            - Dictionary - dictionary updated to include the Entity passed in,
                either mapped to None or to Entity model instances,
                depending on the store_entity_IN flag value.
        """

        # return reference
        entity_dict_OUT = {}

        # declare variables
        me = "add_entity_to_dict"
        current_relation = None
        current_entity = None
        current_entity_id = None
        current_value = None

        # set the output dictionary
        if ( dictionary_IN ):

            # yes, store in output parameter
            entity_dict_OUT = dictionary_IN

        #-- END check to see if dictionary passed in --#

        current_entity = entity_IN

        # see if there is an entity
        if ( current_entity is not None ):

            # are we also loading the Entity?
            current_entity_id = current_entity.id

            if ( store_entity_IN == True ):

                # yes, use Entity model as value.
                current_value = current_entity

            else:

                # no, use None as value.
                current_value = None

            #-- END conditional to check if we are storing actual model instances --#

            # store the Entity in the output dict.
            entity_dict_OUT[ current_entity_id ] = current_value

        #-- END check to see if there is an entity --#

        return entity_dict_OUT

    #-- END function add_entity_to_dict() --#


    def build_filter_spec_aggregate_q( self, filter_spec_IN ):
        
        # return reference
        status_OUT = None

        # declare variables
        me = "build_filter_spec_aggregate_q"
        debug_flag = False
        status_message = None
        status_code = None
        comparison_type = None
        filter_type = None
        filter_spec_dict_list = None
        filter_spec_dict = None
        filter_spec = None
        result_status = None
        result_status_is_error = None
        
        # init
        debug_flag = self.DEBUG_FLAG
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # make sure we have filter spec
        if ( filter_spec_IN is not None ):
        
            # get comparison type, make sure it is aggregate type
            comparison_type = filter_spec_IN.get_comparison_type()
        
            if ( debug_flag == True ):
                status_message = "In {}(): comparison type = {}".format( me, comparison_type )
                self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.DEBUG )
            #-- END DEBUG --#

            # figure out what to do based on type - aggregate (AND or OR)?
            if ( comparison_type not in self.AGGREGATE_COMPARISON_TYPE_LIST ):
            
                # not aggregate type - call standard build method.
                status_OUT = self.build_filter_spec_q( filter_spec_IN )
                
            else:
            
                # comparison type is AND or OR - nested list of filter specs OK?
                filter_spec_dict_list = filter_spec_IN.get_value_list()
                if ( ( filter_spec_dict_list is not None ) and ( len( filter_spec_dict_list ) > 0 ) ):
                                        
                    # loop over filters, build a Q() list.
                    for filter_spec_dict in filter_spec_dict_list:
                    
                        if ( debug_flag == True ):
                            status_message = "In {}(): looping over nested spec JSON, current JSON: {}".format( me, filter_spec_dict )
                            self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.DEBUG )
                        #-- END DEBUG --#
            
                        # load into FilterSpec instance.
                        filter_spec = FilterSpec()
                        filter_spec.set_filter_spec( filter_spec_dict )
                        
                        # add FilterSpec to my list.
                        filter_spec_IN.add_to_child_filter_spec_list( filter_spec )
                        
                        # call the method to create a Q() filter based on type.
                        result_status = self.build_filter_spec_q( filter_spec )

                        # errors?
                        result_status_is_error = result_status.is_error()
                        if ( result_status_is_error == True ):
                        
                            # set status to error, add a message, then nest
                            #     the StatusContainer instance.
                            status_message = "In {}(): ERROR - error returned by build_filter_spec_q() for filter_spec: {}; See nested StatusContainer for more details.".format( me, filter_spec )
                            self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.ERROR )
                            status_code = StatusContainer.STATUS_CODE_ERROR
                            status_OUT.set_status_code( status_code )
                            status_OUT.add_message( status_message )
                            status_OUT.add_status_container( result_status )
                        
                        #-- END check to see if errors. --#

                    #-- END loop over filter specs. --#
                                                            
                else:
                
                    # ERROR - no filter list passed in.
                    status_message = "In {}(): ERROR - no filter list passed in ( {} ), nothing to do.".format( me, filter_spec_list )
                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                    status_code = StatusContainer.STATUS_CODE_ERROR
                    status_OUT.set_status_code( status_code )
                    status_OUT.add_message( status_message )
                    
                #-- END check to make there is a nested list of filters --#
                
            #-- END check to make sure the type is aggregate (AND or OR) --#
            
        else:
        
            # ERROR - no filter spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in ( {} ), nothing to do.".format( me, filter_spec_IN )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            status_code = StatusContainer.STATUS_CODE_ERROR
            status_OUT.set_status_code( status_code )
            status_OUT.add_message( status_message )
            
        #-- END check to make sure combine type is known and valid --#
        
        return status_OUT
        
    #-- END method build_filter_spec_aggregate_q() --#
                    

    def build_filter_spec_entity_id_q( self, filter_spec_IN ):
        
        # return reference
        status_OUT = None
        
        # declare variables
        me = "build_filter_spec_entity_id_q"
        debug_flag = None
        status_message = None
        status_code = None
        status_result = None
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
        my_q = None
        
        # init
        is_ok = True
        debug_flag = self.DEBUG_FLAG
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # retrieve comparison type
            filter_comparison_type = filter_spec.get_comparison_type()
            
            # valid type?
            if ( filter_comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - aggregate or not?
                if ( filter_comparison_type in self.AGGREGATE_COMPARISON_TYPE_LIST ):
                
                    # call method to build aggregate Q from filter spec.
                    status_OUT = self.build_filter_spec_aggregate_q( filter_spec )
                    
                else:
                
                    # not aggregate, retrieve values
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
                        status_code = StatusContainer.STATUS_CODE_ERROR
                        status_OUT.set_status_code( status_code )
                        status_OUT.add_message( status_message )
                    
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
                            status_code = StatusContainer.STATUS_CODE_ERROR
                            status_OUT.set_status_code( status_code )
                            status_OUT.add_message( status_message )
                            is_ok = False
                                                    
                        else:
                        
                            # ERROR - unknown comparison type.
                            status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            status_code = StatusContainer.STATUS_CODE_ERROR
                            status_OUT.set_status_code( status_code )
                            status_OUT.add_message( status_message )
                            is_ok = False
                        
                        #-- END check to see what comparison type. --#
                        
                        # everything still OK?
                        if ( is_ok == True ):
                        
                            # ! ----> call method to then apply this to requested roles.
                            my_q = self.build_filter_spec_entity_q_target_roles( entity_qs, filter_relation_roles_list )
                            
                            # and store in filter_spec.
                            filter_spec.set_my_q( my_q )
                            
                        else:
                        
                            # no need for more error messages - status has been
                            #     set above
                            pass
                        
                        #-- END check to see if everything OK after finding matching entities --#
                        
                    else:
                    
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - required elements of filter spec missing for this type: {}, from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                        status_code = StatusContainer.STATUS_CODE_ERROR
                        status_OUT.set_status_code( status_code )
                        status_OUT.add_message( status_message )
                    
                    #-- END check to see if OK --#
                    
                #-- END check to see if aggregate type, or atomic. --#
                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                status_code = StatusContainer.STATUS_CODE_ERROR
                status_OUT.set_status_code( status_code )
                status_OUT.add_message( status_message )
            
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            status_code = StatusContainer.STATUS_CODE_ERROR
            status_OUT.set_status_code( status_code )
            status_OUT.add_message( status_message )

        #-- END check to make sure spec passed in. --#
        
        return status_OUT
        
    #-- END method build_filter_spec_entity_id_q() --#


    def build_filter_spec_entity_q_target_roles( self, filtered_entity_qs_IN, filter_relation_roles_list_IN, q_IN = None ):

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
        if ( ( filter_relation_roles_list_IN is not None ) and ( len( filter_relation_roles_list_IN ) > 0 ) ):
        
            # got a QuerySet?
            if ( filtered_entity_qs_IN is not None ):

                # yes - set up variables
                filter_relation_roles_list = filter_relation_roles_list_IN
                entity_qs = filtered_entity_qs_IN
                
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


    def build_filter_spec_entity_trait_q( self, filter_spec_IN ):        
        
        # return reference
        status_OUT = None

        # declare variables
        me = "build_filter_spec_entity_trait_q"
        debug_flag = None
        status_message = None
        status_code = None
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
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
         
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # retrieve comparison type
            filter_comparison_type = filter_spec.get_comparison_type()
            
            # valid type?
            if ( filter_comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - aggregate or not?
                if ( filter_comparison_type in self.AGGREGATE_COMPARISON_TYPE_LIST ):
                
                    # call method to build aggregate Q from filter spec.
                    q_OUT = self.build_filter_spec_aggregate_q( filter_spec )
                    
                else:
                
                    # not aggregate, retrieve values
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
                        status_message = "In {}(): ERROR - name is required for type \"{}\", is missing from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                        status_code = StatusContainer.STATUS_CODE_ERROR
                        status_OUT.set_status_code( status_code )
                        status_OUT.add_message( status_message )
                                
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
                            status_code = StatusContainer.STATUS_CODE_ERROR
                            status_OUT.set_status_code( status_code )
                            status_OUT.add_message( status_message )

                            # Not OK.
                            is_ok = False
                        
                        #-- END check to see what comparison type. --#
                        
                        # everything still OK?
                        if ( is_ok == True ):
                        
                            # ! ----> call method to then apply this to requested roles.
                            my_q = self.build_filter_spec_entity_q_target_roles( entity_qs, filter_relation_roles_list )
                            
                            # and store in filter_spec.
                            filter_spec.set_my_q( my_q )                            
                                                        
                        else:
                        
                            # no need for more error messages - status has been
                            #     set above
                            pass
                        
                        #-- END check to see if everything OK after finding matching entities --#
                        
                    else:
                    
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - required elements of filter spec missing for this type: {}, from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                        status_code = StatusContainer.STATUS_CODE_ERROR
                        status_OUT.set_status_code( status_code )
                        status_OUT.add_message( status_message )
                                
                    #-- END check to see if OK --#
                    
                #-- END check to see if aggregate type, or atomic. --#
                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                status_code = StatusContainer.STATUS_CODE_ERROR
                status_OUT.set_status_code( status_code )
                status_OUT.add_message( status_message )
            
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            status_code = StatusContainer.STATUS_CODE_ERROR
            status_OUT.set_status_code( status_code )
            status_OUT.add_message( status_message )

        #-- END check to make sure spec passed in. --#
        
        return status_OUT
        
    #-- END method build_filter_spec_entity_trait_q() --#


    def build_filter_spec_entity_type_slug_q( self, filter_spec_IN ):

        # return reference
        status_OUT = None
        
        # declare variables
        me = "build_filter_spec_entity_type_slug_q"
        debug_flag = None
        status_message = None
        status_code = None
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
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # retrieve comparison type
            filter_comparison_type = filter_spec.get_comparison_type()
            
            # valid type?
            if ( filter_comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - aggregate or not?
                if ( filter_comparison_type in self.AGGREGATE_COMPARISON_TYPE_LIST ):
                
                    # call method to build aggregate Q from filter spec.
                    q_OUT = self.build_filter_spec_aggregate_q( filter_spec )
                    
                else:
                
                    # not aggregate, retrieve values
                    filter_name = filter_spec.get_name()  # name of identifier
                    filter_type_id = filter_spec.get_type_id()
                    filter_type_label = filter_spec.get_type_label()
                    filter_data_type = filter_spec.get_data_type()
                    filter_value = filter_spec.get_value()
                    filter_value_list = filter_spec.get_value_list()
                    filter_value_from = filter_spec.get_value_from()
                    filter_value_to = filter_spec.get_value_to()
                    filter_relation_roles_list = filter_spec.get_relation_roles_list()
                    
                    # ! ----> no required fields

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
                            status_code = StatusContainer.STATUS_CODE_ERROR
                            status_OUT.set_status_code( status_code )
                            status_OUT.add_message( status_message )

                            # Not OK.
                            is_ok = False
                                                    
                        else:
                        
                            # ERROR - unknown comparison type.
                            status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            status_code = StatusContainer.STATUS_CODE_ERROR
                            status_OUT.set_status_code( status_code )
                            status_OUT.add_message( status_message )
                
                            # Not OK.
                            is_ok = False
                        
                        #-- END check to see what comparison type. --#
                        
                        # everything still OK?
                        if ( is_ok == True ):
                        
                            # ! ----> call method to then apply this to requested roles.
                            my_q = self.build_filter_spec_entity_q_target_roles( entity_qs, filter_relation_roles_list )
                            
                            # and store in filter_spec.
                            filter_spec.set_my_q( my_q )
                            
                        else:
                        
                            # no need for more error messages - status has been
                            #     set above
                            pass
                        
                        #-- END check to see if everything OK after finding matching entities --#
                        
                    else:
                    
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - required elements of filter spec missing for this type: {}, from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                        status_code = StatusContainer.STATUS_CODE_ERROR
                        status_OUT.set_status_code( status_code )
                        status_OUT.add_message( status_message )
                    
                    #-- END check to see if OK --#
                    
                #-- END check to see if aggregate type, or atomic. --#
                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                status_code = StatusContainer.STATUS_CODE_ERROR
                status_OUT.set_status_code( status_code )
                status_OUT.add_message( status_message )
            
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            status_code = StatusContainer.STATUS_CODE_ERROR
            status_OUT.set_status_code( status_code )
            status_OUT.add_message( status_message )

        #-- END check to make sure spec passed in. --#
        
        return status_OUT
        
    #-- END method build_filter_spec_entity_type_slug_q() --#


    def build_filter_spec_q( self, filter_spec_IN ):
        
        '''
        Accepts filter spec, either creates a Q that filters
            appropriately to match the filters specified in the spec passed in.
            If the filter type is AND or OR, hands off processing to method
            build_filter_spec_aggregate_q(), which then recursively calls this
            method for each item in the list being ANDed or ORed together.  If
            not an aggregating type, passes processing off to a type-specific
            processing method to be correctly handled for the particular type.
        Postconditions: Stores the resulting Q in the filter spec instance passed
            in, returns a status instance.  If the filter spec passed in is an
            aggregating type (AND, OR, etc.), also creates child filter spec
            instances and and stores Qs in them.
        '''
        
        # return reference
        status_OUT = None
        
        # declare variables
        me = "build_filter_spec_q"
        debug_flag = False
        status_message = None
        status_code = None
        filter_spec = None
        filter_type = None
        comparison_type = None
        method_name = None
        method_pointer = None
        result_status = None
        result_status_is_error = None
        
        # init
        debug_flag = self.DEBUG_FLAG
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN
            
            # clear out any existing child filter specs and my_q.
            filter_spec.set_child_filter_spec_list( [] )
            filter_spec.set_my_q( None )

            # retrieve comparison type
            comparison_type = filter_spec.get_comparison_type()
            
            status_message = "\n\nIn {}(): comparison type = {}\n".format( me, comparison_type )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.DEBUG )

            # valid type?
            if ( comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - aggregate or not?
                if ( comparison_type in self.AGGREGATE_COMPARISON_TYPE_LIST ):
                
                    status_message = "----> In {}(): calling aggregate method.".format( me, comparison_type )
                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.DEBUG )
        
                    # call method to build aggregate Q from filter spec.
                    status_OUT = self.build_filter_spec_aggregate_q( filter_spec )
                    
                else:
                
                    # not aggregate - call appropriate method based on filter
                    #     type, then let it implement the different comparisons.
                    
                    # get filter type
                    filter_type = filter_spec.get_filter_type()
                    
                    # get method name for filter type
                    method_name = self.FILTER_TYPE_TO_BUILD_FUNCTION_NAME_MAP.get( filter_type )
                    
                    if ( debug_flag == True ):
                        print( "----> In {}(): method_name: {}; for filter_type: {}".format( me, method_name, filter_type ) )
                    #-- END DEBUG --#
        
                    # get method pointer
                    method_pointer = getattr( self, method_name )
                    
                    # call method, passing spec.
                    result_status = method_pointer( filter_spec )
                        
                    # errors?
                    result_status_is_error = result_status.is_error()
                    if ( result_status_is_error == True ):
                    
                        # set status to error, add a message, then nest the
                        #     StatusContainer instance.
                        status_message = "In {}(): ERROR - errors creating Q() for filter spec {}; See nested StatusContainer for more details.".format( me, filter_spec )
                        self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.ERROR )
                        status_code = StatusContainer.STATUS_CODE_ERROR
                        status_OUT.set_status_code( status_code )
                        status_OUT.add_message( status_message )
                        status_OUT.add_status_container( result_status )
                    
                    #-- END check to see if errors. --#
                
                #-- END check to see what to do based on filter type. --#
                                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                status_code = StatusContainer.STATUS_CODE_ERROR
                status_OUT.set_status_code( status_code )
                status_OUT.add_message( status_message )
                
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            status_code = StatusContainer.STATUS_CODE_ERROR
            status_OUT.set_status_code( status_code )
            status_OUT.add_message( status_message )

        #-- END check to make sure spec passed in. --#
        
        return status_OUT
        
    #-- END method build_filter_spec_q() --#


    def build_filter_spec_relation_trait_q( self, filter_spec_IN ):
        
        # return reference
        status_OUT = None
        
        # declare variables
        me = "build_filter_spec_relation_trait_q"
        debug_flag = None
        status_message = None
        status_code = None
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
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # retrieve comparison type
            filter_comparison_type = filter_spec.get_comparison_type()
            
            # valid type?
            if ( filter_comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - aggregate or not?
                if ( filter_comparison_type in self.AGGREGATE_COMPARISON_TYPE_LIST ):
                
                    # call method to build aggregate Q from filter spec.
                    status_OUT = self.build_filter_spec_aggregate_q( filter_spec )
                    
                else:
                
                    # not aggregate, retrieve values
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
                        status_code = StatusContainer.STATUS_CODE_ERROR
                        status_OUT.set_status_code( status_code )
                        status_OUT.add_message( status_message )
                    
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
                            status_code = StatusContainer.STATUS_CODE_ERROR
                            status_OUT.set_status_code( status_code )
                            status_OUT.add_message( status_message )
                        
                        #-- END check to see what comparison type. --#
                        
                        # everything still OK?
                        if ( is_ok == True ):
                        
                            # OK!  Store current_q.
                            filter_spec.set_my_q( current_q )
                                                        
                        else:
                        
                            # no need for more error messages - status has been
                            #     set above
                            pass
                        
                        #-- END check to see if everything OK after finding matching entities --#
                        
                    else:
                    
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - required elements of filter spec missing for this type: {}, from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                        status_code = StatusContainer.STATUS_CODE_ERROR
                        status_OUT.set_status_code( status_code )
                        status_OUT.add_message( status_message )

                    #-- END check to see if OK --#
                    
                #-- END check to see if aggregate type, or atomic. --#
                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                status_code = StatusContainer.STATUS_CODE_ERROR
                status_OUT.set_status_code( status_code )
                status_OUT.add_message( status_message )
            
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            status_code = StatusContainer.STATUS_CODE_ERROR
            status_OUT.set_status_code( status_code )
            status_OUT.add_message( status_message )

        #-- END check to make sure spec passed in. --#
        
        return status_OUT
        
    #-- END method build_filter_spec_relation_trait_q() --#


    def build_filter_spec_relation_type_slug_q( self, filter_spec_IN ):
        
        # return reference
        status_OUT = None
        
        # declare variables
        me = "build_filter_spec_relation_type_slug_q"
        debug_flag = None
        status_message = None
        status_code = None
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
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # retrieve comparison type
            filter_comparison_type = filter_spec.get_comparison_type()
            
            # valid type?
            if ( filter_comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - aggregate or not?
                if ( filter_comparison_type in self.AGGREGATE_COMPARISON_TYPE_LIST ):
                
                    # call method to build aggregate Q from filter spec.
                    status_OUT = self.build_filter_spec_aggregate_q( filter_spec )
                    
                else:
                
                    # not aggregate, retrieve values
                    filter_name = filter_spec.get_name()  # name of identifier
                    filter_type_id = filter_spec.get_type_id()
                    filter_type_label = filter_spec.get_type_label()
                    filter_data_type = filter_spec.get_data_type()
                    filter_value = filter_spec.get_value()
                    filter_value_list = filter_spec.get_value_list()
                    filter_value_from = filter_spec.get_value_from()
                    filter_value_to = filter_spec.get_value_to()
                    filter_relation_roles_list = filter_spec.get_relation_roles_list()
                    
                    # ! ----> no non-filter-related required fields

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
                            status_code = StatusContainer.STATUS_CODE_ERROR
                            status_OUT.set_status_code( status_code )
                            status_OUT.add_message( status_message )

                            # Not OK.
                            is_ok = False
                                                    
                        else:
                        
                            # ERROR - unknown comparison type.
                            status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            status_code = StatusContainer.STATUS_CODE_ERROR
                            status_OUT.set_status_code( status_code )
                            status_OUT.add_message( status_message )

                            # Not OK.
                            is_ok = False
                        
                        #-- END check to see what comparison type. --#
                        
                        # everything still OK?
                        if ( is_ok == True ):
                        
                            # OK!  store in filter_spec.
                            filter_spec.set_my_q( current_q )
                                                        
                        else:
                        
                            # no need for more error messages - status has been
                            #     set above
                            pass
                        
                        #-- END check to see if everything OK after finding matching entities --#
                        
                    else:
                    
                        # ERROR - required elements of spec missing.  could not filter.
                        status_message = "In {}(): ERROR - required elements of filter spec missing for this type: {}, from filter spec: {}.  Doing nothing.".format( me, filter_comparison_type, filter_spec )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )                        
                        status_code = StatusContainer.STATUS_CODE_ERROR
                        status_OUT.set_status_code( status_code )
                        status_OUT.add_message( status_message )
                    
                    #-- END check to see if OK --#
                    
                #-- END check to see if aggregate type, or atomic. --#
                
            else:
            
                # ERROR - unknown comparison type.
                status_message = "In {}(): ERROR - unknown valid comparison type: {}, from filter spec: {}.  Doing nothing.  Valid types: {}".format( me, filter_comparison_type, filter_spec, FilterSpec.COMPARISON_TYPE_VALUES )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                status_code = StatusContainer.STATUS_CODE_ERROR
                status_OUT.set_status_code( status_code )
                status_OUT.add_message( status_message )
                
            #-- END check to see if valid comparison type. --#   
            
        else:
        
            # ERROR - no spec passed in.
            status_message = "In {}(): ERROR - no filter spec passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            status_code = StatusContainer.STATUS_CODE_ERROR
            status_OUT.set_status_code( status_code )
            status_OUT.add_message( status_message )

        #-- END check to make sure spec passed in. --#
        
        return status_OUT
        
    #-- END method build_filter_spec_relation_type_slug_q() --#


    def create_entity_ids_and_traits_header_list( self ):
        
        # return reference
        list_OUT = None
        
        # declare variables
        me = "create_entity_ids_and_traits_header_list"
        entity_ids_list = None
        entity_id_dict = None
        entity_traits_list = None
        entity_trait_dict = None
        header_label = None
        
        # init
        list_OUT = []
        
        # retrieve lists
        entity_ids_list = self.get_output_entity_identifiers_list()
        entity_traits_list = self.get_output_entity_traits_list()
        
        # got ids list?
        if ( entity_ids_list is not None ):
        
            # yes - loop, create header label for each, append to list.
            for entity_id_dict in entity_ids_list:
            
                # get header label for id filter
                header_label = self.create_entity_id_header_label( entity_id_dict )
                
                # add to list?
                if ( ( header_label is not None ) and ( header_label != "" ) ):
                
                    # add to list.
                    list_OUT.append( header_label )
                    
                #-- END check to make sure the label contained something --#
                
            #-- END loop over entity ID details dicts --#
                
        #-- END check to see if list present. --#
        
        # got traits list?
        if ( entity_traits_list is not None ):
        
            # yes - loop, create header label for each, append to list.
            for entity_trait_dict in entity_traits_list:
            
                # get header label for id filter
                header_label = self.create_entity_trait_header_label( entity_trait_dict )
                
                # add to list?
                if ( ( header_label is not None ) and ( header_label != "" ) ):
                
                    # add to list.
                    list_OUT.append( header_label )
                    
                #-- END check to make sure the label contained something --#
                
            #-- END loop over entity ID details dicts --#
                            
        #-- END check to see if list present. --#
        
        # store the list, for future reference.
        self.set_entity_ids_and_traits_header_list( list_OUT )
            
        return list_OUT
    
    #-- END method create_entity_ids_and_traits_header_list() --#


    def create_entity_ids_and_traits_value_dict( self, entity_id_list_IN = None ):

        """
            Method: create_entity_ids_and_traits_value_dict()

            Purpose: retrieves list of ids and traits headers, loops and builds
                list of values for each for all entities, then adds them to
                dictionary that maps label to list.

            Returns:
            - dictionary mapping ids and traits labels to value lists for each.
        """

        # return reference
        ids_and_traits_values_dict_OUT = None

        # declare variables
        me = "create_entity_ids_and_traits_value_dict"
        status_message = None
        debug_flag = None
        ids_and_traits_header_labels_list = None
        header_label = None
        value_list = None
        
        # initialize
        debug_flag = self.DEBUG_FLAG
        
        # get list of headers
        ids_and_traits_header_labels_list = self.get_entity_ids_and_traits_header_list()

        # initialize
        ids_and_traits_values_dict_OUT = {}
    
        # loop over role list.
        for header_label in ids_and_traits_header_labels_list:
        
            # get values
            value_list = self.create_entity_ids_and_traits_value_list( header_label, entity_id_list_IN = entity_id_list_IN )
            
            # add to output dictionary
            ids_and_traits_values_dict_OUT[ header_label ] = value_list
            
        #-- END loop over roles --#
            
        return relation_type_role_values_dict_OUT

    #-- END method create_entity_ids_and_traits_value_dict() --#


    def create_entity_ids_and_traits_value_list( self, header_label_IN, entity_id_list_IN = None ):

        """
            Method: create_entity_ids_and_traits_value_list()

            Purpose: accepts an ids and traits header label, creates list of
                values for all entities in master entity list for that
                header label.  If not present for a given entity, sets to None.

            Returns:
            - List of values for id or trait of header_label passed in.
        """

        # return reference
        value_list_OUT = None

        # declare variables
        me = "create_entity_ids_and_traits_value_list"
        debug_flag = None
        status_message = None
        entity_list = None
        entity_to_ids_and_traits_map = None
        entity_id = None
        entity_ids_and_traits = None
        relation_type_roles = None
        current_value = None
        
        # initialization
        debug_flag = self.DEBUG_FLAG
        
        # make sure we have a header label
        if ( ( header_label_IN is not None ) and ( header_label_IN != "" ) ):
        
            # initialize output list
            value_list_OUT = []
    
            # init entity list - list passed in?
            if ( entity_id_list_IN is not None ):
            
                # yes.  Use it.
                entity_list = entity_id_list_IN
                
            else:
            
                # no.  Retrieve from this instance.
                entity_list = self.get_entity_id_list()
            
            #-- END check to see if entity list pasesd in. --#
            
            if ( ( entity_list is not None ) and ( len( entity_list ) > 0 ) ):
            
                # retrieve map of entities to their relation types and roles.
                entity_to_ids_and_types_map = self.get_entity_id_to_traits_map()
            
                # we have a list.  Loop.
                for entity_id in entity_list:
                
                    # retrieve the ids and traits for this entity.
                    entity_ids_and_traits = entity_to_ids_and_types_map.get( entity_id, None )
                    
                    # got anything at all?
                    if ( entity_ids_and_traits is not None ):
                    
                        # yes.  any value for requested header label?
                        current_value = entity_ids_and_traits.get( header_label_IN, None )
                    
                    else:
                    
                        # no ids or traits, either no ties, just here for comparison.
                        current_value = None
                        
                    #-- END check to see if any relation type roles at all --#
                    
                    # add value to list.
                    value_list_OUT.append( current_value )
                    
                #-- END loop over entity IDs. --#
                
            else:
            
                # no entities, output a warning.
                status_message = "In {}(): WARNING - No entities to process.  Returning empty list.  relation_type_slug_IN: {}; relation_role_IN: {}".format( me, relation_type_slug_IN, relation_role_IN )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.WARNING )
                    
            #-- END check to see if entity list. --#
        
        else:
        
            # no slug passed in, can't do anything.
            status_message = "In {}(): ERROR - No relation type slug passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
        
        #-- END check to see if relation type slug passed in --#

        return value_list_OUT

    #-- END method create_relation_type_role_value_list --#


    def create_ids_and_traits_values_for_entity( self, entity_id_IN ):

        """
            Method: create_ids_and_traits_values_for_entity()

            Purpose: retrieves ids and traits header label list. For each label,
                retrieves value for the entity and adds it to the list (with
                None added if trait or ID is not present). Returns list of
                values.

            Returns:
            - List of values for the entity for each label in header label list.
        """

        # return reference
        value_list_OUT = None

        # declare variables
        me = "create_ids_and_traits_values_for_entity"
        status_message = None
        debug_flag = None
        ids_and_traits_header_labels_list = None
        entity_to_ids_and_types_map = None
        entity_ids_and_traits = None
        header_label = None
        current_value = None
        value_list = None
        
        # initialize
        debug_flag = self.DEBUG_FLAG
        value_list = []

        # make sure we have entity ID
        if ( entity_id_IN is not None ):
        
            # retrieve ids and traits header labels.
            ids_and_traits_header_labels_list = self.get_entity_ids_and_traits_header_list()        

            # get ids and traits for this entity.
            entity_ids_and_traits = self.get_ids_and_traits_for_entity( entity_id_IN )
                        
            # loop over labels, retrieving value for each and adding it to list.
            for header_label in ids_and_traits_header_labels_list:
            
                # retrieve value from entity_ids_and_traits
                current_value = entity_ids_and_traits.get( header_label, None )
                
                # append to the list.
                value_list.append( current_value )
                
            #-- END loop over header labels --#
            
            value_list_OUT = value_list

        else:
        
            # no Entity ID passed in.
            status_message = "In {}(): ERROR - no Entity ID passed in.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            value_list_OUT = None 

        #-- END check to see if entity ID passed in. --#

        return value_list_OUT

    #-- END method create_ids_and_traits_values_for_entity --#


    def do_output_entity_ids_or_traits( self ):
        
        # return reference
        boolean_OUT = False
        
        # declare variables
        entity_ids_list = None
        entity_ids_list_count = None
        entity_traits_list = None
        entity_traits_list_count = None
        is_list = None
        
        # retrieve lists
        entity_ids_list = self.get_output_entity_identifiers_list()
        entity_traits_list = self.get_output_entity_traits_list()
        
        # got ids list?
        if ( entity_ids_list is not None ):
        
            # is it a list?
            is_list = isinstance( entity_ids_list, list )
            if ( is_list == True ):
        
                # yes - get count
                entity_ids_list_count = len( entity_ids_list )
                
                # greater than 0?
                if ( entity_ids_list_count > 0 ):
                    
                    # at least one thing in identifiers list, so True!
                    boolean_OUT = True
                    
                #-- END check to make sure the list has something in it. --#
                
            #-- END check to see if it is actually a list. --#
            
        else:
        
            # no - count = 0
            entity_ids_list_count = 0
            
        #-- END check to see if list present. --#
        
        # got traits list?
        if ( entity_traits_list is not None ):
        
            # is it a list?
            is_list = isinstance( entity_traits_list, list )
            if ( is_list == True ):
        
                # yes - get count
                entity_traits_list_count = len( entity_traits_list )
                
                # greater than 0?
                if ( entity_traits_list_count > 0 ):
                    
                    # at least one thing in identifiers list, so True!
                    boolean_OUT = True
                    
                #-- END check to make sure the list has something in it. --#
                
            #-- END check to see if it is actually a list. --#

        else:
        
            # no - count = 0
            entity_traits_list_count = 0
            
        #-- END check to see if list present. --#
        
        return boolean_OUT
    
    #-- END method do_output_entity_ids_or_traits() --#


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
        selection_filters = self.get_selection_filters( use_entity_selection_IN )
        
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
        
            # ! ----> process filters.

            # call filter_relations() with the selected filters.
            qs_OUT = self.filter_relations( qs_IN = qs_OUT,
                                            selection_filters_IN = selection_filters )            
            
        else:

            # ERROR - no selection filters, can't process.
            status_message = "In {}(): ERROR - no selection filters found in NetworkDataRequest, so nothing to do.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
        
        #-- END check to see if we have selection filters --#

        return qs_OUT

    #-- end method filter_relation_query_set() ---------------------------#


    def filter_relations( self, qs_IN = None, selection_filters_IN = None ):
        
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
        filter_spec_dict = None
        filter_spec = None
        result_status = None
        result_status_is_error = None
        
        # initialize.
        debug_flag = self.DEBUG_FLAG
        qs_OUT = qs_IN
        selection_filters = selection_filters_IN
        
        # got filters?
        if ( selection_filters is not None ):
        
            # is there a filter_specification?
            filter_spec_dict = selection_filters.get( self.PROP_NAME_FILTER_SPECIFICATION, None )
            if ( filter_spec_dict is not None):
            
                # there is a filter_specification
                filter_spec = FilterSpec()
                filter_spec.set_filter_spec( filter_spec_dict )
                
                # initialize QuerySet - QuerySet passed in?
                if ( qs_IN is not None ):
                
                    # use QuerySet passed in.
                    qs_OUT = qs_IN
                    
                else:
                
                    # start with all relations.
                    qs_OUT = Entity_Relation.objects.all()
                    
                #-- END initialize QuerySet --#
            
                # call method build_filter_spec_q()
                result_status = self.build_filter_spec_q( filter_spec )

                # errors?
                result_status_is_error = result_status.is_error()
                if ( result_status_is_error == True ):
                
                    # set status to error, add a message, then nest the
                    #     StatusContainer instance.
                    status_message = "In {}(): ERROR - errors creating Q() for filter spec {}; StatusContainer: {}".format( me, filter_spec, result_status )
                    self.output_message( status_message, do_print_IN = self.DEBUG_FLAG, log_level_code_IN = logging.ERROR )
                
                else:
                
                    # call the method to filter based on a filter_spec.
                    qs_OUT = self.filter_relations_by_filter_spec( qs_OUT, filter_spec )
                
                #-- END check to see if errors. --#
                
            else:
    
                # ERROR - no filter specification.
                status_message = "In {}(): ERROR - no filter specification, nothing to do.  Should I return all?".format( me )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
            #-- END check to see if we have selection filters --#
    
        else:

            # ERROR - no selection filters, can't process.
            status_message = "In {}(): ERROR - no selection filters passed in, so nothing to do.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
        
        #-- END check to see if we have selection filters --#

        return qs_OUT

    #-- end method filter_relations() ---------------------------#


    def filter_relations_by_filter_spec( self, qs_IN, filter_spec_IN, do_compact_queryset_IN = False, recursion_stack_IN = [] ):
        
        '''
        Accepts Entity_Relation QuerySet and filter spec.  Filters the QuerySet
            as specified in the filter spec.  If the filter spec is an aggregate
            type (AND or OR), deal appropriately with the type (more details
            below).  Returns the filtered QuerySet that results.
            
            Aggregate type processing:
            - AND - calls .filter() on each filter criteria in child filters.
            - OR - uses "|" to OR the Q()s in children together.
            
            Note: This will work for a two-level deep set of filters.  Anything
            past that and you probably want to chuck your data into a graph
            store like neo4j.
            
        Preconditions: assumes that the method build_filter_spec_q() has been
            called on the filter spec passed in.  If not, does not do anything.
        '''
        
        # return reference
        qs_OUT = None
        
        # declare variables - input
        level_IN = None
        
        # declare variables
        me = "filter_relations_by_filter_spec"
        debug_flag = False
        status_message = None
        status_code = None
        filter_spec = None
        filter_type = None
        comparison_type = None
        method_name = None
        method_pointer = None
        result_status = None
        result_status_is_error = None
        filter_q = None
        
        # declare variables - processing an aggregate filter spec.
        child_filter_spec_list = None
        child_filter_spec = None
        child_comparison_type = None
        child_q = None
        child_q_list = None
        child_counter = None
        has_child_aggregate = None
        combined_q = None
        child_stack = None
        
        # compacting queryset
        relation_id_list = None
        temp_qs = None
        
        # init
        debug_flag = self.DEBUG_FLAG
        #debug_flag = True
        level_IN = len( recursion_stack_IN )

        status_message = "\n\n[{}] In {}():\n- filter = {}\n- level = {}\n- recursion stack: {}".format( level_IN, me, filter_spec_IN, level_IN, recursion_stack_IN )
        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.DEBUG )
        
        # got a filter spec passed in?
        if ( filter_spec_IN is not None ):

            status_message = "- filter dict:\n{}".format( filter_spec_IN.to_json_string() )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.DEBUG )
    
            # make FilterSpec instance and load dictionary
            filter_spec = filter_spec_IN

            # initialize QuerySet - QuerySet passed in?
            if ( qs_IN is not None ):
            
                # use QuerySet passed in.
                qs_OUT = qs_IN
                
            else:
            
                # start with all relations.
                qs_OUT = Entity_Relation.objects.all()
                
            #-- END initialize QuerySet --#
        
            # retrieve comparison type
            comparison_type = filter_spec.get_comparison_type()
            
            status_message = "- comparison type = {}".format( comparison_type )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.DEBUG )

            # valid type?
            if ( comparison_type in FilterSpec.COMPARISON_TYPE_VALUES ):
            
                # figure out what to do based on type - aggregate or not?
                if ( comparison_type in self.AGGREGATE_COMPARISON_TYPE_LIST ):
                
                    # ! ----> try to process child Q list
                    child_filter_spec_list = filter_spec.get_child_filter_spec_list()
                    child_q_list = []
                    child_counter = 0

                    status_message = "\n\n[{}] ----> In {}(): aggregate ( {} ) filter_spec.  Looping over {} children ( {} ).".format( level_IN, me, comparison_type, len( child_filter_spec_list ), child_filter_spec_list )
                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.DEBUG )

                    for child_filter_spec in child_filter_spec_list:
                    
                        # increment counter
                        child_counter += 1
                    
                        # get comparison type
                        child_comparison_type = child_filter_spec.get_comparison_type()
                        
                        status_message = "\n\n[{}] --------> In {}(): child item #{} - comparison type = {}; JSON:\n{}".format( level_IN, me, child_counter, child_comparison_type, child_filter_spec.to_json_string() )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.DEBUG )
                        
                        # figure out what to do based on type - aggregate (AND or OR)?
                        if ( child_comparison_type not in self.AGGREGATE_COMPARISON_TYPE_LIST ):
                        
                            # get Q
                            child_q = child_filter_spec.get_my_q()

                            # process based on comparison type.
                            if ( ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND )
                                or ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND_FILTER ) ):
                        
                                # AND or AND_filter, so filter the query with
                                #     each Q(), as we go.
                                qs_OUT = qs_OUT.filter( child_q )
                                
                            elif ( ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_OR )
                                or ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND_AMPERSAND ) ):
                            
                                # OR or AND_ampersand - add to list to combine
                                #     later.
                                child_q_list.append( child_q )
                                
                            else:
                            
                                # unknown comparison type.  Just filter?
                                qs_OUT = qs_OUT.filter( child_q )
                                
                                # child aggregate type.
                                status_message = "In {}(): Unknown but valid comparison type: ( {}, valid types: {} ).  adding it via .filter(), since I don't know what bitwise operator to use on it ( filter spec: {} ).  ( level: {}; recursion stack: {} ). ".format( me, comparison_type, FilterSpec.COMPARISON_TYPE_VALUES, child_filter_spec, level_IN, recursion_stack_IN )
                                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.DEBUG )

                            #-- END check to see how we process Q() based on comparison type. --#
                                                    
                        else:
                        
                            # child aggregate type.
                            status_message = "In {}(): Child is an aggregate comparison type ( {} ).  Parent comparison type: {}  Making recursive call to filter_relations_by_filter_spec() ( filter spec: {} ).  ( level: {}; recursion stack: {} ). ".format( me, child_comparison_type, comparison_type, child_filter_spec, level_IN, recursion_stack_IN )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.DEBUG )

                            # is comparison type one of those that shouldn't
                            #     have nested aggregate comparison type?
                            if ( ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_OR )
                                or ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND_AMPERSAND ) ):
                                
                                # oh dear, it is.  Apologize for this not being
                                #     a full-featured database.
                                status_message = "ERROR (probably) - In {}(): Having a child aggregate comparison type ( {} ) inside OR or AND_ampersand comparison types ( current type: {} ) is not supported because of django's & operator for Q() objects not behaving the same as using filter() to AND a Q().  For now, this results in the nested aggregate filter being AND-ed to the QuerySet, not combined with the other filters.  This might work sometimes, and it will probably not out-and-out error, but it won't return correct results.  For 100% reliable execution, you'll need to write custom Python or SQL to filter the relations table like this, or migrate your data store to a graph database.  Sorry.  ( filter spec: {} ).  ( level: {}; recursion stack: {} ). ".format( me, child_comparison_type, comparison_type, child_filter_spec, level_IN, recursion_stack_IN )
                                self.output_message( status_message, do_print_IN = True, log_level_code_IN = logging.ERROR )
                                
                            #-- END check to see if unsupported child comparison type. --#

                            # call me and let me deal with it.  Notes:
                            # - For AND and AND_filter, this is fine - it is
                            #     just another thing added on via filter().
                            # - For OR, this means that we have an out-of-stream
                            #     thing that is being AND-ed.  This most likely
                            #     effectively breaks the OR for at least some
                            #     cases.
                            # - For AND_ampersand, it is all AND-ed, but this
                            #     one is filter()-ed separately, rather than
                            #     bundled up in a single Q().  Probably trouble.
                            # 
                            # So, the take-away here is: If you use OR or
                            #     AND_ampersand, don't AND or OR inside.
                            
                            # add the comparison type to the recursion command
                            #     stack.
                            child_stack = list( recursion_stack_IN )
                            child_stack.append( child_comparison_type )
                            
                            # call the method.
                            qs_OUT = self.filter_relations_by_filter_spec( qs_OUT, child_filter_spec, recursion_stack_IN = child_stack )
                            
                            # no need to pop on exit - the copy of
                            #     recursion_stack_IN in method context is as it
                            #     should be.
                            
                            # compact?
                            if ( do_compact_queryset_IN == True ):
                            
                                # yes, compact.
                                qs_OUT = self.compact_entity_relation_queryset( qs_OUT )
                            
                            #-- END check to see if we compact QuerySet --#
                                                    
                        #-- END check to see if child FilterSpec is also an aggregate. --#
                        
                    #-- END loop over child filter specs. --#
                    
                    # ! ----> is combined_q empty?
                    if ( ( child_q_list is not None ) and ( len ( child_q_list ) > 0 ) ):
                    
                        # we have Qs - what comparison type?
                        if ( ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND )
                            or ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND_FILTER ) ):
                        
                            # AND - loop over list, filter on each.  BUT, you
                            #     should never get here.
                            for child_q in child_q_list:
                            
                                # filter on the Q() instance
                                qs_OUT = qs_OUT.filter( child_q )
                                
                            #-- END loop over child Q() instances. --#

                        elif ( ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_OR )
                            or ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND_AMPERSAND ) ):
                            
                            # OR - loop over list, create combined Q() with |
                            combined_q = None
                            for child_q in child_q_list:
                            
                                # is this the first Q()?
                                if ( combined_q is None ):
                                
                                    # first in list.  set combined_q to child_q.
                                    combined_q = child_q
                                    
                                else:
                                
                                    # append with...
                                    if ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_OR ):
                                    
                                        # ...| (OR)
                                        combined_q = combined_q | child_q
                                        
                                    elif ( comparison_type == FilterSpec.PROP_VALUE_COMPARISON_TYPE_AND_AMPERSAND ):
                                    
                                        # ...& (AND)
                                        combined_q = combined_q & child_q
                                    
                                    else:
                                    
                                        # impossible.
                                        status_message = "ERROR (impossible) - In {}(): comparison_type \"{}\" is neither OR nor AND_ampersand, but it had to be one of those two to get here. ( filter spec: {} ).  ( level: {}; recursion stack: {} ). ".format( me, comparison_type, child_filter_spec, level_IN, recursion_stack_IN )
                                        self.output_message( status_message, do_print_IN = True, log_level_code_IN = logging.ERROR )
                                        
                                    #-- END check to see how to append. --#
                                    
                                #-- END check to see if combined_q is None --#
                                
                            #-- END loop over child Q() instances. --#
                        
                            # filter on the combined Q()
                            qs_OUT = qs_OUT.filter( combined_q )

                            # compact?
                            if ( do_compact_queryset_IN == True ):
                            
                                # yes, compact.
                                qs_OUT = self.compact_entity_relation_queryset( qs_OUT )
                            
                            #-- END check to see if we compact QuerySet --#
                                                    
                        else:
                        
                            # ERROR.
                            status_message = "In {}(): ERROR - In aggregate part of method, comparison_type is not a known aggregate type ( {}; known types: {} ).  Doing nothing.".format( me, comparison_type, self.AGGREGATE_COMPARISON_TYPE_LIST )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                        
                        #-- END check to see if AND or OR --#

                    #-- END check to see if combined_q --#
                    
                else:
                
                    status_message = "\n\n[{}] ----> In {}(): basic filter_spec".format( level_IN, me )
                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.DEBUG )
        
                    # not aggregate - retrieve the Q for the FilterSpec, use it
                    #     to filter.
                    filter_q = filter_spec.get_my_q()
                    
                    # use it to filter relations.
                    qs_OUT = qs_OUT.filter( filter_q )

                    # compact?
                    if ( do_compact_queryset_IN == True ):
                    
                        # yes, compact.
                        qs_OUT = self.compact_entity_relation_queryset( qs_OUT )
                    
                    #-- END check to see if we compact QuerySet --#

                #-- END check to see if aggregate or not.
                                
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
        
        return qs_OUT
        
    #-- END method filter_relations_by_filter_spec() --#


    def generate_entity_id_list( self, is_sorted_IN = True ):

        """
            Method: generate_entity_id_list()

            Purpose: Uses nested entity_dict and map of Entity IDs to Entity
               relation details to make a big list of all the Entities we need
               to include in the network we output.

            Preconditions: self.m_entity_dictionary must be initialized and populated.

            Returns:
            - List - reference to the generated master Entity list.
        """

        # return reference
        list_OUT = []

        # declare variables
        me = "generate_master_entity_list"
        debug_flag = None
        status_message = None
        my_logger = None
        debug_string = ""
        entity_dict = None
        entity_dict_count = None
        entity_ids_list = None
        entity_ids_list_count = None

        # initialize
        my_logger = self.get_logger()
        debug_flag = self.DEBUG_FLAG

        # retrieve the Entity dictionary
        entity_dict = self.get_entity_id_to_instance_map()
        entity_dict_count = len( entity_dict )

        status_message = "In {}: len( entity_dict ) = {}; entity_dict: {}".format( me, entity_dict_count, entity_dict )
        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.DEBUG )            

        # grab list of keys from self.m_entity_dictionary.
        entity_ids_list = list( six.viewkeys( entity_dict ) )

        # do we want it sorted?
        if ( is_sorted_IN == True ):
        
            # we want it sorted.
            entity_ids_list.sort()
        
        #-- END check to see if we want the list sorted. --#

        # output list and length
        entity_ids_list_count = len( entity_ids_list )
        status_message = "In {}(): master entity ID list length: {} ( list: {} )".format( me, entity_ids_list_count, entity_ids_list )
        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )            
    
        # save this as the master entity list.
        self.set_entity_id_list( entity_ids_list )

        list_OUT = self.get_entity_id_list()
        
        my_logger.debug( "In {}: len( self.m_entity_id_list ) = {}".format( me, len( list_OUT ) ) )

        return list_OUT

    #-- END method generate_entity_id_list() --#



    def get_entity_id_list( self, is_sorted_IN = True ):

        """
            Method: get_entity_id_list()

            Purpose: Checks if list is set and has something in it.  If yes,
               returns list nested in instance.  If no, calls the generate
               method and returns the result.

            Preconditions: self.m_entity_dictionary must be initialized and populated.

            Returns:
            - List - reference to the generated master Entity list.
        """

        # return reference
        list_OUT = []

        # declare variables
        me = "get_entity_id_list"
        debug_flag = None
        status_message = None
        is_ok = True
        list_length = None

        # initialize
        debug_flag = self.DEBUG_FLAG

        # retrieve master Entity list
        list_OUT = self.m_entity_id_list

        # just check for None - empty list is OK.
        if ( list_OUT is None ):

            # no list.  not OK.
            is_ok = False

            # List not OK.
            status_message = "In {}(): master list is None ( {} )".format( me, list_OUT )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )            

        #-- END check to see if stored list is OK --#

        # is stored list OK?
        if ( is_ok == False ):

            # not OK.  Try generating list.
            list_OUT = self.generate_entity_id_list( is_sorted_IN )

        #-- END check if list is OK. --#
        
        return list_OUT

    #-- END method get_entity_id_list() --#


    def get_entity_id_to_instance_map( self, init_if_empty_IN = False ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        empty_map = None
        
        # see if already stored.
        value_OUT = self.m_entity_id_to_instance_map
        
        # init if None?
        if ( ( value_OUT is None ) and ( init_if_empty_IN == True ) ):
        
            # yes.
            empty_map = {}
            self.set_entity_id_to_instance_map( empty_map )
            value_OUT = self.get_entity_id_to_instance_map()
            
        #-- END check to see if init on None --#
            
        return value_OUT
    
    #-- END method get_entity_id_to_instance_map() --#
    

    def get_entity_id_to_traits_map( self, init_if_empty_IN = False ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        empty_map = None
        
        # see if already stored.
        value_OUT = self.m_entity_id_to_traits_map
                
        # init if None?
        if ( ( value_OUT is None ) and ( init_if_empty_IN == True ) ):
        
            # yes.
            empty_map = {}
            self.set_entity_id_to_instance_map( empty_map )
            value_OUT = self.get_entity_id_to_instance_map()
            
        #-- END check to see if init on None --#
            
        return value_OUT
    
    #-- END method get_entity_id_to_traits_map() --#
    

    def get_entity_ids_and_traits_header_list( self ):
        
        # return reference
        value_OUT = None
        
        # declare variables
        header_list = None
        
        # see if already stored.
        value_OUT = self.m_entity_ids_and_traits_header_list
        if ( value_OUT is None ):
        
            # create, store, and return.
            header_list = self.create_entity_ids_and_traits_header_list()
            
            # store it.
            self.set_entity_ids_and_traits_header_list( header_list )
            
            # return it
            value_OUT = self.get_entity_ids_and_traits_header_list()
            
        #-- END check to see if not yet created. --#
                
        return value_OUT
    
    #-- END method get_entity_id_to_instance_map() --#
    

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
        
        # retrieve the named value.
        value_OUT = prop_dict.get( name_IN, default_IN )
        
        return value_OUT
    
    #-- END method get_entity_selection_property() --#


    def get_ids_and_traits_for_entity( self, entity_id_IN ):

        """
            Method: get_ids_and_traits_for_entity()

            Purpose: retrieves nested ids and traits map.  Retrieves ids and
                traits for the entity whose ID was passed in.

            Returns:
            - dictionary - dictionary that maps id and trait labels to their
                values for this entity.
        """

        # return reference
        value_OUT = {}

        # declare variables
        entity_id_to_ids_and_traits_dict = None

        # got an ID?
        if ( entity_id_IN != '' ):

            # grab map
            entity_id_to_ids_and_traits_dict = self.get_entity_id_to_traits_map()

            # anything there?
            if ( ( entity_id_to_ids_and_traits_dict is not None ) and ( len( entity_id_to_ids_and_traits_dict ) > 0 ) ):

                # yes.  Check if ID is a key.
                if entity_id_IN in entity_id_to_ids_and_traits_dict:

                    # it is.  Return what is there.
                    value_OUT = entity_id_to_ids_and_traits_dict[ entity_id_IN ]

                else:

                    # no relation roles.  Return empty dictionary.
                    value_OUT = {}

                #-- END check to see if Entity has any relations.

            #-- END check to make sure dict is populated. --#

        #-- END check to see if ID passed in. --#

        return value_OUT

    #-- END method get_ids_and_traits_for_entity() --#


    def get_output_entity_identifiers_list( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_include_column_headers value.
        value_OUT = self.get_output_spec_property( self.PROP_NAME_OUTPUT_ENTITY_IDENTIFIERS_LIST )
        
        return value_OUT
    
    #-- END method get_output_entity_identifiers_list() --#


    def get_output_entity_traits_list( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_include_column_headers value.
        value_OUT = self.get_output_spec_property( self.PROP_NAME_OUTPUT_ENTITY_TRAITS_LIST )
        
        return value_OUT
    
    #-- END method get_output_entity_traits_list() --#


    def get_output_file_path( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_file_path value.
        value_OUT = self.get_output_spec_property( self.PROP_NAME_OUTPUT_FILE_PATH )
        
        return value_OUT
    
    #-- END method get_output_file_path() --#


    def get_output_format( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_format value.
        value_OUT = self.get_output_spec_property( self.PROP_NAME_OUTPUT_FORMAT )
        
        return value_OUT
    
    #-- END method get_output_format() --#


    def get_output_include_column_headers( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_include_column_headers value.
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
        
        # retrieve the named output spec value.
        value_OUT = output_spec.get( name_IN, default_IN )
        
        return value_OUT
    
    #-- END method get_output_spec_property() --#


    def get_output_structure( self ):
        
        # return reference
        value_OUT = None
        
        # retrieve the output_structure value.
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


    def get_relation_query_set( self ):
        
        # return reference
        value_OUT = None
        
        # see if already stored.
        value_OUT = self.m_relation_query_set
                
        return value_OUT
    
    #-- END method get_relation_query_set() --#
    

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
        
        # retrieve the named relation selection value.
        value_OUT = prop_dict.get( name_IN, default_IN )
        
        return value_OUT
    
    #-- END method get_relation_selection_property() --#


    def get_selection_filters( self, use_entity_selection_IN = False ):
        
        '''
        Uses nested selection filters to it to build up an Entity_Relation
            QuerySet that filters as requested.  If use_entity_selection_IN is
            True, but no entity selection present, will just return relation
            selection.
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


    def load_entities_ids_and_traits( self,
                                      relation_qs_IN,
                                      dictionary_IN,
                                      include_through_IN = False ):

        """
            Accepts a dictionary, a list of Entity_Relation instances, and flag
                that indicates if we want THROUGH in addition to FROM and TO.
                Retrieves entities from the FROM and TO of the relations in the
                Entity_Relation query set passed in to the dictionary, making
                the Entity ID the key and then a dictionary of traits and
                identifiers where name is mapped to either value or UUID.  If
                include_through_IN == True, also adds Entities stored in
                relations as THROUGH to the map.  If trait or identifier is not
                present, stores an entry for it in the traits map with value of
                None.

            Preconditions: request must have contained at least a valid filter
                specification, else this will likely be a list of all relations
                (or we won't even get to calling this method).

            Postconditions: Returns the same dictionary passed in, but with
                the entities in relation_qs_IN added, where ID is associated
                with a dictionary of name-value traits and identifiers.

            Parameters:
            - self - self instance variable.
            - relation_qs_IN - django query set object that contains the relations we
                want to add to our dictionary.
            - dictionary_IN - dictionary we want to add people to.  Returned
                with people added.
            - include_through_IN - boolean, defaults to False - If True,
                includes the entity in relation_through in the dictionary along
                with the FROM and TO.  If False, ignores THROUGH.

            Returns:
            - Dictionary - dictionary updated to include all entities from the
                FROM, TO, and optionally THROUGH references in the
                Entity_Relation QuerySet passed in, with entity ID mapped to a
                dictionary of traits and identifiers where name is mapped to
                either value or UUID.
        """

        # return reference
        entity_dict_OUT = {}

        # declare variables
        me = "load_entities_ids_and_traits"
        current_relation = None
        current_entity = None
        current_entity_id = None
        current_value = None
        entity_id = None

        # set the output dictionary
        if ( dictionary_IN ):

            # yes, store in output parameter
            entity_dict_OUT = dictionary_IN

        #-- END check to see if dictionary passed in --#

        # loop over the articles
        for current_relation in relation_qs_IN:

            # ! ----> FROM

            # add FROM Entity ID to list.  If no Entity ID, don't add.
            current_entity = current_relation.relation_from
            
            # add to dictionary
            entity_dict_OUT = self.load_entity_identifiers( current_entity, entity_dict_OUT )
            entity_dict_OUT = self.load_entity_traits( current_entity, entity_dict_OUT )

            # ! ----> TO

            # add TO Entity ID to list.  If no Entity ID, don't add.
            current_entity = current_relation.relation_to
            
            # add to dictionary
            entity_dict_OUT = self.load_entity_identifiers( current_entity, entity_dict_OUT )
            entity_dict_OUT = self.load_entity_traits( current_entity, entity_dict_OUT )

            # ! ----> THROUGH?

            if ( include_through_IN == True ):

                # add THROUGH Entity ID to list.  If no Entity ID, don't add.
                current_entity = current_relation.relation_through
                
                # add to dictionary
                entity_dict_OUT = self.load_entity_identifiers( current_entity, entity_dict_OUT )
                entity_dict_OUT = self.load_entity_traits( current_entity, entity_dict_OUT )
                
            #-- END check to see if we include THROUGH --#
    
        #-- END loop over Entities --#
        
        return entity_dict_OUT

    #-- END function load_entities_ids_and_traits() --#


    def load_entity_identifiers( self, entity_IN, dictionary_IN, multi_value_separator_IN = "||" ):

        """
            Accepts a dictionary, an Entity instance.  Retrieves the Entity's ID
                and if it is not already in the dictionary, adds it, making the
                Entity ID the key and a map of requested identifier
                names to their associated UUIDs the associated value.

            Postconditions: Returns the same dictionary passed in, but with
                the Entity passed in added, associated with a dict of its
                identifiers.

            Parameters:
            - self - self instance variable.
            - entity_IN - django Entity instance to be added to dictionary
                passed in.
            - dictionary_IN - dictionary we want to add entity to.  Returned
                with entity added.

            Returns:
            - Dictionary - dictionary updated to include the Entity passed in,
                associated with a dict of its values for requested identifiers.
        """

        # return reference
        entity_dict_OUT = {}

        # declare variables
        me = "load_entity_identifiers"
        current_relation = None
        current_entity = None
        current_entity_id = None
        entity_ids_list = None
        entity_ids_list_count = None
        identifier_dict = None
        
        # declare variables - ids
        id_info_dict = None
        id_name = None
        id_id_type = None
        id_source = None
        id_source_in_list = None
        id_identifier_type_id = None
        id_qs = None
        id_count = None
        id_instance = None
        id_value = None
        id_value_list = None
        id_value_list_count = None
        current_id = None
        id_dict_key = None
        
        # set the output dictionary
        if ( dictionary_IN ):

            # yes, store in output parameter
            entity_dict_OUT = dictionary_IN

        #-- END check to see if dictionary passed in --#

        current_entity = entity_IN

        # see if there is an entity
        if ( current_entity is not None ):

            # get Entity ID
            current_entity_id = current_entity.id
            identifier_dict = None

            # Does entity already have a traits/ids dictionary?
            if ( current_entity_id in entity_dict_OUT ):
            
                # retrieve trait/id dict
                identifier_dict = entity_dict_OUT.get( current_entity_id, None )
                
            #-- END retrieve trait/id dict. --#
            
            # anything in trait/id dict?
            if ( identifier_dict is None ):
            
                # no trait dict - create and add one.
                identifier_dict = {}
                entity_dict_OUT[ current_entity_id ] = identifier_dict
            
            #-- END check to see if existing trait/id dictionary --#

            # are there identifiers to collect?
            entity_ids_list = self.get_output_entity_identifiers_list()
            if ( entity_ids_list is None ):

                # no list.  Make an empty one, so we can just always loop.
                entity_ids_list = []
                
            #-- END check to see if ids list --#
            
            # loop over id filters.
            for id_info_dict in entity_ids_list:
            
                # get values from the dict
                id_name = id_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_NAME, None )
                id_id_type = id_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_ID_TYPE, None )
                id_source = id_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_SOURCE, None )
                id_source_in_list = id_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_SOURCE_IN_LIST, None )
                id_identifier_type_id = id_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_IDENTIFIER_TYPE_ID, None )
                id_header = id_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_OUTPUT_HEADER, None )
                
                # Must have at least a name
                if ( ( id_name is not None ) and ( id_name != "" ) ):
                
                    # filter entity's identifier QuerySet
                    id_qs = current_entity.entity_identifier_set.all()
                    
                    # got a name?
                    if ( ( id_name is not None ) and ( id_name != "" ) ):
                    
                        # yes. Filter.
                        id_qs = id_qs.filter( name = id_name )
                        
                    #-- END check to see if name. --#
                    
                    # got a string id type value?
                    if ( ( id_id_type is not None ) and ( id_id_type != "" ) ):
                    
                        # yes. Filter.
                        id_qs = id_qs.filter( id_type = id_id_type )
                        
                    #-- END check to see if id_id_type. --#                    
                    
                    # got a id_source?
                    if ( ( id_source is not None ) and ( id_source != "" ) ):
                    
                        # yes. Filter.
                        id_qs = id_qs.filter( source = id_source )
                        
                    #-- END check to see if id_source. --#                    
                    
                    # got a id_source IN list?
                    if ( ( id_source_in_list is not None ) and ( len( id_source_in_list ) > 0 ) ):
                    
                        # yes. Filter.
                        id_qs = id_qs.filter( source__in = id_source_in_list )
                        
                    #-- END check to see if id_source. --#                    
                    
                    # got an identifier type id?
                    if ( ( id_identifier_type_id is not None ) and ( id_identifier_type_id != "" ) ):
                    
                        # yes. Filter.
                        id_qs = id_qs.filter( entity_identifier_type_id = id_identifier_type_id )
                        
                    #-- END check to see if identifier type id. --#
                    
                    # got any matches?
                    id_count = id_qs.count()
                    if ( id_count > 0 ):
                    
                        # yes.  Build value.
                        id_value_list = []
                        for id_instance in id_qs:
                            
                            # retrieve UUID and add to list.
                            id_value = id_instance.uuid
                            id_value_list.append( id_value )
                        
                        #-- END loop over id instances. --#
                        
                        # how many values?
                        id_value_list_count = len( id_value_list )
                        if ( id_value_list_count > 1 ):
                        
                            # more than one.  Smoosh them together.
                            id_value = multi_value_separator_IN.join( id_value_list )
                            
                        elif ( id_value_list_count == 1 ):
                        
                            # just one.
                            id_value = id_value_list[ 0 ]
                            
                        else:
                        
                            # neither one or > 1... 0, so set to None.
                            id_value = None
                            
                        #-- END check to see how many values. --#
                        
                    else:
                    
                        # no.  Set value to None.
                        id_value = None
                        
                    #-- END chec to see if traits for trait spec --#
                    
                    # get id_dict_key
                    id_dict_key = self.create_entity_id_header_label( id_info_dict )
                    
                    # add value to map.
                    identifier_dict[ id_dict_key ] = id_value
                    
                #-- END check to see if enough info to filter. --#
                
            #-- END loop over traits we are to collect. --#
        
            # store the Entity in the output dict.
            entity_dict_OUT[ current_entity_id ] = identifier_dict

        #-- END check to see if there is an entity --#

        return entity_dict_OUT

    #-- END function load_entity_identifiers() --#


    def load_entity_traits( self, entity_IN, dictionary_IN, multi_value_separator_IN = "||" ):

        """
            Accepts a dictionary, an Entity instance.  Retrieves the Entity's ID
                and if it is not already in the dictionary, adds it, making the
                Entity ID the key and a map of requested trait and identifier
                names to their associated values/UUIDs the associated value.

            Postconditions: Returns the same dictionary passed in, but with
                the Entity passed in added, associated with a dict of its traits
                and identifiers.

            Parameters:
            - self - self instance variable.
            - entity_IN - django Entity instance to be added to dictionary
                passed in.
            - dictionary_IN - dictionary we want to add entity to.  Returned
                with entity added.

            Returns:
            - Dictionary - dictionary updated to include the Entity passed in,
                associated with a dict of its values for requested traits and
                identifiers.
        """

        # return reference
        entity_dict_OUT = {}

        # declare variables
        me = "load_entity_traits"
        current_relation = None
        current_entity = None
        current_entity_id = None
        entity_traits_list = None
        entity_traits_list_count = None
        trait_dict = None
        
        # declare variables - traits
        trait_info_dict = None
        trait_name = None
        trait_slug = None
        trait_entity_type_trait_id = None
        trait_qs = None
        trait_count = None
        trait_instance = None
        trait_value = None
        trait_value_list = None
        trait_value_list_count = None
        current_trait = None
        trait_dict_key = None
        
        # set the output dictionary
        if ( dictionary_IN ):

            # yes, store in output parameter
            entity_dict_OUT = dictionary_IN

        #-- END check to see if dictionary passed in --#

        current_entity = entity_IN

        # see if there is an entity
        if ( current_entity is not None ):

            # get Entity ID
            current_entity_id = current_entity.id
            trait_dict = None

            # Does entity already have a traits/ids dictionary?
            if ( current_entity_id in entity_dict_OUT ):
            
                # retrieve trait dict
                trait_dict = entity_dict_OUT.get( current_entity_id, None )
                
            #-- END retrieve trait dict. --#
            
            # anything in trait dict?
            if ( trait_dict is None ):
            
                # no trait dict - create and add one.
                trait_dict = {}
                entity_dict_OUT[ current_entity_id ] = trait_dict
            
            #-- END check to see if existing trait dictionary --#

            # are there traits to collect?
            entity_traits_list = self.get_output_entity_traits_list()
            if ( entity_traits_list is None ):

                # no list.  Make an empty one, so we can just always loop.
                entity_traits_list = []
                
            #-- END check to see if traits list --#
            
            # loop over trait filters.
            for trait_info_dict in entity_traits_list:
            
                # get values from the dict
                trait_name = trait_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_NAME, None )
                trait_slug = trait_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_SLUG, None )
                trait_entity_type_trait_id = trait_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_TRAITS_ENTITY_TYPE_TRAIT_ID, None )
                
                # Must have at least a name
                if ( ( trait_name is not None ) and ( trait_name != "" ) ):
                
                    # filter entity's trait QuerySet
                    trait_qs = current_entity.entity_trait_set.all()
                    
                    # got a name?
                    if ( ( trait_name is not None ) and ( trait_name != "" ) ):
                    
                        # yes. Filter.
                        trait_qs = trait_qs.filter( name = trait_name )
                        
                    #-- END check to see if name. --#
                    
                    # got a slug?
                    if ( ( trait_slug is not None ) and ( trait_slug != "" ) ):
                    
                        # yes. Filter.
                        trait_qs = trait_qs.filter( slug = trait_slug )
                        
                    #-- END check to see if slug. --#                    
                    
                    # got a trait type id?
                    if ( ( trait_entity_type_trait_id is not None ) and ( trait_entity_type_trait_id != "" ) ):
                    
                        # yes. Filter.
                        trait_qs = trait_qs.filter( entity_type_trait_id = trait_entity_type_trait_id )
                        
                    #-- END check to see if trait_entity_type_trait_id. --#
                    
                    # got any matches?
                    trait_count = trait_qs.count()
                    if ( trait_count > 0 ):
                    
                        # yes.  Build value.
                        trait_value_list = []
                        for trait_instance in trait_qs:
                            
                            # retrieve value and add to list.
                            trait_value = trait_instance.value
                            trait_value_list.append( trait_value )
                        
                        #-- END loop over trait instances. --#
                        
                        # how many values?
                        trait_value_list_count = len( trait_value_list )
                        if ( trait_value_list_count > 1 ):
                        
                            # more than one.  Smoosh them together.
                            trait_value = multi_value_separator_IN.join( trait_value_list )
                            
                        elif ( trait_value_list_count == 1 ):
                        
                            # just one.
                            trait_value = trait_value_list[ 0 ]
                            
                        else:
                        
                            # neither one or > 1... 0, so set to None.
                            trait_value = None
                            
                        #-- END check to see how many values. --#
                        
                    else:
                    
                        # no.  Set value to None.
                        trait_value = None
                        
                    #-- END chec to see if traits for trait spec --#
                    
                    # get trait_dict_key
                    trait_dict_key = self.create_entity_trait_header_label( trait_info_dict )
                    
                    # add value to map.
                    trait_dict[ trait_dict_key ] = trait_value
                    
                #-- END check to see if enough info to filter. --#
                
            #-- END loop over traits we are to collect. --#
        
            # store the Entity in the output dict.
            entity_dict_OUT[ current_entity_id ] = trait_dict

        #-- END check to see if there is an entity --#

        return entity_dict_OUT

    #-- END function load_entity_traits() --#


    def load_ids_and_traits_for_entities( self, entity_id_list_IN, dictionary_IN ):
        
        """
            Accepts a dictionary, a list of Entity_Relation instances, and flag
                that indicates if we want THROUGH in addition to FROM and TO.
                Retrieves entities from the FROM and TO of the relations in the
                Entity_Relation query set passed in to the dictionary, making
                the Entity ID the key and then a dictionary of traits and
                identifiers where name is mapped to either value or UUID.  If
                include_through_IN == True, also adds Entities stored in
                relations as THROUGH to the map.  If trait or identifier is not
                present, stores an entry for it in the traits map with value of
                None.

            Preconditions: request must have contained at least a valid filter
                specification, else this will likely be a list of all relations
                (or we won't even get to calling this method).

            Postconditions: Returns the same dictionary passed in, but with
                the entities in relation_qs_IN added, where ID is associated
                with a dictionary of name-value traits and identifiers.

            Parameters:
            - self - self instance variable.
            - relation_qs_IN - django query set object that contains the relations we
                want to add to our dictionary.
            - dictionary_IN - dictionary we want to add people to.  Returned
                with people added.
            - include_through_IN - boolean, defaults to False - If True,
                includes the entity in relation_through in the dictionary along
                with the FROM and TO.  If False, ignores THROUGH.

            Returns:
            - Dictionary - dictionary updated to include all entities from the
                FROM, TO, and optionally THROUGH references in the
                Entity_Relation QuerySet passed in, with entity ID mapped to a
                dictionary of traits and identifiers where name is mapped to
                either value or UUID.
        """

        # return reference
        entity_dict_OUT = {}

        # declare variables
        me = "load_entities_ids_and_traits"
        current_entity_id = None
        current_entity = None
        current_value = None
        entity_id = None

        # set the output dictionary
        if ( dictionary_IN ):

            # yes, store in output parameter
            entity_dict_OUT = dictionary_IN

        #-- END check to see if dictionary passed in --#

        # loop over the articles
        for current_entity_id in entity_id_list_IN:

            # add FROM Entity ID to list.  If no Entity ID, don't add.
            current_entity = Entity.objects.get( pk = current_entity_id )

            # add to dictionary
            entity_dict_OUT = self.load_entity_identifiers( current_entity, entity_dict_OUT )
            entity_dict_OUT = self.load_entity_traits( current_entity, entity_dict_OUT )

        #-- END loop over Entities --#
        
        return entity_dict_OUT

    #-- END function load_ids_and_traits_for_entities() --#


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
    
    
    def process_entities( self, include_through_IN = False, load_instance_IN = False ):

        """
            Accepts flag that dictates whether we load the actual Entity
                record or not.  Uses nested request to retrieve all matching
                relations, then builds a dictionary of all the IDs of FROM and
                TO Entities in those relations, mapped either to None or to
                their Entity instance.

            Preconditions: request must have contained required parameters, and
                so contained at least a start and end date and a publication.
                Should we have a flag that says to use the same criteria as the
                selection criteria?

            Postconditions: uses a lot of memory if you choose a large date
                range.

            Parameters:
            - load_instance_IN - boolean, if False, doesn't load Entity model
                instances while building the dictionary.  If True, loads Entity
                models and stores them in the dictionary.
            - include_through_IN - boolean, if False does not include Entities
                referenced in relation_through, if True does include them.

            Returns:
            - Dictionary - dictionary that maps entity IDs to Entity model
                instances for all TO and FROM entities associated with all
                matching Entity_Relations.
        """

        # return reference
        dict_OUT = None

        # declare variables
        me = "process_entities"
        my_logger = None
        relation_query_set = None
        request_instance = None
        entity_id_to_instance_map = None
        do_gather_ids_and_traits = None
        entity_id_to_traits_map = None
        
        # initialize
        my_logger = self.get_logger()
        entity_id_to_instance_map = {}
        entity_id_to_traits_map = {}

        # get query set to loop over Entity_Relations that match the filter
        #     criteria in the request for selecting included Entities.  This
        #     might or might not be the same as the QuerySet for included
        #     Entity_Relations.
        relation_query_set = self.filter_relation_query_set( use_entity_selection_IN = True )
        
        # store the QuerySet
        self.set_relation_query_set( relation_query_set )
        
        my_logger.debug( "In {}(): relation_query_set.count() = {}".format( me, relation_query_set.count() ) )

        # add entities from relation QuerySet to dict.
        entity_id_to_instance_map = self.add_entities_to_dict( relation_query_set,
                                                               entity_id_to_instance_map,
                                                               include_through_IN = include_through_IN,
                                                               store_entity_IN = load_instance_IN )
                                              
        # store dictionary internally
        self.set_entity_id_to_instance_map( entity_id_to_instance_map )
        
        # also return it.
        dict_OUT = entity_id_to_instance_map
                                              
        # do we need to also gather traits and/or identifiers?
        do_gather_ids_and_traits = self.do_output_entity_ids_or_traits()
        if ( do_gather_ids_and_traits == True ):
        
            # yes.  Call method.
            entity_id_to_traits_map = self.load_entities_ids_and_traits( relation_query_set,
                                                                         entity_id_to_traits_map,
                                                                         include_through_IN = include_through_IN )
            
            # store dictionary internally
            self.set_entity_id_to_traits_map( entity_id_to_traits_map )
            
        #-- END check to see if we gather traits and IDs. --#
        
        # generate entity ID list.
        self.generate_entity_id_list()
            
        my_logger.debug( "In {}(): len( dict_OUT ) = {}".format( me, len( dict_OUT ) ) )

        return dict_OUT

    #-- END function process_entities() --#


    def process_entities_from_id_list( self, entity_id_list_IN, include_through_IN = False, load_instance_IN = False ):

        """
            Accepts flag that dictates whether we load the actual Entity
                record or not.  Uses nested request to retrieve all matching
                relations, then builds a dictionary of all the IDs of FROM and
                TO Entities in those relations, mapped either to None or to
                their Entity instance.

            Preconditions: request must have contained required parameters, and
                so contained at least a start and end date and a publication.
                Should we have a flag that says to use the same criteria as the
                selection criteria?

            Postconditions: uses a lot of memory if you choose a large date
                range.

            Parameters:
            - load_instance_IN - boolean, if False, doesn't load Entity model
                instances while building the dictionary.  If True, loads Entity
                models and stores them in the dictionary.
            - include_through_IN - boolean, if False does not include Entities
                referenced in relation_through, if True does include them.

            Returns:
            - Dictionary - dictionary that maps entity IDs to Entity model
                instances for all TO and FROM entities associated with all
                matching Entity_Relations.
        """

        # return reference
        status_OUT = None

        # declare variables
        me = "process_entities_from_id_list"
        my_logger = None
        entity_id_list_count = None
        entity_id = None
        request_instance = None
        entity_id_to_instance_map = None
        do_gather_ids_and_traits = None
        entity_id_to_traits_map = None
        
        # initialize
        my_logger = self.get_logger()
        entity_id_to_instance_map = self.get_entity_id_to_instance_map( init_if_empty_IN = True )
        entity_id_to_traits_map = self.get_entity_id_to_traits_map( init_if_empty_IN = True )
        do_gather_ids_and_traits = self.do_output_entity_ids_or_traits()
        
        # got an ID list?
        if ( ( entity_id_list_IN is not None )
            and ( isinstance( entity_id_list_IN, list ) )
            and ( len( entity_id_list_IN ) > 0 ) ):

            entity_id_list_count = len( entity_id_list_IN )

            my_logger.debug( "In {}(): entity_id_list_count = {}".format( me, entity_id_list_count ) )
            my_logger.debug( "In {}(): BEFORE - len( entity_id_to_instance_map ) = {}".format( me, len( entity_id_to_instance_map ) ) )
                        
            # loop over entity IDs.
            for entity_id in entity_id_list_IN:
            
                # retrieve instance
                entity_instance = Entity.objects.get( pk = entity_id )
            
                # add to instance map.
                entity_id_to_instance_map = self.add_entity_to_dict( entity_instance, entity_id_to_instance_map, store_entity_IN = load_instance_IN )
                                                                                                    
            #-- END check to see if we gather traits and IDs. --#
            
            # do we need to also gather traits and/or identifiers?
            if ( do_gather_ids_and_traits == True ):
        
                # yes.  Call method.
                self.load_ids_and_traits_for_entities( entity_id_list_IN, entity_id_to_traits_map )

            #-- END check to see if we gather IDs and traits.
                
            # generate entity ID list.
            self.generate_entity_id_list()
                            
            my_logger.debug( "In {}(): AFTER - len( entity_id_to_instance_map ) = {}".format( me, len( entity_id_to_instance_map ) ) )
            
        else:
        
            # do nothing.
            my_logger.debug( "In {}(): no entity ID list passed in, so doing nothing.".format( me, len( dict_OUT ) ) )
        
        #-- END check to make sure there is a list. --#
        
        return status_OUT
        
    #-- END function process_entities_from_id_list() --#


    def set_entity_id_list( self, value_IN ):

        """
            Method: set_entity_id_list()

            Purpose: accepts a list, stores it in the instance.

            Params:
            - value_IN - list of IDs of all entities in current network data set.
        """

        # return value
        value_OUT = None

        # store value
        self.m_entity_id_list = value_IN
        
        # sanity check - retrieve and return.
        value_OUT = self.get_entity_id_list()
        
        return value_OUT

    #-- END method set_entity_id_list() --#


    def set_entity_id_to_instance_map( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_entity_id_to_instance_map = value_IN
        
        # return it
        value_OUT = self.get_entity_id_to_instance_map()
        
        return value_OUT
    
    #-- END method set_entity_id_to_instance_map() --#


    def set_entity_id_to_traits_map( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_entity_id_to_traits_map = value_IN
        
        # return it
        value_OUT = self.get_entity_id_to_traits_map()
        
        return value_OUT
    
    #-- END method set_entity_id_to_traits_map() --#


    def set_entity_ids_and_traits_header_list( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_entity_ids_and_traits_header_list = value_IN
        
        # return it
        value_OUT = self.get_entity_ids_and_traits_header_list()
        
        return value_OUT
    
    #-- END method set_entity_ids_and_traits_header_list() --#


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


    def set_output_entity_identifiers_list( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_output_spec_property( self.PROP_NAME_OUTPUT_ENTITY_IDENTIFIERS_LIST, value_IN )
        
        return value_OUT
    
    #-- END method set_output_entity_identifiers_list() --#


    def set_output_entity_traits_list( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # return it
        value_OUT = self.set_output_spec_property( self.PROP_NAME_OUTPUT_ENTITY_TRAITS_LIST, value_IN )
        
        return value_OUT
    
    #-- END method set_output_entity_traits_list() --#


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


    def set_relation_query_set( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_relation_query_set = value_IN
        
        # return it
        value_OUT = self.get_relation_query_set()
        
        return value_OUT
    
    #-- END method set_relation_query_set() --#


    def process_entities_from_id_list( self, entity_id_list_IN, include_through_IN = False, load_instance_IN = False ):

        """
            Accepts flag that dictates whether we load the actual Entity
                record or not.  Uses nested request to retrieve all matching
                relations, then builds a dictionary of all the IDs of FROM and
                TO Entities in those relations, mapped either to None or to
                their Entity instance.

            Preconditions: request must have contained required parameters, and
                so contained at least a start and end date and a publication.
                Should we have a flag that says to use the same criteria as the
                selection criteria?

            Postconditions: uses a lot of memory if you choose a large date
                range.

            Parameters:
            - load_instance_IN - boolean, if False, doesn't load Entity model
                instances while building the dictionary.  If True, loads Entity
                models and stores them in the dictionary.
            - include_through_IN - boolean, if False does not include Entities
                referenced in relation_through, if True does include them.

            Returns:
            - Dictionary - dictionary that maps entity IDs to Entity model
                instances for all TO and FROM entities associated with all
                matching Entity_Relations.
        """

        # return reference
        status_OUT = None

        # declare variables
        me = "process_entities_from_id_list"
        my_logger = None
        entity_id_list_count = None
        entity_id = None
        request_instance = None
        entity_id_to_instance_map = None
        do_gather_ids_and_traits = None
        entity_id_to_traits_map = None
        
        # initialize
        my_logger = self.get_logger()
        entity_id_to_instance_map = self.get_entity_id_to_instance_map( init_if_empty_IN = True )
        entity_id_to_traits_map = self.get_entity_id_to_traits_map( init_if_empty_IN = True )
        do_gather_ids_and_traits = self.do_output_entity_ids_or_traits()
        
        # got an ID list?
        if ( ( entity_id_list_IN is not None )
            and ( isinstance( entity_id_list_IN, list ) )
            and ( len( entity_id_list_IN ) > 0 ) ):

            entity_id_list_count = len( entity_id_list_IN )

            my_logger.debug( "In {}(): entity_id_list_count = {}".format( me, entity_id_list_count ) )
            my_logger.debug( "In {}(): BEFORE - len( entity_id_to_instance_map ) = {}".format( me, len( entity_id_to_instance_map ) ) )
                        
            # loop over entity IDs.
            for entity_id in entity_id_list_IN:
            
                # retrieve instance
                entity_instance = Entity.objects.get( pk = entity_id )
            
                # add to instance map.
                entity_id_to_instance_map = self.add_entity_to_dict( entity_instance, entity_id_to_instance_map, store_entity_IN = load_instance_IN )
                                                                                                    
            #-- END check to see if we gather traits and IDs. --#
            
            # do we need to also gather traits and/or identifiers?
            if ( do_gather_ids_and_traits == True ):
        
                # yes.  Call method.
                self.load_ids_and_traits_for_entities( entity_id_list_IN, entity_id_to_traits_map )

            #-- END check to see if we gather IDs and traits.
                
            # generate entity ID list.
            self.generate_entity_id_list()
                            
            my_logger.debug( "In {}(): AFTER - len( entity_id_to_instance_map ) = {}".format( me, len( entity_id_to_instance_map ) ) )
            
        else:
        
            # do nothing.
            my_logger.debug( "In {}(): no entity ID list passed in, so doing nothing.".format( me, len( dict_OUT ) ) )
        
        #-- END check to make sure there is a list. --#
        
        return status_OUT
        
    #-- END function process_entities_from_id_list() --#


#-- END class NetworkDataRequest --#