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

# python libraries
import csv
import logging
# documentation: https://docs.python.org/2/library/csv.html

# six imports - support Pythons 2 and 3
import six
# import StringIO
from six import StringIO

# Django DB classes, just to play with...
#from django.db.models import Count # for aggregating counts of authors, sources.
#from django.db.models import Max   # for getting max value of author, source counts.

# parent abstract class.
from context.export.network.network_data_output import NetworkDataOutput

#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class NDO_CSVMatrix( NetworkDataOutput ):

    
    #---------------------------------------------------------------------------
    # CONSTANTS-ish
    #---------------------------------------------------------------------------


    DEBUG_FLAG = True
    LOGGER_NAME = "context.export.network.ndo_csv_matrix.NDO_CSVMatrix"
    ME = LOGGER_NAME

    # output format
    MY_OUTPUT_FORMAT = NetworkDataOutput.NETWORK_DATA_FORMAT_CSV_MATRIX

    # LOCAL_DEBUG_FLAG
    LOCAL_DEBUG_FLAG = False


    #---------------------------------------------------------------------------
    # instance variables
    #---------------------------------------------------------------------------


    csv_string_buffer = None
    csv_writer = None
    delimiter = ","

    
    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------


    def __init__( self ):

        # call parent's __init__() - I think...
        super( NDO_CSVMatrix, self ).__init__()

        # override things set in parent.
        self.set_output_format( self.MY_OUTPUT_FORMAT )
        self.debug = "{} debug:\n\n".format( self.ME )

        # initialize variables.
        self.csv_string_buffer = None
        self.csv_writer = None
        self.delimiter = ","

        # variables for outputting result as file
        self.mime_type = "text/csv"
        self.file_extension = "csv"

    #-- END method __init__() --#


    #---------------------------------------------------------------------------
    # instance methods, in alphabetical order
    #---------------------------------------------------------------------------


    def append_entity_row( self, entity_id_IN, row_count_IN = "" ):

        """
            Method: append_entity_row()

            Purpose: retrieves the master entity list from the instance, uses it
               and the entity ID passed in to output the row for the current
               entity in a square matrix where rows and columns are entities,
               sorted by entity ID, and the value at the intersection between
               two entities is the number of times they were linked by relations
               from the pool of Entity_Relation instances that make up the
               network.

            Postconditions: Doesn't return anything, but appends row for current
               user to the nested CSV writer.

            Returns:
            - nothing.
        """

        # return reference

        # declare variables
        current_entity_label = ""
        entity_list = None
        do_output_network = False
        current_entity_relations = None
        current_other_id = -1
        current_other_count = -1
        column_value_list = []
        csv_writer = None
        do_output_attrs = False
        relation_type_role_counts_list = None
        
        # related attributes - ids and traits
        request_instance = None
        do_gather_ids_and_traits = None
        ids_and_traits_value_list = None

        # get entity ID?
        if ( entity_id_IN ):
        
            if ( ( self.LOCAL_DEBUG_FLAG == True ) or ( self.DEBUG_FLAG == True ) ):
                self.debug += "entity " + str( entity_id_IN ) + "; "
            #-- END DEBUG --#
                
            # get label for current user
            current_entity_label = str( row_count_IN ) + "__" + self.get_entity_label( entity_id_IN )
            
            # make it first column in row.
            column_value_list.append( current_entity_label )
            
            # are we outputting network?
            do_output_network = self.do_output_network()
            if ( do_output_network == True ):

                # get entity list
                entity_list = self.get_master_entity_list()
    
                # get relations for this entity.
                current_entity_relations = self.get_relations_for_entity( entity_id_IN )
    
                # loop over master list, checking for relations with each entity.
                for current_other_id in sorted( entity_list ):
    
                    # try to retrieve relation count from relations
                    if current_other_id in current_entity_relations:
    
                        # they are related.  Get count.
                        current_other_count = current_entity_relations[ current_other_id ]
    
                    else:
    
                        # no relation.  Set current count to 0
                        current_other_count = 0
    
                    #-- END check to see if related.
    
                    # output the count for the current entity.
                    column_value_list.append( str( current_other_count ) )
    
                #-- END loop over master list --#
                
            #-- END check to see if we output network data. --#
            
            # do we append node attributes to the end of each row?
            do_output_attrs = self.do_output_attribute_columns()
            if ( do_output_attrs == True ):

                # yes - append attributes.
                
                # append entity's ID.
                column_value_list.append( str( entity_id_IN ) )

                # walk the entity's relation type data structure in the same
                #     order as the relation type list, and output FROM, TO, and
                #     THROUGH numbers for each, 0 if not found.  Will result in
                #     many attribute columns.
                relation_type_role_counts_list = self.create_relation_type_roles_for_entity( entity_id_IN )
                
                # extend the row's column_value_list with these new values.
                column_value_list.extend( relation_type_role_counts_list )
                            
                # do we have any additional traits or IDs to add?
                request_instance = self.get_network_data_request()
                do_gather_ids_and_traits = request_instance.do_output_entity_ids_or_traits()
                if ( do_gather_ids_and_traits == True ):
                
                    # we do.  Retrieve values.
                    ids_and_traits_value_list = request_instance.create_ids_and_traits_values_for_entity( entity_id_IN )
                
                    # got anything?
                    if ( ( ids_and_traits_value_list is not None ) and ( len( ids_and_traits_value_list ) > 0 ) ):
                    
                        # yes.  Append items to end of list.
                        column_value_list.extend( ids_and_traits_value_list )
                        
                    #-- END check to see if any traits and ids returned --#
                    
                #-- END check to see if we have traits or ids --#
            
            #-- END check to see if we append attributes to the end of rows. --#
            
            # append row to CSV
            self.append_row_to_csv( column_value_list )

        #-- END check to make sure we have a entity --#

    #-- END method append_entity_row --#


    def append_entity_id_row( self ):

        '''
            Method: append_entity_id_row()

            Purpose: Create a list of entity IDs for the entities in
               master list, then append the list to the end of the
               CSV document.

            Preconditions: Master entity list must be present.

            Params: none
            
            Postconditions: Row is appended to the end of the nested CSV document, but nothing is returned.
        '''

        # return reference

        # declare variables
        entity_id_list = None

        # get entity type ID list
        entity_id_list = self.create_entity_id_list( True )

        if ( ( self.LOCAL_DEBUG_FLAG == True ) or ( self.DEBUG_FLAG == True ) ):
            self.debug += "\n\nentity id list:\n" + "; ".join( entity_id_list )
        #-- END DEBUG --#

        # got it?
        if ( ( entity_id_list != None ) and ( len( entity_id_list ) > 0 ) ):

            # add label to front
            entity_id_list.insert( 0, "entity_id" )

            # write the row
            self.append_row_to_csv( entity_id_list )
            
        #-- END check to make sure we have list.

    #-- END method append_entity_id_row --#


    def append_entity_ids_and_traits_rows( self ):

        '''
            Method: append_entity_relation_type_rows()

            Purpose: Pull in all relation types, then for each
                entity-->type-->role, walk all entities and output their value
                for that relation type in the row.  So, will result in many rows
                of attribute values.

            Preconditions: Master entity list must be present.  Note: if the
                network is large, might take a lot of memory...

            Params: none
            
            Postconditions: Rows are appended to the end of the nested CSV document, but nothing is returned.
        '''

        # declare variables
        me = "append_entity_ids_and_traits_rows"
        debug_flag = None
        status_message = None
        request_instance = None
        label_to_value_list_map = None
        sorted_label_list = None
        current_label = None
        label_value_list = None
        row_label = None
        
        # initialize
        debug_flag = self.DEBUG_FLAG

        # first, retrieve the values.
        request_instance = self.get_network_data_request()
        label_to_value_list_map = request_instance.create_entity_ids_and_traits_value_dict()
        
        # got anything?
        if ( label_to_value_list_map is not None ):
        
            # get list of labels, sorted appropriately
            sorted_label_list = request_instance.get_entity_ids_and_traits_header_list()
            
            # loop over labels
            for current_label in sorted_label_list:
            
                # retrieve value list for this label
                label_value_list = label_to_value_list_map.get( current_label, None )
                
                # got anything?
                if ( label_value_list is not None ):
                
                    # build row label
                    row_label = current_label
                    
                    # prepend row label
                    label_value_list.insert( 0, row_label )

                    # write the row
                    self.append_row_to_csv( label_value_list )
                    
                else:
                
                    # No value list for relation type slug+role
                    status_message = "In {}(): WARNING - No value list for label: {}.  No row added for this type and role.".format( me, current_label )
                    self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.WARNING )
                    
                #-- END check to see if list for label --#
                
            #-- END loop over ids and traits labels --#
            
        else:
        
            # no slug passed in, can't do anything.
            status_message = "In {}(): ERROR - Call to self.create_all_relation_type_values_lists() returned None.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
        
        #-- END check to see if create list method returned anything --#

    #-- END method append_entity_ids_and_traits_rows --#


    def append_entity_relation_type_rows( self ):

        '''
            Method: append_entity_relation_type_rows()

            Purpose: Pull in all relation types, then for each
                entity-->type-->role, walk all entities and output their value
                for that relation type in the row.  So, will result in many rows
                of attribute values.

            Preconditions: Master entity list must be present.  Note: if the
                network is large, might take a lot of memory...

            Params: none
            
            Postconditions: Rows are appended to the end of the nested CSV document, but nothing is returned.
        '''

        # declare variables
        me = "append_entity_relation_type_rows"
        debug_flag = None
        status_message = None
        relation_type_slug_to_roles_map = None
        sorted_slug_list = None
        role_list = None
        current_slug = None
        role_to_value_list_map = None
        current_role = None
        value_list = None
        row_label = None
        
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
                            row_label = "{}-{}".format( current_slug, current_role )
                            
                            # prepend row label
                            value_list.insert( 0, row_label )
        
                            # write the row
                            self.append_row_to_csv( value_list )
                            
                        else:
                        
                            # No value list for relation type slug+role
                            status_message = "In {}(): WARNING - No value list for relation type slug: {}; role: {}.  No row added for this type and role.".format( me, current_slug, current_role )
                            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.WARNING )
                            
                        #-- END check to see if list for role --#
                        
                    else:
                    
                        # No role-to-values map relation type slug
                        status_message = "In {}(): WARNING - No role-to-values map for relation type slug: {}.  No rows added for this type.".format( me, current_slug )
                        self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.WARNING )
                            
                    #-- END check to see if role-to-values map for slug --#
                    
                #-- END loop over roles. --#
                
            #-- END loop over relation type slugs --#
            
        else:
        
            # no slug passed in, can't do anything.
            status_message = "In {}(): ERROR - Call to self.create_all_relation_type_values_lists() returned None.  Doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
        
        #-- END check to see if create list method returned anything --#

    #-- END method append_entity_relation_type_rows --#


    def append_row_to_csv( self, column_value_list_IN ):
        
        '''
        Accepts list of column values that make up a row in a CSV document.
           Retrieves nested CSV writer, writes the row to the document.
        '''
        
        # declare variables.
        my_csv_writer = None
        
        # got a list?
        if ( ( column_value_list_IN != None ) and ( len( column_value_list_IN ) > 0 ) ):

            # yes - get writer.
            my_csv_writer = self.get_csv_writer()
            
            # write the list to the CSV writer
            my_csv_writer.writerow( column_value_list_IN ) 
        
        #-- END check to see if got list. --#
        
    #-- END method append_row_to_csv() --#


    def cleanup( self ):
        
        # declare variables
        my_csv_string_buffer = None
        
        # get string buffer.
        my_csv_string_buffer = self.get_csv_string_buffer()
        
        # close string buffer
        my_csv_string_buffer.close()
        
        # None out string buffer and writer
        self.csv_writer = None
        self.csv_string_buffer = None
        
    #-- END method cleanup() --#


    def create_csv_document( self ):

        """
            Method: create_csv_document()

            Purpose: retrieves the master entity list from the instance, uses it
                to output a CSV square matrix where rows and columns are entities,
                sorted by entity ID, and the value at the intersection between
                two entities is the number of times they were linked by relations
                from the pool of Entity_Relation instances that make up the
                network.

            Preconditions: Assumes that csv output is already initialized.
            
            Returns:
            - nothing - CSV is stored in internal CSV Writer and String buffer.
        """

        # return reference

        # declare variables
        header_label_list = None
        master_list = None
        current_entity_id = -1
        entity_counter = -1
        my_csv_buffer = None
        do_output_attr_rows = False

        # get list of column headers.
        header_label_list = self.create_header_list()
        
        # add header label row to csv document.
        self.append_row_to_csv( header_label_list )

        # get sorted master list (returns it sorted by default)
        master_list = self.get_master_entity_list()

        # got something?
        if ( ( master_list != None ) and ( len( master_list ) > 0 ) ):

            # loop over sorted entity list, calling method to output network
            #    row for each entity.  Leaving in sorted() since it copies
            #    the array, and we are looping twice - not sure if it will
            #    maintain two separate positions in nested loops.
            entity_counter = 0
            for current_entity_id in sorted( master_list ):

                # increment counter
                entity_counter += 1

                # add the entity's row to the CSV writer.
                self.append_entity_row( current_entity_id, entity_counter )

            #-- END loop over entities.

        #-- END check to make sure we have a entity list. --#
        
        # add attributes as rows?
        do_output_attr_rows = self.do_output_attribute_rows()
        if ( do_output_attr_rows == True ):

            # yes - append the "entity_id" attribute string...
            self.append_entity_id_row()
            
            # ...and append the "entity_type" attribute string.
            self.append_entity_relation_type_rows()
            
            # do we have any additional traits or IDs to add?
            request_instance = self.get_network_data_request()
            do_gather_ids_and_traits = self.do_output_entity_ids_or_traits()
            if ( do_gather_ids_and_traits == True ):
            
                # we do.  append ids and traits rows.
                self.append_entity_ids_and_traits_rows()
                
            #-- END check to see if we have traits or ids --#

        #-- END check to see if include attributes. --#

    #-- END method create_csv_document --#


    def create_csv_string( self ):

        """
            Method: create_csv_string()

            Purpose: retrieves the master entity list from the instance, uses it
                to output a CSV square matrix where rows and columns are entities,
                sorted by entity ID, and the value at the intersection between
                two entities is the number of times they were linked by relations
                from the pool of Entity_Relation instances that make up the
                network.

            Returns:
            - string CSV representation of network.
        """

        # return reference
        network_string_OUT = ""

        # declare variables
        master_list = None
        current_entity_id = -1
        entity_counter = -1
        my_csv_buffer = None

        # initialize CSV output.
        self.init_csv_output()

        # create the CSV document.
        self.create_csv_document()

        # get underlying string buffer.
        my_csv_buffer = self.csv_string_buffer
        
        # convert contents to string
        network_string_OUT = my_csv_buffer.getvalue()

        # cleanup.
        self.cleanup()

        return network_string_OUT

    #-- END method create_csv_string --#


    def get_csv_string_buffer( self ):
        
        # return reference
        buffer_OUT = None
        
        # got an instance nested already?
        if ( self.csv_string_buffer != None ):
        
            # yes.  Return it.
            buffer_OUT = self.csv_string_buffer
            
        else:
        
            # no - init, then return self.csv_writer.
            self.init_csv_output()
            buffer_OUT = self.csv_string_buffer
            
        #-- END check to see if we already have a CSV writer. --#
        
        return buffer_OUT
        
    #-- END method get_csv_string_buffer() --#
    

    def get_csv_writer( self ):
        
        # return reference
        writer_OUT = None
        
        # got an instance nested already?
        if ( self.csv_writer != None ):
        
            # yes.  Return it.
            writer_OUT = self.csv_writer
            
        else:
        
            # no - init, then return self.csv_writer.
            self.init_csv_output()
            writer_OUT = self.csv_writer
            
        #-- END check to see if we already have a CSV writer. --#
        
        return writer_OUT
        
    #-- END method get_csv_writer() --#
    

    def init_csv_output( self ):
        
        '''
        Creates a string buffer, then uses that to create a CSV writer.  The
           writer is used to create the CSV file.  You pass lists of column
           values to the method writerow() and the CSV writer creates a row
           where each value in the list is a column value.
           Stores both the string buffer and writer in instance variables.
        '''

        # declare variables
        output_string_buffer = None
        output_writer = None
        
        # Make string buffer.
        output_string_buffer = StringIO()
        
        # Use it to create writer.
        output_writer = csv.writer( output_string_buffer, delimiter=self.delimiter )

        # store off these instances.
        self.csv_string_buffer = output_string_buffer
        self.csv_writer = output_writer

    #-- END method init_csv_output() --#


    def render_network_data( self ):

        """
            Assumes render method has already created network data and entity
                relation types details.  Outputs a simple text
                matrix of ties.  For a given cell in the matrix, the value is an
                integer: 0 if no tie, 1 or greater if tie.

            Postconditions: returns the delimited network data in a string.

            Returns:
            - String - Outputs a simple text matrix of ties.  For a given cell in the matrix, the value is an integer: 0 if no tie, 1 or greater if tie.
        """

        # return reference
        network_data_OUT = ''

        # declare variables

        #--------------------------------------------------------------------
        # render network data
        #--------------------------------------------------------------------
        
        # output network.
        network_data_OUT += self.create_csv_string()
        
        # if local debug is on but global debug isn't, output debug.
        if ( ( self.LOCAL_DEBUG_FLAG == True ) and ( self.DEBUG_FLAG == False ) ):
            network_data_OUT += "\n\n\n====================\nDEBUG\n====================\n\n" + self.debug
        #-- END DEBUG --#

        return network_data_OUT

    #-- END render_network_data() --#


#-- END class NDO_CSVMatrix --#