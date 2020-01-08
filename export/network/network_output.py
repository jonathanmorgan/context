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
The network_output module contains objects and code to filter, parse and output
    social network data from context in a variety of formats, and also generates
    some descriptive statistics as it builds output.
    
This is based on context_text/export/network_output.py --> NetworkOutput.

Main method is "render_network_data".  Example usage, starting with pre-loaded
    NetworkDataRequest:
    
from context.export.network.network_output import NetworkOutput

# create instance
my_network_outputter = NetworkOutput()

# store request
my_network_outputter.set_network_data_request( my_request )

# render network data.
my_network_outputter.render_network_data()
'''

'''
If a NetworkDataOutput implementer will need to access or use variables, you
   should declare them in class NetworkDataOutput in file
   /export/network/network_data_output.py, then reference those variables here.
'''

__author__="jonathanmorgan"
__date__ ="$May 1, 2010 12:49:50 PM$"

if __name__ == "__main__":
    print( "Hello World" )

#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================

# python base imports
#from datetime import date
from datetime import datetime
import logging
import operator

# django database classes
from django.db.models import Q

# python_utilities
from python_utilities.parameters.param_container import ParamContainer

# Import the classes for our context application
from context.models import Entity_Relation

# Import context export classes.
from context.export.network.filter_spec import FilterSpec
from context.export.network.network_data_output import NetworkDataOutput
from context.export.network.ndo_simple_matrix import NDO_SimpleMatrix
from context.export.network.ndo_csv_matrix import NDO_CSVMatrix
from context.export.network.ndo_tab_delimited_matrix import NDO_TabDelimitedMatrix

# Import context shared classes.
from context.shared.context_base import ContextBase


#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class NetworkOutput( ContextBase ):


    #---------------------------------------------------------------------------
    # CONSTANTS-ish
    #---------------------------------------------------------------------------


    DEBUG_FLAG = True
    LOGGER_NAME = "context.export.network.network_output.NetworkOutput"
    ME = LOGGER_NAME

    # Network data output formats
    NETWORK_OUTPUT_FORMAT_SIMPLE_MATRIX = NetworkDataOutput.NETWORK_DATA_FORMAT_SIMPLE_MATRIX
    NETWORK_OUTPUT_FORMAT_CSV_MATRIX = NetworkDataOutput.NETWORK_DATA_FORMAT_CSV_MATRIX
    NETWORK_OUTPUT_FORMAT_TAB_DELIMITED_MATRIX = NetworkDataOutput.NETWORK_DATA_FORMAT_TAB_DELIMITED_MATRIX
    NETWORK_OUTPUT_FORMAT_DEFAULT = NetworkDataOutput.NETWORK_DATA_FORMAT_DEFAULT
    
    NETWORK_OUTPUT_FORMAT_CHOICES_LIST = NetworkDataOutput.NETWORK_DATA_FORMAT_CHOICES_LIST

    #---------------------------------------------------------------------------
    # __init__() method
    #---------------------------------------------------------------------------


    def __init__( self ):

        # call parent's __init__()
        super( NetworkOutput, self ).__init__()

        # declare variables - moved to parent
        #self.request = None
        #self.parameters = ParamContainer()

        # define parameters - moved to parent
        #self.define_parameters( NetworkOutput.PARAM_NAME_TO_TYPE_MAP )
        
        # variables for outputting result as file
        self.mime_type = ""
        self.file_extension = ""
        
        # place to store NetworkDataRequest
        self.m_network_data_request = None
        
        # entity relation query set, for populating network ties.
        self.m_relation_query_set = None
        
        # for debugging, reference to last NetworkDataOutput instance used.
        self.m_NDO_instance = None
        
        # set logger name (for LoggingHelper parent class: (LoggingHelper --> BasicRateLimited --> ContextTextBase --> ArticleCoding).
        self.set_logger_name( self.LOGGER_NAME )
        
    #-- END method __init__() --#


    #---------------------------------------------------------------------------
    # instance methods, in alphabetical order
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


    def create_entity_dict( self, include_through_IN = False, load_instance_IN = False ):

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
        dict_OUT = {}

        # declare variables
        me = "create_entity_dict"
        my_logger = None
        network_data_request = None
        relation_query_set = None
        current_relation = None
        author_qs = None
        source_qs = None
        
        # initialize logger
        my_logger = self.get_logger()

        # get request instance
        network_data_request = self.get_network_data_request()

        # got request?
        if ( network_data_request ):

            # get query set to loop over Entity_Relations that match the filter
            #     criteria in the request for selecting included Entities.  This
            #     might or might not be the same as the QuerySet for included
            #     Entity_Relations.
            relation_query_set = network_data_request.filter_relation_query_set( use_entity_selection_IN = True )
            
            my_logger.debug( "In {}(): relation_query_set.count() = {}".format( me, relation_query_set.count() ) )

            # add entities from relation QuerySet to dict.
            dict_OUT = self.add_entities_to_dict( relation_query_set,
                                                  dict_OUT,
                                                  include_through_IN = include_through_IN,
                                                  store_entity_IN = load_instance_IN )
            
        #-- END check to make sure we have a request --#
        
        my_logger.debug( "In {}(): len( dict_OUT ) = {}".format( me, len( dict_OUT ) ) )

        return dict_OUT

    #-- END function create_entity_dict() --#


    def create_NDO_instance( self ):

        '''
        Assumes there is an output format property specified in the request
            stored in this instance.  Retrieves this output type, creates a
            NetworkDataOutput implementer instance to match the type, then
            returns the instance.  If no type or unknown type, returns None.
        '''
        
        # return reference
        NDO_instance_OUT = None

        # declare variables
        request_instance = None
        output_format = None

        # get output type.
        request_instance = self.get_network_data_request()
        output_format = request_instance.get_output_format()
        
        # make instance for output format.
        if ( output_format == self.NETWORK_OUTPUT_FORMAT_SIMPLE_MATRIX ):
        
            # simple matrix.
            NDO_instance_OUT = NDO_SimpleMatrix()
        
        elif ( output_format == self.NETWORK_OUTPUT_FORMAT_CSV_MATRIX ):
        
            # CSV matrix.
            NDO_instance_OUT = NDO_CSVMatrix()
        
        elif ( output_format == self.NETWORK_OUTPUT_FORMAT_TAB_DELIMITED_MATRIX ):
        
            # Tab-delimited matrix.
            NDO_instance_OUT = NDO_TabDelimitedMatrix()
        
        else:
        
            # no output type, or unknown.  Make simple output matrix.
            NDO_instance_OUT = NDO_SimpleMatrix()
        
        #-- END check to see what type we have. --#
        
        # set mime type and file extension from instance
        self.mime_type = NDO_instance_OUT.mime_type
        self.file_extension = NDO_instance_OUT.file_extension
        
        # store instance
        NDO_instance_OUT = self.set_NDO_instance( NDO_instance_OUT )

        return NDO_instance_OUT

    #-- END create_NDO_instance() --#


    def get_NDO_instance( self ):

        '''
        Assumes there is an output type property specified in the POST parameters
           passed in as part of the current request.  Retrieves this output type,
           creates a NetworkDataOutput implementer instance to match the type,
           then returns the instance.  If no type or unknown type, returns None.
        '''
        
        # return reference
        NDO_instance_OUT = None

        # declare variables

        # try to just retrieve the instance.
        NDO_instance_OUT = self.m_NDO_instance
        
        # got one?
        if ( NDO_instance_OUT is None ):

            # no.  Create one, then return it.
            self.create_NDO_instance()
            
            # Recursive call to make sure it got set.
            NDO_instance_OUT = self.get_NDO_instance()

        #-- END check to see if nested instance. --#

        return NDO_instance_OUT

    #-- END get_NDO_instance() --#


    def get_network_data_request( self ):
        
        # return reference
        value_OUT = None
        
        # see if already stored.
        value_OUT = self.m_network_data_request
                
        return value_OUT
    
    #-- END method get_network_data_request() --#
    

    def get_relation_query_set( self ):
        
        # return reference
        value_OUT = None
        
        # see if already stored.
        value_OUT = self.m_relation_query_set
                
        return value_OUT
    
    #-- END method get_relation_query_set() --#
    

    def render_network_data( self, network_data_request_IN = None, relation_qs_IN = None ):

        """
            Accepts optional Entity_Relation QuerySet and NetworkDataRequest
                instance.  If None passed in for Entity_Relation QuerySet, just
                filters based on request.  If no request passed in, tries to
                retrieve request stored in this instance.  If no request, does
                nothing, returns None.  If request found, sets up output to
                match the request; creates network data; renders it to the spec
                in the request, and returns whatever the render type returns
                from its render method. 

            Preconditions: assumes that we have a NetworkDataRequest populated,
                either in the instance variable m_network_data_request in this
                instance, or passed in.  If not, does nothing, returns None.

            Postconditions: returns the rendered network data, with actual
                format decided by the output format specified in the spec.

            Parameters:
            - network_data_request_IN - NetworkDataRequest instance with the data request specified inside.

            Returns:
            - output for the network described by the request passed in.
        """

        # return reference
        network_OUT = None

        # declare variables
        me = "render_network_data"
        debug_flag = None
        status_message = None
        network_data_request = None
        network_data_outputter = None
        entity_dictionary = None
        my_params = None
        relation_qs = None
        output_file_path = None
        output_file = None
        exception_instance = None

        # init
        debug_flag = False

        # do we have a request passed in?
        if ( network_data_request_IN is not None ):
        
            # yes - use it.
            self.set_network_data_request( network_data_request_IN )
            
        #-- END check to see if request passed in.
        
        # do we have a relation QuerySet passed in?
        if ( relation_qs_IN is not None ):
        
            relation_qs = relation_qs_IN
            
        #-- END check to see if QS passed in --#
        
        # got a request?
        network_data_request = self.get_network_data_request()
        if ( network_data_request is not None ):
            
            # ! ----> build network data from request.

            # create the entity_dictionary
            entity_dictionary = self.create_entity_dict()

            # create and store the tie Entity_Relation QuerySet
            relation_qs = network_data_request.filter_relation_query_set( qs_IN = relation_qs,
                                                                          use_entity_selection_IN = False )

            # create instance of NetworkDataOutput.
            network_data_outputter = self.get_NDO_instance()

            # initialize it.
            network_data_outputter.set_query_set( relation_qs )
            network_data_outputter.set_entity_dictionary( entity_dictionary )

            # initialize NetworkDataOutput instance from request.
            network_data_outputter.initialize_from_request( network_data_request )

            # render and return the result.
            network_OUT = network_data_outputter.render()

            # add some debug?
            if ( debug_flag == True ):

                # yup.
                network_OUT += "\n\n" + network_data_outputter.debug + "\n\n"

            #-- END check to see if we have debug to output. --#
            
            # ! ----> output
            
            # Are we to output to a file?
            output_file_path = network_data_request.get_output_file_path()
            if ( ( output_file_path is not None ) and ( output_file_path != "" ) ):
            
                try:
                
                    # yes.  Output to file.
                    with open( output_file_path, "w" ) as output_file:
                    
                        # write to file
                        output_file.write( network_OUT )
                        
                    #-- END with open( output_file_path, "w" ) as output_file --#
                    
                except:
                
                    # no slug passed in, can't do anything.
                    status_message = "ERROR - Exception thrown writing network data to {}.  Ignoring error, returning data.".format( output_file_path )
                    exception_instance = sys.exc_info()[0]
                    self.log_exception( exception_instance, message_IN = status_message, method_IN = me, logger_name_IN = self.LOGGER_NAME, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
                    
                #-- END try...except around writing output to file --#
            
            #-- END check to see if output file path set --#

        else:
        
            # no request spec, so can't process.
            status_message = "In {}(): ERROR - no request specification, so doing nothing.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
        
        #-- END check to make sure we have a query set. --#

        return network_OUT

    #-- END render_network_data() --#


    def set_NDO_instance( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_NDO_instance = value_IN
        
        # return it
        value_OUT = self.get_NDO_instance()
        
        return value_OUT
    
    #-- END method set_NDO_instance() --#


    def set_network_data_request( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_network_data_request = value_IN
        
        # return it
        value_OUT = self.get_network_data_request()
        
        return value_OUT
    
    #-- END method set_network_data_request() --#


    def set_relation_query_set( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_relation_query_set = value_IN
        
        # return it
        value_OUT = self.get_relation_query_set()
        
        return value_OUT
    
    #-- END method set_relation_query_set() --#


#-- END class NetworkOutput --#