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
import datetime
import logging

# Django imports
#from django.contrib.postgres.fields import JSONField
from django.db import models

# python_utilities
from python_utilities.json.json_helper import JSONHelper
from python_utilities.logging.logging_helper import LoggingHelper
from python_utilities.status.status_container import StatusContainer

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
    LOGGING_LOGGER_NAME = "context.shared.entity_models.Abstract_Related_JSON_Content"


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


    @classmethod
    def update_related_json( cls, related_instance_IN, json_IN, json_source_IN = None ):

        '''
        Accepts related instance, JSON. Checks if identical record exists
            in this related class related to instance passed in. If not, adds
            this one. If yes, updates the description to note that it was
            encountered an additional time.

        Preconditions: assumes you'll pass something in to every argument. A
            None in any of them will cause errors.

        Postconditions: Also outputs error log message if there was a problem.
            Could throw exception on incorrect calls, but for now, we'll just
            make sure there is a good error message logged.

        Returns: StatusContainer with information on results.
        '''

        # return reference
        status_OUT = None

        # declare variables
        me = "update_related_json"
        status_message = None
        my_related_instance = None
        update_status = None
        update_success = None
        my_json = None
        my_json_hash = None
        related_qs = None
        related_count = None
        related_content = None
        related_instance = None

        # init
        status_OUT = StatusContainer()
        status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
        do_store_related = False

        # do we have a related instance?
        my_related_instance = related_instance_IN
        if ( my_related_instance is not None ):

            # do we have JSON?
            my_json = json_IN
            if ( my_json is not None ):

                # look for related instance associated with this instance that
                #     matches this JSON.
                # if not found, make one and associate it with this instance.

                # create hash from standardized string representation of JSON passed
                #     in.
                my_json_hash = cls.make_standard_json_string_hash( my_json )

                # check if any related have same hash.
                related_qs = cls.objects.filter( related_instance = my_related_instance )
                related_qs = related_qs.filter( content_json_hash = my_json_hash )
                related_count = related_qs.count()

                # got any matches? If no, just make new.
                if ( related_count == 0 ):

                    # no related so far, add one!
                    related_instance = cls()
                    related_instance.related_instance = my_related_instance
                    related_instance.set_content_json( my_json )
                    related_instance.content_type = cls.CONTENT_TYPE_JSON

                    if ( json_source_IN is not None ):
                        related_instance.source = json_source_IN
                        related_instance.content_description = "- Updated from {source}: {timestamp}".format(
                            source = json_source_IN,
                            timestamp = datetime.datetime.now()
                        )
                    else:
                        related_instance.source = None
                        related_instance.content_description = "- Updated: {timestamp}".format( timestamp = datetime.datetime.now() )
                    #-- END check to see if json_source_IN --#

                    related_instance.save()

                    # status
                    status_message = "In {method}(): created new related data - {related_instance} ( class: {class_ref} )".format(
                        method = me,
                        related_instance = related_instance,
                        class_ref = cls
                    )
                    status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
                    status_OUT.add_message( status_message )

                    # TODO - log message, also.

                elif ( related_count == 1 ):

                    # 1 match - update notes to include mention of today.
                    related_instance = related_qs.get()
                    related_instance.content_description += "\n- Loaded: {timestamp}".format( timestamp = datetime.datetime.now() )
                    related_instance.save()

                    # status
                    status_message = "In {method}(): found matching related data - {related_instance} ( class: {class_ref} )".format(
                        method = me,
                        related_instance = related_instance,
                        class_ref = cls
                    )
                    status_OUT.set_status_code( StatusContainer.STATUS_CODE_SUCCESS )
                    status_OUT.add_message( status_message )

                    # TODO - log message, also.

                else:

                    # multiple matches...? Error.
                    status_message = "ERROR - In {method}(): either multiple or negative record count ( {related_count} )".format(
                        method = me,
                        related_count = related_count
                    )
                    status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                    status_OUT.add_message( status_message )

                    # log message, also.
                    LoggingHelper.log_message(
                        status_message,
                        method_IN = me,
                        logger_name_IN = self.LOGGING_LOGGER_NAME,
                        do_print_IN = True,
                        log_level_code_IN = logging.ERROR
                    )

                    # raise exception.
                    raise ETLError( status_message )

                #-- END check to see if related --#

            else:

                # no record passed in - log error, return false.
                status_message = "ERROR - No json dictionary passed in ( {} ).".format( record_IN )
                LoggingHelper.log_message(
                    status_message,
                    method_IN = me,
                    logger_name_IN = self.LOGGING_LOGGER_NAME,
                    do_print_IN = True,
                    log_level_code_IN = logging.ERROR
                )

                # status
                status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
                status_OUT.add_message( status_message )

            #-- END check to see if record is not None --#

        else:

            # no related class - can't do anything, log error, return false.
            status_message = "ERROR - No related_class, can't update related."
            LoggingHelper.log_message(
                status_message,
                method_IN = me,
                logger_name_IN = self.LOGGING_LOGGER_NAME,
                do_print_IN = True,
                log_level_code_IN = logging.ERROR
            )

            # status
            status_OUT.set_status_code( StatusContainer.STATUS_CODE_ERROR )
            status_OUT.add_message( status_message )

        #-- END check to see if we have a related class --#

        return status_OUT

    #-- END method update_related_json()


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
