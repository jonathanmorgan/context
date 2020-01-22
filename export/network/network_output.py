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
        
        # entity dictionary and trait map
        self.m_entity_id_to_instance_map = {}
        self.m_entity_id_to_traits_map = {}
        
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
        network_data_request = None
        relation_query_set = None
        request_instance = None
        entity_id_to_instance_map = None
        do_gather_traits_and_ids = None
        entity_id_to_traits_map = None
        
        # initialize
        my_logger = self.get_logger()
        entity_id_to_instance_map = {}
        entity_id_to_traits_map = {}

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
            entity_id_to_instance_map = self.add_entities_to_dict( relation_query_set,
                                                                   entity_id_to_instance_map,
                                                                   include_through_IN = include_through_IN,
                                                                   store_entity_IN = load_instance_IN )
                                                  
            # store dictionary internally
            self.set_entity_id_to_instance_map( entity_id_to_instance_map )
            
            # also return it.
            dict_OUT = entity_id_to_instance_map
                                                  
            # do we need to also gather traits and/or identifiers?
            request_instance = self.get_network_data_request()
            do_gather_traits_and_ids = request_instance.do_output_entity_traits_or_ids()
            if ( do_gather_traits_and_ids == True ):
            
                # yes.  Call method.
                entity_id_to_traits_map = self.load_entities_traits_and_ids( relation_query_set, entity_id_to_traits_map )
                
                # store dictionary internally
                self.set_entity_id_to_traits_map( entity_id_to_traits_map )
                
            #-- END check to see if we gather traits and IDs. --#
            
        #-- END check to make sure we have a request --#
        
        my_logger.debug( "In {}(): len( dict_OUT ) = {}".format( me, len( dict_OUT ) ) )

        return dict_OUT

    #-- END function process_entities() --#


    def create_entity_id_dict_key( self, id_info_dict_IN ):

        '''
        Assumes there is an output format property specified in the request
            stored in this instance.  Retrieves this output type, creates a
            NetworkDataOutput implementer instance to match the type, then
            returns the instance.  If no type or unknown type, returns None.
        '''
        
        # return reference
        value_OUT = None

        # declare variables
        me = "create_entity_id_dict_key"
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
            id_name = id_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_NAME, None )
            id_id_type = id_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_ID_TYPE, None )
            id_source = id_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_SOURCE, None )
            id_identifier_type_id = id_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_IDENTIFIER_TYPE_ID, None )
            id_header = id_info_dict.get( NetworkDataRequest.PROP_NAME_ENTITY_IDENTIFIERS_OUTPUT_HEADER, None )
            
            # first, do we have a header?
            if ( ( id_header is not None ) and ( id_header != "" ) ):
            
                # yes.  Use it.
                value_OUT = id_header
                
            else:
            
                # start with mandatory name.
                value_OUT = id_name
                
                # got an id type?
                if ( ( id_id_type is not None ) and ( id_id_type != "" ) ):
                
                    # yes.  Append
                    value_OUT = "{}_{}".format( value_OUT, id_id_type )
                    
                #-- END check to see if id_type --#
                    
                # got a source?
                if ( ( id_source is not None ) and ( id_source != "" ) ):
                
                    # yes.  Append
                    value_OUT = "{}_{}".format( value_OUT, id_source )
                    
                #-- END check to see if id_source --#
                
            #-- END check to see if pre-built header --#
                
        else:
        
            # no info dictionary passed in.  Nothing to see here.
            value_OUT = None
            
        #-- END check to make sure info passed in. --#

        return value_OUT

    #-- END create_entity_id_dict_key() --#


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


    def get_entity_id_to_instance_map( self ):
        
        # return reference
        value_OUT = None
        
        # see if already stored.
        value_OUT = self.m_entity_id_to_instance_map
                
        return value_OUT
    
    #-- END method get_entity_id_to_instance_map() --#
    

    def get_entity_id_to_traits_map( self ):
        
        # return reference
        value_OUT = None
        
        # see if already stored.
        value_OUT = self.m_entity_id_to_traits_map
                
        return value_OUT
    
    #-- END method get_entity_id_to_traits_map() --#
    

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
    

    def load_entities_traits_and_ids( self, relation_qs_IN, dictionary_IN, include_through_IN = False ):

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
        me = "load_entities_traits_and_ids"
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

    #-- END function load_entities_traits_and_ids() --#


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
        my_request = None
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
        id_identifier_type_id = None
        id_qs = None
        id_count = None
        id_instance = None
        id_value = None
        id_value_list = None
        id_value_list_count = None
        current_id = None
        id_dict_key = None
        
        # initialize
        my_request = self.get_network_data_request()

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
            entity_ids_list = my_request.get_output_entity_identifiers_list()
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
                    
                    # got an identifier type id?
                    if ( ( id_identifier_type_id is not None ) and ( id_identifier_type_id != "" ) ):
                    
                        # yes. Filter.
                        id_qs = id_qs.filter( identifier_type_id = id_identifier_type_id )
                        
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
                    id_dict_key = self.create_entity_id_dict_key( id_info_dict )
                    
                    # add value to map.
                    trait_dict[ id_dict_key ] = id_value
                    
                #-- END check to see if enough info to filter. --#
                
            #-- END loop over traits we are to collect. --#
        
            # store the Entity in the output dict.
            entity_dict_OUT[ current_entity_id ] = trait_dict

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
        my_request = None
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
        trait_dict = None
        
        # initialize
        my_request = self.get_network_data_request()

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
            entity_traits_list = my_request.get_output_entity_traits_list()
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
                    
                    # add value to map.
                    trait_dict[ trait_name ] = trait_value
                    
                #-- END check to see if enough info to filter. --#
                
            #-- END loop over traits we are to collect. --#
        
            # store the Entity in the output dict.
            entity_dict_OUT[ current_entity_id ] = trait_dict

        #-- END check to see if there is an entity --#

        return entity_dict_OUT

    #-- END function load_entity_traits() --#


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
            entity_dictionary = self.process_entities()

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
                
                    # Error writing data to file, let's still return data.
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