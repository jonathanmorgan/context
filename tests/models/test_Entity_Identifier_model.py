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


    # DEBUG
    DEBUG = False

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
    
    # Entity_Identifier
    ENTITY_ID_UUID_NO_MATCH = "calliope_1234567890"
    ENTITY_ID_NAME_NO_MATCH = "hunterlane"
    ENTITY_ID_SOURCE_NO_MATCH = "chiquita_brain_fuel"
    ENTITY_ID_ID_TYPE_NO_MATCH = "shady_salads"
    ENTITY_ID_NOTES_NO_MATCH = "these notes should not match."


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
        
        print( '\n====> In {}.{}'.format( self.CLASS_NAME, me ) )
        
        # get setup error count
        setup_error_count = self.setup_error_count
        
        # should be 0
        error_message = ";".join( self.setup_error_list )
        self.assertEqual( setup_error_count, 0, msg = error_message )
        
    #-- END test method test_django_config_installed() --#


    def test_filter_identifiers( self ):
        
        '''
        Test using the default test entity and entity identifier.  Identifier
            has the following values:
            - # Test Entity_Identifier default information
            - TEST_ENTITY_IDENTIFIER_NAME = "calliope_type"
            - TEST_ENTITY_IDENTIFIER_UUID = "123456"
            - TEST_ENTITY_IDENTIFIER_ID_TYPE = "made-up"
            - TEST_ENTITY_IDENTIFIER_SOURCE = "my_brain"
            - TEST_ENTITY_IDENTIFIER_NOTE = "default initialization notes"
        '''
        
        # declare variables
        me = "test_filter_identifiers"
        my_entity = None
        my_entity_id = None
        my_entity_identifier = None
        result_qs = None
        result_entity = None
        result_entity_id = None
        result_qs = None
        result_count = None
        bad_identifier_type = None
        
        # declare variables - Entity_Identifier info.
        my_identifier_id = None
        my_identifier_name = None
        my_identifier_uuid = None
        my_identifier_id_type = None
        my_identifier_source = None
        my_identifier_entity_id_type = None
        my_identifier_notes = None        
        
        # declare variables - test values
        test_id_uuid = None
        test_id_name = None
        test_id_source = None
        test_id_entity_id_type = None
        test_id_id_type = None
        test_id_notes = None
        
        
        # debug
        debug_flag = self.DEBUG
        eiqs = None
        
        # create test entity, with test identifier.
        my_entity = TestHelper.create_test_entity()
        my_entity_id = my_entity.id
        
        # create identifier
        my_entity_identifier = TestHelper.create_test_entity_identifier( my_entity )
        
        # set type and update identifier from it (must then save())
        my_identifier_type = my_entity_identifier.set_identifier_type_from_name( self.TYPE_NAME_PERSON_SOURCENET_ID, do_use_to_update_fields_IN = True )
        my_entity_identifier.save()

        # identifier details
        my_identifier_id = my_entity_identifier.id
        my_identifier_uuid = my_entity_identifier.uuid
        my_identifier_name = my_entity_identifier.name
        my_identifier_source = my_entity_identifier.source
        my_identifier_id_type = my_entity_identifier.id_type
        my_identifier_entity_id_type = my_entity_identifier.entity_identifier_type
        my_identifier_notes = my_entity_identifier.notes
        
        print( '\n====> In {}.{}'.format( self.CLASS_NAME, me ) )
        print( "my_entity_identifier: {}".format( my_entity_identifier ) )

        #======================================================================#
        # ! ==> DEBUG - try to get Entity  - manual test
        #======================================================================#
        
        # DEBUG
        if ( debug_flag == True ):

            eiqs = Entity_Identifier.objects.all()
            print( "- ALL record count: {}".format( eiqs.count() ) )
            
            for entity_id in eiqs:
                
                print( "    - {}".format( entity_id ) )
                
            #-- END loop over entity ids. --#
            
            eiqs = eiqs.filter( uuid = my_identifier_uuid )
            print( "- after UUID filer - record count: {}".format( eiqs.count() ) )
            
            eiqs = eiqs.filter( name = my_identifier_name )
            print( "- after name filter -  record count: {}".format( eiqs.count() ) )
            
            eiqs = eiqs.filter( source = my_identifier_source )
            print( "- after source filter - record count: {}".format( eiqs.count() ) )
            
            eiqs = eiqs.filter( entity_identifier_type = my_identifier_type )
            print( "- after Entity_Identifier_Type filter - record count: {}".format( eiqs.count() ) )
            
        #-- END DEBUG --#
        
        #======================================================================#
        # ! ==> try to get identifier - good matches
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! ----> Just UUID

        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Identifier based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
        #-- END DEBUG --#

        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = my_identifier_uuid )
        result_entity_id = result_qs.get()
        result_entity = result_entity_id.entity
        
        # instance should not be None
        error_string = "Getting entity for uuid: {}, should return Entity instance, not None.".format( my_identifier_uuid )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Returned Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> UUID + ID name

        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Identifier based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
        #-- END DEBUG --#

        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid,
                                                          id_name_IN = my_identifier_name )
        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = my_identifier_uuid,
                                                          id_name_IN = my_identifier_name )
        result_entity_id = result_qs.get()
        result_entity = result_entity_id.entity
                
        # instance should not be None
        error_string = "Getting entity for uuid: {} and name: {}, should return Entity instance, not None.".format( my_identifier_uuid, my_identifier_name )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> UUID + ID name + source

        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Identifier based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
        #-- END DEBUG --#
        
        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source )
        result_entity_id = result_qs.get()
        result_entity = result_entity_id.entity                
        
        # instance should not be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {}, should return Entity instance, not None.".format( my_identifier_uuid, my_identifier_name, my_identifier_source )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> UUID + ID name + source + type instance

        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Identifier based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
        #-- END DEBUG --#
        
        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = my_identifier_entity_id_type )
        result_entity_id = result_qs.get()
        result_entity = result_entity_id.entity                
        
        # instance should not be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {}, should return Entity instance, not None.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> UUID + ID name + source + type instance + id_type

        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Identifier based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
        #-- END DEBUG --#
        
        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = my_identifier_entity_id_type,
                                                          id_id_type_IN = my_identifier_id_type )
        result_entity_id = result_qs.get()
        result_entity = result_entity_id.entity                
        
        # instance should not be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {} and id_type: {}, should return Entity instance, not None.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type, my_identifier_id_type )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> UUID + ID name + source + Entity_Identifier_Type + id_type + notes

        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Identifier based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
            print( " - notes: {}".format( my_identifier_notes ) )
        #-- END DEBUG --#
        
        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = my_identifier_entity_id_type,
                                                          id_id_type_IN = my_identifier_id_type,
                                                          id_notes_IN = my_identifier_notes )
        result_entity_id = result_qs.get()
        result_entity = result_entity_id.entity                
        
        # instance should not be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {} and id_type: {} and notes: {}, should return Entity instance, not None.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type, my_identifier_id_type, my_identifier_notes )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #======================================================================#
        # ! ==> try to get entity - bad matches
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! ----> Just UUID
        test_id_uuid = self.ENTITY_ID_UUID_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( test_id_uuid ) )
        #-- END DEBUG --#

        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = test_id_uuid )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {}, should return {}, instead returned {}.".format( my_identifier_uuid, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> UUID + ID name
        test_id_name = self.ENTITY_ID_NAME_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( test_id_name ) )
        #-- END DEBUG --#

        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = my_identifier_uuid,
                                                          id_name_IN = test_id_name )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {} and name: {}; should return {}, instead returned {}.".format( my_identifier_uuid, test_id_name, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> UUID + ID name + source
        test_id_source = self.ENTITY_ID_SOURCE_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( test_id_source ) )
        #-- END DEBUG --#
        
        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = test_id_source )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {} and name: {} and source: {}; should return {}, instead returned {}.".format( my_identifier_uuid, my_identifier_name, test_id_source, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> UUID + ID name + source + Entity_Identifier_Type
        bad_identifier_type = Entity_Identifier_Type.get_type_for_name( self.TYPE_NAME_ARTICLE_NEWSBANK_ID )

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( bad_identifier_type ) )
        #-- END DEBUG --#
        
        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = bad_identifier_type )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {}; should return {}, instead returned {}.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> UUID + ID name + source + Entity_Identifier_Type + id_type
        test_id_id_type = self.ENTITY_ID_ID_TYPE_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
            print( " - id_type: {}".format( test_id_id_type ) )
        #-- END DEBUG --#
        
        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = my_identifier_entity_id_type,
                                                          id_id_type_IN = test_id_id_type )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {} and id_type: {}; should return {}, instead returned {}.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_id_type, test_id_id_type, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> UUID + ID name + source + Entity_Identifier_Type + id_type + notes
        test_id_notes = self.ENTITY_ID_NOTES_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
            print( " - id_type: {}".format( test_id_id_type ) )
            print( " - notes: {}".format( test_id_notes ) )
        #-- END DEBUG --#
        
        # get Entity_Identifier and related Entity.
        result_qs = Entity_Identifier.filter_identifiers( id_uuid_IN = my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = my_identifier_entity_id_type,
                                                          id_id_type_IN = my_identifier_id_type,
                                                          id_notes_IN = test_id_notes )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {} and id_type: {} and notes: {}; should return {}, instead returned {}.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type, my_identifier_id_type, test_id_notes, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

    #-- END test method test_filter_identifiers --#
        
    
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
        
        print( '\n====> In {}.{}'.format( self.CLASS_NAME, me ) )
        
        # create Entity
        entity_instance = TestHelper.create_test_entity()
        
        # create an Entity_Identifier instance
        identifier_instance = TestHelper.create_test_entity_identifier( entity_instance )
        
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
        
        print( '\n====> In {}.{}'.format( self.CLASS_NAME, me ) )
        
        # create Entity
        entity_instance = TestHelper.create_test_entity()
        
        # create an Entity_Identifier instance
        identifier_instance = TestHelper.create_test_entity_identifier( entity_instance )
        
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
