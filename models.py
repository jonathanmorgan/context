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


# Django imports
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# taggit tagging APIs
from taggit.managers import TaggableManager

# python_utilities - logging
from python_utilities.logging.logging_helper import LoggingHelper

# shared abstract models.
from context.shared.models import Abstract_Context_Parent
from context.shared.models import Abstract_Context_With_JSON
from context.shared.models import Abstract_UUID


#================================================================================
# Shared variables and functions
#================================================================================


'''
Debugging code, shared across all models.
'''

DEBUG = True

def output_debug( message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = "" ):
    
    '''
    Accepts message string.  If debug is on, logs it.  If not,
       does nothing for now.
    '''
    
    # declare variables
    my_message = ""
    my_logger = None
    my_logger_name = ""

    # got a message?
    if ( message_IN ):
    
        # only print if debug is on.
        if ( DEBUG == True ):
        
            my_message = message_IN
        
            # got a method?
            if ( method_IN ):
            
                # We do - append to front of message.
                my_message = "In " + method_IN + ": " + my_message
                
            #-- END check to see if method passed in --#
            
            # indent?
            if ( indent_with_IN ):
                
                my_message = indent_with_IN + my_message
                
            #-- END check to see if we indent. --#
        
            # debug is on.  Start logging rather than using print().
            #print( my_message )
            
            # got a logger name?
            my_logger_name = "context.models"
            if ( ( logger_name_IN is not None ) and ( logger_name_IN != "" ) ):
            
                # use logger name passed in.
                my_logger_name = logger_name_IN
                
            #-- END check to see if logger name --#
                
            # get logger
            my_logger = LoggingHelper.get_a_logger( my_logger_name )
            
            # log debug.
            my_logger.debug( my_message )
        
        #-- END check to see if debug is on --#
    
    #-- END check to see if message. --#

#-- END method output_debug() --#


#================================================================================
# ! ==> Abstract Models
#================================================================================


# Abstract_Relation model
@python_2_unicode_compatible
class Abstract_Relation( Abstract_Context_With_JSON ):

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
        
            string_list.append( str( self.relation_from ) )
            
        #-- END check for relation_from. --#

        # got a to_term?
        if ( self.relation_to is not None ):
        
            string_list.append( str( self.relation_to ) )
            
        #-- END check to see if relation_to. --#
        
        # directed?
        if ( self.directed is not None ):
        
            string_list.append( "( {} )".format( self.directed ) )
            
        #-- END check to see if directed. --#
 
        string_OUT += " - ".join( string_list )
 
        return string_OUT

    #-- END method __str__() --#

#-- END model Abstract_Relation --#


# Abstract Trait model
@python_2_unicode_compatible
class Abstract_Trait( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    #entity = models.ForeignKey( "Entity", on_delete = models.CASCADE )
    name = models.CharField( max_length = 255 )
    #slug = models.SlugField()?   
    value = models.CharField( max_length = 255, blank = True, null = True )
    value_json = JSONField( blank = True, null = True )
    label = models.CharField( max_length = 255, blank = True, null = True )
    description = models.TextField( blank = True )

    # context
    trait_type = models.ForeignKey( "Trait_Type", on_delete = models.SET_NULL, blank = True, null = True )
    term = models.ForeignKey( "Term", on_delete = models.SET_NULL, blank = True, null = True )


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
        super( Abstract_Trait, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    
    # use parent def __str__( self ):

#-- END model Abstract_Trait --#


# Abstract_Type model
@python_2_unicode_compatible
class Abstract_Type( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # model fields and meta
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
    # instance methods
    #----------------------------------------------------------------------


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

#-- END model Abstract_Type --#


# Abstract_Related_Type_Trait model
@python_2_unicode_compatible
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


# Abstract_Work_Log model
@python_2_unicode_compatible
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
@python_2_unicode_compatible
class Entity( Abstract_Context_With_JSON ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    name = models.CharField( max_length = 255 )

    # JSON field to hold structured related information.
    #details_json = JSONField( blank = True, null = True )
    

    #----------------------------------------------------------------------
    # instance methods
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

#-- END model Entity --#


# Entity_Identifier model
@python_2_unicode_compatible
class Entity_Identifier( Abstract_UUID ):

    entity = models.ForeignKey( Entity, on_delete = models.CASCADE )
    #name = models.CharField( max_length = 255, null = True, blank = True )
    #uuid = models.TextField( blank = True, null = True )
    #source = models.CharField( max_length = 255, null = True, blank = True )
    #notes = models.TextField( blank = True, null = True )

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Entity_Identifier, self ).__init__( *args, **kwargs )

        # then, initialize variable.
        self.bs_helper = None
        
    #-- END method __init__() --#

    # just use the parent stuff.

#= End Entity_Identifier Model ======================================================


# Entity_Relation model
@python_2_unicode_compatible
class Entity_Relation( Abstract_Relation ):

    #----------------------------------------------------------------------
    # model fields and meta
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
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Entity_Relation, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    
    # use parent def __str__( self ):

#-- END model Entity_Relation --#


# Entity_Identifier model
@python_2_unicode_compatible
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
@python_2_unicode_compatible
class Entity_Relation_Trait( Abstract_Trait ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    entity_relation = models.ForeignKey( "Entity_Relation", on_delete = models.CASCADE )
    

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Entity_Relation_Trait, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    
    # use parent def __str__( self ):

#-- END model Entity_Relation_Trait --#


# Entity_Relation_Type model
@python_2_unicode_compatible
class Entity_Relation_Type( Abstract_Type ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    #name = models.CharField( max_length = 255, blank = True, null = True )
    #related_model = models.CharField( max_length = 255, blank = True, null = True )
    parent_type = models.ForeignKey( "Entity_Relation_Type", on_delete = models.SET_NULL, blank = True, null = True )
    relation_from_entity_type = models.ForeignKey( "Entity_Type", on_delete = models.SET_NULL, blank = True, null = True, related_name = "relation_from_entity_type_set" )
    relation_to_entity_type = models.ForeignKey( "Entity_Type", on_delete = models.SET_NULL, blank = True, null = True, related_name = "relation_to_entity_type_set" )
    relation_through_entity_type = models.ForeignKey( "Entity_Type", on_delete = models.SET_NULL, blank = True, null = True, related_name = "relation_through_entity_type_set" )
    

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Entity_Relation_Type, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#-- END model Entity_Relation_Type --#


# Entity_Type_Trait model
@python_2_unicode_compatible
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

    # use parent def __str__( self ):

    
#-- END model Entity_Relation_Type_Trait --#


# Entity_Types model
@python_2_unicode_compatible
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
@python_2_unicode_compatible
class Entity_Trait( Abstract_Trait ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    entity = models.ForeignKey( "Entity", on_delete = models.CASCADE )
    

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Entity_Trait, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    
    # use parent def __str__( self ):

#-- END model Entity_Trait --#


# Entity_Type model
@python_2_unicode_compatible
class Entity_Type( Abstract_Type ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    #name = models.CharField( max_length = 255, blank = True, null = True )
    #related_model = models.CharField( max_length = 255, blank = True, null = True )
    parent_type = models.ForeignKey( "Entity_Type", on_delete = models.SET_NULL, blank = True, null = True )



    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Entity_Type, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#-- END model Entity_Type --#


# Entity_Type_Trait model
@python_2_unicode_compatible
class Entity_Type_Trait( Abstract_Related_Type_Trait ):


    '''
    Used to capture the traits that should be associated with an entity type.
    '''


    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    related_type = models.ForeignKey( "Entity_Type", on_delete = models.CASCADE )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Entity_Type_Trait, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.


#-- END model Entity_Type_Trait --#


# Entity_Types model
@python_2_unicode_compatible
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
@python_2_unicode_compatible
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
@python_2_unicode_compatible
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
@python_2_unicode_compatible
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
@python_2_unicode_compatible
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
@python_2_unicode_compatible
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
@python_2_unicode_compatible
class Work_Log( Abstract_Work_Log ):

    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Work_Log, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#-- END model Work_Log --#

