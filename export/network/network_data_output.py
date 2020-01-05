from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2010-2014 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context_text.

context_text is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context_text is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context_text. If not, see http://www.gnu.org/licenses/.
'''

__author__="jonathanmorgan"
__date__ ="$May 1, 2010 6:26:35 PM$"

if __name__ == "__main__":
    print( "Hello World" )

#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================

# python libraries
from abc import ABCMeta, abstractmethod

#import copy

# import six for Python 2 and 3 compatibility.
import six

# Django DB classes, just to play with...
#from django.db.models import Count # for aggregating counts of authors, sources.
#from django.db.models import Max   # for getting max value of author, source counts.

# python_utilities
from python_utilities.parameters.param_container import ParamContainer

# Import the classes for our context_text application
#from context_text.models import Article
#from context_text.models import Article_Author
#from context_text.models import Article_Subject
#from context_text.models import Person
#from context_text.models import Topic

# export classes
from context.export.network.network_data_request import NetworkDataRequest

# Import context shared classes.
from context.shared.context_base import ContextBase


#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class NetworkDataOutput( ContextBase ):

    
    #---------------------------------------------------------------------------
    # META!!!
    #---------------------------------------------------------------------------

    
    __metaclass__ = ABCMeta


    #---------------------------------------------------------------------------
    # CONSTANTS-ish
    #---------------------------------------------------------------------------


    DEBUG_FLAG = True
    LOGGER_NAME = "context.export.network.network_data_output.NetworkDataOutput"
    ME = LOGGER_NAME

    # network output type constants
    
    # Network data format output types
    NETWORK_DATA_FORMAT_SIMPLE_MATRIX = "simple_matrix"
    NETWORK_DATA_FORMAT_CSV_MATRIX = "csv_matrix"
    NETWORK_DATA_FORMAT_TAB_DELIMITED_MATRIX = "tab_delimited_matrix"
    NETWORK_DATA_FORMAT_DEFAULT = NETWORK_DATA_FORMAT_TAB_DELIMITED_MATRIX
    
    NETWORK_DATA_FORMAT_CHOICES_LIST = [
        ( NETWORK_DATA_FORMAT_SIMPLE_MATRIX, "Simple Matrix" ),
        ( NETWORK_DATA_FORMAT_CSV_MATRIX, "CSV Matrix" ),
        ( NETWORK_DATA_FORMAT_TAB_DELIMITED_MATRIX, "Tab-Delimited Matrix" ),
    ]

    # Network data output types
    NETWORK_DATA_OUTPUT_TYPE_NETWORK = NetworkDataRequest.PROP_VALUE_OUTPUT_STRUCTURE_JUST_TIES
    NETWORK_DATA_OUTPUT_TYPE_ATTRIBUTES = NetworkDataRequest.PROP_VALUE_OUTPUT_STRUCTURE_JUST_TRAITS
    NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_COLS = NetworkDataRequest.PROP_VALUE_OUTPUT_STRUCTURE_BOTH_TRAIT_COLUMNS
    NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_ROWS = NetworkDataRequest.PROP_VALUE_OUTPUT_STRUCTURE_BOTH_TRAIT_ROWS
    NETWORK_DATA_OUTPUT_TYPE_DEFAULT = NetworkDataRequest.PROP_VALUE_OUTPUT_STRUCTURE_DEFAULT
    
    NETWORK_DATA_OUTPUT_TYPE_CHOICES_LIST = [
        ( NETWORK_DATA_OUTPUT_TYPE_NETWORK, "Just Network" ),
        ( NETWORK_DATA_OUTPUT_TYPE_ATTRIBUTES, "Just Attributes" ),
        ( NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_COLS, "Network + Attribute Columns" ),
        ( NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_ROWS, "Network + Attribute Rows" ),
    ]

    # Person Query Types
    PERSON_QUERY_TYPE_ALL = "all"
    PERSON_QUERY_TYPE_ARTICLES = "articles"
    PERSON_QUERY_TYPE_CUSTOM = "custom"
    PERSON_QUERY_TYPE_DEFAULT = PERSON_QUERY_TYPE_ARTICLES

    PERSON_QUERY_TYPE_CHOICES_LIST = [ 
        ( PERSON_QUERY_TYPE_ALL, "All persons" ),
        ( PERSON_QUERY_TYPE_ARTICLES, "From selected articles" ),
        ( PERSON_QUERY_TYPE_CUSTOM, "Custom, defined below" ),
    ]

    # Filtering Article_Data on coder_type.
    CODER_TYPE_FILTER_TYPE_NONE = ContextTextBase.CODER_TYPE_FILTER_TYPE_NONE
    CODER_TYPE_FILTER_TYPE_AUTOMATED = ContextTextBase.CODER_TYPE_FILTER_TYPE_AUTOMATED
    CODER_TYPE_FILTER_TYPE_ALL = ContextTextBase.CODER_TYPE_FILTER_TYPE_ALL
    CODER_TYPE_FILTER_TYPE_DEFAULT = ContextTextBase.CODER_TYPE_FILTER_TYPE_DEFAULT
    
    CODER_TYPE_FILTER_TYPE_CHOICES_LIST = [ 
        ( CODER_TYPE_FILTER_TYPE_NONE, "Do not filter" ),
        ( CODER_TYPE_FILTER_TYPE_AUTOMATED, "Just automated" ),
        ( CODER_TYPE_FILTER_TYPE_ALL, "All users" ),
    ]

    # person types
    PERSON_TYPE_UNKNOWN = 'unknown'
    PERSON_TYPE_AUTHOR = 'author'
    PERSON_TYPE_SOURCE = 'source'
    PERSON_TYPE_BOTH = 'both'
    PERSON_TYPE_TO_ID = {
        PERSON_TYPE_UNKNOWN : 1,
        PERSON_TYPE_AUTHOR : 2,
        PERSON_TYPE_SOURCE : 3,
        PERSON_TYPE_BOTH : 4
    }

    # status variables
    STATUS_OK = "OK!"
    STATUS_ERROR_PREFIX = "Error: "

    # variables for choosing yes or no.
    CHOICE_YES = 'yes'
    CHOICE_NO = 'no'

    # source types
    SOURCE_TYPE_INDIVIDUAL = 'individual'

    # source contact types
    SOURCE_CONTACT_TYPE_DIRECT = 'direct'
    SOURCE_CONTACT_TYPE_EVENT = 'event'

    # parameter constants
    PARAM_OUTPUT_TYPE = 'output_type'
    PARAM_NETWORK_DOWNLOAD_AS_FILE = 'network_download_as_file'
    PARAM_NETWORK_DATA_OUTPUT_TYPE = 'network_data_output_type'   # type of data you want to output - either just the network, just node attributes, or network with attributes in same table, either with attributes as additional rows or additional columns.
    PARAM_NETWORK_INCLUDE_HEADERS = 'network_include_headers'
    PARAM_SOURCE_CAPACITY_INCLUDE_LIST = Article_Subject.PARAM_SOURCE_CAPACITY_INCLUDE_LIST
    PARAM_SOURCE_CAPACITY_EXCLUDE_LIST = Article_Subject.PARAM_SOURCE_CAPACITY_EXCLUDE_LIST
    PARAM_SOURCE_CONTACT_TYPE_INCLUDE_LIST = Article_Subject.PARAM_SOURCE_CONTACT_TYPE_INCLUDE_LIST
    PARAM_PERSON_QUERY_TYPE = "person_query_type"
    PARAM_CODER_TYPE_FILTER_TYPE = "coder_type_filter_type"
    PARAM_PERSON_CODER_TYPE_FILTER_TYPE = "person_" + PARAM_CODER_TYPE_FILTER_TYPE
    
    # node attributes
    NODE_ATTRIBUTE_PERSON_ID = "person_id"
    NODE_ATTRIBUTE_PERSON_TYPE = "person_type"
    NODE_ATTRIBUTE_LIST = [
        NODE_ATTRIBUTE_PERSON_ID,
        NODE_ATTRIBUTE_PERSON_TYPE,
    ]
    
    # relation type roles
    VALID_RELATION_TYPE_ROLES = []
    VALID_RELATION_TYPE_ROLES.append( ContextBase.RELATION_ROLES_FROM )
    VALID_RELATION_TYPE_ROLES.append( ContextBase.RELATION_ROLES_TO )
    VALID_RELATION_TYPE_ROLES.append( ContextBase.RELATION_ROLES_THROUGH )

    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------


    def __init__( self ):

        # call parent's __init__()
        super( NetworkDataOutput, self ).__init__()

        # declare variables
        self.m_query_set = None
        self.output_type = NetworkDataOutput.NETWORK_DATA_FORMAT_DEFAULT
        self.data_format = NetworkDataOutput.NETWORK_DATA_FORMAT_DEFAULT
        self.data_output_type = NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_DEFAULT
        self.m_entity_dictionary = {}
        self.relation_map = {}
        self.include_row_and_column_headers = False
        
        # variables for outputting result as file
        self.mime_type = ""
        self.file_extension = ""
        
        # need a way to keep track of all the relation types an entity has been
        #     a part of, and what roles they played.
        self.m_entity_relation_type_summary_dict = {}

        # variable to hold master Entity list.
        self.m_master_entity_list = []

        # internal debug string
        self.debug = "NetworkDataOutput debug:\n\n"

        # store the current request
        self.m_network_data_request = None

        # set logger name (for LoggingHelper parent class: (LoggingHelper --> BasicRateLimited --> ContextBase).
        self.set_logger_name( self.LOGGER_NAME )
                
    #-- END method __init__() --#


    #---------------------------------------------------------------------------
    # instance methods, in alphabetical order
    #---------------------------------------------------------------------------


    def add_directed_relation( self, entity_from_id_IN, entity_to_id_IN ):

        """
            Method: add_directed_relation()

            Purpose: Accepts two Entity IDs.  For the FROM entity, goes into the
               nested connection map, grabs that entity's connection dictionary,
               and checks if the TO entity is in the map.  If so, grabs the
               counter for number of contacts and increments it by one.  If not,
               adds the entity and sets counter to 1.

            Preconditions: connection_map must be initialized to a dictionary.

            Params:
            - entity_from_id_IN - Entity ID of FROM entity.
            - entity_to_id_IN - Entity ID of TO entity.

            Returns:
            - string status message, either STATUS_OK if success, or
               STATUS_ERROR_PREFIX followed by descriptive error message.
        """

        # return reference
        status_OUT = NetworkDataOutput.STATUS_OK

        # declare variables
        me = "add_directed_relation"
        status_message = None
        my_relation_map = None
        entity_relations = None
        current_entity_count = -1
        updated_entity_count = -1

        # got FROM ID?
        if ( entity_from_id_IN is not None ):
        
            # got TO ID?
            if ( entity_to_id_IN is not None ):

                # got IDs.  retrieve relation_map.
                my_relation_map = self.get_relation_map()
    
                # got a map?
                if ( my_relation_map is not None ):
    
                    # look for FROM entity in map.
                    if entity_from_id_IN in my_relation_map:
    
                        # already there - grab their relations map.
                        entity_relations = my_relation_map[ entity_from_id_IN ]
    
                    else:
    
                        # not yet in connection map.  Create a dictionary to hold
                        #    their relations.
                        entity_relations = {}
    
                        # store it in the relation map
                        my_relation_map[ entity_from_id_IN ] = entity_relations
    
                    #- END check to see if entity has relations. --#
    
                    # is TO entity in relations map?
                    if entity_to_id_IN in entity_relations:
    
                        # yes.  Retrieve that entity's value, add one, and place
                        #    incremented value back in hash.
                        current_entity_count = entity_relations[ entity_to_id_IN ]
                        updated_entity_count = current_entity_count + 1
    
                    else: # not already connected.
    
                        # not in entity relations.  Set count to 1
                        updated_entity_count = 1
    
                    #-- END check to see if already are connected. --#
    
                    # update the count.
                    entity_relations[ entity_to_id_IN ] = updated_entity_count
    
                else:
                
                    # no relation map set.
                    status_message = "In {}(): ERROR - no nested relation map set.  should not be possible.  Doing nothing.  entity_from_id_IN: {}; entity_to_id_IN: {}".format( me, entity_from_id_IN, entity_to_id_IN )
                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                    status_OUT = "{}{}".format( self.STATUS_ERROR_PREFIX, status_message )
        
                #-- END sanity check to make sure we have a map. --#

            else:
            
                # no TO Entity ID set.
                status_message = "In {}(): ERROR - no TO Entity ID set.  Doing nothing. entity_from_id_IN: {}; entity_to_id_IN: {}".format( me, entity_from_id_IN, entity_to_id_IN )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                status_OUT = "{}{}".format( self.STATUS_ERROR_PREFIX, status_message )
    
            #-- END check of TO entity --#
            
        else:
        
            # no FROM entity ID set.
            status_message = "In {}(): ERROR - no FROM Entity ID set.  Doing nothing. entity_from_id_IN: {}; entity_to_id_IN: {}".format( me, entity_from_id_IN, entity_to_id_IN )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            status_OUT = "{}{}".format( self.STATUS_ERROR_PREFIX, status_message )

        #-- END check of FROM entity --# 

        if ( self.DEBUG_FLAG == True ):
            # output the author map
            self.debug += "\n\n*** in {}(), after adding relations, my_relation_map:\n{}\n\n".format( me, my_relation_map )
        #-- END DEBUG --#

        return status_OUT

    #-- END method add_directed_relation --#


    def add_reciprocal_relation( self, entity_1_id_IN, entity_2_id_IN ):

        """
            Method: add_reciprocal_relation()

            Purpose: Accepts two Entity IDs.  For each, goes into the nested
               connection map, grabs that Entity's connection dictionary, and
               checks if the other Entity is in the map.  If so, grabs the
               counter for number of contacts and increments it by one.  If not,
               adds the Entity and sets counter to 1.

            Preconditions: connection_map must be initialized to a dictionary.

            Params:
            - entity_1_id_IN - Entity ID of 1st Entity to connect.
            - entity_2_id_IN - Entity ID of 2nd Entity to connect.

            Returns:
            - string status message, either STATUS_OK if success, or
               STATUS_ERROR_PREFIX followed by descriptive error message.
        """

        # return reference
        status_OUT = NetworkDataOutput.STATUS_OK
        
        # declare variables
        me = "add_reciprocal_relation"
        status_message = None
        debug_flag = None
        my_logger = None
        debug_string = ""
        
        # initialize
        my_logger = self.get_logger()
        debug_flag = self.DEBUG_FLAG

        # got FROM ID?
        if ( entity_1_id_IN is not None ):
        
            # got TO ID?
            if ( entity_2_id_IN is not None ):

                if ( self.DEBUG_FLAG == True ):
    
                    # output message about having two values.
                    debug_string = "In " + me + ": got two IDs: " + str( entity_1_id_IN ) + "; " + str( entity_2_id_IN ) + "."
                    
                    # add to debug string?
                    self.debug += "\n\n" + debug_string + "\n\n"
                    
                    my_logger.debug( debug_string )
                                
                #-- END DEBUG --#
    
                # add directed relations from 1 to 2 and from 2 to 1.
                self.add_directed_relation( entity_1_id_IN, entity_2_id_IN )
                self.add_directed_relation( entity_2_id_IN, entity_1_id_IN )
    
                if ( self.DEBUG_FLAG == True ):
                    # output the relation map
                    self.debug += "\n\n*** in add_reciprocal_relation, after adding relations, relation_map:\n" + str( self.relation_map ) + "\n\n"
                #-- END DEBUG --#

            else:
            
                # no Entity 1 ID set.
                status_message = "In {}(): ERROR - no Entity 1 ID set.  Doing nothing. entity_1_id_IN: {}; entity_2_id_IN: {}".format( me, entity_1_id_IN, entity_2_id_IN )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                status_OUT = "{}{}".format( self.STATUS_ERROR_PREFIX, status_message )
    
            #-- END check of Entity 1 ID --#
            
        else:
        
            # no Entity 2 ID set.
            status_message = "In {}(): ERROR - no Entity 2 ID set.  Doing nothing. entity_1_id_IN: {}; entity_2_id_IN: {}".format( me, entity_1_id_IN, entity_2_id_IN )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            status_OUT = "{}{}".format( self.STATUS_ERROR_PREFIX, status_message )

        #-- END check of Entity 2 ID --# 

        return status_OUT

    #-- END method add_reciprocal_relation() --#


    def create_header_list( self ):

        """
            Method: create_header_list()

            Purpose: checks data_output_type, renders header list based on what
               data we are outputting.  Returns list of headers.

            Returns:
            - List of headers for our CSV document.
        """

        # return reference
        header_list_OUT = None

        # declare variables
        my_data_output_type = ""
        node_attribute_list = []
        current_attr_name = ""

        # get the data output type.
        my_data_output_type = self.data_output_type
        
        # only need to get list of labels if we are outputting network as well as attributes.

        # include network?
        if ( ( my_data_output_type == NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NETWORK )
            or ( my_data_output_type == NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_COLS )
            or ( my_data_output_type == NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_ROWS ) ):

            # yes.  Start with list of labels.
            header_list_OUT = self.create_label_list()
            
        else:
        
            # not outputting whole network.  Start with empty list.
            header_list_OUT = []
            
        #-- END check to see if outputting network. --#
        
        # add "id" to the beginning of list (header for column of labels that
        #    starts each row).
        header_list_OUT.insert( 0, "id" )
        
        # Are we outputting attributes in columns, either just attributes, or network plus attributes as columns?
        if ( ( my_data_output_type == NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_ATTRIBUTES )
            or ( my_data_output_type == NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_COLS ) ):

            # we are - add column headers for attributes - loop over NODE_ATTRIBUTE_LIST.
            node_attribute_list = NetworkDataOutput.NODE_ATTRIBUTE_LIST
            for current_attr_name in node_attribute_list:
            
                # add the attribute name to the list.
                header_list_OUT.append( current_attr_name )
            
            #-- END loop over attributes
            
        #-- END check to see if output attributes as columns --#

        return header_list_OUT

    #-- END method create_header_list --#


    def create_label_list( self, quote_character_IN = '' ):

        """
            Method: create_label_list()

            Purpose: retrieves the master Entity list from the instance, uses it
               to output a list of Entity labels.  Each Entity's label consists
               of: "<entity_counter>__Entity-<entity_id>"
               WHERE:
               - <entity_counter> is the simple integer count of Entities in list, incremented as each Entity is added.
               - <entity_id> is the ID of the Entity's Entity record in the system.

            Returns:
            - list of string representation of labels for each row in network.
        """

        # return reference
        list_OUT = []

        # declare variables
        master_list = None
        my_label = ''
        current_entity_id = -1
        entity_count = -1
        current_label = ""
        current_value = ''

        # get master list
        master_list = self.get_master_entity_list()

        # got something?
        if ( master_list ):

            # loop over sorted entity list, building label line for each entity.
            entity_count = 0
            for current_entity_id in sorted( master_list ):

                entity_count += 1
                
                # get label
                current_label = self.get_entity_label( current_entity_id )

                # append the Entity's row to the output string.
                current_value = str( entity_count ) + "__" + current_label

                # do we want quotes?
                if ( quote_character_IN != '' ):

                    # yes.  Add quotes around the value.
                    current_value = quote_character_IN + current_value + quote_character_IN

                #-- END quote values check --#

                # append to output
                list_OUT.append( current_value )

            #-- END loop over Entities. --#

        #-- END check to make sure we have an Entity list. --#

        return list_OUT

    #-- END method create_label_list --#


    def create_entity_id_list( self, as_string_IN = True ):

        """
            Method: create_entity_id_list()

            Purpose: Create a list of Entity IDs for the Entities in master
               list.

            Preconditions: Master Entity list must be present.

            Params: none

            Returns:
            - list_OUT - list of Entity IDs, in sorted master Entity list order.
        """

        # return reference
        list_OUT = []

        # declare variables
        entity_list = None
        current_entity_id = -1
        output_entity_id = -1

        # get master list
        entity_list = self.get_master_entity_list()

        # got it?
        if ( entity_list ):

            # loop over the master list.
            for current_entity_id in sorted( entity_list ):
            
                # store in output variable
                output_entity_id = current_entity_id

                # append as a string?
                if ( as_string_IN == True ):

                    output_entity_id = str( output_entity_id )

                #-- END check to see if append as string --#

                # append to output list.
                list_OUT.append( output_entity_id )

            #-- END loop over Entities --#

        #-- END check to make sure we have list. --#

        return list_OUT

    #-- END method create_entity_id_list --#


    def do_output_attribute_columns( self ):

        """
            Method: do_output_attribute_columns()

            Purpose: Examines self.data_output_type to see if we are to output
               node attribute rows.  If so, returns True, if not, returns False.
               Values that mean we output attribute columns:
               - NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_ATTRIBUTES
               - NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_COLS

            Returns:
            - boolean - If we are to output attribute columns, returns True.  If not, returns False.
        """

        # return reference
        do_it_OUT = False

        # declare variables
        my_data_output_type = ""

        # get data output type
        my_data_output_type = self.data_output_type
        
        # do the output?
        if ( ( my_data_output_type == NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_ATTRIBUTES )
            or ( my_data_output_type == NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_COLS ) ):

            # yes.
            do_it_OUT = True

        else:
        
            # no.
            do_it_OUT = False
    
        #-- END check to see if include network matrix --#

        return do_it_OUT

    #-- END method do_output_attribute_columns() --#


    def do_output_attribute_rows( self ):

        """
            Method: do_output_attribute_rows()

            Purpose: Examines self.data_output_type to see if we are to output
               node attribute rows.  If so, returns True, if not, returns False.
               Values that mean we output attribute rows:
               - NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_ROWS

            Returns:
            - boolean - If we are to output attribute rows, returns True.  If not, returns False.
        """

        # return reference
        do_it_OUT = False

        # declare variables
        my_data_output_type = ""

        # get data output type
        my_data_output_type = self.data_output_type
        
        # do the output?
        if ( my_data_output_type == NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_ROWS ):

            # yes.
            do_it_OUT = True

        else:
        
            # no.
            do_it_OUT = False
    
        #-- END check to see if include network matrix --#

        return do_it_OUT

    #-- END method do_output_attribute_rows() --#


    def do_output_network( self ):

        """
            Method: do_output_network()

            Purpose: Examines self.data_output_type to see if we are to output
               network data.  If so, returns True, if not, returns False.
               Values that mean we output network data:
               - NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NETWORK
               - NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_COLS
               - NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_ROWS

            Returns:
            - boolean - If we are to output network data, returns True.  If not, returns False.
        """

        # return reference
        do_it_OUT = False

        # declare variables
        my_data_output_type = ""

        # get data output type
        my_data_output_type = self.data_output_type
        
        # include network?
        if ( ( my_data_output_type == NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NETWORK )
            or ( my_data_output_type == NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_COLS )
            or ( my_data_output_type == NetworkDataOutput.NETWORK_DATA_OUTPUT_TYPE_NET_AND_ATTR_ROWS ) ):

            # yes, we output network.
            do_it_OUT = True

        else:
        
            # no, not outputting network.
            do_it_OUT = False
    
        #-- END check to see if include network matrix --#

        return do_it_OUT

    #-- END method do_output_network() --#


    def generate_master_entity_list( self, is_sorted_IN = True ):

        """
            Method: generate_master_entity_list()

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
        my_logger = None
        debug_string = ""
        entity_dict = None
        entity_ids_list = None
        current_entity_id = None
        entity_id_to_relation_details_dict = None
        master_entity_relations_details = None
        merged_entity_id_list = None

        # initialize logger
        my_logger = self.get_logger()

        # retrieve the Entity dictionary
        entity_dict = self.get_entity_dictionary()

        my_logger.debug( "In " + me + ": len( entity_dict ) = " + str( len( entity_dict ) ) )

        # grab list of keys from self.m_entity_dictionary.
        entity_ids_list = entity_dict.keys()

        # make a dictionary that maps entities from entity_dictionary to
        #     relation details...
        entity_id_to_relation_details_dict = {}
        for current_entity_id in entity_ids_list:
        
            # to start, add all Entities to dictionary with no details.
            entity_id_to_relation_details_dict[ current_entity_id ] = {}
            
        #-- END loop over IDs from dictionary. --#

        # update or add entities and corresponding type details from the nested
        #    self.m_entity_relation_type_summary_dict.
        master_entity_relations_details = self.get_entity_relation_type_summary_dict()
        entity_id_to_relation_details_dict.update( master_entity_relations_details )

        my_logger.debug( "In {}(): after entity_id_to_relation_details_dict.update( master_entity_relations_details ), len( entity_id_to_relation_details_dict ) = {}".format( me, len( entity_id_to_relation_details_dict ) ) )

        # ! TODO - store this in the entity_relation_type_summary_dict?

        # grab the ID list from this merged dictionary, sort it, and use it
        #    as your list of entities to iterate over as you create actual
        #    output.
        merged_entity_id_list = list( six.viewkeys( entity_id_to_relation_details_dict ) )
        
        # do we want it sorted?
        if ( is_sorted_IN == True ):
        
            # we want it sorted.
            merged_entity_id_list = sorted( merged_entity_id_list )
        
        #-- END check to see if we want the list sorted. --#

        # save this as the master entity list.
        self.set_master_entity_list( merged_entity_id_list )

        list_OUT = self.get_master_entity_list()
        
        my_logger.debug( "In {}: len( self.m_master_entity_list ) = {}".format( me, len( list_OUT ) ) )

        return list_OUT

    #-- END method generate_master_entity_list() --#


    def get_entity_dictionary( self ):
        
        # return reference
        value_OUT = None
        
        # see if already stored.
        value_OUT = self.m_entity_dictionary
                
        return value_OUT
    
    #-- END method get_entity_dictionary() --#
    

    def get_entity_relation_type_summary_dict( self ):
        
        # return reference
        value_OUT = None
        
        # see if already stored.
        value_OUT = self.m_entity_relation_type_summary_dict
                
        return value_OUT
    
    #-- END method get_entity_relation_type_summary_dict() --#
    

    def get_master_entity_list( self, is_sorted_IN = True ):

        """
            Method: get_master_entity_list()

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
        is_ok = True

        # retrieve master Entity list
        list_OUT = self.get_master_entity_list()

        if ( list_OUT ):

            if ( len( list_OUT ) < 1 ):

                # nothing in list.  Not OK.
                is_ok = False

            #-- END check to see if anything in list.

        else:

            # no list.  not OK.
            is_ok = False

        #-- END check to see if stored list is OK --#

        # is stored list OK?
        if ( is_ok == False ):

            # not OK.  Try generating list.
            list_OUT = self.generate_master_entity_list( is_sorted_IN )

        #-- END check if list is OK. --#
        
        return list_OUT

    #-- END method get_master_entity_list() --#


    def get_network_data_request( self ):
        
        # return reference
        value_OUT = None
        
        # see if already stored.
        value_OUT = self.m_network_data_request
                
        return value_OUT
    
    #-- END method get_network_data_request() --#
    

    def get_entity_label( self, entity_id_IN ):

        """
            Method: get_entity_label()

            Purpose: accepts an Entity ID, creates label "Entity-<id>".

            Params:
            - entity_id_IN - ID of Entity we want a label for.

            Returns:
            - String - label for the current Entity.
        """

        # return reference
        value_OUT = ""

        # got a value?
        if ( entity_id_IN ):

            # make a label.
            value_OUT = "Entity-{}".format( entity_id_IN )

        #-- END check to see if we have an Entity ID --#

        return value_OUT

    #-- END method get_entity_label() --#


    def get_query_set( self ):
        
        # return reference
        value_OUT = None
        
        # see if already stored.
        value_OUT = self.m_query_set
                
        return value_OUT
    
    #-- END method get_query_set() --#
    

    def get_relation_map( self ):

        """
            Method: get_relation_map()

            Purpose: retrieves nested relation map.  Eventually could be
               used to manage access to multiple types of relations.

            Returns:
            - dictionary - dictionary that maps Entity IDs to their connections
               to other Entities.
        """

        # return reference
        value_OUT = ''

        # grab map
        value_OUT = self.relation_map

        return value_OUT

    #-- END method get_relation_map() --#


    def get_relations_for_entity( self, entity_id_IN ):

        """
            Method: get_relations_for_entity()

            Purpose: retrieves nested relation map.  Eventually could be
               used to manage access to multiple types of relations.

            Returns:
            - dictionary - dictionary that maps Entity IDs to their connections
               to other Entities.
        """

        # return reference
        value_OUT = {}

        # declare variables
        relation_dict = None

        # got an ID?
        if ( entity_id_IN != '' ):

            # grab map
            relation_dict = self.get_relation_map()

            # anything there?
            if ( relation_dict ):

                # yes.  Check if ID is a key.
                if entity_id_IN in relation_dict:

                    # it is.  Return what is there.
                    value_OUT = relation_dict[ entity_id_IN ]

                else:

                    # no relations.  Return empty dictionary.
                    value_OUT = {}

                #-- END check to see if Entity has any relations.

            #-- END check to make sure dict is populated. --#

        #-- END check to see if ID passed in. --#

        return value_OUT

    #-- END method get_relations_for_entity() --#


    def initialize_from_request( self, network_data_request_IN ):

        # declare variables
        output_type_IN = ''
        data_output_type_IN = ''

        # retrieve info.
        output_type_IN = network_data_request_IN.get_output_type()
        data_output_type_IN = network_data_request_IN.get_output_structure()

        # store
        self.set_output_type( output_type_IN )
        self.data_output_type = data_output_type_IN
        
        # and store the request, as well, for reference.
        self.set_network_data_request( network_data_request_IN )

    #-- END method initialize_from_request() --#


    def render( self ):

        """
            Assumes query set of Entity_Relation instances has been placed in
                this instance.  Uses the query set to output delimited data in
                the format specified in the output_type instance variable.

            Preconditions: assumes that we have a query set of Entity_Relations
                stored in the instance.  If not, does nothing, returns empty
                string.

            Postconditions: returns the delimited network data, each column separated by two spaces, in a string.

            Parameters - all inputs are stored in instance variables:
            - self.m_query_set - Query set of articles for which we want to create network data.
            - self.m_entity_dictionary - QuerySet of Entities we want included in our network (can include people not mentioned in a relation, in case we want to include all entities from two different time periods, for example).
            - self.inclusion_params

            Returns:
            - String - delimited output (two spaces separate each column value in a row) for the network described by the articles selected based on the parameters passed in.
        """

        # return reference
        network_data_OUT = None

        # declare variables
        me = "render"
        debug_flag = None
        status_message = None
        my_logger = None
        debug_string = ""
        entity_relation_query_set = None
        entity_dict = None
        entity_relation_counter = 0
        current_entity_relation = None
        from_entity = None
        to_entity = None
        from_entity_id = None
        to_entity_id = None
        is_directed = None
        relation_type = None
        relation_type_slug = None
        relation_role = None
        result_status = None

        # initialize
        debug_flag = self.DEBUG_FLAG
        my_logger = self.get_logger()

        # start by grabbing entity dict, Entiry_Relation QuerySet.
        entity_relation_query_set = self.get_query_set()
        entity_dict = self.get_entity_dictionary()

        # make sure each of these has something in it.
        if ( entity_relation_query_set is not None ):
        
            if ( entity_dict is not None ):

                #--------------------------------------------------------------------
                # ! ----> create ties
                #--------------------------------------------------------------------
                
                # loop over the Entity_Relations.
                for current_entity_relation in entity_relation_query_set:
    
                    entity_relation_counter += 1
    
                    if ( self.DEBUG_FLAG == True ):
    
                        # output message about connectedness of source.
                        debug_string = "In " + me + ": +++ Current Entity_Relation = " + str( current_entity_relation.id ) + " +++"
                        
                        # add to debug string?
                        self.debug += "\n\n" + debug_string + "\n\n"
                        
                        my_logger.debug( debug_string )
    
                    #-- END DEBUG --#
    
                    # retrieve FROM and TO entities, make sure they are both
                    #     populated.
                    from_entity = current_entity_relation.relation_from
                    to_entity = current_entity_relation.relation_to
                    
                    # got FROM?
                    if ( from_entity is not None ):
                    
                        # got TO?
                        if ( to_entity is not None ):

                            # got FROM and TO.
                            from_entity_id = from_entity.id
                            to_entity_id = to_entity.id

                            # Is it directed?                        
                            is_directed = current_entity_relation.directed
                            if ( is_directed == True ):
                            
                                # create tie from FROM to TO.
                                result_status = self.add_directed_relation( from_entity_id, to_entity_id )
                            
                            elif ( is_directed == False ):
                            
                                # create tie from FROM to TO.
                                result_status = self.add_reciprocal_relation( from_entity_id, to_entity_id )
                            
                            else:
                            
                                # relation is neither directed or not directed...
                                status_message = "In {}(): ERROR - Boolean relation.directed is neither True nor False.  Ummm...  Doing nothing.  Relation: {}".format( me, current_entity_relation )
                                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                    
                            #-- END check to see if directed --#
                            
                            # status OK?
                            if ( result_status == NetworkDataOutput.STATUS_OK ):
                            
                                # ! --------> update relation type counts for entities
                                
                                # got relation type?
                                relation_type = current_entity_relation.relation_type
                                if ( relation_type is not None ):

                                    # got a type.  Get slug.
                                    relation_type_slug = relation_type.slug
                                    
                                    # update FROM entity's relation type details
                                    self.update_entity_relations_details( from_entity_id, relation_type_slug, ContextBase.RELATION_ROLES_FROM, current_entity_relation )
                                    
                                    # update TO entity's relation type details
                                    self.update_entity_relations_details( to_entity_id, relation_type_slug, ContextBase.RELATION_ROLES_TO, current_entity_relation )
                                
                                else:
                                
                                    # no formal relation type, nothing to do here.
                                    pass
                                    
                                #-- END check to see if relation type. --#
                        
                        else:
                        
                            # no TO Entity set.
                            status_message = "In {}(): ERROR - no TO Entity set.  Doing nothing.  Relation: {}".format( me, current_entity_relation )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                
                        #-- END check of TO entity --#
                        
                    else:
                    
                        # no FROM entity set.
                        status_message = "In {}(): ERROR - no FROM Entity set.  Doing nothing.  Relation: {}".format( me, current_entity_relation )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
                    #-- END check of FROM entity --# 
                    
                #-- END loop over Entity_Relation instances to be processed. --#
                    
                #---------------------------------------------------------------------------
                # ! ----> generate_master_entity_list (list of network matrix rows/columns)
                #---------------------------------------------------------------------------
                
                # now that all relations are mapped, need to build our master
                #     Entity list, so we can loop to build out the network.  All
                #     entities who need to be included should be in the
                #     self.m_entity_dictionary passed in.  To be sure, we can
                #     make a copy that places source type of unknown as value
                #     for all, then update with entity relations details, so we
                #     make sure all entities included in the network are in the
                #     dict.
                self.generate_master_entity_list()
    
                if ( self.DEBUG_FLAG == True ):
                    self.debug += "\n\nEntity Dictionary:\n{}\n\n".format( self.get_entity_dictionary() )
                    self.debug += "\n\nMaster entity list:\n{}\n\n".format( self.get_master_entity_list() )
                #-- END DEBUG --#
    
                #--------------------------------------------------------------------
                # ! ----> render network data based on people and ties.
                #--------------------------------------------------------------------
                
                # ! TODO - render_network_data()
                network_data_OUT += self.render_network_data()
            
            else:
            
                # no m_entity_dictionary set.
                status_message = "In {}(): ERROR - no m_entity_dictionary set.  Doing nothing.".format( me )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                network_data_OUT = None 
    
            #-- END check to see if entity dictionary --#
        
        else:
        
            # no Entity_Relation QuerySet present.
            status_message = "In {}(): ERROR - no Entity_Relation QuerySet present.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            network_data_OUT = None 

        #-- END check to make sure we have the data we need. --#

        return network_data_OUT

    #-- END render() --#


    @abstractmethod
    def render_network_data( self ):

        '''
        Invoked from render(), after ties have been generated based on articles
           and people passed in.  Returns a string.  This string can contain the
           rendered data (CSV file, etc.), or it can just contain a status
           message if the data is rendered to a file or a database.
        '''

        pass

    #-- END abstract method render_network_data() --#
    

    def set_entity_dictionary( self, value_IN ):

        """
            Method: set_entity_dictionary()

            Purpose: accepts a dictionary, with entity ID as key, values...
               undetermined at this time, stores it in the instance.

            Params:
            - value_IN - Python dictionary with Entity IDs as keys.
        """

        # return value
        value_OUT = None

        # store value
        self.m_entity_dictionary = value_IN
        
        # sanity check - retrieve and return.
        value_OUT = self.get_entity_dictionary()
        
        return value_OUT

    #-- END method set_entity_dictionary() --#


    def set_entity_relation_type_summary_dict( self, value_IN ):

        """
            Method: set_entity_relation_type_summary_dict()

            Purpose: accepts a dictionary, with entity ID as key, values are a
                map of relation types for each Entity that maps each relation
                type an Entity has been mentioned in to dictionary of FROM, TO,
                and THROUGH, each mapped to counts of the times the Entity was
                in each role for a given relation type.

            Params:
            - value_IN - Python dictionary with entity IDs as keys.
        """

        # return value
        value_OUT = None

        # store value
        self.m_entity_relation_type_summary_dict = value_IN
        
        # sanity check - retrieve and return.
        value_OUT = self.get_entity_relation_type_summary_dict()
        
        return value_OUT

    #-- END method set_entity_relation_type_summary_dict() --#


    def set_master_entity_list( self, value_IN ):

        """
            Method: set_master_entity_list()

            Purpose: accepts a list, stores it in the instance.

            Params:
            - value_IN - list of IDs of all entities in current network data set.
        """

        # return value
        value_OUT = None

        # store value
        self.m_master_entity_list = value_IN
        
        # sanity check - retrieve and return.
        value_OUT = self.get_master_entity_list()
        
        return value_OUT

    #-- END method set_master_entity_list() --#


    def set_output_type( self, value_IN ):

        """
            Method: set_output_type()

            Purpose: accepts an output type, stores it in instance.

            Params:
            - value_IN - String output type value.
        """

        # got a value?
        if ( value_IN ):

            # store value
            self.output_type = value_IN
            self.data_format = value_IN

        #-- END check to see if we have a value --#

    #-- END method set_output_type() --#


    def set_query_set( self, value_IN ):

        """
            Method: set_request()

            Purpose: accepts a query set, stores it in instance.

            Params:
            - value_IN - django QuerySet instance that contains Entity_Relation
               instances from which we are to build our network data.
        """

        # return value
        value_OUT = None

        # store value
        self.m_query_set = value_IN
        
        # sanity check - retrieve and return.
        value_OUT = self.get_query_set()
        
        return value_OUT

    #-- END method set_query_set() --#


    def set_network_data_request( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_network_data_request = value_IN
        
        # return it
        value_OUT = self.get_network_data_request()
        
        return value_OUT
    
    #-- END method set_network_data_request() --#


    def update_entity_relations_details( self,
                                         entity_id_IN,
                                         relation_type_slug_IN,
                                         relation_role_IN,
                                         relation_instance_IN = None ):

        """
            Method: update_entity_relations_details()

            Purpose: accepts an entity ID, a relation type the entity is a part
                of, and the role they play in the relation type, one of:
                - ContextBase.RELATION_ROLES_FROM ( = "FROM")
                - ContextBase.RELATION_ROLES_TO ( = "TO")
                - ContextBase.RELATION_ROLES_THROUGH ( = "THROUGH" )
                
            Checks to see if entity is in dict already. If not, adds them,
                creates dictionary to hold role types mapped to a nested
                dictionary of counts of each time they have each role for that
                type.  Then, checks if relation type passed in is present.  If
                not, adds a FROM/TO/THROUGH map for that type.  Then, based on
                role, updates the counter for the role passed in for the type
                passed in.
                
            Postconditions: returns the updated count for the relation type
                and role.

            Params:
            - entity_id_IN - ID of Entity whose type we are updating.
            - relation_type_slug_IN - slug of relation type we are processing.
            - relation_role_IN - ROLE the entity was assigned in the relation (FROM, TO, THROUGH)
            - relation_instance_IN - optional Entity_Relation instance, in case we want to keep track eventually.
        """

        # return reference
        role_count_OUT = None
        
        # declare variables
        me = "update_entity_relations_details"
        debug_flag = None
        status_message = None
        entity_to_relation_type_map = None
        entity_relation_type_map = None
        relation_type_role_map = None
        role_count = None
        
        # init
        debug_flag = self.DEBUG_FLAG

        # got entity ID?
        if ( entity_id_IN is not None ):

            # got a relation type?
            if ( relation_type_slug_IN is not None ):
            
                # got a role?
                if ( relation_role_IN is not None ):

                    # see if entity is already in dict.
                    entity_to_relation_type_map = self.get_entity_relation_type_summary_dict()
    
                    # present in dict?
                    if entity_id_IN not in entity_to_relation_type_map:
                    
                        # no.  Set them up.
                        entity_to_relation_type_map[ entity_id_IN ] = {}
                        
                    #-- END check to see if entity in dict. --#
                    
                    # retrieve entity's role map
                    entity_relation_type_map = entity_to_relation_type_map.get( entity_id_IN, None )
                    
                    # got a map?
                    if ( entity_relation_type_map is not None ):
    
                        # yes.  Get role map for relation type.
                        relation_type_role_map = entity_relation_type_map.get( relation_type_slug_IN, None )

                        # is there a role map?  If not, first encounter of this
                        #     role.
                        if ( relation_type_role_map is None ):
                        
                            # create new role map.
                            relation_type_role_map = {}
                            relation_type_role_map[ ContextBase.RELATION_ROLES_FROM ] = 0
                            relation_type_role_map[ ContextBase.RELATION_ROLES_TO ] = 0
                            relation_type_role_map[ ContextBase.RELATION_ROLES_THROUGH ] = 0
                            
                            # store it
                            entity_relation_type_map[ relation_type_slug_IN ] = relation_type_role_map
                            
                        #-- END check to see if role map present. --#
                        
                        # based on role, update the map.  Is it a valid role?
                        if ( relation_role_IN in self.VALID_RELATION_TYPE_ROLES ):
                            
                            # valid role, update count for that role.
                            role_count = entity_relation_type_map.get( relation_role_IN, None )
                            
                            # got something?
                            if ( role_count is not None ):

                                # increment, store.
                                role_count += 1
                                
                            else:
                            
                                # error.  valid role, but not in map.  set to 1.
                                role_count = 1
                                
                                # DEBUG - should never get here with no role
                                #     count.  Should be 0 or greater.
                                status_message = "In {}(): DEBUG - role count retrieved was empty, should never be.  Should either be 0 or greater.  Strange.  entity_id_IN: {}; relation_type_slug_IN: {}; relation_role_IN: {}; relation_instance_IN: {}.  entity_relation_type_map: {}".format( me, entity_id_IN, relation_type_slug_IN, relation_role_IN, relation_instance_IN, entity_relation_type_map )
                                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                                role_count_IN = None
                                
                            #-- END Check to see if count set --#

                            # store the updated count, and return it.
                            entity_relation_type_map[ relation_role_IN ] = role_count
                            role_count_OUT = role_count
                            
                        else:
                        
                            # unknown role, error.
                            status_message = "In {}(): ERROR - role passed in is not valid.  entity_id_IN: {}; relation_type_slug_IN: {}; relation_role_IN: {}; relation_instance_IN: {}.  Doing nothing. Valid roles: {}".format( me, entity_id_IN, relation_type_slug_IN, relation_role_IN, relation_instance_IN, self.VALID_RELATION_TYPE_ROLES )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                            role_count_IN = None
                            
                        #-- END check if valid role. --#
    
                    else: # still no relation type map...
    
                        # no relation type to role types and counts map... strange.
                        status_message = "In {}(): ERROR - no map of relation type to roles and counts for entity.  Should have been created above, or already exist.  entity_id_IN: {}; relation_type_slug_IN: {}; relation_role_IN: {}; relation_instance_IN: {}.  Doing nothing.".format( me, entity_id_IN, relation_type_slug_IN, relation_role_IN, relation_instance_IN )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                        role_count_IN = None
                            
                    #-- END check to see if map of relation type to roles and counts for entity --#

                else:
                
                    # no relation type passed in.
                    status_message = "In {}(): ERROR - no relation type role passed in. entity_id_IN: {}; relation_type_slug_IN: {}; relation_role_IN: {}; relation_instance_IN: {}.  Doing nothing.".format( me, entity_id_IN, relation_type_slug_IN, relation_role_IN, relation_instance_IN )
                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                    role_count_IN = None
                        
                #-- END check to see if we have a role --#
        
            else:
            
                # no relation type passed in.
                status_message = "In {}(): ERROR - no relation type passed in. entity_id_IN: {}; relation_type_slug_IN: {}; relation_role_IN: {}; relation_instance_IN: {}.  Doing nothing.".format( me, entity_id_IN, relation_type_slug_IN, relation_role_IN, relation_instance_IN )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                role_count_IN = None
    
            #-- END check to see if we have a relation type --#

        else:
        
            # no entity ID passed in.
            status_message = "In {}(): ERROR - no entity ID passed in. entity_id_IN: {}; relation_type_slug_IN: {}; relation_role_IN: {}; relation_instance_IN: {}.  Doing nothing.".format( me, entity_id_IN, relation_type_slug_IN, relation_role_IN, relation_instance_IN )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            role_count_IN = None

        #-- END check to see if we have entity ID --#
        
        return role_count_OUT

    #-- END method update_entity_relations_details() --#


#-- END class NetworkDataOutput --#