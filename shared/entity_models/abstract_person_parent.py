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
from context.shared.entity_models import Abstract_Entity_Container
from context.shared.entity_models import output_debug
from context.shared.entity_models import output_log_message
from context.shared.person_details import PersonDetails



#================================================================================
# ! ==> Abstract Models
#================================================================================


#-------------------------------------------------------------------------------
# ! --------> Abstract Human Models
#-------------------------------------------------------------------------------


# Abstract_Person_Parent model
class Abstract_Person_Parent( Abstract_Entity_Container ):

    #----------------------------------------------------------------------
    # ! ----> model fields and meta
    #----------------------------------------------------------------------


    # moving title up from Article_Person
    title = models.CharField( max_length = 255, blank = True, null = True )
    more_title = models.TextField( blank = True, null = True )
    #organization = models.ForeignKey( Organization, on_delete = models.SET_NULL, blank = True, null = True )
    organization_string = models.CharField( max_length = 255, blank = True, null = True )
    more_organization = models.TextField( blank = True, null = True )

    # field to store how person was captured.
    capture_method = models.CharField( max_length = 255, blank = True, null = True )

    # moved up to parent
    #notes = models.TextField( blank = True, null = True )
    #create_date = models.DateTimeField( auto_now_add = True )
    #last_modified = models.DateTimeField( auto_now = True )


    #----------------------------------------------------------------------
    # ! ----> Meta
    #----------------------------------------------------------------------


    # Meta-data for this class.
    class Meta:

        abstract = True

    #-- END class Meta --#


    #---------------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super().__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        if ( ( self.title ) or ( self.organization_string ) ):

            string_OUT += "( "

            string_list = []

            if ( self.title ):

                # add title to list
                string_list.append( "title = " + self.title )

            #-- END check for title --#

            if ( self.organization_string ):

                # add title to list
                string_list.append( "organization = " + self.organization_string )

            #-- END check for title --#

            string_OUT += "; ".join( string_list )

            string_OUT += " )"

        #-- END check to see if we have a title, organization, or capture_method. --#

        return string_OUT

    #-- END method __str__() --#


    #----------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------


    def set_capture_method( self, value_IN = "", overwrite_IN = False ):

        '''
        Accepts capture method value.  If there is already a value in the
            capture_method field, does nothing.  If not, stores the value passed
            in inside the capture_method field.

        Returns capture_method value.
        '''

        # return reference
        value_OUT = ""

        # declare variables
        existing_capture_method = ""

        # get existing value
        existing_capture_method = self.capture_method

        # are we allowed to update (either is empty, or overwrite flag is True).
        if ( ( ( existing_capture_method is None ) or ( existing_capture_method == "" ) )
            or ( overwrite_IN == True ) ):

            # OK to update.
            self.capture_method = value_IN

        #-- END check to see if we can update capture_method. --#

        # retrieve value_OUT from instance variable.
        value_OUT = self.capture_method

        return value_OUT

    #-- END method set_capture_method() --#


    def set_organization_string( self, organization_string_IN, do_save_IN = True, do_append_IN = True ):

        '''
        Accepts organization string and boolean flag that indicates whether to
           save if we make changes.  If no existing organization string, places
           first 255 characters into organization string.  If there is already a
           value, does nothing.

        Returns the organization string.
        '''

        # return reference
        value_OUT = ""

        # declare variables
        is_updated = False
        value_cleaned = ""
        value_length = -1
        existing_value = ""
        more_value_cleaned = ""

        # got a value passed in?
        if ( ( organization_string_IN is not None ) and ( organization_string_IN != "" ) ):

            # not updated so far...
            is_updated = False

            # got one.  strip off white space.
            value_cleaned = organization_string_IN.strip()

            # yes.  First, deal with existing value.
            existing_value = self.organization_string
            if ( ( existing_value is not None ) and ( existing_value != "" ) ):

                # we have an existing value.  Append it?
                if ( do_append_IN == True ):

                    # yes - anything in more_organization already?
                    if ( ( self.more_organization is not None ) and ( self.more_organization != "" ) ):

                        # yes.  Append.
                        self.more_organization += "\n" + existing_value

                    else:

                        # no - just chuck it in there.
                        self.more_organization = existing_value

                    #--END check to see if anything in more_organization --#

                    is_updated = True

                #-- END check to see if we append. --#

            #-- END check to see if we have an existing value. --#

            # Is new value longer than 255?
            value_length = len( value_cleaned )
            if ( value_length > 255 ):

                # field is 255 characters - truncate to 255, put that in
                #    org string, store full value in more_organization.
                self.organization_string = value_cleaned[ : 255 ]

                # already got more?
                if ( ( self.more_organization is not None ) and ( self.more_organization != "" ) ):

                    # yes.  Append entire value.
                    self.more_organization += "\n" + value_cleaned

                else:

                    # no - just chuck it in there.
                    self.more_organization = value_cleaned

                #--END check to see if anything in more_organization --#

                is_updated = True

            else:

                # value is not long.  Just put it in field.
                self.organization_string = value_cleaned
                is_updated = True

            #-- END check to see if value is too long. --#

            # updated?
            if ( is_updated == True ):

                # yes.  Do we save?
                if ( do_save_IN == True ):

                    # yes.  Save.
                    self.save()

                #-- END check to see if we save or not. --#

            #-- END check to see if changes made --#

        #-- END check to see anything passed in. --#

        value_OUT = self.organization_string

        return value_OUT

    #-- END method set_organization_string() --#


    def set_title( self, title_string_IN, do_save_IN = True, do_append_IN = True ):

        '''
        Accepts title string and boolean flag that indicates if we want to
           append to more_title if there is already a title.  If no existing
           title, places first 255 characters into title and stores the rest in
           more_title.  If there is title, if do_append, will just append the
           string passed in to more_title, preceded by a newline.

        Returns the title.
        '''

        # return reference
        value_OUT = ""

        # declare variables
        is_updated = False
        value_cleaned = ""
        value_length = -1
        existing_value = ""
        more_value_cleaned = ""

        # got a title passed in?
        if ( ( title_string_IN is not None ) and ( title_string_IN != "" ) ):

            # not updated so far...
            is_updated = False

            # got one.  strip off white space.
            value_cleaned = title_string_IN.strip()

            # yes.  First, deal with existing value.
            existing_value = self.title
            if ( ( existing_value is not None ) and ( existing_value != "" ) ):

                # we have an existing value.  Append it?
                if ( do_append_IN == True ):

                    # yes - anything in more_title already?
                    if ( ( self.more_title is not None ) and ( self.more_title != "" ) ):

                        # yes.  Append.
                        self.more_title += "\n" + existing_value

                    else:

                        # no - just chuck it in there.
                        self.more_title = existing_value

                    #--END check to see if anything in more_title --#

                    is_updated = True

                #-- END check to see if we append. --#

            #-- END check to see if we have an existing value. --#

            # Is new value longer than 255?
            value_length = len( value_cleaned )
            if ( value_length > 255 ):

                # field is 255 characters - truncate to 255, put that in
                #    title, store full value in more_title.
                self.title = value_cleaned[ : 255 ]

                # already got more?
                if ( ( self.more_title is not None ) and ( self.more_title != "" ) ):

                    # yes.  Append entire value.
                    self.more_title += "\n" + value_cleaned

                else:

                    # no - just chuck it in there.
                    self.more_title = value_cleaned

                #--END check to see if anything in more_title --#

                is_updated = True

            else:

                # value is not long.  Just put it in field.
                self.title = value_cleaned
                is_updated = True

            #-- END check to see if value is too long. --#

            # updated?
            if ( is_updated == True ):

                # yes.  Do we save?
                if ( do_save_IN == True ):

                    # yes.  Save.
                    self.save()

                #-- END check to see if we save or not. --#

            #-- END check to see if changes made --#

        #-- END check to see anything passed in. --#

        value_OUT = self.title

        return value_OUT

    #-- END method set_title() --#


    def update_from_person_details( self, person_details_IN, do_save_IN = True ):

        '''
        Accepts PersonDetails instance and an optional boolean flag that tells
            whether we want to save at the end or not.  For PersonDetails that
            are present in this abstract class (title and organization),
            retrieves values from person_details, then processes them
            appropriately.  End result is that this instance is updated, and if
            the do_save_IN flag is set, the updated values are persisted to the
            database, as well.

        Preconditions: Must pass a PersonDetails instance, even if it is empty.

        Postconditions: Instance is updated, and if do_save_IN is True, any
            changes are saved to the database.

        Returns the title.
        '''

        # return reference
        status_OUT = None

        # declare variables
        me = "update_from_person_details"
        my_person_details = None
        my_id = -1
        existing_title = ""
        existing_organization_string = ""
        existing_organization = None
        existing_notes = ""
        title_IN = ""
        organization_string_IN = ""
        organization_IN = None
        notes_IN = ""
        capture_method_IN = ""
        is_insert = False
        is_updated = False

        # get values of interest from this instance.
        existing_title = self.title
        existing_organization_string = self.organization_string
        existing_organization = self.organization
        existing_notes = self.notes
        existing_capture_method = self.capture_method

        # got person_details?
        my_person_details = PersonDetails.get_instance( person_details_IN )
        if ( my_person_details is not None ):

            # we have PersonDetails.  Get values of interest.
            title_IN = my_person_details.get( PersonDetails.PROP_NAME_TITLE, None )
            organization_string_IN = my_person_details.get( PersonDetails.PROP_NAME_PERSON_ORGANIZATION, None )
            organization_IN = my_person_details.get( PersonDetails.PROP_NAME_ORGANIZATION_INSTANCE, None )
            notes_IN = my_person_details.get( PersonDetails.PROP_NAME_NOTES, None )
            capture_method_IN = my_person_details.get( PersonDetails.PROP_NAME_CAPTURE_METHOD, None )

            # got an ID (check to see if update or insert)?
            my_id = self.id
            if ( ( my_id is not None ) and ( int( my_id ) > 0 ) ):

                # no ID.  Insert.
                is_insert = True

            else:

                # there is an id.  Not an insert.
                is_insert = False

            #-- END check to see if insert or update --#

            #------------------------------------------------------#
            # ==> title

            # value passed in?
            if ( title_IN is not None ):

                # yes.  has title changed?
                if ( existing_title != title_IN ):

                    # yes.  Update title.
                    self.set_title( title_IN, do_save_IN = do_save_IN, do_append_IN = True )

                    # we need to save.
                    is_updated = True

                #-- END check to see if title changed --#

            #-- END check to see if title value passed in. --#

            #------------------------------------------------------#
            # ==> organization string

            # value passed in?
            if ( organization_string_IN is not None ):

                # has organization changed?
                if ( existing_organization_string != organization_string_IN ):

                    # yes.  Replace.
                    self.organization_string = ""
                    self.set_organization_string( organization_string_IN, do_save_IN = do_save_IN, do_append_IN = True )

                    # we need to save.
                    is_updated = True

                #-- END check to see if new value. --#

            #-- END check to see if organization string value passed in --#

            #------------------------------------------------------#
            # ==> organization instance

            # value passed in?
            if ( organization_IN is not None ):

                # store it.
                self.organization = organization_IN

                # we need to save.
                is_updated = True

            #-- END check to see if organization instance passed in --#

            #------------------------------------------------------#
            # ==> notes

            # value passed in?
            if ( notes_IN is not None ):

                # notes already?
                if ( existing_notes is not None ):

                    # other than empty?
                    if ( existing_notes != "" ):

                        # not empty. Add a semi-colon and a space.
                        self.notes += "; "

                    #-- END check to see if empty --#

                    # Append.
                    self.notes += notes_IN

                else:

                    # no.  Just store.
                    self.notes = notes_IN

                #-- END check to see if new value. --#

                # we need to save.
                is_updated = True

            #-- END check to see if organization string value passed in --#

            #------------------------------------------------------#
            # ==> capture_method

            # value passed in?
            if ( capture_method_IN is not None ):

                # store it.
                self.set_capture_method( capture_method_IN )

                # we need to save.
                is_updated = True

            #-- END check to see if capture_method passed in --#

            # updated?
            if ( is_updated == True ):

                # yes.  Do we save?
                if ( do_save_IN == True ):

                    # yes.  Save.
                    self.save()

                #-- END check to see if we save or not. --#

            #-- END check to see if changes made --#

        #-- END check to see anything passed in. --#

        return status_OUT

    #-- END method update_from_person_details() --#


#== END abstract Abstract_Person_Parent Model =================================#
