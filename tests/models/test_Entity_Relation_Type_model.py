"""
This file contains tests of the context_text Person model (and by extension
   Abstract_Person).

Functions tested:
- Person.look_up_person_from_name()
"""

# python imports
import datetime
import json

# import six
import six

# django imports
import django.test

# context_text imports
from context.models import Entity_Relation_Type
from context.tests.test_helper import TestHelper


class Entity_Relation_TypeModelTest( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ----> Constants-ish
    #----------------------------------------------------------------------------


    # DEBUG
    DEBUG = False

    # CLASS NAME
    CLASS_NAME = "Entity_Relation_TypeModelTest"


    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # ! ----> instance methods
    #----------------------------------------------------------------------------


    def setUp( self ):
        
        """
        setup tasks.  Call function that we'll re-use.
        """

        # call TestHelper.standardSetUp()
        TestHelper.standardSetUp( self )

    #-- END function setUp() --#
        

    def test_setup( self ):

        """
        Tests whether there were errors in setup.
        """
        
        # declare variables
        me = "test_setup"
        error_count = -1
        error_message = ""
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # get setup error count
        setup_error_count = self.setup_error_count
        
        # should be 0
        error_message = ";".join( self.setup_error_list )
        self.assertEqual( setup_error_count, 0, msg = error_message )
        
    #-- END test method test_django_config_installed() --#


    def test_get_type_for_slug( self ):

        '''
        Things to test passing to the method:

            get_type_for_slug( self, slug_IN ):
        '''

        # declare variables
        me = "get_type_for_slug"
        test_slug = None
        type_instance = None
                
        # debug
        debug_flag = self.DEBUG

        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # ! ----> try a slug that should have a match
        test_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_MENTIONED
        
        # look it up.
        type_instance = Entity_Relation_Type.get_type_for_slug( test_slug )
        
        # should not be None
        error_string = "None returned getting type for slug {}, should have found a match.".format( test_slug )
        self.assertIsNotNone( type_instance, msg = error_string )

        # ! ----> try another slug that should have a match
        test_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_NEWSPAPER_SOURCE
        
        # look it up.
        type_instance = Entity_Relation_Type.get_type_for_slug( test_slug )
        
        # should not be None
        error_string = "None returned getting type for slug {}, should have found a match.".format( test_slug )
        self.assertIsNotNone( type_instance, msg = error_string )

        # ! ----> try a slug that should not have a match
        test_slug = TestHelper.ENTITY_TRAIT_NAME_GIBBERISH
        
        # look it up.
        type_instance = Entity_Relation_Type.get_type_for_slug( test_slug )
        
        # should not be None
        error_string = "Type {} returned for slug {}, should have been None.".format( type_instance, test_slug )
        self.assertIsNone( type_instance, msg = error_string )
                
    #-- END test method test_get_type_for_slug() --#


#-- END test class Entity_Relation_TypeModelTest --#
