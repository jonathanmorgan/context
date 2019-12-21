from __future__ import unicode_literals

'''
Copyright 2010-2019 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context.

context is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context. If not, see http://www.gnu.org/licenses/.
'''


#===============================================================================
# imports (in alphabetical order by package, then by name)
#===============================================================================

# python libraries
import os

# import six
import six

# Django imports
from django.contrib.auth.models import User
from django.core.management import call_command

# import basic django configuration application.
from django_config.models import Config_Property

# python_utilities - logging
from python_utilities.exceptions.exception_helper import ExceptionHelper
from python_utilities.logging.logging_helper import LoggingHelper

# context imports
from context.export.network.filter_spec import FilterSpec
from context.export.network.network_data_request import NetworkDataRequest
import context.tests.test_helper


#===============================================================================
# Shared variables and functions
#===============================================================================


#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class TestHelper( context.tests.test_helper.TestHelper ):

    
    #---------------------------------------------------------------------------
    # ! ==> CONSTANTS-ish
    #---------------------------------------------------------------------------


    # JSON files
    FILE_PATH_BASE_FOLDER = "{}/".format( os.path.dirname( os.path.realpath( __file__ ) ) )
    FILE_PATH_NETWORK_DATA_REQUEST_BASIC = "{}network_data_request_basic.json".format( FILE_PATH_BASE_FOLDER )
    FILE_PATH_NETWORK_DATA_REQUEST_BASIC_2 = "{}network_data_request_basic_2.json".format( FILE_PATH_BASE_FOLDER )    
    FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_ID_FILTER = "{}network_data_request_with_entity_id_filter.json".format( FILE_PATH_BASE_FOLDER )
    FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_SELECTION = "{}network_data_request_with_entity_select.json".format( FILE_PATH_BASE_FOLDER )
    FILE_PATH_LIST = []
    FILE_PATH_LIST.append( FILE_PATH_NETWORK_DATA_REQUEST_BASIC )
    #FILE_PATH_LIST.append( FILE_PATH_NETWORK_DATA_REQUEST_BASIC_2 )
    FILE_PATH_LIST.append( FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_ID_FILTER )
    FILE_PATH_LIST.append( FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_SELECTION )
    

    #----------------------------------------------------------------------------
    # ! ==> Class variables
    # - overriden by __init__() per instance if same names, but if not set
    #     there, shared!
    #----------------------------------------------------------------------------

    
    DEBUG = True
        

    #-----------------------------------------------------------------------------
    # ! ==> class methods
    #-----------------------------------------------------------------------------


    @classmethod
    def load_basic( cls ):
        
        # return reference
        instance_OUT = None
        
        # create instance
        instance_OUT = NetworkDataRequest()
        
        # load basic.
        instance_OUT.load_network_data_request_json_file( cls.FILE_PATH_NETWORK_DATA_REQUEST_BASIC )
        
        return instance_OUT
        
    #-- END class method load_basic() --#


    @classmethod
    def load_basic_2( cls ):
        
        # return reference
        instance_OUT = None
        
        # create instance
        instance_OUT = NetworkDataRequest()
        
        # load basic.
        instance_OUT.load_network_data_request_json_file( cls.FILE_PATH_NETWORK_DATA_REQUEST_BASIC_2 )
        
        return instance_OUT
        
    #-- END class method load_basic() --#


    @classmethod
    def load_with_entity_id_filter( cls ):
        
        # return reference
        instance_OUT = None
        
        # create instance
        instance_OUT = NetworkDataRequest()
        
        # load basic.
        instance_OUT.load_network_data_request_json_file( cls.FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_ID_FILTER )
        
        return instance_OUT
        
    #-- END class method load_with_entity_id_filter() --#


    @classmethod
    def load_with_entity_selection( cls ):
        
        # return reference
        instance_OUT = None
        
        # create instance
        instance_OUT = NetworkDataRequest()
        
        # load basic.
        instance_OUT.load_network_data_request_json_file( cls.FILE_PATH_NETWORK_DATA_REQUEST_WITH_ENTITY_SELECTION )
        
        return instance_OUT
        
    #-- END class method load_with_entity_selection() --#


    #---------------------------------------------------------------------------
    # ! ==> overridden built-in methods
    #---------------------------------------------------------------------------


    def __init__( self ):

        # call parent's __init__()
        super( TestHelper, self ).__init__()

    #-- END method __init__() --#


    #----------------------------------------------------------------------------
    # ! ==> instance methods, in alphabetical order
    #----------------------------------------------------------------------------


#-- END class TestHelper --#