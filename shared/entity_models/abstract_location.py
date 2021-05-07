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
from context.shared.entity_models import output_debug
from context.shared.entity_models import output_log_message


#================================================================================
# ! ==> Abstract Models
#================================================================================


#-------------------------------------------------------------------------------
# ! --------> Abstract Human Models
#-------------------------------------------------------------------------------


# Locations
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
        super().__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''
        delimiter = ''

        # see what we can place in the string.
        if ( self.id is not None ):

            string_OUT = "{} - ".format( self.id )

        #-- END check to see if ID --#

        if ( ( self.name is not None ) and ( self.name != '' ) ):

            string_OUT += '"{}"'.format( self.name )
            delimiter = ', '

        #-- END check to see if name --#

        if ( self.address != '' ):
            string_OUT += delimiter + self.address
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

    #-- END method __str__() --#

#= End Abstract_Location Model ===========================================================
