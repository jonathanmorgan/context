from __future__ import unicode_literals
from __future__ import division

'''
Copyright 2019 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/sourcenet.

context is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context. If not, see http://www.gnu.org/licenses/.
'''

#================================================================================
# Imports
#================================================================================


# Django imports
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

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
            my_logger_name = "sourcenet.models"
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


# Abstract_Context_Parent model
@python_2_unicode_compatible
class Abstract_Context_Parent( models.Model ):

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

#-- END abstract model Abstract_Context_Parent --#


# Abstract_Type model
@python_2_unicode_compatible
class Abstract_Type( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    slug = models.SlugField( unique = True )
    name = models.CharField( max_length = 255, blank = True, null = True )
    related_model = models.CharField( max_length = 255, blank = True, null = True )


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
class Entity( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    name = models.CharField( max_length = 255 )


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


# Entity_Relation model
@python_2_unicode_compatible
class Entity_Relation( Abstract_Context_Parent ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------


    from_entity = models.ForeignKey( "Entity", on_delete = models.CASCADE, related_name = "relation_from_entity_set" )
    to_entity = models.ForeignKey( "Entity", on_delete = models.CASCADE, related_name = "relation_to_entity_set" )
    directed = models.BooleanField( default = False )


    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Entity_Types, self ).__init__( *args, **kwargs )

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
        
        # got a from_entity?
        if ( self.from_entity is not None ):
        
            string_list.append( str( self.from_entity ) )
            
        #-- END check for from_entity. --#

        # got a to_entity?
        if ( self.to_entity is not None ):
        
            string_list.append( str( self.to_entity ) )
            
        #-- END check to see if to_entity. --#
        
        # directed?
        if ( self.directed is not None ):
        
            string_list.append( "( {} )".format( self.directed ) )
            
        #-- END check to see if directed. --#
 
        string_OUT += " - ".join( string_list )
 
        return string_OUT

    #-- END method __str__() --#

#-- END model Entity_Relation --#


# Entity_Relation_Type model
@python_2_unicode_compatible
class Entity_Relation_Type( Abstract_Type ):

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
        super( Entity_Relation_Type, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#-- END model Entity_Relation_Type --#


# Entity_Relation_Types model
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
        super( Entity_Types, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    
#-- END model Entity_Relation_Types --#


# Entity_Type model
@python_2_unicode_compatible
class Entity_Type( Abstract_Type ):

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
        super( Entity_Type, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#-- END model Entity_Type --#


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


# Abstract_Work_Log model
@python_2_unicode_compatible
class Work_Log( Abstract_Work_Log ):

    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Work_Log, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    # just use the stuff in the parent class.
    
#-- END model Work_Log --#

