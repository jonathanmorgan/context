from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2019 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context.

context is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context. If not, see http://www.gnu.org/licenses/.
'''

#================================================================================
# Imports
#================================================================================

# python imports
import datetime
import json
import logging
import six

# Django imports
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
#from django.core.exceptions import DoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from django.db import models

# Django query object for OR-ing selection criteria together.
from django.db.models import Q

# taggit tagging APIs
from taggit.managers import TaggableManager

# python_utilities - logging
from python_utilities.logging.logging_helper import LoggingHelper


#================================================================================
# Shared variables and functions
#================================================================================


'''
Debugging code, shared across all models.
'''

DEBUG = False
DEFAULT_LOGGER_NAME = "context.models"

def output_log_message( message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = DEFAULT_LOGGER_NAME, log_level_code_IN = logging.DEBUG, do_print_IN = None ):

    '''
    Accepts message string.  If debug is on, logs it.  If not,
       does nothing for now.
    '''

    # declare variables
    do_print = False

    # init
    do_print = do_print_IN
    if ( do_print is None ):

        # parameter not set, default to instance debug flag.
        do_print = DEBUG

    #-- END check to see if print parameter set --#

    # got a message?
    if ( message_IN ):

        # call LoggingHelper method
        LoggingHelper.log_message( message_IN,
                                   method_IN = method_IN,
                                   indent_with_IN = indent_with_IN,
                                   logger_name_IN = logger_name_IN,
                                   log_level_code_IN = log_level_code_IN,
                                   do_print_IN = do_print )

    #-- END check to see if message. --#

#-- END method output_log_message() --#


def output_debug( message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = DEFAULT_LOGGER_NAME, do_print_IN = None ):

    '''
    Accepts message string.  If debug is on, logs it.  If not,
       does nothing for now.
    '''

    # declare variables
    do_print = False

    # init
    do_print = do_print_IN
    if ( do_print is None ):

        # parameter not set, default to instance debug flag.
        do_print = DEBUG

    #-- END check to see if print parameter set --#

    # got a message?
    if ( message_IN ):

        # call LoggingHelper method
        LoggingHelper.output_debug( message_IN,
                                    method_IN = method_IN,
                                    indent_with_IN = indent_with_IN,
                                    logger_name_IN = logger_name_IN,
                                    do_print_IN = do_print )

    #-- END check to see if message. --#

#-- END method output_debug() --#


#================================================================================
# ! ==> Abstract Models
#================================================================================


# Abstract_Context_Parent model
class Abstract_Context_Parent( models.Model ):

    #----------------------------------------------------------------------
    # ! ==> CONSTANTS-ish
    #----------------------------------------------------------------------

    # logging
    LOGGING_LOGGER_NAME = "context.models.Abstract_Context_Parent"

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------

    notes = models.TextField( blank = True, null = True )

    # tags!
    tags = TaggableManager( blank = True )

    # time stamps.
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )

    #----------------------------------------------------------------------
    # Meta
    #----------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:

        abstract = True
        ordering = [ 'last_modified' ]

    #-- END class Meta --#

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Abstract_Context_Parent, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        string_list.append( "Abstract_Context_Parent __str__() method" )
        string_list.append( "write a child version!" )

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#


    def output_log_message( self, message_IN, method_IN = "", indent_with_IN = "", log_level_code_IN = logging.DEBUG, do_print_IN = None ):

        '''
        Accepts message string.  If debug is on, logs it.  If not,
        does nothing for now.
        '''

        # declare variables
        logger_name = None
        do_print = False

        # init
        logger_name = self.LOGGING_LOGGER_NAME
        do_print = do_print_IN
        if ( do_print is None ):

            # parameter not set, default to instance debug flag.
            do_print = self.debug_flag

        #-- END check to see if print parameter set --#

        # got a message?
        if ( message_IN ):

            # call LoggingHelper method
            LoggingHelper.log_message( message_IN,
                                    method_IN = method_IN,
                                    indent_with_IN = indent_with_IN,
                                    logger_name_IN = logger_name,
                                    log_level_code_IN = log_level_code_IN,
                                    do_print_IN = do_print )

        #-- END check to see if message. --#

    #-- END method output_log_message() --#


    def output_debug( self, message_IN, method_IN = "", indent_with_IN = "", do_print_IN = None ):

        '''
        Accepts message string.  If debug is on, logs it.  If not,
        does nothing for now.
        '''

        # declare variables
        logger_name = None
        do_print = False

        # init
        logger_name = self.LOGGING_LOGGER_NAME
        do_print = do_print_IN
        if ( do_print is None ):

            # parameter not set, default to instance debug flag.
            do_print = self.debug_flag

        #-- END check to see if print parameter set --#

        # got a message?
        if ( message_IN ):

            # call LoggingHelper method
            LoggingHelper.output_debug( message_IN,
                                        method_IN = method_IN,
                                        indent_with_IN = indent_with_IN,
                                        logger_name_IN = logger_name,
                                        do_print_IN = do_print )

        #-- END check to see if message. --#

    #-- END method output_debug() --#


# Abstract_Context_With_JSON model
class Abstract_Context_With_JSON( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # ! ==> CONSTANTS-ish
    #----------------------------------------------------------------------

    # logging
    LOGGING_LOGGER_NAME = "context.models.Abstract_Context_With_JSON"

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------

    # from parent:
    #notes = models.TextField( blank = True, null = True )

    # tags!
    #tags = TaggableManager( blank = True )

    # time stamps.
    #create_date = models.DateTimeField( auto_now_add = True )
    #last_modified = models.DateTimeField( auto_now = True )

    # JSON field to hold structured related information.
    details_json = models.JSONField( blank = True, null = True )


    #----------------------------------------------------------------------
    # Meta
    #----------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:

        abstract = True
        ordering = [ 'last_modified' ]

    #-- END class Meta --#

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Abstract_Context_With_JSON, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        string_list.append( "Abstract_Context_With_JSON __str__() method" )
        string_list.append( "write a child version!" )

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#

#-- END abstract model Abstract_Context_With_JSON --#


# Abstract_Identifier_Type model
class Abstract_Identifier_Type( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    name = models.SlugField( unique = True )
    label = models.CharField( max_length = 255, null = True, blank = True )
    source = models.CharField( max_length = 255, null = True, blank = True )
    notes = models.TextField( blank = True, null = True )
    #type_list = models.ManyToManyField( Entity_Type )
    type_list = None

    # meta class so we know this is an abstract class.
    class Meta:

        abstract = True
        ordering = [ 'source', 'name' ]

    #-- END meta class --#


    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Abstract_Identifier_Type, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the parent stuff.

    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []
        type_qs = None
        type_count = None
        type_slug_list = None
        current_type = None
        current_type_slug = None
        type_list_string = None

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got a name?
        if ( self.name is not None ):

            string_list.append( str( self.name ) )

        #-- END check for name. --#

        # got a source?
        if ( self.source is not None ):

            string_list.append( str( self.source ) )

        #-- END check for source. --#

        # got any types?
        if ( self.type_list is not None ):

            # retrieve string list of types.
            type_list_string = self.type_list_to_string()
            if ( ( type_list_string is not None ) and ( type_list_string != "" ) ):

                # add it to string list.
                string_list.append( type_list_string )

            #-- END check to see if any types. --#

        #-- END check to see if type_list defined. --#

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#


    def type_list_to_string( self ):

        # return reference
        string_OUT = None

        # declare variables
        type_qs = None
        type_count = None
        type_slug_list = None
        current_type = None
        current_type_slug = None
        type_list_string = None

        # got any types?
        if ( self.type_list is not None ):

            # retrieve list of types.
            type_qs = self.type_list.all()

            # got any types?
            type_count = type_qs.count()
            if ( type_count > 0 ):

                type_slug_list = []
                for current_type in type_qs:

                    # get name
                    current_type_slug = current_type.slug
                    type_slug_list.append( current_type_slug )

                #-- END loop over types. --#

                # got any?
                if ( len( type_slug_list ) > 0 ):

                    # yes - create string list, add to output list.
                    string_OUT = "( {} )".format( ", ".join( type_slug_list ) )

                #-- END check to see if any types. --#

            #-- END check to see if any types. --#

        #-- END check to see if type_list defined. --#

        return string_OUT

    #-- END method type_list_to_string() --#


#= End Abstract_Identifier_Type Model ======================================================


# Abstract_Related_Type_Trait model
class Abstract_Related_Type_Trait( Abstract_Context_Parent ):


    '''
    Used to capture the traits that should be associated with an entity relation
        type.
    '''


    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    related_type = None
    name = models.CharField( max_length = 255 )
    slug = models.SlugField()
    label = models.CharField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True )
    required = models.BooleanField( default = False )

    # context
    trait_type = models.ForeignKey( "Trait_Type", on_delete = models.SET_NULL, blank = True, null = True )


    #----------------------------------------------------------------------
    # Meta
    #----------------------------------------------------------------------


    # Meta-data for this class.
    class Meta:

        abstract = True
        ordering = [ 'last_modified' ]

    #-- END class Meta --#


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Abstract_Related_Type_Trait, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got name?
        if ( self.name is not None ):

            string_list.append( str( self.name ) )

        #-- END check for name. --#

        # got slug?
        if ( self.slug is not None ):

            string_list.append( "( {} )".format( str( self.slug ) ) )

        #-- END check to see if slug. --#

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#


#-- END model Abstract_Related_Type_Trait --#


# Abstract Trait model
class Abstract_Trait( Abstract_Context_Parent ):

    #---------------------------------------------------------------------------
    # ! ----> model fields and meta
    #---------------------------------------------------------------------------


    #entity = models.ForeignKey( "Entity", on_delete = models.CASCADE )
    name = models.CharField( max_length = 255 )
    slug = models.SlugField( blank = True, null = True )
    value = models.CharField( max_length = 255, blank = True, null = True )
    value_json = models.JSONField( blank = True, null = True )
    label = models.CharField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True )

    # context
    trait_type = models.ForeignKey( "Trait_Type", on_delete = models.SET_NULL, blank = True, null = True )
    term = models.ForeignKey( "Term", on_delete = models.SET_NULL, blank = True, null = True )


    #---------------------------------------------------------------------------
    # ! ----> Meta
    #---------------------------------------------------------------------------


    # Meta-data for this class.
    class Meta:

        abstract = True

    #-- END class Meta --#


    #----------------------------------------------------------------------
    # ! ----> class variables
    #----------------------------------------------------------------------


    DEBUG = False


    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------


    @classmethod
    def filter_trait_qs( cls,
                         trait_qs_IN,
                         name_IN,
                         slug_IN = None,
                         label_IN = None,
                         *args,
                         **kwargs ):

        '''
        Shared method to perform filtering of trait QuerySets based on fields
            contained in this abstract class.  Should be called first in child
            filter methods, then they can do additional filtering from there.
        '''

        # return reference
        trait_qs_OUT = None

        # declare variables
        me = "filter_trait_qs"
        debug_flag = cls.DEBUG
        debug_message = None
        trait_qs = None
        trait_count = None
        trait_instance = None

        if ( debug_flag == True ):
            debug_message = "Inputs: trait_qs: {}; name: {}; slug: {}; label: {}".format( trait_qs_IN, name_IN, slug_IN, label_IN )
            output_debug(  debug_message, me )
        #-- END DEBUG --#

        # init
        trait_qs = trait_qs_IN

        # make sure we have a QuerySet
        if ( trait_qs is not None ):

            # make sure we have a name
            if ( ( name_IN is not None ) and ( name_IN != "" ) ):

                # look up name in Entity's trait set.
                trait_qs = trait_qs.filter( name = name_IN )
                trait_count = trait_qs.count()

            #-- END check to see if name. --#

            if ( debug_flag == True ):
                debug_message = "after name filter (name_IN = {}), result count: {}".format( name_IN, trait_qs.count() )
                output_debug( debug_message, me )
            #-- END DEBUG --#

            # got a slug?
            if ( slug_IN is not None ):

                # also filter on slug
                trait_qs = trait_qs.filter( slug = slug_IN )

            #-- END check to see if slug --#

            if ( debug_flag == True ):
                debug_message = "after slug filter (slug_IN = {}), result count: {}".format( slug_IN, trait_qs.count() )
                output_debug( debug_message, me )
            #-- END DEBUG --#

            # got a label?
            if ( label_IN is not None ):

                # also filter on label
                trait_qs = trait_qs.filter( label = label_IN )

            #-- END check to see if label --#

            if ( debug_flag == True ):
                debug_message = "after label filter (label_IN = {}), result count: {}".format( label_IN, trait_qs.count() )
                output_debug( debug_message, me )
            #-- END DEBUG --#

            # How many traits match?
            trait_count = trait_qs.count()

            # return QuerySet
            trait_qs_OUT = trait_qs

        else:

            # error
            debug_message = "ERROR - no trait QuerySet passed in, can't process."
            output_debug( debug_message, me )
            trait_qs_OUT = trait_qs_IN

        #-- END check to see if QuerySet passed in --#

        return trait_qs_OUT

    #-- END class method filter_trait_qs() --#


    #---------------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Abstract_Trait, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    # use parent def __str__( self ):


    #---------------------------------------------------------------------------
    # ! ----> instance methods
    #---------------------------------------------------------------------------


    def get_trait_value( self ):

        '''
        Retrieves the trait's value.  If value contains a "term", that takes
            precedence over the "value, so returns the Term's value.
        '''

        # return reference
        value_OUT = None

        # declare variables
        term_instance = None
        my_value = None
        my_value_json = None

        # got a term instance?
        term_instance = self.term
        if ( term_instance is not None ):

            # there is a term.  Return its value.
            value_OUT = term_instance.value

        else:

            # no term.  Is there a value?  If so, return it.
            my_value = self.value
            my_value_json = self.value_json
            if ( my_value is not None ):

                # there is a value.  Return it.
                value_OUT = self.value

            elif ( my_value_json is not None ):

                # no value, but there is JSON.  Return it.
                value_OUT = self.value_json

            else:

                # no value or JSON value.  Return None.
                value_OUT = None

            #-- END check to see if value or value JSON --#

        #-- END check to see if term instance --#

        return value_OUT

    #-- END method get_trait_value --#


    def get_trait_value_as_str( self ):

        '''
        retrieve value, cast to str, then return.
        '''

        # return reference
        value_OUT = None

        # get value.
        value_OUT = self.get_trait_value()

        # convert to string.
        value_OUT = str( value_OUT )

        return value_OUT

    #-- END method get_trait_value_as_str() --#


    def get_trait_value_as_int( self ):

        '''
        retrieve value, cast to int, then return.
        '''

        # return reference
        value_OUT = None

        # get value.
        value_OUT = self.get_trait_value()

        # convert to int.
        value_OUT = int( value_OUT )

        return value_OUT

    #-- END method get_trait_value_as_int() --#


    def get_trait_value_as_datetime( self, datetime_format_string_IN ):

        '''
        retrieve value, convert to datetime using format string passed in,
            return the result.
        '''

        # return reference
        value_OUT = None

        # get value.
        value_OUT = self.get_trait_value()

        # convert to int.
        value_OUT = datetime.datetime.strptime( value_OUT, datetime_format_string_IN )

        return value_OUT

    #-- END method get_trait_value_as_datetime() --#


    def get_trait_value_as_json( self ):

        '''
        retrieve value, convert to datetime using format string passed in,
            return the result.
        '''

        # return reference
        value_OUT = None

        # get value.
        value_OUT = self.get_trait_value()

        # convert to int.
        value_OUT = json.loads( value_OUT )

        return value_OUT

    #-- END method get_trait_value_as_json() --#


    def get_value_json( self, do_parse_IN = True ):

        '''
        Retrieves the trait's value.  If value contains a "term", that takes
            precedence over the "value, so returns the Term's value.
        '''

        # return reference
        value_OUT = None

        # declare variables

        # get from instance
        value_OUT = self.value_json

        # are we to parse?
        if ( do_parse_IN == True ):

            # yes.
            value_OUT = json.loads( value_OUT )

        #-- END check if we are to parse --#

        return value_OUT

    #-- END method get_value_json --#


#-- END model Abstract_Trait --#


# Abstract Trait model
class Abstract_Trait_Container( Abstract_Context_With_JSON ):

    #---------------------------------------------------------------------------
    # ! ----> model fields and meta
    #---------------------------------------------------------------------------


    #---------------------------------------------------------------------------
    # ! ----> Meta
    #---------------------------------------------------------------------------


    # Meta-data for this class.
    class Meta:

        abstract = True

    #-- END class Meta --#


    #----------------------------------------------------------------------
    # ! ----> class variables
    #----------------------------------------------------------------------


    DEBUG = False


    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------


    #---------------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Abstract_Trait_Container, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    # use parent def __str__( self ):


    #---------------------------------------------------------------------------
    # ! ----> instance methods
    #---------------------------------------------------------------------------


    def create_trait_instance( self, *args, **kwargs ):

        '''
        Creates an empty Abstract_Trait descendent, initializes it
            appropriately, then returns it.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        value_OUT = None

        print( "ERROR - you need to implement your create_trait_instance() method." )

        return value_OUT

    #-- END method get_trait_qs() --#


    def filter_trait_qs( self, trait_qs_IN, inheriting_type_trait_IN, *args, **kwargs ):

        '''
        Accepts trait QuerySet and type trait spec for the inheriting class's
            type (independent of Trait_Type).  Returns the trait QuerySet for
            the model class extending this class, filtered appropriately to only
            include traits that reference the trait specification stored in
            inheriting_type_trait_IN.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        value_OUT = None

        print( "ERROR - you need to implement your filter_trait_qs() method." )

        return value_OUT

    #-- END method filter_trait_qs() --#


    def get_trait( self,
                   name_IN,
                   slug_IN = None,
                   label_IN = None,
                   child_type_trait_IN = None ):

        '''
        Accepts identifying details of a trait whose instance (and so values)
            we want to retrieve.  If trait is found, returns it.  If not,
            returns None.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "get_entity_trait"
        debug_flag = self.DEBUG
        debug_message = None
        trait_qs = None
        trait_count = None
        trait_instance = None

        if ( debug_flag == True ):
            debug_message = "Inputs: name: {}; slug: {}; label: {}; entity_type_trait: {}.".format( name_IN, slug_IN, label_IN, entity_type_trait_IN )
            output_debug(  debug_message, me )
        #-- END DEBUG --#

        # make sure we have a name
        if ( ( name_IN is not None ) and ( name_IN != "" ) ):

            # look up name in Entity's trait set.
            trait_qs = self.get_trait_qs()

            # filter on name, slug, and label.
            trait_qs = Abstract_Trait.filter_trait_qs( trait_qs, name_IN, slug_IN = slug_IN, label_IN = label_IN )

            # got a child Abstract_Related_Type_Trait instance?
            if ( child_type_trait_IN is not None ):

                # also filter on Entity_Type_Trait
                trait_qs = self.filter_trait_qs( trait_qs, inheriting_type_trait_IN = child_type_trait_IN )

            #-- END check to see if source --#

            if ( debug_flag == True ):
                debug_message = "after Trait filter (child_type_trait_IN = {}), result count: {}".format( child_type_trait_IN, trait_qs.count() )
                output_debug( debug_message, me )
            #-- END DEBUG --#

            # How many traits match?
            trait_count = trait_qs.count()

            # if one, retrieve Trait and return it.
            if ( trait_count == 1 ):

                # call get()
                trait_instance = trait_qs.get()

                # return it
                instance_OUT = trait_instance

            elif ( trait_count > 1 ):

                # Multiple matches.  Return None.
                if ( debug_flag == True ):
                    debug_message = "Trait count = {}.".format( trait_count )
                    output_debug( debug_message, me )
                #-- END DEBUG --#

                instance_OUT = None

            elif ( trait_count == 0 ):

                # no matches.
                if ( debug_flag == True ):
                    debug_message = "No matches found."
                    output_debug( debug_message, me )
                #-- END DEBUG --#

                entity_OUT = None

            else:

                # ERROR - not 0 or 1 or > 1.
                if ( debug_flag == True ):
                    debug_message = "Inconceivable! - Trait count = {}.".format( trait_count )
                    output_debug( debug_message, me )
                #-- END DEBUG --#

                entity_OUT = None

            #-- END check to see if trait count is 1. --#

        else:

            # error
            print( "ERROR - no trait name passed in, can't process." )
            instance_OUT = None

        #-- END check to see if slug passed in --#

        return instance_OUT

    #-- END method get_trait() --#


    def get_trait_qs( self, *args, **kwargs ):

        '''
        Returns the trait QuerySet for the model class extending this class.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        value_OUT = None

        print( "ERROR - you need to implement your get_trait_qs() method." )

        return value_OUT

    #-- END method get_trait_qs() --#


    def set_child_type_trait( self, trait_instance_IN, child_type_trait_IN, *args, **kwargs ):

        '''
        Accepts trait instance and trait type appropriate to the inheriting
            class.  Places the type in the trait instance, return trait
            instance.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        value_OUT = None

        print( "ERROR - you need to implement your set_child_type_trait() method." )

        return value_OUT

    #-- END method set_child_type_trait() --#


    def set_trait( self,
                   name_IN,
                   value_IN,
                   slug_IN = None,
                   value_json_IN = None,
                   label_IN = None,
                   description_IN = None,
                   trait_type_IN = None,
                   term_IN = None,
                   child_type_trait_IN = None ):

        '''
        Accepts details of a trait we want to set for a given entity.

            - Checks to see if the entity already has a trait with the name passed in.
            - If entity_type_trait_IN is set, the name from this type supersedes the
            name passed in.
            - If existing trait exists, loads it into instance. If not, creates one.
            - then, updates based on the values passed in.
                - If trait specification passed in, updates meta information (not
            value) from there.
                - If not, updates from other parameters passed in.
                - Updates value of the trait based on parameters passed in.

        preconditions: Entity must already be saved for this to work.

        postconditions: Throws exception if type not found.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "set_entity_trait"
        trait_name = None
        trait_qs = None
        trait_count = None
        trait_instance = None
        is_updated = None

        # if trait definition passed in, get name from there.
        if ( child_type_trait_IN is not None ):

            # got one - it takes precedence.
            trait_name = child_type_trait_IN.name

        else:

            # no trait definition, use name passed in.
            trait_name = name_IN

        #-- END check to see where name comes from --#

        # make sure we have a name
        if ( ( trait_name is not None ) and ( trait_name != "" ) ):

            # init
            is_updated = False

            # look up name in Entity's trait set.
            trait_qs = self.get_trait_qs()
            trait_qs = trait_qs.filter( name = trait_name )
            trait_count = trait_qs.count()

            # what have we got?
            if ( trait_count == 0 ):

                # does not exist.  Create new.
                trait_instance = self.create_trait_instance()
                trait_instance.name = trait_name

                # save()
                trait_instance.save()

            elif ( trait_count == 1 ):

                # one exists.  Retrieve it.
                trait_instance = trait_qs.get()

            else:

                # more than one.  Error.
                print( "There are {} traits for the requested name {}.  Not right.  Dropping out.".format( trait_count, trait_name ) )
                trait_instance = None

            #-- END retrieve Entity_Trait instance. --#

            if ( trait_instance is not None ):

                # update values from those passed in.

                # do we have a trait definition?
                if ( child_type_trait_IN is not None ):

                    # we do - use it to set name and other metadata details.
                    self.set_child_type_trait( trait_instance, child_type_trait_IN )
                    is_updated = True

                else:

                    # no - set manually.

                    # --> trait_type
                    if ( trait_type_IN is not None ):

                        trait_instance.trait_type = trait_type_IN
                        is_updated = True

                    #-- END trait_type --#

                    # --> slug
                    if ( slug_IN is not None ):

                        trait_instance.slug = slug_IN
                        is_updated = True

                    #-- END slug --#

                    # --> label
                    if ( label_IN is not None ):

                        trait_instance.label = label_IN
                        is_updated = True

                    #-- END label --#

                    # --> description
                    if ( description_IN is not None ):

                        trait_instance.description = description_IN
                        is_updated = True

                    #-- END description --#

                #-- END check to see if trait definition from trait type passed in --#

                # --> value
                if ( value_IN is not None ):

                    trait_instance.value = value_IN
                    is_updated = True

                #-- END value --#

                # --> value_json
                if ( value_json_IN is not None ):

                    trait_instance.value_json = value_json_IN
                    is_updated = True

                #-- END value_json --#

                # --> term
                if ( term_IN is not None ):

                    trait_instance.term = term_IN
                    is_updated = True

                #-- END term --#

                # do we need to save?
                if ( is_updated == True ):

                    # yes.  save()
                    trait_instance.save()

                #-- END check to see if we need to save() --#

            #-- END check to see if we have an instance. --#

            instance_OUT = trait_instance

        else:

            # error
            print( "ERROR - no trait name passed in, can't process." )
            instance_OUT = None

        #-- END check to see if slug passed in --#

        return instance_OUT

    #-- END method set_trait() --#


#-- END model Abstract_Trait_Container --#


# Abstract_Relation model
class Abstract_Relation( Abstract_Trait_Container ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    relation_from = None
    relation_to = None
    directed = models.BooleanField( default = False )
    relation_type = None


    #----------------------------------------------------------------------
    # Meta
    #----------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:

        abstract = True

    #-- END class Meta --#

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Abstract_Relation, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got a relation_from?
        if ( self.relation_from is not None ):

            string_list.append( "FROM: {}".format( self.relation_from ) )

        #-- END check for relation_from. --#

        # got a to_term?
        if ( self.relation_to is not None ):

            string_list.append( "TO: {}".format( self.relation_to ) )

        #-- END check to see if relation_to. --#

        # directed?
        if ( self.directed is not None ):

            string_list.append( "( DIRECTED?: {} )".format( self.directed ) )

        #-- END check to see if directed. --#

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#

#-- END model Abstract_Relation --#


# Abstract_Type model
class Abstract_Type( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # ! ----> model fields and meta
    #----------------------------------------------------------------------


    slug = models.SlugField( unique = True )
    name = models.CharField( max_length = 255, blank = True, null = True )
    related_model = models.CharField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True )
    parent_type = None


    #----------------------------------------------------------------------
    # Meta
    #----------------------------------------------------------------------


    # Meta-data for this class.
    class Meta:

        abstract = True
        ordering = [ 'last_modified' ]

    #-- END class Meta --#


    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------


    @classmethod
    def get_type_for_slug( cls, type_slug_IN ):

        # return reference
        instance_OUT = None

        # declare variables
        me = "get_type_for_slug"
        type_qs = None
        type_count = None
        debug_message = None

        # try to retrieve based on slug
        type_qs = cls.objects.filter( slug = type_slug_IN )

        # got anything?
        type_count = type_qs.count()
        if ( type_count == 1 ):

            # yes.  Return it.
            instance_OUT = type_qs.get()

        elif ( type_count > 1 ):

            # more than one match. Impossible.
            debug_message = "In {}: more than one match for slug {} ( {} )".format( me, type_slug_IN, type_count )
            output_debug( debug_message, me )
            instance_OUT = None

        elif ( type_count == 0 ):

            # no match.
            debug_message = "In {}: no match for slug {}".format( me, type_slug_IN )
            output_debug( debug_message, me )
            instance_OUT = None

        else:

            # what?
            debug_message = "In {}: match count {} is neither 1, > 1, or 0 for slug {}?!?".format( me, type_count, type_slug_IN )
            output_debug( debug_message, me )
            instance_OUT = None

        #-- END check of result count --#

        return instance_OUT

    #-- END class method get_type_for_slug --#



    #---------------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Abstract_Type, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got a slug?  (slimy)
        if ( ( self.slug is not None ) and ( self.slug != "" ) ):

            string_list.append( str( self.slug ) )

        #-- END check for slug. --#

        # got a name?
        if ( ( self.name is not None ) and ( self.name != "" ) ):

            string_list.append( str( self.name ) )

        #-- END check to see if name. --#

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#


    #----------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------


    def get_trait_spec( self, slug_IN ):

        '''
        For Types that can have associated trait specifications (instances of
            descendants of Abstract_Related_Type_Trait, where you specify a set
            of traits that a type knows about and that are associated with the
            type), this method should be overridden to correctly look for and
            retrieve the Abstract_Related_Type_Trait child instance (I call it
            a "trait spec" since I think the name is confusing) for the slug
            passed in.
        postconditions: by default, just return None every time.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "get_trait_spec"
        trait_spec = None

        return instance_OUT

    #-- END method get_trait_spec() --#


#-- END model Abstract_Type --#


# Abstract_UUID model
class Abstract_UUID( Abstract_Context_Parent ):

    #---------------------------------------------------------------------------
    # ! ----> model fields and meta
    #---------------------------------------------------------------------------


    name = models.CharField( max_length = 255, null = True, blank = True )
    uuid = models.TextField( blank = True, null = True )
    id_type = models.CharField( max_length = 255, null = True, blank = True )
    source = models.CharField( max_length = 255, null = True, blank = True )
    notes = models.TextField( blank = True, null = True )

    # meta class so we know this is an abstract class.
    class Meta:
        abstract = True
        ordering = [ 'id_type', 'source', 'name', 'uuid' ]


    #---------------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Abstract_UUID, self ).__init__( *args, **kwargs )

        # then, initialize variable.
        self.bs_helper = None

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ""

        # declare variables
        prefix_string = ""

        if ( self.id ):

            # yes. output.
            string_OUT += str( self.id )
            prefix_string = " - "

        #-- END check to see if ID --#

        if ( self.name ):

            string_OUT += "{}name: {}".format( prefix_string, self.name )
            prefix_string = " - "

        #-- END check to see if name. --#

        if ( self.source ):

            string_OUT += "{}source: {}".format( prefix_string, self.source )
            prefix_string = " - "

        #-- END check to see if source. --#

        if ( self.uuid ):

            string_OUT += "{}uuid: {}".format( prefix_string, self.uuid )
            prefix_string = " - "

        #-- END check to see if uuid. --#

        if ( self.id_type ):

            string_OUT += "{}id_type: {}".format( prefix_string, self.id_type )
            prefix_string = " - "

        #-- END check to see if id_type. --#

        return string_OUT

    #-- END method __str__() --#


    #---------------------------------------------------------------------------
    # ! ----> instance methods
    #---------------------------------------------------------------------------


#= End Abstract_UUID Model ======================================================


# Abstract_Work_Log model
class Abstract_Work_Log( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------

    slug = models.SlugField( unique = True )
    name = models.CharField( max_length = 255, blank = True, null = True )
    worker = models.ForeignKey( User, on_delete = models.CASCADE, blank = True, null = True )

    #----------------------------------------------------------------------
    # Meta
    #----------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:

        abstract = True
        ordering = [ 'last_modified', 'slug' ]

    #-- END class Meta --#

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Abstract_Work_Log, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got a slug?  (slimy)
        if ( ( self.slug is not None ) and ( self.slug != "" ) ):

            string_list.append( str( self.slug ) )

        #-- END check for slug. --#

        # got a name?
        if ( ( self.name is not None ) and ( self.name != "" ) ):

            string_list.append( str( self.name ) )

        #-- END check to see if name. --#

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#

#-- END abstract model Abstract_Work_Log --#


#===============================================================================
# ! ==> Models
#===============================================================================


# Entity model
class Entity( Abstract_Trait_Container ):

    #----------------------------------------------------------------------
    # ! ----> model fields and meta
    #----------------------------------------------------------------------


    name = models.CharField( max_length = 255 )
    #entity_type = models.ForeignKey( 'Entity_Type', on_delete = models.SET_NULL, blank = True, null = True )
    my_entity_types = models.ManyToManyField( 'Entity_Type', through = 'Entity_Types', blank = True )

    # JSON field to hold structured related information.
    #details_json = JSONField( blank = True, null = True )


    #----------------------------------------------------------------------
    # ! ----> class variables
    #----------------------------------------------------------------------


    DEBUG = False


    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------


    @classmethod
    def filter_entities( cls,
                         entity_type_IN = None,
                         entity_type_slug_IN = None,
                         qs_IN = None ):

        # return reference
        qs_OUT = None

        # declare variables
        me = "Entity.filter_entities"
        debug_flag = cls.DEBUG
        debug_message = None
        entity_qs = None

        if ( debug_flag == True ):
            debug_message = "Inputs: entity_type_IN: {}; entity_type_slug_IN: {}".format( entity_type_IN, entity_type_slug_IN )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # figure out starting QuerySet
        if ( qs_IN is not None ):

            # QuerySet passed in.  Use it.
            entity_qs = qs_IN

        else:

            # no QuerySet passed in, use Entity_Identifier.objects.all()
            entity_qs = Entity.objects.all()

        #-- END init QuerySet --#

        #----------------------------------------------------------------------#
        # ! ----> entity type instance
        if ( entity_type_IN is not None ):

            # we have a type instance
            entity_qs = entity_qs.filter( my_entity_types = entity_type_IN )

        #-- END check to see if Entity_Type instance passed in. --#

        #----------------------------------------------------------------------#
        # ! ----> entity type slug
        if ( entity_type_slug_IN is not None ):

            # we have a type instance
            entity_qs = entity_qs.filter( my_entity_types__slug = entity_type_slug_IN )

        #-- END check to see if Entity_Type slug passed in. --#

        qs_OUT = entity_qs
        return qs_OUT

    #-- END class method filter_entities() --#


    @classmethod
    def lookup_entities( cls,
                         entity_type_IN = None,
                         entity_type_slug_IN = None,
                         id_uuid_IN = None,
                         id_name_IN = None,
                         id_source_IN = None,
                         id_id_type_IN = None,
                         id_entity_id_type_IN = None,
                         id_notes_IN = None,
                         qs_IN = None ):

        # return reference
        qs_OUT = None

        # declare variables
        me = "Entity.lookup_entities"
        debug_flag = cls.DEBUG
        debug_message = None
        entity_id_qs = None
        entity_id_count = None
        entity_id_instance = None
        entity_instance = None
        entity_id = None
        entity_id_set = None
        entity_id_set_count = None
        entity_qs = None

        if ( debug_flag == True ):
            debug_message = "Inputs: entity_type_IN: {}; entity_type_slug_IN: {}, id uuid: {}; id name: {}; id source: {}; id type: {}; Entity_Identifier_Type.".format( entity_type_IN, entity_type_slug_IN, id_uuid_IN, id_name_IN, id_source_IN, id_id_type_IN, id_entity_id_type_IN )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # figure out starting QuerySet
        if ( qs_IN is not None ):

            # QuerySet passed in.  Use it.
            entity_qs = qs_IN

        else:

            # no QuerySet passed in, use Entity_Identifier.objects.all()
            entity_qs = Entity.objects.all()

        #-- END init QuerySet --#

        # start with Entity_Identifier filtering.
        entity_id_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = id_uuid_IN,
                                                             id_name_IN = id_name_IN,
                                                             id_source_IN = id_source_IN,
                                                             id_id_type_IN = id_id_type_IN,
                                                             id_entity_id_type_IN = id_entity_id_type_IN,
                                                             id_notes_IN = id_notes_IN )

        # How many identifiers match?
        entity_id_count = entity_id_qs.count()

        # make a set of Entity IDs.
        entity_id_set = set()
        for entity_id_instance in entity_id_qs:

            # get entity and its ID
            entity_instance = entity_id_instance.entity
            entity_id = entity_instance.id

            # if not already in set, add it.
            if ( entity_id not in entity_id_set ):

                # add it.
                entity_id_set.add( entity_id )

            #-- END check to see if ID in set. --#

        #-- END loop over identifiers --#

        # filter entities to only these IDs.
        entity_qs = entity_qs.filter( id__in = entity_id_set )

        # do standard Entity-specific filtering
        entity_qs = cls.filter_entities( entity_type_IN, entity_type_slug_IN, entity_qs )

        # return QuerySet.
        qs_OUT = entity_qs

        return qs_OUT

    #-- END class method lookup_entities() --#


    @classmethod
    def get_entity_for_identifier( cls,
                                   id_uuid_IN,
                                   id_name_IN = None,
                                   id_source_IN = None,
                                   id_id_type_IN = None,
                                   id_entity_id_type_IN = None,
                                   id_notes_IN = None ):

        # return reference
        entity_OUT = None

        # declare variables
        me = "Entity.get_entity_for_identifier"
        debug_flag = cls.DEBUG
        debug_message = None
        entity_id_qs = None
        entity_id_count = None
        entity_id_instance = None
        entity_instance = None
        entity_id = None
        entity_id_set = None
        entity_id_set_count = None

        if ( debug_flag == True ):
            debug_message = "Inputs: uuid: {}; name: {}; source: {}; id_type: {}; Entity_Identifier_Type: {}.".format( id_uuid_IN, id_name_IN, id_source_IN, id_id_type_IN, id_entity_id_type_IN )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # first, filter identifiers
        entity_id_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = id_uuid_IN,
                                                             id_name_IN = id_name_IN,
                                                             id_source_IN = id_source_IN,
                                                             id_id_type_IN = id_id_type_IN,
                                                             id_entity_id_type_IN = id_entity_id_type_IN,
                                                             id_notes_IN = id_notes_IN )

        # How many identifiers match?
        entity_id_count = entity_id_qs.count()

        # if one, retrieve Entity and return it.
        if ( entity_id_count == 1 ):

            # call get()
            entity_id_instance = entity_id_qs.get()

            # retrieve related entity
            entity_instance = entity_id_instance.entity

            # return it
            entity_OUT = entity_instance

        elif ( entity_id_count > 1 ):

            # Multiple matches.
            if ( debug_flag == True ):
                debug_message = "Entity identifier count = {} for uuid: {}; name: {}; source: {}; type: {}.".format( entity_id_count, uuid_IN, id_name_IN, id_source_IN, id_type_IN )
                output_debug( debug_message, me )
            #-- END DEBUG --#

            # loop and see if they all have same entity.
            entity_id_set = set()
            for entity_id_instance in entity_id_qs:

                # get entity and its ID
                entity_instance = entity_id_instance.entity
                entity_id = entity_instance.id

                # if not already in set, add it.
                if ( entity_id not in entity_id_set ):

                    # add it.
                    entity_id_set.add( entity_id )

                #-- END check to see if ID in set. --#

            #-- END loop over identifiers --#

            # how many things in set?
            entity_id_set_count = len( entity_id_set )
            if ( entity_id_set_count == 1 ):

                # all are the same entity, so return it (still set from loop).
                entity_OUT = entity_instance

            else:

                # multiple entities match.  Print, then return None.
                if ( debug_flag == True ):
                    debug_message = "Multiple entities match for uuid: {}; name: {}; source: {}; type: {}.  IDs: {}".format( entity_id_count, uuid_IN, id_name_IN, id_source_IN, id_type_IN, entity_id_set )
                    output_debug( debug_message, me )
                #-- END DEBUG --#

                entity_OUT = None

            #-- END check to see if all identifiers refer to the same entity. --#

        elif ( entity_id_count == 0 ):

            # no matches.
            if ( debug_flag == True ):
                debug_message = "No matches for uuid: {}; name: {}; source: {}; type: {}.".format( uuid_IN, id_name_IN, id_source_IN, id_type_IN )
                output_debug( debug_message, me )
            #-- END DEBUG --#

            entity_OUT = None

        else:

            # ERROR - not 0 or 1 or > 1.
            if ( debug_flag == True ):
                debug_message = "Inconceivable! - Entity identifier count = {} for uuid: {}; name: {}; source: {}; type: {}.".format( entity_id_count, uuid_IN, id_name_IN, id_source_IN, id_type_IN )
                output_debug( debug_message, me )
            #-- END DEBUG --#

            entity_OUT = None

        #-- END check to see if entity identifier count is 1. --#

        return entity_OUT

    #-- END class method get_entity_for_identifier() --#


    #----------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got a name?
        if ( self.name is not None ):

            string_list.append( str( self.name ) )

        #-- END check for name. --#

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#

    #----------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------


    def add_entity_type( self, type_slug_IN = None, type_IN = None ):

        '''
        Accepts entity type slug.  Looks up type for that entity, adds it to
            those associated with this entity, then returns Type.

        preconditions: Entity must already be saved for this to work.

        postconditions: Throws exception if type not found.
        '''

        # return reference
        type_OUT = None

        # declare variables
        me = "add_entity_type"

        # make sure we have a type slug...
        if ( ( type_slug_IN is not None ) and ( type_slug_IN != "" ) ):

            # look up type using slug
            type_OUT = Entity_Type.objects.get( slug = type_slug_IN )

        #-- END check to see if slug passed in. --#

        # ...or a type.
        if ( type_IN is not None ):

            # look up type using slug
            type_OUT = type_IN

        #-- END check to see if slug passed in. --#

        # got a type?
        if ( type_OUT is not None ):

            # add to entity instance - won't create duplicate if already there.
            self.my_entity_types.add( type_OUT )

        else:

            # error
            print( "ERROR - no type ( type_slug_IN: {}; type_IN: {} ), can't process.".format( type_slug_IN, type_IN ) )
            type_OUT = None

        #-- END check to see if slug passed in --#

        return type_OUT

    #-- END method add_entity_type() --#


    def create_trait_instance( self, *args, **kwargs ):

        '''
        Creates an empty Abstract_Trait descendent, initializes it
            appropriately, then returns it.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        value_OUT = None

        # declare variables
        trait_instance = None

        # Create Entity_Trait, set self into "entity".
        trait_instance = Entity_Trait()
        trait_instance.entity = self
        value_OUT = trait_instance

        return value_OUT

    #-- END method get_trait_qs() --#


    def filter_trait_qs( self, trait_qs_IN, inheriting_type_trait_IN = None, *args, **kwargs ):

        '''
        Accepts trait QuerySet and type trait spec for the inheriting class's
            type (independent of Trait_Type).  Returns the trait QuerySet for
            the model class extending this class, filtered appropriately to only
            include traits that reference the trait specification stored in
            inheriting_type_trait_IN.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        qs_OUT = None

        # declare variables

        # init
        qs_OUT = trait_qs_IN

        # got an Entity_Type_Trait instance?
        if ( inheriting_type_trait_IN is not None ):

            # also filter on Entity_Type_Trait
            qs_OUT = qs_OUT.filter( entity_type_trait = inheriting_type_trait_IN )

        #-- END check to see if source --#

        return qs_OUT

    #-- END method filter_trait_qs() --#


    def get_entity_trait( self,
                          name_IN,
                          slug_IN = None,
                          label_IN = None,
                          entity_type_trait_IN = None ):

        '''
        Accepts identifying details of a trait whose instance (and so values)
            we want to retrieve.  If trait is found, returns it.  If not,
            returns None.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "get_entity_trait"
        debug_flag = self.DEBUG
        debug_message = None

        if ( debug_flag == True ):
            debug_message = "Inputs: name: {}; slug: {}; label: {}; entity_type_trait: {}.".format( name_IN, slug_IN, label_IN, entity_type_trait_IN )
            output_debug(  debug_message, me )
        #-- END DEBUG --#

        # call parent get_trait()
        instance_OUT = self.get_trait( name_IN,
                                       slug_IN = slug_IN,
                                       label_IN = label_IN,
                                       child_type_trait_IN = entity_type_trait_IN )

        return instance_OUT

    #-- END method get_entity_trait() --#


    def get_my_entity_type( self, slug_IN = None ):

        '''
        Retrieves Entity_Type(s) for the current instance.  If no slug passed
            in, tries to retrieve a single entity type.  If multiple found,
            returns None.  If slug passed in, tries to retrieve the a type
            instance matching that slug that is associated with this instance.
            If none found, returns None.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "get_my_entity_type"
        debug_flag = self.DEBUG
        debug_message = None
        type_qs = None
        type_count = None

        if ( debug_flag == True ):
            debug_message = "Inputs: name: {}; slug: {}; label: {}; entity_type_trait: {}.".format( name_IN, slug_IN, label_IN, entity_type_trait_IN )
            output_debug(  debug_message, me )
        #-- END DEBUG --#

        # got a slug?
        if ( ( slug_IN is not None ) and ( slug_IN != "" ) ):

            # we have a slug.
            type_qs = self.my_entity_types.filter( slug = slug_IN )

        else:

            # no slug.  Just get all.
            type_qs = self.my_entity_types.all()

        #-- END make type QuerySet --#

        # got a single match?
        type_count = type_qs.count()
        if ( type_count == 1 ):

            # yes, we have a single match.  Return it.
            instance_OUT = type_qs.get()

        else:

            # not a single match.  Return None.
            instance_OUT = None

        #-- END check to see if match --#

        return instance_OUT

    #-- END method get_my_entity_type() --#


    def get_identifier( self,
                        id_name_IN,
                        id_source_IN = None,
                        id_id_type_IN = None,
                        id_type_IN = None,
                        id_uuid_IN = None,
                        id_notes_IN = None ):

        # return reference
        instance_OUT = None

        # declare variables
        me = "Entity.get_identifier"
        debug_flag = self.DEBUG
        debug_message = None
        entity_id_qs = None
        entity_id_count = None
        entity_id_instance = None

        if ( debug_flag == True ):
            debug_message = "Inputs: uuid: {}; name: {}; source: {}; type: {}.".format( id_uuid_IN, id_name_IN, id_source_IN, id_type_IN )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # ! ----> start with name
        entity_id_qs = self.entity_identifier_set.filter( name = id_name_IN )

        if ( debug_flag == True ):
            debug_message = "after name filter (id_name_IN = {}), result count: {}".format( id_name_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # ! ----> got an id_type string?
        if ( id_id_type_IN is not None ):

            # also filter on type
            entity_id_qs = entity_id_qs.filter( id_type = id_id_type_IN )

        #-- END check to see if type --#

        if ( debug_flag == True ):
            debug_message = "after type filter (id_type_IN = {}), result count: {}".format( id_type_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # ! ----> got a type?
        if ( id_type_IN is not None ):

            # also filter on type
            entity_id_qs = entity_id_qs.filter( entity_identifier_type = id_type_IN )

        #-- END check to see if type --#

        if ( debug_flag == True ):
            debug_message = "after type filter (id_type_IN = {}), result count: {}".format( id_type_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # ! ----> got a source?
        if ( id_source_IN is not None ):

            # also filter on source
            entity_id_qs = entity_id_qs.filter( source = id_source_IN )

        #-- END check to see if source --#

        if ( debug_flag == True ):
            debug_message = "after source filter (id_source_IN = {}), result count: {}".format( id_source_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # ! ----> got a UUID (value)?
        if ( id_uuid_IN is not None ):

            # also filter on source
            entity_id_qs = entity_id_qs.filter( uuid = id_uuid_IN )

        #-- END check to see if UUID --#

        if ( debug_flag == True ):
            debug_message = "after UUID filter (id_uuid_IN = {}), result count: {}".format( id_uuid_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # ! ----> got notes?
        if ( id_notes_IN is not None ):

            # also filter on source
            entity_id_qs = entity_id_qs.filter( notes = id_notes_IN )

        #-- END check to see if notes --#

        if ( debug_flag == True ):
            debug_message = "after notes filter (id_notes_IN = {}), result count: {}".format( id_notes_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # How many identifiers match?
        entity_id_count = entity_id_qs.count()

        # if one, retrieve Entity and return it.
        if ( entity_id_count == 1 ):

            # call get()
            entity_id_instance = entity_id_qs.get()

            # return it.
            instance_OUT = entity_id_instance

        elif ( entity_id_count > 1 ):

            # Multiple matches.
            if ( debug_flag == True ):
                debug_message = "Entity identifier count = {} for name: {}; source: {}; id_type: {}; entity ID type: {}; UUID: {}.".format( entity_id_count, id_name_IN, id_source_IN, id_id_type_IN, id_type_IN, id_uuid_IN )
                output_debug( debug_message, me )
            #-- END DEBUG --#

            instance_OUT = None

        elif ( entity_id_count == 0 ):

            # no matches.
            if ( debug_flag == True ):
                debug_message = "No matches for name: {}; source: {}; id_type: {}; entity ID type: {}; UUID: {}.".format( id_name_IN, id_source_IN, id_id_type_IN, id_type_IN, id_uuid_IN )
                output_debug( debug_message, me )
            #-- END DEBUG --#

            instance_OUT = None

        else:

            # ERROR - not 0 or 1 or > 1.
            if ( debug_flag == True ):
                debug_message = "Inconceivable! - Entity identifier count = {} for name: {}; source: {}; id_type: {}; entity ID type: {}; UUID: {}.".format( entity_id_count, id_name_IN, id_source_IN, id_id_type_IN, id_type_IN, id_uuid_IN )
                output_debug( debug_message, me )
            #-- END DEBUG --#

            instance_OUT = None

        #-- END check to see if entity identifier count is 1. --#

        return instance_OUT

    #-- END class method get_identifier() --#


    def get_trait_qs( self, *args, **kwargs ):

        '''
        Returns the trait QuerySet for the model class extending this class.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        value_OUT = None

        # return the Entity_Trait related set.
        value_OUT = self.entity_trait_set.all()

        return value_OUT

    #-- END method get_trait_qs() --#


    def set_child_type_trait( self, trait_instance_IN, child_type_trait_IN, *args, **kwargs ):

        '''
        Accepts trait instance and trait type appropriate to the inheriting
            class.  Places the type in the trait instance, return trait
            instance.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        value_OUT = None

        # we do - use it to set name and other metadata details.
        trait_instance_IN.set_entity_type_trait( child_type_trait_IN )
        value_OUT = trait_instance_IN

        return value_OUT

    #-- END method set_child_type_trait() --#


    def set_entity_trait( self,
                          name_IN,
                          value_IN,
                          slug_IN = None,
                          value_json_IN = None,
                          label_IN = None,
                          description_IN = None,
                          trait_type_IN = None,
                          term_IN = None,
                          entity_type_trait_IN = None ):

        '''
        Accepts details of a trait we want to set for a given entity.

            - Checks to see if the entity already has a trait with the name passed in.
            - If entity_type_trait_IN is set, the name from this type supersedes the
            name passed in.
            - If existing trait exists, loads it into instance. If not, creates one.
            - then, updates based on the values passed in.
                - If trait specification passed in, updates meta information (not
            value) from there.
                - If not, updates from other parameters passed in.
                - Updates value of the trait based on parameters passed in.

        preconditions: Entity must already be saved for this to work.

        postconditions: Throws exception if type not found.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "set_entity_trait"

        # call parent method
        instance_OUT = self.set_trait( name_IN,
                                       value_IN,
                                       slug_IN = slug_IN,
                                       value_json_IN = value_json_IN,
                                       label_IN = label_IN,
                                       description_IN = description_IN,
                                       trait_type_IN = trait_type_IN,
                                       term_IN = term_IN,
                                       child_type_trait_IN = entity_type_trait_IN )

        return instance_OUT

    #-- END method set_entity_trait() --#


    def set_identifier( self,
                        uuid_IN,
                        name_IN = None,
                        id_type_IN = None,
                        source_IN = None,
                        notes_IN = None,
                        entity_identifier_type_IN = None ):

        '''
        Accepts identifier UUID value, optional details, and optional identifier
            type instance reference.  Creates entity identifier, stores
            information passed in inside.

        preconditions: Entity must already be saved for this to work.

        postconditions: Throws exception if type not found.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "set_entity_trait"
        id_name = None
        id_qs = None
        id_count = None
        id_instance = None
        is_updated = None

        # if trait definition passed in, get name from there.
        if ( entity_identifier_type_IN is not None ):

            # got one - it takes precedence.
            id_name = entity_identifier_type_IN.name

        else:

            # no trait definition, use name passed in.
            id_name = name_IN

        #-- END check to see where name comes from --#

        # make sure we have a name
        if ( ( id_name is not None ) and ( id_name != "" ) ):

            # init
            is_updated = False

            # look up name in Entity's identifier set.
            id_qs = self.entity_identifier_set.filter( name = id_name )
            id_count = id_qs.count()

            # what have we got?
            if ( id_count == 0 ):

                # does not exist.  Create new.
                id_instance = Entity_Identifier()
                id_instance.entity = self
                id_instance.name = id_name

                # save()
                id_instance.save()

            elif ( id_count == 1 ):

                # one exists.  Retrieve it.
                id_instance = id_qs.get()

            else:

                # more than one.  Error.
                print( "There are {} identifiers for the requested name {}.  Not right.  Dropping out.".format( id_count, id_name ) )
                id_instance = None

            #-- END retrieve Entity_Identifier instance. --#

            if ( id_instance is not None ):

                # update values from those passed in.

                # do we have an identifier type?
                if ( entity_identifier_type_IN is not None ):

                    # we do - use it to set name and other metadata details.
                    id_instance.set_entity_identifier_type( entity_identifier_type_IN )
                    is_updated = True

                #-- END check to see if type passed in. --#

                # then, update with other parameters if they are passed in.

                # --> id_type
                if ( id_type_IN is not None ):

                    id_instance.id_type = id_type_IN
                    is_updated = True

                #-- END id_type --#

                # --> source
                if ( source_IN is not None ):

                    id_instance.source = source_IN
                    is_updated = True

                #-- END source --#

                # --> notes
                if ( notes_IN is not None ):

                    id_instance.notes = notes_IN
                    is_updated = True

                #-- END notes --#

                # --> UUID
                if ( uuid_IN is not None ):

                    id_instance.uuid = uuid_IN
                    is_updated = True

                #-- END UUID --#

                # do we need to save?
                if ( is_updated == True ):

                    # yes.  save()
                    id_instance.save()

                #-- END check to see if we need to save() --#

            #-- END check to see if we have an instance. --#

            instance_OUT = id_instance

        else:

            # error
            print( "ERROR - no identifier name passed in, can't process." )
            instance_OUT = None

        #-- END check to see if id name passed in --#

        return instance_OUT

    #-- END method set_identifier() --#


#-- END model Entity --#


# Entity_Identifier_Type model
class Entity_Identifier_Type( Abstract_Identifier_Type ):

    #----------------------------------------------------------------------
    # ! ----> model fields and meta
    #----------------------------------------------------------------------


    # inherited:
    #name = models.SlugField( unique = True )
    #label = models.CharField( max_length = 255, null = True, blank = True )
    #source = models.CharField( max_length = 255, null = True, blank = True )
    #notes = models.TextField( blank = True, null = True )
    type_list = models.ManyToManyField( 'Entity_Type', blank = True )

    # meta class so we know this is an abstract class.
    class Meta:

        ordering = [ 'source', 'name' ]

    #-- END meta class --#


    #----------------------------------------------------------------------
    # ! ----> class variables
    #----------------------------------------------------------------------


    DEBUG = False


    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------


    @classmethod
    def get_type_for_name( cls, type_name_IN ):

        # return reference
        type_OUT = None

        # declare variables
        me = "Entity_Identifier_Type.get_type_for_name"
        error_message = None
        type_qs = None
        type_instance = None

        # make sure we have a type name
        if ( ( type_name_IN is not None ) and ( type_name_IN != "" ) ):

            # we have a type name.  Try to retrieve it.
            type_qs = cls.objects.filter( name = type_name_IN )

            try:

                # look up type using slug
                type_instance = type_qs.get()

            except cls.MultipleObjectsReturned as mor:

                if ( cls.DEBUG == True ):
                    error_message = "Multiple instances returned for name {}.  Unfortunate!".format( type_name_IN )
                    output_debug( error_message, method_IN = me )
                #-- END DEBUG --#

                type_instance = None

            except cls.DoesNotExist as dne:

                if ( cls.DEBUG == True ):
                    error_message = "No instance found for name {}.".format( type_name_IN )
                    output_debug( error_message, method_IN = me )
                #-- END DEBUG --#

                type_instance = None

            #-- END try-except --#

        #-- END check to see if type name passed in --#

        type_OUT = type_instance

        return type_OUT

    #-- END class method get_type_for_name() --#


    #----------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Identifier_Type, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the parent stuff.


    #----------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------


#= End Entity_Identifier_Type Model ======================================================


# Entity_Identifier model
class Entity_Identifier( Abstract_UUID ):

    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------

    @classmethod
    def filter_identifiers( cls,
                            id_uuid_IN = None,
                            id_name_IN = None,
                            id_source_IN = None,
                            id_id_type_IN = None,
                            id_entity_id_type_IN = None,
                            id_notes_IN = None,
                            qs_IN = None ):

        # return reference
        qs_OUT = None

        # declare variables
        me = "Entity_Identifier.filter_identifiers"
        debug_flag = cls.DEBUG
        debug_message = None
        entity_id_qs = None
        entity_id_count = None
        entity_id_instance = None
        entity_instance = None
        entity_id = None
        entity_id_set = None
        entity_id_set_count = None

        if ( debug_flag == True ):
            debug_message = "Inputs: uuid: {}; name: {}; source: {}; id_type: {}; entity ID type: {}.".format( id_uuid_IN, id_name_IN, id_source_IN, id_id_type_IN, id_entity_id_type_IN )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # figure out starting QuerySet
        if ( qs_IN is not None ):

            # QuerySet passed in.  Use it.
            entity_id_qs = qs_IN

        else:

            # no QuerySet passed in, use Entity_Identifier.objects.all()
            entity_id_qs = Entity_Identifier.objects.all()

        #-- END init QuerySet --#

        # got a UUID?
        if ( id_uuid_IN is not None ):

            # start with uuid
            entity_id_qs = entity_id_qs.filter( uuid = id_uuid_IN )

        #-- END check to see if UUID passed in. --#

        if ( debug_flag == True ):
            debug_message = "after UUID filter (uuid_IN = {}), result count: {}".format( id_uuid_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # got a name?
        if ( id_name_IN is not None ):

            # also filter on name
            entity_id_qs = entity_id_qs.filter( name = id_name_IN )

        #-- END check to see if name --#

        if ( debug_flag == True ):
            debug_message = "after name filter (id_name_IN = {}), result count: {}".format( id_name_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # got a basic type?
        if ( id_id_type_IN is not None ):

            # also filter on type
            entity_id_qs = entity_id_qs.filter( id_type = id_id_type_IN )

        #-- END check to see if type --#

        if ( debug_flag == True ):
            debug_message = "after basic string id_type filter (id_id_type_IN = {}), result count: {}".format( id_id_type_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # got an Entity_Identifier_Type to match?
        if ( id_entity_id_type_IN is not None ):

            # also filter on type
            entity_id_qs = entity_id_qs.filter( entity_identifier_type = id_entity_id_type_IN )

        #-- END check to see if type --#

        if ( debug_flag == True ):
            debug_message = "after Entity_Identifier_Type filter (id_type_IN = {}), result count: {}".format( id_type_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # got a source?
        if ( id_source_IN is not None ):

            # also filter on source
            entity_id_qs = entity_id_qs.filter( source = id_source_IN )

        #-- END check to see if source --#

        if ( debug_flag == True ):
            debug_message = "after source filter (id_source_IN = {}), result count: {}".format( id_source_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # got notes?
        if ( id_notes_IN is not None ):

            # also filter on source
            entity_id_qs = entity_id_qs.filter( notes = id_notes_IN )

        #-- END check to see if source --#

        if ( debug_flag == True ):
            debug_message = "after notes filter (id_notes_IN = {}), result count: {}".format( id_notes_IN, entity_id_qs.count() )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # How many identifiers match?
        entity_id_count = entity_id_qs.count()

        # Multiple matches.
        if ( debug_flag == True ):
            debug_message = "Entity identifier count = {} for uuid: {}; name: {}; source: {}; id_type: {}; Entity_Identifier_Type: {}; notes: {}.".format( entity_id_count, uuid_IN, id_name_IN, id_source_IN, id_id_type_IN, id_entity_id_type_IN, id_notes_IN )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # return the result
        qs_OUT = entity_id_qs

        return qs_OUT

    #-- END class method filter_identifiers() --#


    #----------------------------------------------------------------------
    # ! ----> model fields and meta
    #----------------------------------------------------------------------


    #name = models.CharField( max_length = 255, null = True, blank = True )
    #uuid = models.TextField( blank = True, null = True )
    #id_type = models.CharField( max_length = 255, null = True, blank = True )
    #source = models.CharField( max_length = 255, null = True, blank = True )
    #notes = models.TextField( blank = True, null = True )
    entity = models.ForeignKey( Entity, on_delete = models.CASCADE )
    entity_identifier_type = models.ForeignKey( Entity_Identifier_Type, blank = True, null = True, on_delete = models.SET_NULL )


    #----------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Identifier, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ""

        # declare variables
        prefix_string = ""

        if ( self.id ):

            # yes. output.
            string_OUT += str( self.id )
            prefix_string = " - "

        #-- END check to see if ID --#

        if ( self.name ):

            string_OUT += "{}name: {}".format( prefix_string, self.name )
            prefix_string = " - "

        #-- END check to see if name. --#

        if ( self.source ):

            string_OUT += "{}source: {}".format( prefix_string, self.source )
            prefix_string = " - "

        #-- END check to see if source. --#

        if ( self.uuid ):

            string_OUT += "{}uuid: {}".format( prefix_string, self.uuid )
            prefix_string = " - "

        #-- END check to see if uuid. --#

        if ( self.id_type ):

            string_OUT += "{}id_type: {}".format( prefix_string, self.id_type )
            prefix_string = " - "

        #-- END check to see if id_type. --#

        if ( self.entity ):

            string_OUT += "{}Entity ID: {}".format( prefix_string, self.entity.id )
            prefix_string = " - "

        #-- END check to see if id_type. --#

        if ( self.entity_identifier_type ):

            string_OUT += "{}Type: {}".format( prefix_string, self.entity_identifier_type )
            prefix_string = " - "

        #-- END check to see if id_type. --#

        return string_OUT

    #-- END method __str__() --#


    #----------------------------------------------------------------------
    # ! ----> class variables
    #----------------------------------------------------------------------


    DEBUG = False


    #----------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------


    def set_entity_identifier_type( self,
                                    entity_identifier_type_IN,
                                    do_use_to_update_fields_IN = True ):

        '''
        Accepts entity identifier instance.  Stores it internally, then if not
            None and we have been asked to update, updates other fields from it.

        postconditions: Returns the type instance that was stored.  Does not
            actually save the Entity_Identifier.  If you want updates from
            setting type to persist, you must call save() on the instance.

        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "set_entity_identifier_type"
        my_name = None
        my_source = None
        my_notes = None

        # store what was passed in.
        self.entity_identifier_type = entity_identifier_type_IN
        instance_OUT = self.entity_identifier_type

        # are we to update other fields?
        if ( do_use_to_update_fields_IN == True ):

            # was anything passed in?
            if ( entity_identifier_type_IN is not None ):

                # yes - set other values from it.

                # ----> name
                my_name = entity_identifier_type_IN.name
                self.name = my_name

                # ----> source
                my_source = entity_identifier_type_IN.source
                self.source = my_source

                # ----> notes - not for now...
                #my_notes = entity_type_trait_spec.notes
                #self.notes = my_notes

            else:

                # None - print a message.
                print( "In {}: nothing passed in, so not updating anything - should we clear things out?  Not right now...".format( me ) )

            #-- END check to see if anything passed in. --#

        #-- END check to see if we are to update --#

        return instance_OUT

    #-- END method set_entity_identifier_type() --#


    def set_identifier_type_from_name( self,
                                       entity_identifier_type_name_IN,
                                       do_use_to_update_fields_IN = True ):

        '''
        Accepts entity identifier name value.  Looks up type for that name, if
            found, calls set_entity_identifier_type and passes it the found
            instance.

        postconditions: Returns type for name passed in, or None if there was
            a problem with the lookup.  Does not actually save the
            Entity_Identifier.  If you want updates from setting type to
            persist, you must call save() on the instance.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "Entity_Identifier.set_identifier_type_from_name"
        type_instance = None

        # do we have a name?
        if ( ( entity_identifier_type_name_IN is not None ) and ( entity_identifier_type_name_IN != "" ) ):

            # yes - try looking up type using name.
            try:

                # look up type using slug
                type_instance = Entity_Identifier_Type.objects.get( name = entity_identifier_type_name_IN )

                # set type
                self.set_entity_identifier_type( type_instance, do_use_to_update_fields_IN )

            except Entity_Identifier_Type.MultipleObjectsReturned as mor:

                if ( self.DEBUG == True ):
                    error_message = "Multiple instances returned for name \"{}\".  Unfortunate!".format( entity_identifier_type_name_IN )
                    output_debug( error_message, method_IN = me )
                #-- END DEBUG --#

                type_instance = None

            except Entity_Identifier_Type.DoesNotExist as dne:

                if ( self.DEBUG == True ):
                    error_message = "No instance found for name \"{}\".".format( entity_identifier_type_name_IN )
                    output_debug( error_message, method_IN = me )
                #-- END DEBUG --#

                type_instance = None

            #-- END try-except --#

        #-- END check to see if we are to update --#

        instance_OUT = type_instance

        return instance_OUT

    #-- END method set_identifier_type_from_name() --#


#= End Entity_Identifier Model ======================================================


# Entity_Relation model
class Entity_Relation( Abstract_Relation ):

    #----------------------------------------------------------------------
    # ! ----> model fields and meta
    #----------------------------------------------------------------------


    relation_from = models.ForeignKey( "Entity", on_delete = models.CASCADE, related_name = "relation_from_entity_set" )
    relation_to = models.ForeignKey( "Entity", on_delete = models.CASCADE, related_name = "relation_to_entity_set" )
    #directed = models.BooleanField( default = False )
    relation_type = models.ForeignKey( "Entity_Relation_Type", on_delete = models.SET_NULL, blank = True, null = True )

    # JSON field to hold structured related information.
    #details_json = JSONField( blank = True, null = True )

    # add a way to tie this to a containing entity (article in which a reporter
    #     quotes a source, for example).
    relation_through = models.ForeignKey( "Entity", on_delete = models.SET_NULL, related_name = "relation_through_entity_set", blank = True, null = True )


    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------


    @classmethod
    def create_entity_relation( cls,
                                from_IN,
                                to_IN,
                                through_IN = None,
                                type_IN = None,
                                type_slug_IN = None,
                                trait_name_to_value_map_IN = None,
                                match_trait_dict_IN = None ):

        '''
        Create relation based on information passed in.  If relation matching
            this information already exists, returns it, does not create new or
            alter anything.  This includes not updating traits from the trait
            dictionary passed in.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        relation_type = None
        relation_qs = None
        relation_count = None
        relation = None
        trait_dict = None
        trait_count = None
        trait_name = None
        trait_value = None
        trait_spec = None

        # first, see if from entity passed in.
        if ( from_IN is not None ):

            # got to entity?
            if ( to_IN is not None ):

                # pull in type
                if ( type_IN is not None ):

                    # if type, use it.
                    relation_type = type_IN

                elif ( ( type_slug_IN is not None ) and ( type_slug_IN != "" ) ):

                    # if type slug, try to look up that type.
                    relation_type = Entity_Relation_Type.objects.get( slug = type_slug_IN )

                #-- END check to see if we have a type. --#

                # ! ----> look for existing relation...
                relation_qs = cls.lookup_relations( from_IN = from_IN,
                                                    to_IN = to_IN,
                                                    through_IN = through_IN,
                                                    type_IN = relation_type,
                                                    match_trait_dict_IN = match_trait_dict_IN )

                # what have we got?
                relation_count = relation_qs.count()
                if ( relation_count == 0 ):

                    # ! ----> Not present.  Create it.
                    relation = Entity_Relation()
                    relation.relation_from = from_IN
                    relation.relation_to = to_IN

                    # got THROUGH?
                    if ( through_IN is not None ):

                        # store it
                        relation.relation_through = through_IN

                    #-- END check for THROUGH --#

                    # got type?
                    if ( relation_type is not None ):

                        # filter on type.
                        relation.relation_type = relation_type

                    #-- END check to see if type. --#

                    # save, so we can add related records.
                    relation.save()

                    # ! ----> set traits

                    # use trait dictionary to initialize traits
                    relation.set_basic_traits_from_dict( trait_name_to_value_map_IN )

                    # return the new instance
                    instance_OUT = relation

                elif ( relation_count == 1 ):

                    # get relation
                    relation = relation_qs.get()

                    # return the instance
                    instance_OUT = relation

                    # relation already present.
                    status_message = "relation of type {} FROM {} TO {} THROUGH {} already exists ( {} ).".format( relation_type, from_IN, to_IN, through_IN, relation )
                    output_log_message( status_message, do_print_IN = DEBUG, log_level_code_IN = logging.DEBUG )

                elif ( relation_count > 1 ):

                    # ERROR - multiple matching relations found.
                    status_message = "ERROR - more then 1 relation of type {} FROM {} TO {} THROUGH {} already exists ( {} ).".format( relation_type, from_IN, to_IN, through_IN, relation_count )
                    output_log_message( status_message, do_print_IN = True, log_level_code_IN = logging.ERROR )

                else:

                    # ERROR - relation count is not 0, 1, or > 1...?
                    status_message = "UNEXPECTED ERROR - count of relations is {}, not 0, 1, or > 1, for relation of type {} FROM {} TO {} THROUGH {}.".format( relation_type, from_IN, to_IN, through_IN )
                    output_log_message( status_message, do_print_IN = True, log_level_code_IN = logging.ERROR )

                #-- END check of count of results --#

            else:

                # ERROR - no TO entity passed in.
                status_message = "ERROR - no TO entity passed in, so no relations to create."
                output_log_message( status_message, do_print_IN = True, log_level_code_IN = logging.ERROR )

            #-- END check to see if TO entity. --#

        else:

            # ERROR - no FROM entity passed in.
            status_message = "ERROR - no FROM entity passed in, so no relations to create."
            output_log_message( status_message, do_print_IN = True, log_level_code_IN = logging.ERROR )

        #-- END check to see if FROM entity passed in. --#

        return instance_OUT

    #-- END class method create_entity_relation() --#


    @classmethod
    def filter_relations( cls,
                          from_IN = None,
                          to_IN = None,
                          through_IN = None,
                          type_IN = None,
                          type_slug_IN = None,
                          qs_IN = None ):

        '''
        Accepts parameters, filters a QuerySet of Entity_Relations, returns the
            resulting QuerySet.  Does not look into related models.
        '''

        # return reference
        qs_OUT = None

        # declare variables
        me = "Entity_Relation.filter_relations"
        debug_flag = cls.DEBUG
        debug_message = None
        relation_qs = None

        if ( debug_flag == True ):
            debug_message = "Inputs: FROM: {}; TO: {}; THROUGH: {}; Entity_Relation_Type: {}; type slug: {}".format( from_IN, to_IN, through_IN, type_IN, type_slug_IN )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # figure out starting QuerySet
        if ( qs_IN is not None ):

            # QuerySet passed in.  Use it.
            relation_qs = qs_IN

        else:

            # no QuerySet passed in, use Entity_Relation.objects.all()
            relation_qs = cls.objects.all()

        #-- END init QuerySet --#

        #----------------------------------------------------------------------#
        # ! ----> FROM entity instance
        if ( from_IN is not None ):

            # we have a FROM entity instance
            relation_qs = relation_qs.filter( relation_from = from_IN )

        #-- END check to see if FROM entity instance passed in. --#

        #----------------------------------------------------------------------#
        # ! ----> TO entity instance
        if ( to_IN is not None ):

            # we have a TO entity instance
            relation_qs = relation_qs.filter( relation_to = to_IN )

        #-- END check to see if TO entity instance passed in. --#

        #----------------------------------------------------------------------#
        # ! ----> THROUGH entity instance
        if ( through_IN is not None ):

            # we have a THROUGH entity instance
            relation_qs = relation_qs.filter( relation_through = through_IN )

        #-- END check to see if THROUGH entity instance passed in. --#

        #----------------------------------------------------------------------#
        # ! ----> type instance
        if ( type_IN is not None ):

            # we have a type instance
            relation_qs = relation_qs.filter( relation_type = type_IN )

        #-- END check to see if Entity_Relation_Type instance passed in. --#

        #----------------------------------------------------------------------#
        # ! ----> type slug
        if ( type_slug_IN is not None ):

            # we have a type instance
            relation_qs = relation_qs.filter( relation_type__slug = type_slug_IN )

        #-- END check to see if Entity_Relation_Type slug passed in. --#

        qs_OUT = relation_qs
        return qs_OUT

    #-- END class method filter_relations() --#


    @classmethod
    def lookup_relations( cls,
                          from_IN = None,
                          to_IN = None,
                          through_IN = None,
                          type_IN = None,
                          type_slug_IN = None,
                          match_trait_dict_IN = None,
                          qs_IN = None ):

        '''
        Accepts parameters, filters a QuerySet of Entity_Relations, returns the
            resulting QuerySet. Looks into related models as well as this model.
        '''

        # return reference
        qs_OUT = None

        # declare variables
        me = "Entity_Relation.lookup_relations"
        debug_flag = cls.DEBUG
        debug_message = None
        relation_qs = None
        relation_q = None
        match_trait_count = None
        trait_name = None
        trait_value = None

        if ( debug_flag == True ):
            debug_message = "Inputs: FROM: {}; TO: {}; THROUGH: {}; Entity_Relation_Type: {}; type slug: {}".format( from_IN, to_IN, through_IN, type_IN, type_slug_IN )
            output_debug( debug_message, me )
        #-- END DEBUG --#

        # figure out starting QuerySet
        if ( qs_IN is not None ):

            # QuerySet passed in.  Use it.
            relation_qs = qs_IN

        else:

            # no QuerySet passed in, use Entity_Relation.objects.all()
            relation_qs = Entity_Relation.objects.all()

        #-- END init QuerySet --#

        # do standard Entity_Relation-specific filtering
        relation_qs = cls.filter_relations( from_IN = from_IN,
                                            to_IN = to_IN,
                                            through_IN = through_IN,
                                            type_IN = type_IN,
                                            type_slug_IN = type_slug_IN,
                                            qs_IN = relation_qs )

        # do we need to also match trait values?
        if ( match_trait_dict_IN is not None ):

            # anything in the dictionary?
            match_trait_count = len( match_trait_dict_IN )
            if ( match_trait_count > 0 ):

                # there is something there.  limit to those items that have
                #     traits matching those passed in.
                for trait_name, trait_value in six.iteritems( match_trait_dict_IN ):

                    # include relations with traits that have the name and
                    #     value passed in.
                    relation_qs = relation_qs.filter( entity_relation_trait__name = trait_name )
                    relation_qs = relation_qs.filter( entity_relation_trait__value = trait_value )

                #-- END loop over trait values --#

            #-- END check to see if traits passed in. --#

        #-- END check to see if trait dictionary passed in. --#

        # return QuerySet.
        qs_OUT = relation_qs

        return qs_OUT

    #-- END class method lookup_relations() --#


    #----------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Relation, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got a relation_from?
        if ( self.relation_from is not None ):

            string_list.append( "FROM: {}".format( self.relation_from ) )

        #-- END check for relation_from. --#

        # got a to_term?
        if ( self.relation_to is not None ):

            string_list.append( "TO: {}".format( self.relation_to ) )

        #-- END check to see if relation_to. --#

        # THROUGH?
        if ( self.relation_through is not None ):

            string_list.append( "THROUGH: {}".format( self.relation_through ) )

        #-- END check to see if relation_to. --#

        # directed?
        if ( self.directed is not None ):

            string_list.append( "DIRECTED?: {}".format( self.directed ) )

        #-- END check to see if directed. --#

        # type?
        if ( self.relation_type is not None ):

            string_list.append( "( type: {} - {} )".format( self.relation_type.id, self.relation_type.slug ) )

        #-- END check for relation_type. --#

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#


    #----------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------


    def create_trait_instance( self, *args, **kwargs ):

        '''
        Creates an empty Abstract_Trait descendent, initializes it
            appropriately, then returns it.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        value_OUT = None

        # declare variables
        trait_instance = None

        # Create Entity_Trait, set self into "entity".
        trait_instance = Entity_Relation_Trait()
        trait_instance.entity_relation = self
        value_OUT = trait_instance

        return value_OUT

    #-- END method create_trait_instance() --#


    def filter_trait_qs( self, trait_qs_IN, inheriting_type_trait_IN = None, *args, **kwargs ):

        '''
        Accepts trait QuerySet and type trait spec for the inheriting class's
            type (independent of Trait_Type).  Returns the trait QuerySet for
            the model class extending this class, filtered appropriately to only
            include traits that reference the trait specification stored in
            inheriting_type_trait_IN.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        qs_OUT = None

        # declare variables

        # init
        qs_OUT = trait_qs_IN

        # got an Entity_Type_Trait instance?
        if ( inheriting_type_trait_IN is not None ):

            # also filter on Entity_Type_Trait
            qs_OUT = qs_OUT.filter( entity_relation_type_trait = inheriting_type_trait_IN )

        #-- END check to see if source --#

        return qs_OUT

    #-- END method filter_trait_qs() --#


    def get_entity_relation_trait( self,
                                   name_IN,
                                   slug_IN = None,
                                   label_IN = None,
                                   entity_relation_type_trait_IN = None ):

        '''
        Accepts identifying details of a trait whose instance (and so values)
            we want to retrieve.  If trait is found, returns it.  If not,
            returns None.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "get_entity_relation_trait"
        debug_flag = self.DEBUG
        debug_message = None

        if ( debug_flag == True ):
            debug_message = "Inputs: name: {}; slug: {}; label: {}; entity_relation_type_trait: {}.".format( name_IN, slug_IN, label_IN, entity_relation_type_trait_IN )
            output_debug(  debug_message, me )
        #-- END DEBUG --#

        # call parent get_trait()
        instance_OUT = self.get_trait( name_IN,
                                       slug_IN = slug_IN,
                                       label_IN = label_IN,
                                       child_type_trait_IN = entity_relation_type_trait_IN )

        return instance_OUT

    #-- END method get_entity_trait() --#


    def get_trait_qs( self, *args, **kwargs ):

        '''
        Returns the trait QuerySet for the model class extending this class.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        value_OUT = None

        # return the Entity_Trait related set.
        value_OUT = self.entity_relation_trait_set.all()

        return value_OUT

    #-- END method get_trait_qs() --#


    def set_child_type_trait( self, trait_instance_IN, child_type_trait_IN, *args, **kwargs ):

        '''
        Accepts trait instance and trait type appropriate to the inheriting
            class.  Places the type in the trait instance, return trait
            instance.
        Preconditions: None
        Postconditions: None
        '''

        # return reference
        value_OUT = None

        # we do - use it to set name and other metadata details.
        trait_instance_IN.set_entity_relation_type_trait( child_type_trait_IN )
        value_OUT = trait_instance_IN

        return value_OUT

    #-- END method set_child_type_trait() --#


    def set_entity_relation_trait( self,
                                   name_IN,
                                   value_IN,
                                   slug_IN = None,
                                   value_json_IN = None,
                                   label_IN = None,
                                   description_IN = None,
                                   trait_type_IN = None,
                                   term_IN = None,
                                   entity_relation_type_trait_IN = None ):

        '''
        Accepts details of a trait we want to set for a given entity relation.

            - Checks to see if the entity already has a trait with the name passed in.
            - If entity_relation_type_trait_IN is set, the name from this type supersedes the name passed in.
            - If existing trait exists, loads it into instance. If not, creates one.
            - then, updates based on the values passed in.
                - If trait specification passed in, updates meta information (not
            value) from there.
                - If not, updates from other parameters passed in.
                - Updates value of the trait based on parameters passed in.

        preconditions: Entity_Relation must already be saved for this to work.

        postconditions: Throws exception if type not found.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "set_entity_relation_trait"

        # call parent method
        instance_OUT = self.set_trait( name_IN,
                                       value_IN,
                                       slug_IN = slug_IN,
                                       value_json_IN = value_json_IN,
                                       label_IN = label_IN,
                                       description_IN = description_IN,
                                       trait_type_IN = trait_type_IN,
                                       term_IN = term_IN,
                                       child_type_trait_IN = entity_relation_type_trait_IN )

        return instance_OUT

    #-- END method set_entity_relation_trait() --#


    def set_basic_traits_from_dict( self, trait_name_to_value_map_IN = None ):

        # return reference
        counter_OUT = None

        # declare variables
        my_type = None
        trait_dict = None
        trait_count = None
        trait_counter = None
        trait_name = None
        trait_value = None
        trait_spect = None

        # initialize
        my_type = self.relation_type

        # got a trait dictionary?
        trait_dict = trait_name_to_value_map_IN
        trait_counter = 0
        if ( trait_dict is not None ):

            # get count
            trait_count = len( trait_dict )

            # yes.  Loop over traits.
            for trait_name, trait_value in six.iteritems( trait_dict ):

                # increment counter
                trait_counter += 1

                # see if trait spec for type.
                trait_spec = None
                if ( my_type is not None ):

                    trait_spec = my_type.get_trait_spec( trait_name )

                #-- END check to see if relation_type --#

                # set trait.
                self.set_trait( trait_name, trait_value, child_type_trait_IN = trait_spec )

            #-- END loop over traits --#

        #-- END check for a trait dict. --#

        counter_OUT = trait_counter

        return counter_OUT

    #-- END method set_basic_traits_from_dict() --#

#-- END model Entity_Relation --#


# Entity_Identifier model
class Entity_Relation_Identifier( Abstract_UUID ):

    entity_relation = models.ForeignKey( Entity_Relation, on_delete = models.CASCADE )
    #name = models.CharField( max_length = 255, null = True, blank = True )
    #uuid = models.TextField( blank = True, null = True )
    #source = models.CharField( max_length = 255, null = True, blank = True )
    #notes = models.TextField( blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Relation_Identifier, self ).__init__( *args, **kwargs )

        # then, initialize variable.
        self.bs_helper = None

    #-- END method __init__() --#

    # just use the parent stuff.

#= End Entity_Relation_Identifier Model ======================================================


# Entity_Relation_Trait model
class Entity_Relation_Trait( Abstract_Trait ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    entity_relation = models.ForeignKey( "Entity_Relation", on_delete = models.CASCADE )
    entity_relation_type_trait = models.ForeignKey( "Entity_Relation_Type_Trait", on_delete = models.SET_NULL, blank = True, null = True )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Relation_Trait, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got name?
        if ( self.name is not None ):

            string_list.append( str( self.name ) )

        #-- END check for name. --#

        # got slug?
        if ( self.slug is not None ):

            string_list.append( "( {} )".format( str( self.slug ) ) )

        #-- END check to see if slug. --#

        # got value?
        if ( self.value is not None ):

            string_list.append( "= {}".format( str( self.value ) ) )

        #-- END check to see if value. --#

        # related type?
        if ( self.entity_relation_type_trait is not None ):

            string_list.append( "--> Type: {}".format( self.entity_relation_type_trait ) )

        #-- END check for type --#

        # Entity
        if ( self.entity_relation is not None ):

            string_list.append( "Entity: {}".format( self.entity_relation ) )

        #-- END check for entity. --#

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#


    #----------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------


    def set_entity_relation_type_trait( self, instance_IN ):

        '''
        Accepts Entity_Relation_Trait_Type instance that defines the trait we
            are setting for an entity.  Stores the type specification, then
            updates fields accordingly.

        postconditions: You must save() the instance once  you are done for the
            updated field values to be stored in the database.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        entity_relation_type_trait_spec = None
        my_trait_type = None
        my_name = None
        my_slug = None
        my_label = None
        my_description = None

        entity_relation_type_trait_spec = instance_IN
        if ( entity_relation_type_trait_spec is not None ):

            # not None.  Store it...
            self.entity_relation_type_trait = entity_relation_type_trait_spec

            # set other values from it.

            # ----> trait_type
            my_trait_type = entity_relation_type_trait_spec.trait_type
            self.trait_type = my_trait_type

            # ----> name
            my_name = entity_relation_type_trait_spec.name
            self.name = my_name

            # ----> slug
            my_slug = entity_relation_type_trait_spec.slug
            self.slug = my_slug

            # ----> label
            my_label = entity_relation_type_trait_spec.label
            self.label = my_label

            # ----> description
            my_description = entity_relation_type_trait_spec.description
            self.description = my_description

        else:

            # None - just set to None.
            self.entity_relation_type_trait = entity_relation_type_trait_spec

        #-- END check to see if None --#

        # return the type
        instance_OUT = entity_relation_type_trait_spec

        return instance_OUT

    #-- END method set_entity_relation_type_trait() --#


#-- END model Entity_Relation_Trait --#


# Entity_Relation_Type model
class Entity_Relation_Type( Abstract_Type ):

    #----------------------------------------------------------------------
    # ! ----> model fields and meta
    #----------------------------------------------------------------------

    # from parent:
    #slug = models.SlugField( unique = True )
    #name = models.CharField( max_length = 255, blank = True, null = True )
    #related_model = models.CharField( max_length = 255, blank = True, null = True )
    #description = models.TextField( blank = True )

    parent_type = models.ForeignKey( "Entity_Relation_Type", on_delete = models.SET_NULL, blank = True, null = True )
    relation_from_entity_type = models.ForeignKey( "Entity_Type", on_delete = models.SET_NULL, blank = True, null = True, related_name = "relation_from_entity_type_set" )
    relation_to_entity_type = models.ForeignKey( "Entity_Type", on_delete = models.SET_NULL, blank = True, null = True, related_name = "relation_to_entity_type_set" )
    relation_through_entity_type = models.ForeignKey( "Entity_Type", on_delete = models.SET_NULL, blank = True, null = True, related_name = "relation_through_entity_type_set" )


    # Meta-data for this class.
    class Meta:

        ordering = [ 'last_modified' ]

    #-- END class Meta --#


    #---------------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Relation_Type, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.


    #----------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------


    def get_trait_spec( self, slug_IN ):

        '''
        Retrieve trait specification associated with this type for the slug
            passed in.  If no match, output message and return None.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "get_trait_spec"
        trait_spec = None

        # make sure we have a slug
        if ( ( slug_IN is not None ) and ( slug_IN != "" ) ):

            try:

                # look up type using slug
                trait_spec = self.entity_relation_type_trait_set.get( slug = slug_IN )

            except Entity_Relation_Type_Trait.MultipleObjectsReturned as mor:

                print( "In {}: Multiple instances returned for slug {}.  Impossible!".format( me, slug_IN ) )
                trait_spec = None

            except Entity_Relation_Type_Trait.DoesNotExist as dne:

                if ( DEBUG == True ):
                    print( "In {}: No instance found for slug {}.".format( me, slug_IN ) )
                #-- END DEBUG --#
                trait_spec = None

            #-- END try-except --#

        else:

            # error
            print( "In {}: ERROR - no slug passed in, can't process.".format( me ) )
            trait_spec = None

        #-- END check to see if slug passed in --#

        instance_OUT = trait_spec

        return instance_OUT

    #-- END method get_trait_spec() --#


#-- END model Entity_Relation_Type --#


# Entity_Relation_Type_Trait model
class Entity_Relation_Type_Trait( Abstract_Related_Type_Trait ):


    '''
    Used to capture the traits that should be associated with an entity relation
        type.
    '''


    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    related_type = models.ForeignKey( "Entity_Relation_Type", on_delete = models.CASCADE )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Relation_Type_Trait, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got name?
        if ( self.name is not None ):

            string_list.append( str( self.name ) )

        #-- END check for name. --#

        # got slug?
        if ( self.slug is not None ):

            string_list.append( "( {} )".format( str( self.slug ) ) )

        #-- END check to see if slug. --#

        # related type?
        if ( self.related_type is not None ):

            string_list.append( "--> Type: {}".format( self.related_type ) )

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#


#-- END model Entity_Relation_Type_Trait --#


# Entity_Types model
class Entity_Relation_Types( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    entity_relation = models.ForeignKey( "Entity_Relation", on_delete = models.CASCADE )
    entity_relation_type = models.ForeignKey( "Entity_Relation_Type", on_delete = models.CASCADE )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Relation_Types, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


#-- END model Entity_Relation_Types --#


# Entity_Trait model
class Entity_Trait( Abstract_Trait ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    entity = models.ForeignKey( "Entity", on_delete = models.CASCADE )
    entity_type_trait = models.ForeignKey( "Entity_Type_Trait", on_delete = models.SET_NULL, blank = True, null = True )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    #---------------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Trait, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got name?
        if ( self.name is not None ):

            string_list.append( str( self.name ) )

        #-- END check for name. --#

        # got slug?
        if ( self.slug is not None ):

            string_list.append( "( {} )".format( str( self.slug ) ) )

        #-- END check to see if slug. --#

        # got value?
        if ( self.value is not None ):

            string_list.append( "= {}".format( str( self.value ) ) )

        #-- END check to see if value. --#

        # related type?
        if ( self.entity_type_trait is not None ):

            string_list.append( "--> Type: {}".format( self.entity_type_trait ) )

        #-- END check for type --#

        # Entity
        if ( self.entity is not None ):

            string_list.append( "Entity: {}".format( self.entity ) )

        #-- END check for entity. --#

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#


    #----------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------


    def set_entity_type_trait( self, instance_IN ):

        '''
        Accepts Entity_Trait_Type instance that defines the trait we are setting
            for an entity.  Stores the type specification, then updates fields
            accordingly.

        postconditions: You must save() the instance once  you are done for the
            updated field values to be stored in the database.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        entity_type_trait_spec = None
        my_trait_type = None
        my_name = None
        my_slug = None
        my_label = None
        my_description = None

        entity_type_trait_spec = instance_IN
        if ( entity_type_trait_spec is not None ):

            # not None.  Store it...
            self.entity_type_trait = entity_type_trait_spec

            # set other values from it.

            # ----> trait_type
            my_trait_type = entity_type_trait_spec.trait_type
            self.trait_type = my_trait_type

            # ----> name
            my_name = entity_type_trait_spec.name
            self.name = my_name

            # ----> slug
            my_slug = entity_type_trait_spec.slug
            self.slug = my_slug

            # ----> label
            my_label = entity_type_trait_spec.label
            self.label = my_label

            # ----> description
            my_description = entity_type_trait_spec.description
            self.description = my_description

        else:

            # None - just set to None.
            self.entity_type_trait = entity_type_trait_spec

        #-- END check to see if None --#

        # return the type
        instance_OUT = entity_type_trait_spec

        return instance_OUT

    #-- END method set_entity_type_trait() --#

#-- END model Entity_Trait --#


# Entity_Type model
class Entity_Type( Abstract_Type ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    #slug = models.SlugField( unique = True )
    #name = models.CharField( max_length = 255, blank = True, null = True )
    #related_model = models.CharField( max_length = 255, blank = True, null = True )
    #description = models.TextField( blank = True )
    parent_type = models.ForeignKey( "Entity_Type", on_delete = models.SET_NULL, blank = True, null = True )


    #---------------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Type, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.


    #----------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------


    def get_trait_spec( self, slug_IN ):

        '''
        Retrieve trait specification associated with this type for the slug
            passed in.  If no match, output message and return None.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "get_trait_spec"
        trait_spec = None

        # make sure we have a slug
        if ( ( slug_IN is not None ) and ( slug_IN != "" ) ):

            try:

                # look up type using slug
                trait_spec = self.entity_type_trait_set.get( slug = slug_IN )

            except Entity_Type_Trait.MultipleObjectsReturned as mor:

                print( "In {}: Multiple instances returned for slug {}.  Impossible!".format( me, slug_IN ) )
                trait_spec = None

            except Entity_Type_Trait.DoesNotExist as dne:

                if ( DEBUG == True ):
                    print( "In {}: No instance found for slug {}.".format( me, slug_IN ) )
                #-- END DEBUG --#
                trait_spec = None

            #-- END try-except --#

        else:

            # error
            print( "In {}: ERROR - no slug passed in, can't process.".format( me ) )
            trait_spec = None

        #-- END check to see if slug passed in --#

        instance_OUT = trait_spec

        return instance_OUT

    #-- END method get_trait_spec() --#

#-- END model Entity_Type --#


# Entity_Type_Trait model
class Entity_Type_Trait( Abstract_Related_Type_Trait ):


    '''
    Used to capture the traits that should be associated with an entity type.
    '''


    #---------------------------------------------------------------------------
    # model fields and meta
    #---------------------------------------------------------------------------


    related_type = models.ForeignKey( "Entity_Type", on_delete = models.CASCADE )


    #---------------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Type_Trait, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got name?
        if ( self.name is not None ):

            string_list.append( str( self.name ) )

        #-- END check for name. --#

        # got slug?
        if ( self.slug is not None ):

            string_list.append( "( {} )".format( str( self.slug ) ) )

        #-- END check to see if slug. --#

        # related type?
        if ( self.related_type is not None ):

            string_list.append( "--> Type: {}".format( self.related_type ) )

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#


    #---------------------------------------------------------------------------
    # instance methods
    #---------------------------------------------------------------------------


#-- END model Entity_Type_Trait --#


# Entity_Types model
class Entity_Types( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    entity = models.ForeignKey( "Entity", on_delete = models.CASCADE )
    entity_type = models.ForeignKey( "Entity_Type", on_delete = models.CASCADE )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Entity_Types, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


#-- END model Entity_Types --#


# Term model
class Term( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    value = models.CharField( max_length = 255 )
    label = models.CharField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True )
    parent_term = models.ForeignKey( "Term", on_delete = models.SET_NULL, blank = True, null = True )
    vocabulary = models.ForeignKey( "Vocabulary", on_delete = models.CASCADE ) # required to start, so kill all terms if vocabulary is deleted.

    # Meta-data for this class.
    class Meta:
        ordering = [ 'vocabulary', 'value' ]


    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Term, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []
        my_value = None

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got value?
        if ( self.value is not None ):

            my_value = self.value
            string_list.append( str( my_value ) )

        #-- END check for value. --#

        # got label?
        if ( self.label is not None ):

            # different from value?
            if my_value != self.label:

                # different - output as well.
                string_list.append( "( {} )".format( str( self.label ) ) )

            #-- END check to see if value and label are different. --#

        #-- END check to see if label. --#

        # vocabulary
        if ( self.vocabulary is not None ):

            # add vocabulary name
            string_list.append( "vocab: {}".format( str( self.vocabulary ) ) )

        #-- END check for vocabulary --#

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#


#= End Term Model =========================================================


# Term_Relation model
class Term_Relation( Abstract_Relation ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    relation_from = models.ForeignKey( "Term", on_delete = models.CASCADE, related_name = "relation_from_term_set" )
    relation_to = models.ForeignKey( "Term", on_delete = models.CASCADE, related_name = "relation_to_term_set" )
    #directed = models.BooleanField( default = False )
    relation_type = models.ForeignKey( "Term_Relation_Type", on_delete = models.SET_NULL, blank = True, null = True )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Term_Relation, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    # use parent def __str__( self ):

#-- END model Entity_Relation --#


# Term_Relation_Type model
class Term_Relation_Type( Abstract_Type ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    #name = models.CharField( max_length = 255, blank = True, null = True )
    #related_model = models.CharField( max_length = 255, blank = True, null = True )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Term_Relation_Type, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.

#-- END model Term_Relation_Type --#


# Trait_Type model
class Trait_Type( Abstract_Type ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    #name = models.CharField( max_length = 255, blank = True, null = True )
    #related_model = models.CharField( max_length = 255, blank = True, null = True )
    vocabulary = models.ForeignKey( "Vocabulary", on_delete = models.SET_NULL, blank = True, null = True )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Trait_Type, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.

#-- END model Trait_Type --#


# Vocabulary model
class Vocabulary( Abstract_Context_Parent ):

    name = models.CharField( max_length = 255 )
    description = models.TextField( blank = True )

    # eventually need to add more metadata - URL, organization, etc.

    # Meta-data for this class.
    class Meta:
        ordering = [ 'name' ]

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Vocabulary, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        # id
        if ( self.id is not None ):

            string_list.append( str( self.id ) )

        #-- END check to see if ID --#

        # got name?
        if ( self.name is not None ):

            string_list.append( str( self.name ) )

        #-- END check for name. --#

        string_OUT += " - ".join( string_list )

        return string_OUT

    #-- END method __str__() --#


#= End Vocabulary Model =========================================================


# Abstract_Work_Log model
class Work_Log( Abstract_Work_Log ):

    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super( Work_Log, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.

#-- END model Work_Log --#
