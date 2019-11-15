"""
This file contains tests of the context_text Person model (and by extension
   Abstract_Person).

Functions tested:
- Person.look_up_person_from_name()
"""

# import six
import six

# django imports
import django.test

# context_text imports
from context.models import Entity_Identifier_Type
from context.tests.test_helper import TestHelper


class Entity_Identifier_TypeModelTest( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ----> Constants-ish
    #----------------------------------------------------------------------------


    # CLASS NAME
    CLASS_NAME = "Entity_Identifier_TypeModelTest"

    # identifier type names
    TYPE_NAME_ARTICLE_NEWSBANK_ID = TestHelper.ID_TYPE_NAME_ARTICLE_NEWSBANK_ID
    TYPE_NAME_ARTICLE_SOURCENET_ID = TestHelper.ID_TYPE_NAME_ARTICLE_SOURCENET_ID
    TYPE_NAME_PERSON_OPEN_CALAIS_UUID = TestHelper.ID_TYPE_NAME_PERSON_OPEN_CALAIS_UUID
    TYPE_NAME_PERSON_SOURCENET_ID = TestHelper.ID_TYPE_NAME_PERSON_SOURCENET_ID
    
    # map of identifier type names to test IDs
    TYPE_NAME_TO_ID_MAP = TestHelper.ID_TYPE_NAME_TO_ID_MAP


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
        
        print( '\n====> In {}.{}'.format( self.CLASS_NAME, me ) )
        
        # get setup error count
        setup_error_count = self.setup_error_count
        
        # should be 0
        error_message = ";".join( self.setup_error_list )
        self.assertEqual( setup_error_count, 0, msg = error_message )
        
    #-- END test method test_django_config_installed() --#


    def test_get_type_for_name( self ):
        
        # declare variables
        me = "test_get_type_for_name"
        type_name_string = ""
        type_id = None
        should_be = -1
        error_string = ""
        test_type = None
        test_type_id = None
        match_count = -1
        
        print( '\n====> In {}.{}'.format( self.CLASS_NAME, me ) )
        
        # loop over name to ID map
        for type_name_string, type_id in six.iteritems( self.TYPE_NAME_TO_ID_MAP ):

            # try a lookup, compare ID of result to expected ID.        
            should_be = type_id
            test_type = Entity_Identifier_Type.get_type_for_name( type_name_string )
            test_type_id = test_type.id
            error_string = "{} --> type ID {} should = {}".format( type_name_string, test_type_id, should_be )
            self.assertEqual( test_type_id, should_be, msg = error_string )
            
        #-- END loop over valid types --#

        #----------------------------------------------------------------------#
        # Type does not exist for name.
        #----------------------------------------------------------------------#

        type_name_string = "calliope_tree_frog"
        test_type = Entity_Identifier_Type.get_type_for_name( type_name_string )
        error_string = "Entity_Identifier_Type for name_string {} should have returned None, returned instead: {}".format( type_name_string, test_type )
        self.assertIsNone( test_type, msg = error_string )

    #-- END test method test_get_type_for_name() --#

#-- END test class Entity_Identifier_TypeModelTest --#
