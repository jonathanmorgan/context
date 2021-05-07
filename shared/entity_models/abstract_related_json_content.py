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

# python_utilities
from python_utilities.json.json_helper import JSONHelper

# context imports
from context.shared.entity_models import Abstract_Related_Content
from context.shared.entity_models import output_debug
from context.shared.entity_models import output_log_message


#================================================================================
# ! ==> Abstract Models
#================================================================================


# Abstract_Related_JSON_Content model
class Abstract_Related_JSON_Content( Abstract_Related_Content ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------

    content = models.TextField( blank = True, null = True )
    content_json = models.JSONField( blank = True, null = True )
    content_json_hash = models.CharField( max_length = 255, blank = True )

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
    def make_standard_json_string_hash( cls, json_IN ):

        # return reference
        value_OUT = None

        # declare variables
        me = "make_standard_json_string_hash"
        json_object = None
        my_json_hash_hexdigest = None

        # value_IN is json_object
        json_object = json_IN

        # Is JSON not None?
        if ( json_object is not None ):

            # not None - create hash of standardized JSON string and store.
            my_json_hash_hexdigest = JSONHelper.create_standard_json_hash( json_object )
            value_OUT = my_json_hash_hexdigest

        #-- END check to see if JSON is not None. --#

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


    def get_content_json( self, *args, **kwargs ):

        '''
        Returns content nested in this instance.
        Preconditions: None
        Postconditions: None

        Returns the content exactly as it is stored in the instance.
        '''

        # return reference
        content_OUT = None

        # declare variables
        me = "get_content_json"

        # return the content.
        content_OUT = self.content_json

        return content_OUT

    #-- END method get_content_json() --#


    def get_content_json_hash( self, *args, **kwargs ):

        '''
        Returns content_json_hash nested in this instance.
        Preconditions: None
        Postconditions: None

        Returns the content_json_hash exactly as it is stored in the instance.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "get_content_json_hash"

        # return the content.
        value_OUT = self.content_json_hash

        return value_OUT

    #-- END method get_content_json_hash() --#


    def set_content_json( self, value_IN = "", *args, **kwargs ):

        '''
        Accepts a JSON object (dictionary).  Stores it in this instance's
            content_json variable.
        Preconditions: None
        Postconditions: Also creates a sha256 hash of the standardized string
            representation of the JSON passed in and stores it in
            content_json_hash.

        Returns content_json as it is stored in the instance.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "set_content_json"
        json_object = None
        my_json_hash_hexdigest = None

        # value_IN is json_object
        json_object = value_IN

        # set the JSON in the instance.
        self.content_json = value_IN

        # Is JSON not None?
        if ( json_object is not None ):

            # not None - create hash of standardized JSON string and store.
            my_json_hash_hexdigest = self.make_standard_json_string_hash( json_object )
            self.set_content_json_hash( my_json_hash_hexdigest )

        #-- END check to see if JSON is not None. --#

        # return the content.
        value_OUT = self.get_content_json()

        return value_OUT

    #-- END method set_content_json() --#


    def set_content_json_hash( self, value_IN = "", *args, **kwargs ):

        '''
        Accepts a hash of a JSON object's standardized string representation.
            Stores it in this instance's content_json_hash variable.
        Preconditions: None
        Postconditions: Also creates a sha256 hash of the standardized string
            representation of the JSON passed in and stores it in
            content_json_hash.

        Returns content_json as it is stored in the instance.
        '''

        # return reference
        value_OUT = None

        # declare variables
        me = "set_content_json_hash"

        # set the value in the instance.
        self.content_json_hash = value_IN

        # return the content.
        value_OUT = self.get_content_json_hash()

        return value_OUT

    #-- END method set_content_json_hash() --#


#-- END abstract Abstract_Related_JSON_Content model --#
