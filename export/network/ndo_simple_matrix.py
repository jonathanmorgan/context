'''
Copyright 2014 Jonathan Morgan

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

#import copy
import logging

# six imports - support Pythons 2 and 3
import six

# Django DB classes, just to play with...
#from django.db.models import Count # for aggregating counts of authors, sources.
#from django.db.models import Max   # for getting max value of author, source counts.

# parent abstract class.
from context.export.network.network_data_output import NetworkDataOutput

#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class NDO_SimpleMatrix( NetworkDataOutput ):

    
    #---------------------------------------------------------------------------
    # CONSTANTS-ish
    #---------------------------------------------------------------------------

    DEBUG_FLAG = True
    LOGGER_NAME = "context.export.network.ndo_simple_matrix.NDO_SimpleMatrix"
    ME = LOGGER_NAME

    # output constants
    OUTPUT_END_OF_LINE = "\n"
    OUTPUT_DEFAULT_COLUMN_SEPARATOR = "  "
    
    # output type
    MY_OUTPUT_FORMAT = NetworkDataOutput.NETWORK_DATA_FORMAT_SIMPLE_MATRIX


    #---------------------------------------------------------------------------
    # instance variables
    #---------------------------------------------------------------------------

    
    column_separator = OUTPUT_DEFAULT_COLUMN_SEPARATOR


    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------


    def __init__( self ):

        # call parent's __init__() - I think...
        super( NDO_SimpleMatrix, self ).__init__()

        # declare variables
        self.column_separator = self.OUTPUT_DEFAULT_COLUMN_SEPARATOR

        # override things set in parent.
        self.set_output_format( self.MY_OUTPUT_FORMAT )
        self.debug = "{} debug:\n\n".format( self.ME )
        
        # variables for outputting result as file
        self.mime_type = "text/plain"
        self.file_extension = "txt"

    #-- END method __init__() --#


    #---------------------------------------------------------------------------
    # instance methods, in alphabetical order
    #---------------------------------------------------------------------------


    def create_label_string( self, delimiter_IN = OUTPUT_END_OF_LINE, quote_character_IN = '' ):

        """
            Method: create_label_string()

            Purpose: retrieves the master entity list from the instance, uses it
               to output a list of the entity IDS and their source types, one to
               a line, that could be pasted into a column next to the attributes
               or data to make it more readily understandable for someone
               eye-balling it.  Each entity's label consists of:
               "<entity_counter>__<entity_id>"
               WHERE:
               - <entity_counter> is the simple integer count of entities in list, incremented as each entity is added.
               - <entity_id> is the ID of the entity's Entity record in the system.

            Returns:
            - string representation of labels for each row in network and attributes.
        """

        # return reference
        string_OUT = ""

        # declare variables
        master_list = None
        my_label = ''
        current_entity_id = -1
        entity_count = -1
        current_type = ''
        current_type_id = -1
        current_label = ""
        current_value = ''
        delimiter = delimiter_IN

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

                # append the entity's row to the output string.
                current_value = str( entity_count ) + "__" + current_label

                # do we want quotes?
                if ( quote_character_IN != '' ):

                    # yes.  Add quotes around the value.
                    current_value = quote_character_IN + current_value + quote_character_IN

                #-- END quote values check --#

                # append to output
                string_OUT += current_value + delimiter

            #-- END loop over entities.

        #-- END check to make sure we have a entity list. --#

        return string_OUT

    #-- END method create_label_string --#


    def create_network_string( self ):

        """
            Method: create_network_string()

            Purpose: retrieves the master entity list from the instance, uses it
               to output a square matrix where rows and columns are entities, by
               entity ID, and the value at the intersection between two entities
               is the number of time they were linked in articles during the
               time period that the network was drawn from.

            Returns:
            - string representation of network.
        """

        # return reference
        network_string_OUT = ""

        # declare variables
        master_list = None
        my_label = ''
        current_entity_id = -1
        end_of_line = self.OUTPUT_END_OF_LINE

        # get master list
        master_list = self.get_master_entity_list()

        # got something?
        if ( master_list ):

            # loop over sorted entity list, calling method to output network
            #    row for each entity.
            for current_entity_id in sorted( master_list ):

                # append the entity's row to the output string.
                network_string_OUT += self.create_entity_row_string( current_entity_id ) + end_of_line

            #-- END loop over entities. --#

        #-- END check to make sure we have a entity list. --#

        return network_string_OUT

    #-- END method create_network_string --#


    def create_entity_row_string( self, entity_id_IN ):

        """
            Method: create_entity_row_string()

            Purpose: retrieves the master entity list from the instance, uses it
                to output a square matrix where rows and columns are entities,
                by entity ID, and the value at the intersection between two
                entities is the number of time they were linked in the selected
                Entity_Relation instances the network was drawn from.

            Returns:
            - string representation of network.
        """

        # return reference
        string_OUT = ""

        # declare variables
        master_list = None
        current_entity_relations = None
        current_other_id = -1
        current_other_count = -1
        delimiter = self.column_separator

        # get entity ID?
        if ( entity_id_IN ):

            # get master list
            master_list = self.get_master_entity_list()

            # get relations for this entity.
            current_entity_relations = self.get_relations_for_entity( entity_id_IN )

            # loop over master list, checking for relations with each entity.
            for current_other_id in sorted( master_list ):

                # try to retrieve relation count from relations
                if current_other_id in current_entity_relations:

                    # they are related.  Get count.
                    current_other_count = current_entity_relations[ current_other_id ]

                else:

                    # no relation.  Set current count to 0
                    current_other_count = 0

                #-- END check to see if related.

                # output the count for the current entity.
                string_OUT += delimiter + str( current_other_count )

            #-- END loop over master list --#

        #-- END check to make sure we have a entity --#

        return string_OUT

    #-- END method create_entity_row_string --#


    def create_entity_relation_types_attribute_string( self ):

        '''
            Method: create_entity_relation_types_attribute_string()

            Purpose: pulls in all relation types, then outputs a list of counts
                per entity-->type-->role of times the entity had the role for
                a particular relation type.  Will result in many lists, 3 for
                each relation type (FROM, TO, THROUGH).  For use in assigning
                entity type attributes to the corresponding nodes.

            Preconditions: Master entity list must be present.

            Params: none

            Returns:
            - string_OUT - lists of roles for each relation type, with a count of number of times each entity was in that role for that relation type, in sorted master entity list order.
        '''

        # return reference
        string_OUT = ""

        # declare variables
        me = "create_entity_relation_types_attribute_string"
        debug_flag = None
        status_message = None
        relation_type_slug_to_roles_map = None
        sorted_slug_list = None
        role_list = None
        current_slug = None
        role_to_value_list_map = None
        current_role = None
        value_list = None
        string_value_list = None
        attribute_label = None
        
        # initialize
        debug_flag = self.DEBUG_FLAG

        # first, retrieve the values.
        relation_type_slug_to_roles_map = self.create_all_relation_type_values_lists()
        
        # got anything?
        if ( relation_type_slug_to_roles_map is not None ):
        
            # get list of slugs, sort alphabetically
            sorted_slug_list = list( six.viewkeys( relation_type_slug_to_roles_map ) )
            sorted_slug_list.sort()
            
            # get role list
            role_list = self.VALID_RELATION_TYPE_ROLES
            
            # loop over slugs
            for current_slug in sorted_slug_list:
            
                # retrieve per-role value lists for this slug
                role_to_value_list_map = relation_type_slug_to_roles_map.get( current_slug, None )
                
                if ( role_to_value_list_map is not None ):
                
                    # loop over roles
                    for current_role in role_list:
                    
                        # retrieve value list
                        value_list = role_to_value_list_map.get( current_role, None )
                        
                        # got anything?
                        if ( value_list is not None ):
                        
                            # build row label
                            attribute_label = "{}-{}".format( current_slug, current_role )
                            
                            # output the name of this attribute
                            string_OUT += "{}\n".format( attribute_label )

                            # join the list into a string, separated by newlines.
                            string_value_list = [ str( i ) for i in value_list ]
                            string_OUT += "\n".join( string_value_list )
            
                            # add two newlines to the end.
                            string_OUT += "\n\n"

                        else:
                        
                            # No value list for relation type slug+role
                            status_message = "In {}(): WARNING - No value list for relation type slug: {}; role: {}.  No attribute added for this type and role.".format( me, current_slug, current_role )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.WARNING )
                            
                        #-- END check to see if list for role --#
                        
                    #-- END loop over roles. --#
                
                else:
                
                    # No role-to-values map relation type slug
                    status_message = "In {}(): WARNING - No role-to-values map for relation type slug: {}.  No attributes added for this type.".format( me, current_slug )
                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.WARNING )
                        
                #-- END check to see if role-to-values map for slug --#
                    
            #-- END loop over relation type slugs --#
            
        else:
        
            # no slug passed in, can't do anything.
            status_message = "In {}(): ERROR - Call to self.create_all_relation_type_values_lists() returned None.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
        
        #-- END check to see if create list method returned anything --#

        return string_OUT

    #-- END method create_entity_relation_types_attribute_string --#


    def create_entity_ids_and_traits_attribute_string( self ):

        '''
            Method: create_entity_ids_and_traits_attribute_string()

            Purpose: retrieves Entity ids and traits header list.  For each
                header value, loops over entities, uses traits stored in request
                to create a list of values for each.

            Preconditions: Master entity list must be present, and in request,
                process_entities() must have been called.

            Params: none

            Returns:
            - string_OUT - lists of roles for each relation type, with a count of number of times each entity was in that role for that relation type, in sorted master entity list order.
        '''

        # return reference
        string_OUT = ""

        # declare variables
        me = "create_entity_ids_and_traits_attribute_string"
        debug_flag = None
        status_message = None
        request_instance = None
        entity_ids_and_traits_header_list = None
        ids_and_types_labels_to_values_map = None
        current_header_label = None
        value_list = None
        string_value_list = None
        attribute_label = None
        
        # initialize
        debug_flag = self.DEBUG_FLAG
        request_instance = self.get_network_data_request()
        entity_ids_and_traits_header_list = request_instance.create_entity_ids_and_traits_header_list()

        # first, retrieve the values.
        ids_and_types_labels_to_values_map = request_instance.create_entity_ids_and_traits_value_dict()
        
        # got anything?
        if ( ids_and_types_labels_to_values_map is not None ):
        
            # loop over header_labels
            for current_header_label in entity_ids_and_traits_header_list:
            
                # retrieve value list for this header label
                value_list = ids_and_types_labels_to_values_map.get( current_header_label, None )
                
                # got anything?
                if ( value_list is not None ):
                
                    # build row label
                    attribute_label = current_header_label
                    
                    # output the name of this attribute
                    string_OUT += "{}\n".format( attribute_label )

                    # join the list into a string, separated by newlines.
                    string_value_list = [ str( i ) for i in value_list ]
                    string_OUT += "\n".join( string_value_list )
    
                    # add two newlines to the end.
                    string_OUT += "\n\n"

                else:
                
                    # No value list for relation type slug+role
                    status_message = "In {}(): WARNING - No value list for relation type slug: {}; role: {}.  No attribute added for this type and role.".format( me, current_slug, current_role )
                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.WARNING )
                    
                #-- END check to see if list for role --#
                                    
            #-- END loop over relation type slugs --#
            
        else:
        
            # no slug passed in, can't do anything.
            status_message = "In {}(): ERROR - Call to self.create_all_relation_type_values_lists() returned None.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
        
        #-- END check to see if create list method returned anything --#

        return string_OUT

    #-- END method create_entity_ids_and_traits_attribute_string --#


    def render_network_data( self ):

        """
            Assumes render method has already created network data and entity
                relation types details.  Outputs a simple text
                matrix of ties.  For a given cell in the matrix, the value is an
                integer: 0 if no tie, 1 or greater if tie.  Each column value is
                separated by two spaces.

            Postconditions: returns the delimited network data, each column separated by two spaces, in a string.
            
            Returns:
            - String - delimited output (two spaces separate each column value in a row) for the network described by the articles selected based on the parameters passed in.
        """

        # return reference
        network_data_OUT = ''

        # declare variables
        data_output_structure = ""
        master_entity_list = None
        request_instance = None
        do_gather_ids_and_traits = None

        #--------------------------------------------------------------------
        # render network data.
        #--------------------------------------------------------------------
        
        # get data output structure
        data_output_structure = self.get_output_structure()
        
        # then, need to output.  For each network, output the network, then also
        #     output an attribute file that says, for all entities and relation
        #     types, whether each entity was in any role (FROM, TO, THROUGH) for
        #     each of the relation types.
        
        # include network?
        if ( ( data_output_structure == NetworkDataOutput.NETWORK_DATA_OUTPUT_STRUCTURE_NETWORK )
            or ( data_output_structure == NetworkDataOutput.NETWORK_DATA_OUTPUT_STRUCTURE_NET_AND_ATTR_COLS )
            or ( data_output_structure == NetworkDataOutput.NETWORK_DATA_OUTPUT_STRUCTURE_NET_AND_ATTR_ROWS ) ):

            # output the N of the network.
            master_entity_list = self.get_master_entity_list()
            network_data_OUT += "\nN = {}\n".format( len( master_entity_list ) )
    
            # output network.
            network_data_OUT += self.create_network_string()
    
            # Add a couple of new lines
            network_data_OUT += "\n\n"
    
        #-- END check to see if include network matrix --#

        # include attributes?
        if ( ( data_output_structure == NetworkDataOutput.NETWORK_DATA_OUTPUT_STRUCTURE_ATTRIBUTES )
            or ( data_output_structure == NetworkDataOutput.NETWORK_DATA_OUTPUT_STRUCTURE_NET_AND_ATTR_COLS )
            or ( data_output_structure == NetworkDataOutput.NETWORK_DATA_OUTPUT_STRUCTURE_NET_AND_ATTR_ROWS ) ):

            # yes - append the Entity_Relation types attribute string.
            network_data_OUT += self.create_entity_relation_types_attribute_string()
            
            # Do we have entity-specific IDs or traits?
            request_instance = self.get_network_data_request()
            do_gather_ids_and_traits = request_instance.do_output_entity_ids_or_traits()
            if ( do_gather_ids_and_traits == True ):
            
                # we do - build and add the lists of values.
                network_data_OUT += self.create_entity_ids_and_traits_attribute_string()
            
            #-- eND chcek to see if we have ids and traits --#
            
        #-- END check to see if include attributes. --#

        # Add a divider, then row headers and column headers for matrix,
        #    attribute list.
        network_data_OUT += "\n-------------------------------\nColumn and row labels (in the order the rows appear from top to bottom in the network matrix and attribute vector above, and in the order the columns appear from left to right) \n\n"

        # create column of headers
        network_data_OUT += self.create_label_string( "\n" )
        network_data_OUT += "\n\nLabel array, for use in analysis:\n"
        network_data_OUT += self.create_label_string( ",", '"' ) + "\n"

        return network_data_OUT

    #-- END render_network_data() --#


#-- END class NDO_SimpleMatrix --#