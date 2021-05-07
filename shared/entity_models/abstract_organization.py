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


#================================================================================
# ! ==> Abstract Models
#================================================================================


#-------------------------------------------------------------------------------
# ! --------> Abstract Human Models
#-------------------------------------------------------------------------------


# AbstractOrganization model
class Abstract_Organization( Abstract_Entity_Container ):

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

            string_OUT += "{}".format( self.name )
            delimiter = ', '

        #-- END check to see if name --#

        return string_OUT

    #-- END method __str_() --#

#= End Abstract_Organization Model ======================================================
