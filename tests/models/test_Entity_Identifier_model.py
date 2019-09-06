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
from context.models import Entity
from context.models import Entity_Identifier
from context.models import Entity_Identifier_Type
from context.tests.test_helper import TestHelper


class Entity_IdentifierModelTest( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ----> Constants-ish
    #----------------------------------------------------------------------------


    # CLASS NAME
    CLASS_NAME = "Entity_IdentifierModelTest"

    # identifier type names
    TYPE_NAME_ARTICLE_NEWSBANK_ID = "article_newsbank_id"
    TYPE_NAME_ARTICLE_SOURCENET_ID = "article_sourcenet_id"
    TYPE_NAME_PERSON_OPEN_CALAIS_UUID = "person_open_calais_uuid"    
    TYPE_NAME_PERSON_SOURCENET_ID = "person_sourcenet_id"
    TYPE_NAME_DOES_NOT_EXIST = "calliope_tree_frog"
    
    # map of identifier type names to test IDs
    TYPE_NAME_TO_ID_MAP = {}
    TYPE_NAME_TO_ID_MAP[ TYPE_NAME_PERSON_SOURCENET_ID ] = 1
    TYPE_NAME_TO_ID_MAP[ TYPE_NAME_PERSON_OPEN_CALAIS_UUID ] = 2
    TYPE_NAME_TO_ID_MAP[ TYPE_NAME_ARTICLE_SOURCENET_ID ] = 3
    TYPE_NAME_TO_ID_MAP[ TYPE_NAME_ARTICLE_NEWSBANK_ID ] = 4
    
    # Test Entity information
    TEST_ENTITY_NAME = "calliope"
    
    # Test Entity_Identifier default information
    TEST_ENTITY_IDENTIFIER_NAME = "calliope_type"
    TEST_ENTITY_IDENTIFIER_UUID = "123456"
    TEST_ENTITY_IDENTIFIER_ID_TYPE = "made-up"
    TEST_ENTITY_IDENTIFIER_SOURCE = "my_brain"
    TEST_ENTITY_IDENTIFIER_NOTE = "default initialization notes"


    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------


    @classmethod
    def create_test_entity( cls ):
        
        # return reference
        instance_OUT = None
        
        # declare variables
        entity_instance = None
        
        # create entity
        entity_instance = Entity()
        
        # set some values
        entity_instance.name = cls.TEST_ENTITY_NAME
        entity_instance.save()
        
        # return it
        instance_OUT = entity_instance
        return instance_OUT

    #-- END method create_test_entity() --#


    @classmethod
    def create_test_entity_identifier( cls, entity_instance_IN ):
        
        # return reference
        instance_OUT = None
        
        # declare variables
        identifier_instance = None
        
        # create entity
        identifier_instance = Entity_Identifier()
        
        # set some values
        identifier_instance.name = cls.TEST_ENTITY_IDENTIFIER_NAME
        identifier_instance.uuid = cls.TEST_ENTITY_IDENTIFIER_UUID
        identifier_instance.id_type = cls.TEST_ENTITY_IDENTIFIER_ID_TYPE
        identifier_instance.source = cls.TEST_ENTITY_IDENTIFIER_SOURCE
        identifier_instance.note = cls.TEST_ENTITY_IDENTIFIER_NOTE
        identifier_instance.entity = entity_instance_IN
        identifier_instance.save()
        
        # return it
        instance_OUT = identifier_instance
        return instance_OUT

    #-- END method create_test_entity_identifier() --#


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
        
        print( '====> In {}.{}'.format( self.CLASS_NAME, me ) )
        
        # get setup error count
        setup_error_count = self.setup_error_count
        
        # should be 0
        error_message = ";".join( self.setup_error_list )
        self.assertEqual( setup_error_count, 0, msg = error_message )
        
    #-- END test method test_django_config_installed() --#


    def test_set_entity_identifier_type( self ):
        
        # declare variables
        me = "test_set_entity_identifier_type"
        entity_instance = None
        identifier_instance = None
        type_instance = None
        
        # declare variables - lookup type.
        type_name_string = ""
        type_id = None
        should_be = -1
        error_string = ""
        test_type = None
        test_type_id = None
        
        # declare variables - evaluate set.
        stored_type = None
        stored_type_id = None
        stored_name = None
        stored_source = None
        test_name = None
        test_source = None
        
        print( '====> In {}.{}'.format( self.CLASS_NAME, me ) )
        
        # create Entity
        entity_instance = self.create_test_entity()
        
        # create an Entity_Identifier instance
        identifier_instance = self.create_test_entity_identifier( entity_instance )
        
        # store None, telling it not to update.
        stored_type = identifier_instance.set_entity_identifier_type( None, do_use_to_update_fields_IN = False )
        error_string = "Storing None should have returned None, returned instead: {}".format( stored_type )
        self.assertIsNone( stored_type, msg = error_string )

        # store None, telling it not to update.
        stored_type = identifier_instance.set_entity_identifier_type( None, do_use_to_update_fields_IN = True )
        error_string = "Storing None should have returned None, returned instead: {}".format( stored_type )
        self.assertIsNone( stored_type, msg = error_string )
            
        # loop over name to ID map
        for type_name_string, type_id in six.iteritems( self.TYPE_NAME_TO_ID_MAP ):

            # try a lookup, compare ID of result to expected ID.        
            should_be = type_id
            type_instance = Entity_Identifier_Type.get_type_for_name( type_name_string )
            test_type_id = type_instance.id
            test_name = type_instance.name
            test_source = type_instance.source
            error_string = "{} --> type ID {} should = {}".format( type_name_string, test_type_id, should_be )
            self.assertEqual( test_type_id, should_be, msg = error_string )
            
            # store the type, telling it not to update.
            stored_type = identifier_instance.set_entity_identifier_type( type_instance, do_use_to_update_fields_IN = False )
            stored_type_id = stored_type.id
            stored_name = identifier_instance.name
            stored_source = identifier_instance.source
            
            # stored type and test type should have same ID.
            should_be = test_type_id
            error_string = "stored type ID {} should = {}".format( stored_type_id, should_be )
            self.assertEqual( stored_type_id, should_be, msg = error_string )

            # name should not be equal
            should_not_be = test_name
            error_string = "stored name \"{}\" should != \"{}\"".format( stored_name, should_not_be )
            self.assertNotEqual( stored_name, should_not_be, msg = error_string )
            
            # source should not be equal
            should_not_be = test_source
            error_string = "stored source \"{}\" should != \"{}\"".format( stored_source, should_not_be )
            self.assertNotEqual( stored_source, should_not_be, msg = error_string )
            
            # store the type, telling it to update.
            stored_type = identifier_instance.set_entity_identifier_type( type_instance, do_use_to_update_fields_IN = True )
            stored_type_id = stored_type.id
            stored_name = identifier_instance.name
            stored_source = identifier_instance.source
            
            # stored type and test type should have same ID.
            should_be = test_type_id
            error_string = "stored type ID {} should = {}".format( stored_type_id, should_be )
            self.assertEqual( stored_type_id, should_be, msg = error_string )

            # name should be equal
            should_be = test_name
            error_string = "stored name \"{}\" should = \"{}\"".format( stored_name, should_be )
            self.assertEqual( stored_name, should_be, msg = error_string )
            
            # source should be equal
            should_be = test_source
            error_string = "stored source \"{}\" should = \"{}\"".format( stored_source, should_be )
            self.assertEqual( stored_source, should_be, msg = error_string )
            
        #-- END loop over valid types --#

    #-- END test method test_set_entity_identifier_type() --#
    

    def test_set_identifier_type_from_name( self ):
        
        # declare variables
        me = "test_set_identifier_type_from_name"
        entity_instance = None
        identifier_instance = None
        type_instance = None
        
        # declare variables - lookup type.
        type_name_string = ""
        type_id = None
        should_be = -1
        error_string = ""
        test_type = None
        test_type_id = None
        
        # declare variables - evaluate set.
        stored_type = None
        stored_type_id = None
        stored_name = None
        stored_source = None
        test_name = None
        test_source = None
        
        print( '====> In {}.{}'.format( self.CLASS_NAME, me ) )
        
        # create Entity
        entity_instance = self.create_test_entity()
        
        # create an Entity_Identifier instance
        identifier_instance = self.create_test_entity_identifier( entity_instance )
        
        # store DNE name, telling it not to update.
        stored_type = identifier_instance.set_identifier_type_from_name( self.TYPE_NAME_DOES_NOT_EXIST, do_use_to_update_fields_IN = False )
        error_string = "Storing type name that isn't in database should have returned None, returned instead: {}".format( stored_type )
        self.assertIsNone( stored_type, msg = error_string )

        # store DNE name, telling it not to update.
        stored_type = identifier_instance.set_identifier_type_from_name( self.TYPE_NAME_DOES_NOT_EXIST, do_use_to_update_fields_IN = True )
        error_string = "Storing type name that isn't in database should have returned None, returned instead: {}".format( stored_type )
        self.assertIsNone( stored_type, msg = error_string )
            
        # loop over name to ID map
        for type_name_string, type_id in six.iteritems( self.TYPE_NAME_TO_ID_MAP ):

            # try a lookup, compare ID of result to expected ID.        
            should_be = type_id
            type_instance = Entity_Identifier_Type.get_type_for_name( type_name_string )
            test_type_id = type_instance.id
            test_name = type_instance.name
            test_source = type_instance.source
            error_string = "{} --> type ID {} should = {}".format( type_name_string, test_type_id, should_be )
            self.assertEqual( test_type_id, should_be, msg = error_string )

            # store the type, telling it not to update.
            stored_type = identifier_instance.set_identifier_type_from_name( type_name_string, do_use_to_update_fields_IN = False )
            stored_type_id = stored_type.id
            stored_name = identifier_instance.name
            stored_source = identifier_instance.source
            
            # stored type and test type should have same ID.
            should_be = test_type_id
            error_string = "stored type ID {} should = {}".format( stored_type_id, should_be )
            self.assertEqual( stored_type_id, should_be, msg = error_string )

            # name should not be equal
            should_not_be = test_name
            error_string = "stored name \"{}\" should != \"{}\"".format( stored_name, should_not_be )
            self.assertNotEqual( stored_name, should_not_be, msg = error_string )
            
            # source should not be equal
            should_not_be = test_source
            error_string = "stored source \"{}\" should != \"{}\"".format( stored_source, should_not_be )
            self.assertNotEqual( stored_source, should_not_be, msg = error_string )
            
            # store the type, telling it to update.
            stored_type = identifier_instance.set_identifier_type_from_name( type_name_string, do_use_to_update_fields_IN = True )
            stored_type_id = stored_type.id
            stored_name = identifier_instance.name
            stored_source = identifier_instance.source
            
            # stored type and test type should have same ID.
            should_be = test_type_id
            error_string = "stored type ID {} should = {}".format( stored_type_id, should_be )
            self.assertEqual( stored_type_id, should_be, msg = error_string )

            # name should be equal
            should_be = test_name
            error_string = "stored name \"{}\" should = \"{}\"".format( stored_name, should_be )
            self.assertEqual( stored_name, should_be, msg = error_string )
            
            # source should be equal
            should_be = test_source
            error_string = "stored source \"{}\" should = \"{}\"".format( stored_source, should_be )
            self.assertEqual( stored_source, should_be, msg = error_string )
            
        #-- END loop over valid types --#

    #-- END test method test_set_identifier_type_from_name() --#


#-- END test class Entity_Identifier_TypeModelTest --#
