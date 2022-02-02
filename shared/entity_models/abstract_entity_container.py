'''
Copyright 2021 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context.

context is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context. If not, see http://www.gnu.org/licenses/.
'''

#================================================================================
# Imports
#================================================================================

# python imports
import logging

# Django imports
#from django.contrib.postgres.fields import JSONField
from django.db import models

# context imports
from context.models import Abstract_Context_With_JSON
from context.models import Entity
from context.models import Entity_Identifier_Type
from context.shared.entity_models import output_debug
from context.shared.entity_models import output_log_message


#================================================================================
# ! ==> Abstract Models
#================================================================================


# Abstract_Entity_Container model
class Abstract_Entity_Container( Abstract_Context_With_JSON ):

    '''
    To extend:
    - make child model extend this class: `class Article( Abstract_Entity_Container ):`
    - give child model an __init__() method if one not already present.  Example:

        #def __init__( self, *args, **kwargs ):

            # call parent __init()__ first.
            super( Article, self ).__init__( *args, **kwargs )

            # then, initialize variable.
            self.my_entity_name_prefix = self.ENTITY_NAME_PREFIX
            self.my_entity_type_slug = self.ENTITY_TYPE_SLUG_ARTICLE
            self.my_base_entity_id_type = self.ENTITY_ID_TYPE_ARTICLE_SOURCENET_ID

        #-- END method __init__() --#

    - make sure that the three "my_*" variables are set appropriately for the
        class.  For example, in the above, the Article class sets the "my_*"
        variables to its own entity name prefix, entity type slug, and base ID
        type.
    - also consider putting class-specific entity-related values in
        CONSTANTS-ish within the class, as is done in the Article example above.
    - copy the `update_entity()` stub into the class and implement a method to
        first call the `load_entity()` method to make a base entity, then
        populate traits and identifiers, and if needed make related entities and
        relations.
    - add unit test methods for both `load_entity()` and `update_entity()` to
        your project's tests.  Use the context_text Article model test file as a
        template:  `context_text/tests/models/test_Article_model.py` at
        https://github.com/jonathanmorgan/context_text.
    - If you create one or more new Entity Identifier Types for your entity,
        make sure to add them to the database, and then if you use fixtures for
        testing, to whatever fixtures you use.
    '''

    #---------------------------------------------------------------------------
    # ! ----> model fields and meta
    #---------------------------------------------------------------------------


    entity = models.ForeignKey( Entity, on_delete = models.SET_NULL, blank = True, null = True )

    # meta class so we know this is an abstract class.
    class Meta:

        abstract = True

    #-- END class Meta --#



    #----------------------------------------------------------------------
    # ! ----> class variables
    #----------------------------------------------------------------------


    #----------------------------------------------------------------------
    # NOT instance variables
    # Class variables - overriden by __init__() per instance if same names, but
    #    if not set there, shared!
    #----------------------------------------------------------------------


    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------


    #---------------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super().__init__( *args, **kwargs )

        # then, initialize variable.
        self.my_entity_name_prefix = None
        self.my_entity_type_slug = None
        self.my_base_entity__id_type = None

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ""

        string_OUT = self.to_string()

        return string_OUT

    #-- END method __str__() --#


    #---------------------------------------------------------------------------
    # ! ----> instance methods
    #---------------------------------------------------------------------------


    def get_entity( self, *args, **kwargs ):

        '''
        Returns entity nested in this instance.
        Preconditions: None
        Postconditions: None

        Returns the entity stored in the instance.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "get_entity"

        # return the content.
        value_OUT = self.entity

        return value_OUT

    #-- END method get_entity() --#


    def has_entity( self, *args, **kwargs ):

        '''
        Calls load_entity(), with do_create_if_none_IN set to False.  Returns
            True if Entity returned by load_entity(), False if None returned.
        Preconditions: None
        Postconditions: None

        Returns True if Entity returned by load_entity(), False if None found.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "has_entity"
        entity_instance = None

        # call load_entity()
        entity_instance = self.load_entity( do_create_if_none_IN = False )

        # got an entity?
        if ( entity_instance is None ):

            # no.  Return False.
            value_OUT = False

        else:

            # no None.  Check type to make sure it is an Entity?
            value_OUT = True

        #-- END check to see if instance returned from load_entity() --#

        return value_OUT

    #-- END method has_entity() --#


    def load_entity( self, do_create_if_none_IN = True, *args, **kwargs ):

        '''
        Tries to find the entity for this class instance in context:
        - If it finds a match, stores it in instance, and returns it.
        - If not:
            - If it has been asked to create, creates a basic entity, with only
            unique identifier being one that refers to the django ID, saves it,
            stores it in this instance, then returns it.
            - If not creating, then returns None.

        Preconditions: This instance must have been saved so it has an id.  The
            following variables also must be set correctly for the instance in
            the child class __init__() method:
            - self.my_entity_name_prefix
            - self.my_entity_type_slug
            - self.my_base_entity__id_type

        Postconditions: Returns entity for this instance.  If one doesn't exist
            and do_create_if_none_IN == True, then makes a new one and returns
            it.  To actually fully populate the entity instance, once you load a
            new entity instance, you should call update_entity(), or just create
            as part of a call to update_entity() - it calls this method to get
            the entity instance that it updates.
        '''

        # return reference
        value_OUT = None

        # declare variables
        entity_instance = None
        my_instance_id = None
        identifier_type_name = None
        entity_identifier_type = None
        existing_entity_qs = None
        existing_entity_count = None
        entity_name_prefix = None
        entity_type_slug = None
        entity_type = None

        # init
        identifier_type_name = self.my_base_entity_id_type

        # does instance have an entity?
        entity_instance = self.get_entity()
        if ( entity_instance is None ):

            # no nested entity.  check to see if already an entity with this ID.
            my_instance_id = self.id

            # filter on identifier with type from self.my_base_entity_id_type
            entity_identifier_type = Entity_Identifier_Type.get_type_for_name( identifier_type_name )
            existing_entity_qs = Entity.objects.filter( entity_identifier__entity_identifier_type = entity_identifier_type )

            # ...and the ID of the current instance.
            existing_entity_qs = existing_entity_qs.filter( entity_identifier__uuid = my_instance_id )

            # what have we got?
            existing_entity_count = existing_entity_qs.count()
            if existing_entity_count == 1:

                # Found one. Store it and return it.
                entity_instance = existing_entity_qs.get()
                self.set_entity( entity_instance )
                self.save()
                value_OUT = self.get_entity()

            elif existing_entity_count == 0:

                # no match.
                log_message = "No entities with identifier of type {}, uuid = {}".format( identifier_type_name, my_instance_id )
                output_log_message( log_message, log_level_code_IN = logging.DEBUG, do_print_IN = DEBUG )

                # create?
                if ( do_create_if_none_IN == True ):

                    # no match.
                    log_message = "Creating entity with identifier of type {}, uuid = {}".format( identifier_type_name, my_instance_id )
                    output_log_message( log_message, log_level_code_IN = logging.DEBUG, do_print_IN = DEBUG )

                    # got an instance.  Create entity instance.  Init:
                    entity_name_prefix = self.my_entity_name_prefix
                    entity_type_slug = self.my_entity_type_slug

                    # create instance
                    entity_instance = Entity()
                    entity_instance.name = "{}{}".format( entity_name_prefix, my_instance_id )
                    entity_instance.notes = "{}".format( self )
                    entity_instance.save()

                    # set type
                    entity_type = entity_instance.add_entity_type( entity_type_slug )

                    # add identifier for django ID in this system.
                    identifier_type = Entity_Identifier_Type.get_type_for_name( identifier_type_name )
                    identifier_uuid = my_instance_id
                    entity_instance.set_identifier( identifier_uuid,
                                                    name_IN = identifier_type.name,
                                                    entity_identifier_type_IN = identifier_type )

                    # add to article
                    self.set_entity( entity_instance )
                    self.save()
                    value_OUT = self.get_entity()

                else:

                    # no match.
                    log_message = "No entities with identifier of type {}, uuid = {}".format( identifier_type_name, my_instance_id )
                    output_log_message( log_message, log_level_code_IN = logging.DEBUG, do_print_IN = DEBUG )

                    # do not create.
                    value_OUT = None

                #-- END check to see if we create when none found --#

            else:

                # more than one existing match.  Error.
                log_message = "ERROR - more than one entity ( {} ) with identifier of type {}, uuid = {}".format( existing_entity_count, identifier_type_name, my_instance_id )
                output_log_message( log_message, log_level_code_IN = logging.INFO, do_print_IN = True )
                value_OUT = None

            #-- END query for existing entity. --#

        else:

            # something already loaded - return what is nested.
            value_OUT = entity_instance

        #-- END check for associated entity --#

        return value_OUT

    #-- END method load_entity() --#


    def set_entity( self, value_IN = "", *args, **kwargs ):

        '''
        Accepts a reference to an Entity instance.  Stores it in this instance's
            entity variable.
        Preconditions: None
        Postconditions: None

        Returns the entity as it is stored in the instance.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "set_entity"

        # set the value in the instance.
        self.entity = value_IN

        # return the entity.
        value_OUT = self.entity

        return value_OUT

    #-- END method set_entity() --#


    def to_string( self ):

        # return reference
        string_OUT = ""

        if ( self.id ):

            string_OUT += str( self.id ) + " - "

        #-- END check to see if ID --#

        if ( self.entity ):

            string_OUT += self.entity

        #-- END check to see if content_description --#

        return string_OUT

    #-- END method to_string() --#


    def update_entity( self, *args, **kwargs ):

        '''
        Looks for entity for this instance in context.  If not found, creates a
            a new one and stores it in this instance.  Then, updates the entity
            based on information in this model instance.  Returns the entity.
        Preconditions: None
        Postconditions: If no associated entity in context, creates one and
            stores it internally.  Updates the entity in context based on
            current contents of this instance.
        '''

        # return reference
        value_OUT = None

        print( "ERROR - you need to implement your update_entity() method." )

        return value_OUT

    #-- END method update_entity() --#


#-- END abstract Abstract_Entity_Container model --#
