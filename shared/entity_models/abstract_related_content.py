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
import hashlib
import logging

# Django imports
#from django.contrib.postgres.fields import JSONField
from django.db import models

# taggit tagging APIs
from taggit.managers import TaggableManager

# python_utilities
from python_utilities.beautiful_soup.beautiful_soup_helper import BeautifulSoupHelper
from python_utilities.strings.string_helper import StringHelper

# context imports
from context.shared.entity_models import output_debug
from context.shared.entity_models import output_log_message


#================================================================================
# ! ==> Abstract Models
#================================================================================


# Abstract_Related_Content model
class Abstract_Related_Content( models.Model ):

    # Content types:
    CONTENT_TYPE_CANONICAL = 'canonical'
    CONTENT_TYPE_TEXT = 'text'
    CONTENT_TYPE_HTML = 'html'
    CONTENT_TYPE_JSON = 'json'
    CONTENT_TYPE_XML = 'xml'
    CONTENT_TYPE_OTHER = 'other'
    CONTENT_TYPE_NONE = 'none'
    CONTENT_TYPE_DEFAULT = CONTENT_TYPE_TEXT

    CONTENT_TYPE_CHOICES = (
        ( CONTENT_TYPE_CANONICAL, "Canonical" ),
        ( CONTENT_TYPE_TEXT, "Text" ),
        ( CONTENT_TYPE_HTML, "HTML" ),
        ( CONTENT_TYPE_JSON, "JSON" ),
        ( CONTENT_TYPE_XML, "XML" ),
        ( CONTENT_TYPE_OTHER, "Other" ),
        ( CONTENT_TYPE_NONE, "None" )
    )

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------

    #article = models.ForeignKey( Article, on_delete = models.SET_NULL, unique = True, null = True )
    related_instance = None
    content_type = models.CharField( max_length = 255, choices = CONTENT_TYPE_CHOICES, blank = True, null = True, default = "none" )
    content = models.TextField()
    content_hash = models.CharField( max_length = 255, blank = True )
    status = models.CharField( max_length = 255, blank = True, null = True )
    source = models.CharField( max_length = 255, blank = True, null = True )
    source_identifier = models.TextField( blank = True, null = True )
    note_type = models.CharField( max_length = 255, blank = True, null = True )
    content_description = models.TextField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )

    # tags!
    tags = TaggableManager( blank = True )

    # meta class so we know this is an abstract class.
    class Meta:
        abstract = True
        ordering = [ 'last_modified', 'create_date' ]

    #----------------------------------------------------------------------
    # NOT instance variables
    # Class variables - overriden by __init__() per instance if same names, but
    #    if not set there, shared!
    #----------------------------------------------------------------------


    #bs_helper = None


    #----------------------------------------------------------------------------
    # class methods
    #----------------------------------------------------------------------------


    @classmethod
    def make_string_hash( cls, value_IN, hash_function_IN = hashlib.sha256 ):

        # return reference
        value_OUT = None

        # declare variables
        me = "make_string_hash"

        # call StringHelper method.
        value_OUT = StringHelper.make_string_hash( value_IN, hash_function_IN = hash_function_IN )

        return value_OUT

    #-- END class method make_standard_json_string_hash() --#


    #----------------------------------------------------------------------------
    # instance methods
    #----------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super().__init__( *args, **kwargs )

        # then, initialize variable.
        self.bs_helper = None

    #-- END method __init__() --#


    def get_bs_helper( self ):

        # return reference
        instance_OUT = None

        # get instance.
        instance_OUT = self.bs_helper

        # got one?
        if ( not( instance_OUT ) ):

            # no.  Create and store.
            self.bs_helper = BeautifulSoupHelper()

            # try again.  If nothing this time, nothing we can do.  Return it.
            instance_OUT = self.bs_helper

        #-- END check to see if regex is stored in instance --#

        return instance_OUT

    #-- END method get_bs_helper() --#


    def get_content( self, *args, **kwargs ):

        '''
        Returns content nested in this instance.
        Preconditions: None
        Postconditions: None

        Returns the content exactly as it is stored in the instance.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "get_content"

        # return the content.
        value_OUT = self.content

        return value_OUT

    #-- END method get_content() --#


    def get_content_hash( self, *args, **kwargs ):

        '''
        Returns content_hash nested in this instance.
        Preconditions: None
        Postconditions: None

        Returns the content_hash exactly as it is stored in the instance.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "get_content_hash"

        # return the content.
        value_OUT = self.content_hash

        return value_OUT

    #-- END method get_content_hash() --#


    def set_content( self, value_IN = "", hash_function_IN = hashlib.sha256, *args, **kwargs ):

        '''
        Accepts a piece of text.  Stores it in this instance's content variable.
        Preconditions: None
        Postconditions: None

        Returns the content as it is stored in the instance.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "set_content"
        my_value_bytes = None
        my_value_hash = None
        my_value_hash_hexdigest = None

        # set the text in the instance.
        self.content = value_IN

        # Is value not None and not empty?
        if ( ( value_IN is not None ) and ( value_IN != "" ) ):

            # get hex digest of hash
            my_value_hash_hexdigest = self.make_string_hash( value_IN )

            # store it.
            self.set_content_hash( my_value_hash_hexdigest )

        #-- END check to see if value is not None. --#

        # return the content.
        value_OUT = self.get_content()

        return value_OUT

    #-- END method set_content() --#


    def set_content_hash( self, value_IN = "", *args, **kwargs ):

        '''
        Accepts the hash of the data in "content". Stores it in this instance's
            content_hash variable.
        Preconditions: None
        Postconditions: None

        Returns the content_hash as it is stored in the instance.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "set_content_hash"

        # set the text in the instance.
        self.content_hash = value_IN

        # return the content_hash.
        value_OUT = self.get_content_hash()

        return value_OUT

    #-- END method set_content_hash() --#


    def to_string( self ):

        # return reference
        string_OUT = ""

        if ( self.id ):

            string_OUT += str( self.id ) + " - "

        #-- END check to see if ID --#

        if ( self.content_description ):

            string_OUT += self.content_description

        #-- END check to see if content_description --#

        if ( self.content_type ):

            string_OUT += " of type \"" + self.content_type + "\""

        #-- END check to see if there is a type --#

        return string_OUT

    #-- END method __str__() --#


    def __str__( self ):

        # return reference
        string_OUT = ""

        string_OUT = self.to_string()

        return string_OUT

    #-- END method __str__() --#


#-- END abstract Abstract_Related_Content model --#
