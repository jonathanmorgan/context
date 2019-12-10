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
#from context.export.network.csv_article_output import CsvArticleOutput
#from context.export.network.network_data_output import NetworkDataOutput
#from context.export.network.ndo_simple_matrix import NDO_SimpleMatrix
#from context.export.network.ndo_csv_matrix import NDO_CSVMatrix
#from context.export.network.ndo_tab_delimited_matrix import NDO_TabDelimitedMatrix

# Import context_text shared classes.
from context.shared.context_base import ContextBase


#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class NetworkOutput( ContextBase ):


    #---------------------------------------------------------------------------
    # CONSTANTS-ish
    #---------------------------------------------------------------------------


    DEBUG_FLAG = True
    LOGGER_NAME = "context.export.network.network_data_request.NetworkDataRequest"
    ME = LOGGER_NAME

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
        
        # set logger name (for LoggingHelper parent class: (LoggingHelper --> BasicRateLimited --> ContextTextBase --> ArticleCoding).
        self.set_logger_name( "context.export.network.network_output" )
        
    #-- END method __init__() --#


    #---------------------------------------------------------------------------
    # instance methods, in alphabetical order
    #---------------------------------------------------------------------------


    def add_entity_to_dict( self, person_qs_IN, dictionary_IN, store_person_IN = False ):

        """
            Accepts a dictionary, a list of Article_Person instances, and a flag
                that indicates if model instances should be stored in the
                dictionary. Adds the people in the Article_Person query set to
                the dictionary, making the Person ID the key and either None or
                the Person model instance the value, depending on the value in
                the store_person_IN flag.

            Preconditions: request must have contained required parameters, and
                so contained at least a start and end date and a publication.
                Should we have a flag that says to use the same criteria as the
                selection criteria?

            Postconditions: uses a lot of memory if you choose a large date
                range. Returns the same dictionary passed in, but with the
                people in store_person_IN added.

            Parameters:
            - self - self instance variable.
            - dictionary_IN - dictionary we want to add people to.  Returned
                with people added.
            - person_qs_IN - django query set object that contains the people we
                want to add to our dictionary.
            - store_person_IN - boolean, if False, doesn't load Person model
                instances while building the dictionary.  If True, loads Person
                models and stores them in the dictionary.

            Returns:
            - Dictionary - dictionary that contains all the people in the query
                set of Article_Person implementors passed in, either mapped to
                None or to Person model instances, depending on the
                load_person_IN flag value.
        """

        # return reference
        person_dict_OUT = {}

        # declare variables
        me = "add_entity_to_dict"
        current_relation = None
        current_person = None
        current_person_id = ''
        current_value = None

        # set the output dictionary
        if ( dictionary_IN ):

            # yes, store in output parameter
            person_dict_OUT = dictionary_IN

        #-- END check to see if dictionary passed in --#

        # loop over the articles
        for current_relation in person_qs_IN:

            # add author's person ID to list.  If no person ID, don't add (what
            #    to do about anonymous sources?).
            current_person = current_relation.person

            # see if there is a person
            if ( current_person is not None ):

                # are we also loading the person?
                current_person_id = current_person.id

                if ( store_person_IN == True ):

                    # yes, use Person model as value.
                    current_value = current_person

                else:

                    # no, use None as value.
                    current_value = None

                #-- END conditional to check if we are storing actual model instances --#

                # store the person in the output dict.
                person_dict_OUT[ current_person_id ] = current_value

            #-- END check to see if there is a person (in comparison to an anonymous source, for instance, or the author just being the newspaper) --#

        #-- END loop over people --#

        return person_dict_OUT

    #-- END function add_entity_to_dict() --#


    def create_entity_dict( self, load_instance_IN = False ):

        """
            Accepts flag that dictates whether we load the actual Entity
               record or not.  Uses nested request to retrieve all matching
               relations, then builds a dictionary of all the IDs of FROM and TO
               Entities in those relations, mapped either to None or to their
               Entity instance.

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
        request_IN = None
        relation_query_set = None
        current_relation = None
        author_qs = None
        source_qs = None
        
        # initialize logger
        my_logger = self.get_logger()

        # get request instance
        request_IN = self.get_network_data_request()

        # got request?
        if ( request_IN ):

            # get query set to loop over Entity_Relations that match the filter
            #     criteria in the request for selecting included Entities.  This
            #     might or might not be the same as the QuerySet for included
            #     Entity_Relations.
            relation_query_set = self.create_relation_query_set( use_entity_selection_IN = True )
            
            my_logger.debug( "In {}(): relation_query_set.count() = {}".filter( me, relation_query_set.count() ) )

            # loop over the entities
            for current_relation in relation_query_set:
            
                # add FROM and TO entities to entity dictionary.
                pass
            
            #-- END loop over articles --#

        #-- END check to make sure we have a request --#
        
        my_logger.debug( "In " + me + ": len( dict_OUT ) = " + str( len( dict_OUT ) ) )

        return dict_OUT

    #-- END function create_entity_dict() --#


    def filter_relation_query_set( self, use_entity_selection_IN = False, qs_IN = None ):
        
        '''
        retrieves the nested NetworkDataRequest, uses it to build up a
            Entity_Relation
        '''

        # return reference
        qs_OUT = None

        # declare variables
        me = "create_relation_query_set"
        debug_flag = None
        my_logger = None
        network_request = None
        selection_filters = None
        filter_spec_dict = None
        comparison_type = None
        
        # initialize.
        debug_flag = self.DEBUG_FLAG
        
        # retrieve NetworkDataRequest
        network_request = self.get_network_data_request()
        if ( network_request is not None ):
        
            # which selection criteria do we use?
            if ( use_entity_selection_IN == True ):

                status_message = "In {}: use_entity_selection_IN is True".format( me )
                self.output_message( status_message, do_print_IN = True, log_level_code_IN = logging.DEBUG )
                    
                # try to retrieve entity selection.
                selection_filters = network_request.get_entity_selection()
                
                # got something?
                if ( selection_filters is None ):
                
                    # no.  Output info message, default to relation_selection.
                    status_message = "In {}: \"entity_selection\" filtering was requested, but not specified in the request.  Defaulting to \"relation_selection\".".format( me )
                    self.output_message( status_message, do_print_IN = True, log_level_code_IN = logging.INFO )
                    selection_filters = network_request.get_relation_selection()
                    
                #-- END check to see if "entity_selection" is missing --#
                
            else:
            
                status_message = "In {}: use_entity_selection_IN is False".format( me )
                self.output_message( status_message, do_print_IN = True, log_level_code_IN = logging.DEBUG )
                    
                # use relation_selection.
                selection_filters = network_request.get_relation_selection()
                
            #-- END check to ee if we use "entity_selection" --#
        
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
            
                # make a filter_spec instance to re-use
                filter_spec = FilterSpec()
            
                # ! ----> pull in and process the different types of filters.
                
                # ! TODO - relation_type_slug_filters
                
                # ! TODO - relation_trait_filters
                
                # ! TODO - entity_type_slug_filters

                # ! TODO - entity_trait_filters

                # ! TODO - entity_id_filters

            else:

                # ERROR - no selection filters, can't process.
                status_message = "In {}(): ERROR - no selection filters found in NetworkDataRequest, so nothing to do.".format( me )
                self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
            
            #-- END check to see if we have selection filters --#
            
        else:
        
            # ERROR - no NetworkDataRequest, can't process.
            status_message = "In {}(): ERROR - no NetworkDataRequest instance found, so nothing to do.".format( me )
            self.output_message( status_message, do_print_IN = debug_flag, log_level_code_IN = logging.ERROR )
        
        #-- END check to see if NetworkDataRequest --#

        return qs_OUT

    #-- end method create_relation_query_set() ---------------------------#


    def get_network_data_request( self ):
        
        # return reference
        value_OUT = None
        
        # see if already stored.
        value_OUT = self.m_network_data_request
                
        return value_OUT
    
    #-- END method get_network_data_request() --#
    

    def render_network_data( self, network_data_request_IN = None ):

        """
            Accepts optional NetworkDataRequest instance.  If None passed in,
                tries to retrieve request stored in this instance.  If no
                request, does nothing, returns None.  If request found, sets up
                output to match the request; creates network data; renders it to
                the spec in the request, and returns whatever the render type
                returns from its render method. 

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
        network_data_request = None
        network_data_outputter = None
        entity_dictionary = None
        my_params = None

        # init
        debug_flag = False

        # do we have a request passed in?
        if ( network_data_request_IN is not None ):
        
            # yes - use it.
            self.set_network_data_request( network_data_request_IN )
            
        #-- END check to see if request passed in.
        
        # got a request?
        network_data_request = self.get_network_data_request()
        if ( network_data_request is not None ):
            
            # ! TODO - set up output.
            
            # ! ----> build network data from request.

            # create the entity_dictionary
            entity_dictionary = self.create_entity_dict()

            # create instance of NetworkDataOutput.
            #network_data_outputter = self.get_NDO_instance()

            # initialize it.
            #network_data_outputter.set_query_set( query_set_IN )
            #network_data_outputter.set_person_dictionary( person_dictionary )

            # initialize NetworkDataOutput instance from params.
            #my_params = self.get_param_container()
            #network_data_outputter.initialize_from_params( my_params )

            # render and return the result.
            #network_OUT = network_data_outputter.render()

            # add some debug?
            if ( debug_flag == True ):

                # yup.
                network_OUT += "\n\n" + network_data_outputter.debug + "\n\n"

            #-- END check to see if we have debug to output. --#

        #-- END check to make sure we have a query set. --#

        return network_OUT

    #-- END render_network_data() --#


    def set_network_data_request( self, value_IN ):
        
        # return reference
        value_OUT = None
        
        # store it
        self.m_network_data_request = value_IN
        
        # return it
        value_OUT = self.get_network_data_request()
        
        return value_OUT
    
    #-- END method set_network_data_request() --#


#-- END class NetworkOutput --#