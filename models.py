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
# Models
#================================================================================


# Abstract_Work_Log model
@python_2_unicode_compatible
class Abstract_Work_Log( models.Model ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------

    slug = models.SlugField( unique = True )
    name = models.CharField( max_length = 255, blank = True, null = True )
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
        ordering = [ 'last_modified', 'slug' ]
        
    #-- END class Meta --#

    #----------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------


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


# Abstract_Work_Log model
@python_2_unicode_compatible
class Work_Log( Abstract_Work_Log ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------

    #slug = models.SlugField( unique = True )
    #name = models.CharField( max_length = 255, blank = True, null = True )
    #notes = models.TextField( blank = True, null = True )
    
    # tags!
    #tags = TaggableManager( blank = True )

    # time stamps.
    #create_date = models.DateTimeField( auto_now_add = True )
    #last_modified = models.DateTimeField( auto_now = True )
    
    pass

#-- END model Work_Log --#

