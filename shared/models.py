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

# six
import six

# nameparser import
# http://pypi.python.org/pypi/nameparser
from nameparser import HumanName

# Django imports
from django.db import models
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible

# taggit tagging APIs
from taggit.managers import TaggableManager

# python_utilities
from python_utilities.beautiful_soup.beautiful_soup_helper import BeautifulSoupHelper
from python_utilities.logging.logging_helper import LoggingHelper
from python_utilities.strings.string_helper import StringHelper

# context imports
from context.shared.person_details import PersonDetails


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
            my_logger_name = "context.shared.models"
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


# Abstract_UUID model
@python_2_unicode_compatible
class Abstract_UUID( models.Model ):

    name = models.CharField( max_length = 255, null = True, blank = True )
    uuid = models.TextField( blank = True, null = True )
    id_type = models.CharField( max_length = 255, null = True, blank = True )
    source = models.CharField( max_length = 255, null = True, blank = True )
    notes = models.TextField( blank = True, null = True )

    # meta class so we know this is an abstract class.
    class Meta:
        abstract = True
        ordering = [ 'id_type', 'source', 'name', 'uuid' ]

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


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
        
            string_OUT += prefix_string + self.name
            prefix_string = " - "
            
        #-- END check to see if name. --#
            
        if ( self.source ):
        
            string_OUT += prefix_string + " ( " + self.source + " )"
            prefix_string = " - "
            
        #-- END check to see if source. --#
            
        if ( self.uuid ):
        
            string_OUT += prefix_string + self.uuid
            prefix_string = " - "
            
        #-- END check to see if uuid. --#
            
        if ( self.id_type ):
        
            string_OUT += "{} ( {} )".format( prefix_string, self.id_type )
            prefix_string = " - "
            
        #-- END check to see if id_type. --#
            
        return string_OUT
        
    #-- END method __str__() --#


#= End Abstract_UUID Model ======================================================


# Abstract_Related_Content model
@python_2_unicode_compatible
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
    content_type = models.CharField( max_length = 255, choices = CONTENT_TYPE_CHOICES, blank = True, null = True, default = "none" )
    content = models.TextField()
    status = models.CharField( max_length = 255, blank = True, null = True )
    source = models.CharField( max_length = 255, blank = True, null = True )
    content_description = models.TextField( blank = True, null = True )
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )

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
    # methods
    #----------------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Abstract_Related_Content, self ).__init__( *args, **kwargs )

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
        content_OUT = None

        # declare variables
        me = "get_content"

        # return the content.
        content_OUT = self.content
                
        return content_OUT

    #-- END method get_content() --#


    def set_content( self, value_IN = "", *args, **kwargs ):
        
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

        # set the text in the instance.
        self.content = value_IN
        
        # return the content.
        value_OUT = self.content
                
        return value_OUT

    #-- END method set_content() --#
    

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


#-------------------------------------------------------------------------------
# ! --------> Abstract Human Models
#-------------------------------------------------------------------------------


# Locations
@python_2_unicode_compatible
class Abstract_Location( models.Model ):

    # States to choose from.
    STATE_CHOICES = (
        ( 'AL', 'Alabama' ),
        ( 'AK', 'Alaska' ),
        ( 'AS', 'American Samoa' ),
        ( 'AZ', 'Arizona' ),
        ( 'AR', 'Arkansas' ),
        ( 'CA', 'California' ),
        ( 'CO', 'Colorado' ),
        ( 'CT', 'Connecticut' ),
        ( 'DE', 'Delaware' ),
        ( 'DC', 'District of Columbia' ),
        ( 'FM', 'Federated States of Micronesia' ),
        ( 'FL', 'Florida' ),
        ( 'GA', 'Georgia' ),
        ( 'GU', 'Guam' ),
        ( 'HI', 'Hawaii' ),
        ( 'ID', 'Idaho' ),
        ( 'IL', 'Illinois' ),
        ( 'IN', 'Indiana' ),
        ( 'IA', 'Iowa' ),
        ( 'KS', 'Kansas' ),
        ( 'KY', 'Kentucky' ),
        ( 'LA', 'Louisiana' ),
        ( 'ME', 'Maine' ),
        ( 'MH', 'Marshall Islands' ),
        ( 'MD', 'Maryland' ),
        ( 'MA', 'Massachusetts' ),
        ( 'MI', 'Michigan' ),
        ( 'MN', 'Minnesota' ),
        ( 'MS', 'Mississippi' ),
        ( 'MO', 'Missouri' ),
        ( 'MT', 'Montana' ),
        ( 'NE', 'Nebraska' ),
        ( 'NV', 'Nevada' ),
        ( 'NH', 'New Hampshire' ),
        ( 'NJ', 'New Jersey' ),
        ( 'NM', 'New Mexico' ),
        ( 'NY', 'New York' ),
        ( 'NC', 'North Carolina' ),
        ( 'ND', 'North Dakota' ),
        ( 'MP', 'Northern Mariana Islands' ),
        ( 'OH', 'Ohio' ),
        ( 'OK', 'Oklahoma' ),
        ( 'OR', 'Oregon' ),
        ( 'PW', 'Palau' ),
        ( 'PA', 'Pennsylvania' ),
        ( 'PR', 'Puerto Rico' ),
        ( 'RI', 'Rhode Island' ),
        ( 'SC', 'South Carolina' ),
        ( 'SD', 'South Dakota' ),
        ( 'TN', 'Tennessee' ),
        ( 'TX', 'Texas' ),
        ( 'UT', 'Utah' ),
        ( 'VT', 'Vermont' ),
        ( 'VI', 'Virgin Islands' ),
        ( 'VA', 'Virginia' ),
        ( 'WA', 'Washington' ),
        ( 'WV', 'West Virginia' ),
        ( 'WI', 'Wisconsin' ),
        ( 'WY', 'Wyoming' )
    )

    name = models.CharField( max_length = 255, blank = True )
    description = models.TextField( blank=True )
    address = models.CharField( max_length = 255, blank = True )
    city = models.CharField( max_length = 255, blank = True )
    county = models.CharField( max_length = 255, blank = True )
    state = models.CharField( max_length = 2, choices = STATE_CHOICES, blank = True )
    zip_code = models.CharField( 'ZIP Code', max_length = 10, blank = True )

    # Meta-data for this class.
    class Meta:
        ordering = [ 'name', 'city', 'county', 'state', 'zip_code' ]
        abstract = True

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Abstract_Location, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    
    def __str__( self ):
        # return reference
        string_OUT = ''
        delimiter = ''

        # see what we can place in the string.
        if ( self.name != '' ):
            string_OUT = '"' + self.name + '"'
            delimiter = ', '

        if ( self.address != '' ):
            string_OUT = string_OUT + delimiter + self.address
            delimiter = ', '

        if ( self.city != '' ):
            string_OUT = string_OUT + delimiter + self.city
            delimiter = ', '

        if ( self.county != '' ):
            string_OUT = string_OUT + delimiter + self.county + " County"
            delimiter = ', '

        if ( self.state != '' ):
            string_OUT = string_OUT + delimiter + self.state
            delimiter = ', '

        if ( self.zip_code != '' ):
            string_OUT = string_OUT + delimiter + self.zip_code
            delimiter = ', '

        return string_OUT

#= End Abstract_Location Model ===========================================================


# AbstractOrganization model
@python_2_unicode_compatible
class Abstract_Organization( models.Model ):

    name = models.CharField( max_length = 255 )
    description = models.TextField( blank = True )
    #location = models.ForeignKey( Location, on_delete = models.SET_NULL, blank = True, null = True )

    # Meta-data for this class.
    class Meta:
        ordering = [ 'name', 'location' ]
        abstract = True

    #----------------------------------------------------------------------
    # methods
    #----------------------------------------------------------------------

    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Abstract_Organization, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#

    
    def __str__( self ):
        string_OUT = self.name
        return string_OUT
    #-- END method __str_() --#


#= End Abstract_Organization Model ======================================================


# Abstract_Person_Parent model
@python_2_unicode_compatible
class Abstract_Person_Parent( models.Model ):

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------

    # moving title up from Article_Person
    title = models.CharField( max_length = 255, blank = True, null = True )
    more_title = models.TextField( blank = True, null = True )
    #organization = models.ForeignKey( Organization, on_delete = models.SET_NULL, blank = True, null = True )
    organization_string = models.CharField( max_length = 255, blank = True, null = True )
    more_organization = models.TextField( blank = True, null = True )
    notes = models.TextField( blank = True, null = True )
    
    # field to store how person was captured.
    capture_method = models.CharField( max_length = 255, blank = True, null = True )

    #----------------------------------------------------------------------
    # Meta
    #----------------------------------------------------------------------

    # Meta-data for this class.
    class Meta:

        abstract = True
        
    #-- END class Meta --#

    #----------------------------------------------------------------------
    # ! instance methods
    #----------------------------------------------------------------------


    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Abstract_Person_Parent, self ).__init__( *args, **kwargs )

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


# Abstract_Person model
@python_2_unicode_compatible
class Abstract_Person( Abstract_Person_Parent ):

    '''
    HumanName (from package "nameparser" ) code sample:
    
    from nameparser import HumanName
    >>> test = HumanName( "Jonathan Scott Morgan" )
    >>> test
    <HumanName : [
            Title: '' 
            First: 'Jonathan' 
            Middle: 'Scott' 
            Last: 'Morgan' 
            Suffix: ''
    ]>
    >>> import pickle
    >>> test2 = pickle.dumps( test )
    >>> test3 = pickle.loads( test2 )
    >>> test3.__eq__( test2 )
    False
    >>> test3.__eq__( test )
    True
    >>> test3.first
    u'Jonathan'
    >>> test3.middle
    u'Scott'
    >>> test3.last
    u'Morgan'
    >>> test3.title
    u''
    >>> test3.suffix
    u''
    >>> if ( test3 == test ):
    ...     print( "True!" )
    ... else:
    ...     print( "False!" )
    ... 
    True!
    '''


    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------    

    GENDER_CHOICES = (
        ( 'na', 'Unknown' ),
        ( 'female', 'Female' ),
        ( 'male', 'Male' )
    )
    
    # lookup status
    LOOKUP_STATUS_FOUND = "found"
    LOOKUP_STATUS_NEW = "new"
    LOOKUP_STATUS_NONE = "None"

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------

    first_name = models.CharField( max_length = 255, blank = True, null = True )
    middle_name = models.CharField( max_length = 255, blank = True, null = True )
    last_name = models.CharField( max_length = 255, blank = True, null = True )
    name_prefix = models.CharField( max_length = 255, blank = True, null = True )
    name_suffix = models.CharField( max_length = 255, blank = True, null = True )
    nickname = models.CharField( max_length = 255, blank = True, null = True )
    full_name_string = models.CharField( max_length = 255, blank = True, null = True )
    original_name_string = models.CharField( max_length = 255, blank = True, null = True )
    gender = models.CharField( max_length = 6, choices = GENDER_CHOICES, blank = True, null = True )
    nameparser_pickled = models.TextField( blank = True, null = True )
    is_ambiguous = models.BooleanField( default = False )
    # moved up to parent
    #notes = models.TextField( blank = True, null = True )
    
    # field to store how source was captured - moved up to parent.
    # capture_method = models.CharField( max_length = 255, blank = True, null = True )

    # time stamps.
    create_date = models.DateTimeField( auto_now_add = True )
    last_modified = models.DateTimeField( auto_now = True )

    # Meta-data for this class.
    class Meta:

        abstract = True
        ordering = [ 'last_name', 'first_name', 'middle_name' ]
        
    #-- END class Meta --#


    #----------------------------------------------------------------------
    # ! static methods
    #----------------------------------------------------------------------
    
    
    @staticmethod
    def HumanName_to_str( human_name_IN ):
    
        # return reference
        string_OUT = ""
    
        string_OUT += "HumanName: \"" + StringHelper.object_to_unicode_string( human_name_IN ) + "\"\n"
        string_OUT += "- title: " + human_name_IN.title + "\n"
        string_OUT += "- first: " + human_name_IN.first + "\n"
        string_OUT += "- middle: " + human_name_IN.middle + "\n"
        string_OUT += "- last: " + human_name_IN.last + "\n"
        string_OUT += "- suffix: " + human_name_IN.suffix + "\n"
        string_OUT += "- nickname: " + human_name_IN.nickname + "\n"
        
        return string_OUT
    
    #-- END static method HumanName_to_str() --#


    #----------------------------------------------------------------------
    # ! class methods
    #----------------------------------------------------------------------
    
    
    @classmethod
    def create_person_for_name( cls,
                                name_IN,
                                parsed_name_IN = None,
                                remove_periods_IN = False,
                                *args,
                                **kwargs ):
    
        '''
        Accepts name string.  Creates instance of cls, stores name in it, then
           returns the instance.  Eventually, might do more fancy or
           sophisticated things, but for now, not so much.
        '''
        
        # return reference
        instance_OUT = None
        
        # got a name?
        if ( ( name_IN is not None ) and ( name_IN != "" ) ):
        
            # create new Person!
            instance_OUT = cls()
            
            # store name
            instance_OUT.set_name( name_IN,
                                   parsed_name_IN = parsed_name_IN,
                                   remove_periods_IN = remove_periods_IN,
                                   *args,
                                   **kwargs )
            
        else:
        
            instance_OUT = None
            
        #-- END check to make sure there is a name. --#
        
        return instance_OUT
        
    #-- END class method create_person_for_name() --#
        
        
    @classmethod
    def find_person_from_name( cls, name_IN, do_strict_match_IN = True, do_partial_match_IN = False ):
        
        '''
        More flexible way of looking for a person than look_up_person_from_name
            (though it uses it quite extensively).  Accepts name string.  Tries
            the following to find a matching person:
            - looks for exact match.
            - if no match, checks if one word.  If just one word, looks for
                any name part that contains that one word.
            - if not one word, or no one-word match, tries non-exact lookup.
            - if no match, tries non-exact, partial lookup.
        
        Postconditions: returns QuerySet instance with what this method could
            find.  Might be empty.  If fatal error, returns None.
        '''
    
        # return reference
        query_set_OUT = None
        
        # declare variables
        me = "find_person_from_name"
        match_count = -1
        name_part_list = None
        name_part_count = -1
    
        # first, try a strict lookup.
        query_set_OUT = cls.look_up_person_from_name( name_IN, do_strict_match_IN = do_strict_match_IN, do_partial_match_IN = do_partial_match_IN )
        
        # got anything back?
        match_count = query_set_OUT.count()
        if ( match_count == 0 ):
        
            # no exact matches.  Is it just one word?
            name_part_list = name_IN.split()
            name_part_count = len( name_part_list )
            if ( name_part_count == 1 ):
            
                # just one word.  Try the old way, so we get either first,
                #    middle or last.
                query_set_OUT = cls.objects.filter( Q( first_name__icontains = name_IN ) | Q( middle_name__icontains = name_IN ) | Q( last_name__icontains = name_IN ) | Q( full_name_string__icontains = name_IN ) )
                
            #-- END check to see if just one word. --#
            
            # got anything back?
            match_count = query_set_OUT.count()
            if ( match_count == 0 ):

                # no.  Try not strict.
                query_set_OUT = cls.look_up_person_from_name( name_IN, do_strict_match_IN = False, do_partial_match_IN = False )
        
                # got anything back?
                match_count = query_set_OUT.count()
                if ( match_count == 0 ):
                
                    # no exact matches.  Try not strict, allow partial match.
                    query_set_OUT = cls.look_up_person_from_name( name_IN, do_strict_match_IN = False, do_partial_match_IN = True )
                
                    # got anything back?
                    match_count = query_set_OUT.count()
                    if ( match_count == 0 ):
                    
                        # no lookup matches.  Try the old way...
                        query_set_OUT = cls.objects.filter( Q( first_name__icontains = name_IN ) | Q( middle_name__icontains = name_IN ) | Q( last_name__icontains = name_IN ) | Q( full_name_string__icontains = name_IN ) )
                    
                    #-- END check to see if any non-strict partial matches. --#
                
                #-- END check to see if any non-strict matches. --#

            #-- END check to see if any matches for just one word. --#

        #-- END check to see if strict matches. --#
            
        return query_set_OUT

    #-- END class method find_person_from_name() --#

    @classmethod
    def get_person_for_name( cls,
                             name_IN,
                             create_if_no_match_IN = False,
                             parsed_name_IN = None,
                             do_strict_match_IN = False,
                             do_partial_match_IN = False ):
    
        '''
        This method accepts the full name of a person.  Uses NameParse object to
           parse name into prefix/title, first name, middle name(s), last name,
           and suffix.  Looks first for an exact person match.  If one found,
           returns it.  If none found, returns new Person instance with name
           stored in it.
        preconditions: None.
        postconditions: Looks first for an exact person match.  If one found,
           returns it.  If none found, returns new Person instance with name
           stored in it.  If multiple matches found, error, so will return None.
           If new Person instance returned, it will not have been saved.  If you
           want that person to be in the database, you have to save it yourself.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables.
        me = "get_person_for_name"
        person_qs = None
        person_count = -1
        id_list = []
        
        # got a name?
        if ( name_IN ):
        
            # try to retrieve person for name.
            person_qs = cls.look_up_person_from_name( name_IN,
                                                      parsed_name_IN = parsed_name_IN,
                                                      do_strict_match_IN = do_strict_match_IN,
                                                      do_partial_match_IN = do_partial_match_IN )
            
            # got a match?
            person_count = person_qs.count()
            if ( person_count == 1 ):
            
                # got one match.  Return it.
                instance_OUT = person_qs.get()
                
                output_debug( "In " + me + ": found single match for name: " + name_IN )
                
            elif( person_count == 0 ):
            
                # no matches.  What do we do?
                if ( create_if_no_match_IN == True ):
                
                    # create new Person!
                    instance_OUT = cls.create_person_for_name( name_IN, parsed_name_IN = parsed_name_IN )
                    
                    output_debug( "In " + me + ": no match for name: \"" + name_IN + "\"; so, creating new Person instance (but not saving yet)!" )
                    
                else:
                
                    # return None!
                    instance_OUT = None
                    
                    output_debug( "In " + me + ": no match for name: \"" + name_IN + "\"; so, returning None!" )
                    
                #-- END check to see if we create on no match. --#
                
            else:
            
                # Multiple matches.  Trouble.
                id_list = []
                for person in person_qs:
                
                    id_list.append( person.id )
                    
                #-- END loop over person matches. --#
                
                output_debug( "In " + me + ": multiple matches for name \"" + name_IN + "\" ( " + str( id_list ) + " ).  Returning None." )
                instance_OUT = None
            
            #-- END check count of persons returned. --#
            
        else:
        
            # No name passed in.  Nothing to return.
            output_debug( "In " + me + ": no name passed in, so returning None." )
            instance_OUT = None
        
        #-- END check for name string passed in. --#

        return instance_OUT
    
    #-- END method get_person_for_name() --#


    @classmethod
    def get_person_lookup_status( cls, person_IN ):
        
        # return reference
        status_OUT = ""
        
        # declare variables
        
        if ( person_IN is not None ):
        
            if ( ( person_IN.id ) and ( person_IN.id > 0 ) ):
            
                # there is an ID, so this is not a new record.
                status_OUT = cls.LOOKUP_STATUS_FOUND
                
            else:
            
                # Person returne, but no ID, so this is a new record - not found.
                status_OUT = cls.LOOKUP_STATUS_NEW
                
            #-- END check to see if ID present in record returned. --#
                
        else:
        
            # None - either multiple matches (eek!) or error.
            status_OUT = cls.LOOKUP_STATUS_NONE
        
        #-- END check to see if None. --#
    
        return status_OUT
        
    #-- END class method get_person_lookup_status() --#
    
    
    @classmethod
    def is_single_name_part( cls, name_string_IN ):
        
        '''
        Accepts a name string.  If name string just has a single word, returns
            True.  If not, returns False.  If error, returns None.  This works
            with nameparser.HumanName - it parses the name using HumanName, then
            checks to see if there is a value in first_name and the rest of the
            values are empty.  If that is the case, then single name part.  If
            more than one name field is populated, then not single name part.
        '''
        
        # return reference
        is_just_first_name_OUT = False
        
        # declare variables
        human_name = None
        first_name = ""
        other_name_part_list = []
        name_part = ""
        cleaned_name_part = ""
        other_name_part_string = ""
        
        # Make sure we have a string value
        if ( ( name_string_IN is not None ) and ( name_string_IN != "" ) ):
        
            # parse with HumanName
            human_name = HumanName( name_string_IN )
            
            # get first name
            first_name = human_name.first

            # put all the rest of the values into a list.
            other_name_part_list.append( human_name.title )
            other_name_part_list.append( human_name.middle )
            other_name_part_list.append( human_name.last )
            other_name_part_list.append( human_name.suffix )
            other_name_part_list.append( human_name.nickname )
            
            # clump the rest of the name parts together into a string.
            for name_part in other_name_part_list:
                
                # got anything?
                if ( ( name_part is not None ) and ( name_part != "" ) ):
                
                    # clean it up - strip white space.
                    cleaned_name_part = name_part.strip()
                    
                    # got anything now?
                    if ( cleaned_name_part != "" ):
                    
                        # yup.  Add to other_name_part_string.
                        other_name_part_string += cleaned_name_part

                    #-- END check to see if other name parts. --#

                #-- check to see if empty. --#
                
            #-- loop over other name parts. --#
            
            # anything in other_name_part_string?
            if ( ( other_name_part_string is not None ) and ( other_name_part_string != "" ) ):
            
                # yes.  Not just first name.
                is_just_first_name_OUT = False
                
            else:
            
                # no.  Just first name.
                is_just_first_name_OUT = True
            
            #-- END check to see if anything other than first name --#
                
        else:
        
            # None - No string passed in, so returning None.
            is_just_first_name_OUT = None
        
        #-- END check to see if None. --#
    
        return is_just_first_name_OUT
        
    #-- END class method is_single_name_part() --#

    @classmethod
    def look_up_person_from_name( cls,
                                  name_IN = "",
                                  parsed_name_IN = None,
                                  do_strict_match_IN = False, 
                                  do_partial_match_IN = False,
                                  qs_IN = None,
                                  *args,
                                  **kwargs ):
    
        '''
        This method accepts the full name of a person.  Uses NameParse object to
           parse name into prefix/title, first name, middle name(s), last name,
           and suffix.  Uses the result of the parse to lookup the person in
           the database by name part.  If do_strict_match_IN is True, looks for
           the exact combination of the name parts (so if a record has same
           first and last name, and a middle name, but the string passed in just
           has a middle name, no match).  If do_strict_match_IN is False, the
           above example would result in a match.  Returns QuerySet that results
           from filtering Person objects based on name string passed in.  If
           None found, returns empty QuerySet.  If error, returns None.
        preconditions: None.
        postconditions: Returns QuerySet that results from filtering Person
           objects based on name string passed in.  If None found, returns empty
           QuerySet.  If error, returns None.
        '''
        
        # return reference
        qs_OUT = None
        
        # declare variables.
        me = "look_up_person_from_name"
        parsed_name = None
        prefix = ""
        first = ""
        middle = ""
        last = ""
        suffix = ""
        nickname = ""
        strict_q = None
                
        # got a name or a pre-parsed name?
        if ( ( ( name_IN is not None ) and ( name_IN != "" ) )
            or ( parsed_name_IN is not None ) ):
        
            # Got a pre-parsed name?
            if ( parsed_name_IN is not None ):

                # yes. Use it.
                parsed_name = parsed_name_IN
                
            else:
            
                # no. Parse name_IN using HumanName class from nameparser.
                parsed_name = HumanName( name_IN )
                
            #-- END check to see if pre-parsed name. --#         
            
            # Use parsed values to build a search QuerySet.  First, get values.
            prefix = parsed_name.title
            first = parsed_name.first
            middle = parsed_name.middle
            last = parsed_name.last
            suffix = parsed_name.suffix
            nickname = parsed_name.nickname
            
            # build up queryset.
            if ( qs_IN is not None ):
            
                # got one passed in, start with it.
                qs_OUT = qs_IN
            
            else:
            
                # make a new one
                qs_OUT = cls.objects.all()
                
            #-- END check to see if QuerySet passed in. --#
            
            # got a prefix?
            if ( prefix ):
    
                # yes - allow partial match?
                if ( do_partial_match_IN == True ):
                
                    # yes.
                    qs_OUT = qs_OUT.filter( name_prefix__icontains = prefix )
                
                else:
                
                    # no.
                    qs_OUT = qs_OUT.filter( name_prefix__iexact = prefix )
                    
                #-- END check to see if we allow partial match. --#
                
            else:
            
                # are we being strict?
                if ( do_strict_match_IN == True ):
                
                    # yes - None or ""?
                    if ( ( prefix is None ) or ( prefix == "" ) ):
                    
                        # for None or "", match to either NULL OR "".
                        strict_q = Q( name_prefix__isnull = True ) | Q( name_prefix__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )
                        
                    else:
                    
                        # for anything else, what?  Stupid Python False values...
                        pass
                        
                    #-- END check to see what exact value of prefix is. --#
                
                #-- END check to see if strict. --#
            
            #-- END check for prefix --#
            
            # first name
            if ( first ):
    
                # allow partial match?
                if ( do_partial_match_IN == True ):
                
                    # yes.
                    qs_OUT = qs_OUT.filter( first_name__icontains = first )
                
                else:
                
                    # no.
                    qs_OUT = qs_OUT.filter( first_name__iexact = first )
                    
                #-- END check to see if we allow partial match. --#
                
            else:
            
                # are we being strict?
                if ( do_strict_match_IN == True ):
                
                    # yes - None or ""?
                    if ( ( first is None ) or ( first == "" ) ):
                    
                        # for None or "", match to either NULL OR "".
                        strict_q = Q( first_name__isnull = True ) | Q( first_name__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )
                        
                    else:
                    
                        # for anything else, what?  Stupid Python False values...
                        pass
                        
                    #-- END check to see what exact value of first is. --#
                
                #-- END check to see if strict. --#
            
            #-- END check for first name --#
            
            # middle name
            if ( middle ):
    
                # allow partial match?
                if ( do_partial_match_IN == True ):
                
                    # yes.
                    qs_OUT = qs_OUT.filter( middle_name__icontains = middle )
                
                else:
                
                    # no.
                    qs_OUT = qs_OUT.filter( middle_name__iexact = middle )
                    
                #-- END check to see if we allow partial match. --#
                
            else:
            
                # are we being strict?
                if ( do_strict_match_IN == True ):
                
                    # yes - None or ""?
                    if ( ( middle is None ) or ( middle == "" ) ):
                    
                        # for None or "", match to either NULL OR "".
                        strict_q = Q( middle_name__isnull = True ) | Q( middle_name__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )

                    else:
                    
                        # for anything else, what?  Stupid Python False values...
                        pass
                        
                    #-- END check to see what exact value of middle is. --#
                
                #-- END check to see if strict. --#
            
            #-- END check for middle name --#

            # last name
            if ( last ):
    
                # allow partial match?
                if ( do_partial_match_IN == True ):
                
                    # yes.
                    qs_OUT = qs_OUT.filter( last_name__icontains = last )
                
                else:
                
                    # no.
                    qs_OUT = qs_OUT.filter( last_name__iexact = last )
                    
                #-- END check to see if we allow partial match. --#
                
            else:
            
                # are we being strict?
                if ( do_strict_match_IN == True ):
                
                    # yes - None or ""?
                    if ( ( last is None ) or ( last == "" ) ):
                    
                        # for None or "", match to either NULL OR "".
                        strict_q = Q( last_name__isnull = True ) | Q( last_name__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )

                    else:
                    
                        # for anything else, what?  Stupid Python False values...
                        pass
                        
                    #-- END check to see what exact value of last is. --#
                
                #-- END check to see if strict. --#
            
            #-- END check for last name --#
            
            # suffix
            if ( suffix ):
    
                # allow partial match?
                if ( do_partial_match_IN == True ):
                
                    # yes.
                    qs_OUT = qs_OUT.filter( name_suffix__icontains = suffix )
                
                else:
                
                    # no.
                    qs_OUT = qs_OUT.filter( name_suffix__iexact = suffix )
                    
                #-- END check to see if we allow partial match. --#
                
            else:
            
                # are we being strict?
                if ( do_strict_match_IN == True ):
                
                    # yes - None or ""?
                    if ( ( suffix is None ) or ( suffix == "" ) ):
                    
                        # for None or "", match to either NULL OR "".
                        strict_q = Q( name_suffix__isnull = True ) | Q( name_suffix__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )

                    else:
                    
                        # for anything else, what?  Stupid Python False values...
                        pass
                        
                    #-- END check to see what exact value of suffix is. --#
                
                #-- END check to see if strict. --#
            
            #-- END suffix --#
            
            # nickname
            if ( nickname ):
    
                # allow partial match?
                if ( do_partial_match_IN == True ):
                
                    # yes.
                    qs_OUT = qs_OUT.filter( nickname__icontains = nickname )
                
                else:
                
                    # no.
                    qs_OUT = qs_OUT.filter( nickname__iexact = nickname )
                    
                #-- END check to see if we allow partial match. --#
                
            else:
            
                # are we being strict?
                if ( do_strict_match_IN == True ):
                
                    # yes - None or ""?
                    if ( ( nickname is None ) or ( nickname == "" ) ):
                    
                        # for None or "", match to either NULL OR "".
                        strict_q = Q( nickname__isnull = True ) | Q( nickname__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )

                    else:
                    
                        # for anything else, what?  Stupid Python False values...
                        pass
                        
                    #-- END check to see what exact value of nickname is. --#
                
                #-- END check to see if strict. --#
            
            #-- END nickname --#
            
        else:
        
            # No name, returning None
            output_debug( "In " + me + ": no name passed in, returning None." )
        
        #-- END check to see if we have a name. --#
        
        return qs_OUT
    
    #-- END static method look_up_person_from_name() --#
    

    @classmethod
    def standardize_name_part( cls, name_part_IN, remove_periods_IN = False ):
        
        '''
        Accepts string name part, does the following to standardize it, in this
        order:
           - removes any commas.
           - strips white space from the beginning and end.
           - More to come?
           
        preconditions: None.

        postconditions: None.
        '''
        
        # return reference
        name_part_OUT = ""
        
        # declare variables
        working_string = ""
        
        # start with name part passed in.
        working_string = name_part_IN
        
        # first, check to see if anything passed in.
        if ( ( working_string is not None ) and ( working_string != "" ) ):
        
            # remove commas.
            working_string = working_string.replace( ",", "" )
            
            # remove periods as well?
            if ( remove_periods_IN == True ):
            
                # yes.
                working_string = working_string.replace( ".", "" )
            
            #-- END check to see if remove periods --#
            
            # strip white space.
            working_string = working_string.strip()

        #-- END check to see if anything passed in. --#

        # return working_string.
        name_part_OUT = working_string

        return name_part_OUT
        
    #-- END method standardize_name_part() --#
        
        
    #----------------------------------------------------------------------
    # ! instance methods
    #----------------------------------------------------------------------

    def __init__( self, *args, **kwargs ):
        
        # call parent __init()__ first.
        super( Abstract_Person, self ).__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):
 
        # return reference
        string_OUT = ''
        
        # declare variables
        string_list = []
 
        if ( self.id ):
        
            string_OUT = str( self.id ) + " - "
            
        #-- END check to see if ID --#
                
        string_OUT += self.last_name + ', ' + self.first_name
        
        # middle name?
        if ( self.middle_name ):
        
            string_OUT += " " + self.middle_name
            
        #-- END middle name check --#

        if ( ( self.title ) or ( self.organization_string ) or ( self.capture_method ) ):
        
            string_OUT += " ( "
        
            string_list = []
        
            if ( self.title ):
            
                # add title to list
                string_list.append( "title = " + self.title )
                
            #-- END check for title --#
            
            if ( self.organization_string ):
            
                # add title to list
                string_list.append( "organization = " + self.organization_string )
                
            #-- END check for title --#
            
            if ( self.capture_method ):
            
                # add capture method to the list.
                string_list.append( "capture_method = " + self.capture_method )
                
            #-- END check for capture_method --#
            
            string_OUT += "; ".join( string_list )

            string_OUT += " )"
            
        #-- END check to see if we have a title, organization, or capture_method. --#
 
        return string_OUT

    #-- END method __str__() --#


    def get_name_string( self ):
        
        '''
        Converts current person's name into a HumanName, then call the str()
           function on that name to convert it to a string.  Returns that
           string.
        '''
        
        # return reference
        value_OUT = ""
        
        # declare variables
        my_HumanName = None
        
        # get human name for this instance.
        my_HumanName = self.to_HumanName()
        
        # if nickname, remove it so it doesn't get output at the end of the
        #    string like a last name.
        if ( my_HumanName.nickname ):
        
            # yes - get rid of it.
            my_HumanName.nickname = ""
            
        #-- END check to see if nickname. --#
        
        # convert that to a string.
        value_OUT = str( my_HumanName )
        
        return value_OUT
        
    #-- END method get_name_string() --#


    def standardize_name_parts( self, remove_periods_IN = False ):
        
        '''
        This method looks at each part of a name and for each, calls the method
           standardize_name_part() to do the following to standardize it, in this
           order:
           - removes any commas.
           - strips white space from the beginning and end.
           - More to come?  Best list is in standardize_name_part()
           
        preconditions: None.

        postconditions: if needed, name parts in instance are updated to be
           standardized.  Instance is not saved.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        me = "standardize_name_parts"
        
        # standardize name parts.
        if ( self.name_prefix ):
    
            self.name_prefix = self.standardize_name_part( self.name_prefix, remove_periods_IN = remove_periods_IN )
            
        #-- END check to see if name_prefix.
        
        if ( self.first_name ):
    
            self.first_name = self.standardize_name_part( self.first_name, remove_periods_IN = remove_periods_IN )
            
        #-- END check to see if first_name.
        
        if ( self.middle_name ):
    
            self.middle_name = self.standardize_name_part( self.middle_name, remove_periods_IN = remove_periods_IN )
            
        #-- END check to see if middle_name.
        
        if ( self.last_name ):
    
            self.last_name = self.standardize_name_part( self.last_name, remove_periods_IN = remove_periods_IN )
            
        #-- END check to see if last_name.
        
        if ( self.name_suffix ):
    
            self.name_suffix = self.standardize_name_part( self.name_suffix, remove_periods_IN = remove_periods_IN )
            
        #-- END check to see if name_suffix.
        
        if ( self.nickname ):
    
            self.nickname = self.standardize_name_part( self.nickname, remove_periods_IN = remove_periods_IN )
            
        #-- END check to see if nickname.
        
        return instance_OUT
        
    #-- END method clean_up_name_parts() --#


    def save( self, *args, **kwargs ):
        
        '''
        Overridden save() method that automatically creates a full name string
           for a person in case one is not specified.

        Note: looks like child classes don't have to override save method.
        '''
        
        # declare variables.
        name_HumanName = None
        generated_full_name_string = ""
        
        # standardize name parts
        self.standardize_name_parts()
        
        # Make HumanName() instance from this Person's name parts.
        name_HumanName = self.to_HumanName()
            
        # use it to update the full_name_string.
        self.full_name_string = StringHelper.object_to_unicode_string( name_HumanName )

        # call parent save() method.
        super( Abstract_Person, self ).save( *args, **kwargs )
        
    #-- END method save() --#


    def set_name( self,
                  name_IN,
                  parsed_name_IN = None,
                  remove_periods_IN = False,
                  *args,
                  **kwargs ):
    
        '''
        This method accepts the full name of a person.  Uses NameParse object to
           parse name into prefix/title, first name, middle name(s), last name,
           and suffix.  Stores resulting parsed values in this instance, and also
           stores the pickled name object and the full name string.
        preconditions: None.
        postconditions: Updates values in this instance with values parsed out of
           name passed in.
        '''
        
        # declare variables.
        me = "set_name"
        parsed_name = None
        prefix = ""
        first = ""
        middle = ""
        last = ""
        suffix = ""
        nickname = ""
        standardized_hn = None
                
        # No name, returning None
        output_debug( "In " + me + ": storing name: " + str( name_IN ) )

        # got a name?
        if ( ( name_IN is not None ) and ( name_IN != "" ) ):
        
            # yes.  Store original name string
            self.original_name_string = name_IN
            
            # was parsed name passed in?
            if ( parsed_name_IN is not None ):

                # used pre-parsed name.
                parsed_name = parsed_name_IN

                # No name, returning None
                output_debug( "In " + me + ": using pre-parsed name: " + str( parsed_name_IN ) )

            else:

                # Parse it using HumanName class from nameparser.
                parsed_name = HumanName( name_IN )
                
            #-- END check to see if name already parsed. --#
            
            # Use parsed values to build a search QuerySet.  First, get values.
            prefix = parsed_name.title
            first = parsed_name.first
            middle = parsed_name.middle
            last = parsed_name.last
            suffix = parsed_name.suffix
            nickname = parsed_name.nickname
            
            # got a prefix?
            if ( prefix ):
    
                # set value
                self.name_prefix = prefix
                
            #-- END check for prefix --#
            
            # first name
            if ( first ):
    
                # set value
                self.first_name = first
                
            #-- END check for first name --#
            
            # middle name
            if ( middle ):
    
                # set value
                self.middle_name = middle
                
            #-- END check for middle name --#

            # last name
            if ( last ):
    
                # set value
                self.last_name = last
                
            #-- END check for last name --#
            
            # suffix
            if ( suffix ):
    
                # set value
                self.name_suffix = suffix
                
            #-- END suffix --#
            
            # nickname
            if ( nickname ):
    
                # set value
                self.nickname = nickname
                
            #-- END nickname --#
            
            # standardize name parts
            self.standardize_name_parts( remove_periods_IN = remove_periods_IN )
            
            # Finally, store the full name string (and the pickled object?).
            standardized_hn = self.to_HumanName()

            # convert name to string - different in python 2 and 3.
            self.full_name_string = StringHelper.object_to_unicode_string( standardized_hn )

            # not pickling at the moment.
            #self.nameparser_pickled = pickle.dumps( standardized_hn )
            
        else:
        
            # No name, returning None
            output_debug( "In " + me + ": no name passed in, returning None." )
        
        #-- END check to see if we have a name. --#
        
    #-- END method set_name() --#
    

    def to_HumanName( self ):
        
        '''
        This method creates a nameparser HumanName() object instance, then uses
           the values from this Abstract_Person instance to populate it.  Returns
           the HumanName instance.
           
        preconditions: None.
        postconditions: None.
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        me = "to_HumanName"
        
        # make HumanString instance.
        instance_OUT = HumanName()

        # Use nested values to populate HumanName.
        if ( self.name_prefix ):
    
            instance_OUT.title = self.name_prefix
            
        #-- END check to see if name_prefix.
        
        if ( self.first_name ):
    
            instance_OUT.first = self.first_name
            
        #-- END check to see if first_name.
        
        if ( self.middle_name ):
    
            instance_OUT.middle = self.middle_name
            
        #-- END check to see if middle_name.
        
        if ( self.last_name ):
    
            instance_OUT.last = self.last_name
            
        #-- END check to see if last_name.
        
        if ( self.name_suffix ):
    
            instance_OUT.suffix = self.name_suffix
            
        #-- END check to see if name_suffix.
        
        if ( self.nickname ):
    
            instance_OUT.nickname = self.nickname
            
        #-- END check to see if nickname.
        
        return instance_OUT
        
    #-- END method to_HumanName() --#


#== END abstract Abstract_Person Model ========================================#
