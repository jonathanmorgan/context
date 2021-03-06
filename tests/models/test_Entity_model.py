"""
This file contains tests of the context Entity model.

Functions tested:
- add_entity_type()
- get_entity_for_identifier()
- get_entity_trait()
- get_identifier()
- set_entity_trait()
- set_identifier()

"""

# import six
import six

# django imports
import django.test

# context_text imports
from context.models import Entity
from context.models import Entity_Identifier
from context.models import Entity_Identifier_Type
from context.models import Entity_Type
from context.tests.test_helper import TestHelper


class EntityModelTest( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ==> Constants-ish
    #----------------------------------------------------------------------------


    # DEBUG
    DEBUG = False

    # CLASS NAME
    CLASS_NAME = "EntityModelTest"

    # Identifier names
    TEST_IDENTIFIER_NAME = "nickname"
    

    #----------------------------------------------------------------------
    # ! ==> class methods
    #----------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # ! ==> instance methods
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


    def test_add_entity_type( self ):
        
        # declare variables
        me = "test_add_entity_type"
        entity_instance = None
        type_slug_1 = None
        type_slug_2 = None
        type_1 = None
        type_2 = None
        type_qs = None
        type_count = None
        should_be = None

        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )

        # create test entity
        entity_instance = TestHelper.create_test_entity()
        
        # add a type to an entity using slug.
        type_slug_1 = TestHelper.ENTITY_TYPE_SLUG_ARTICLE
        type_1 = entity_instance.add_entity_type( type_slug_1 )
        
        # make sure it is present in the entity's type set.
        type_qs = entity_instance.my_entity_types.filter( slug = type_slug_1 )
        type_count = type_qs.count()
        should_be = 1
        error_string = "type 1: {} --> count {} should = {}".format( type_slug_1, type_count, should_be )
        self.assertEqual( type_count, should_be, msg = error_string )
        
        # add a second.
        type_slug_2 = TestHelper.ENTITY_TYPE_SLUG_NEWSPAPER
        type_2 = entity_instance.add_entity_type( type_slug_2 )
        
        # make sure it is present in the entity's type set.
        type_qs = entity_instance.my_entity_types.filter( slug = type_slug_2 )
        type_count = type_qs.count()
        should_be = 1
        error_string = "type 2: {} --> count {} should = {}".format( type_slug_2, type_count, should_be )
        self.assertEqual( type_count, should_be, msg = error_string )
        
        # make sure the first one is stil there.
        type_qs = entity_instance.my_entity_types.filter( slug = type_slug_1 )
        type_count = type_qs.count()
        should_be = 1
        error_string = "type 1: {} --> count {} should = {}".format( type_slug_1, type_count, should_be )
        self.assertEqual( type_count, should_be, msg = error_string )

        # ! ----> add using Entity_Type instances

        # create test entity
        entity_instance = TestHelper.create_test_entity()
        
        # add a type to an entity.
        type_slug_1 = TestHelper.ENTITY_TYPE_SLUG_ARTICLE
        type_1 = Entity_Type.objects.get( slug = type_slug_1 )
        entity_instance.add_entity_type( type_IN = type_1 )
        
        # make sure it is present in the entity's type set.
        type_qs = entity_instance.my_entity_types.filter( slug = type_slug_1 )
        type_count = type_qs.count()
        should_be = 1
        error_string = "type 1: {} --> count {} should = {}".format( type_slug_1, type_count, should_be )
        self.assertEqual( type_count, should_be, msg = error_string )
        
        # add a second.
        type_slug_2 = TestHelper.ENTITY_TYPE_SLUG_NEWSPAPER
        type_2 = Entity_Type.objects.get( slug = type_slug_2 )
        entity_instance.add_entity_type( type_IN = type_2 )
        
        # make sure it is present in the entity's type set.
        type_qs = entity_instance.my_entity_types.filter( slug = type_slug_2 )
        type_count = type_qs.count()
        should_be = 1
        error_string = "type 2: {} --> count {} should = {}".format( type_slug_2, type_count, should_be )
        self.assertEqual( type_count, should_be, msg = error_string )
        
        # make sure the first one is stil there.
        type_qs = entity_instance.my_entity_types.filter( slug = type_slug_1 )
        type_count = type_qs.count()
        should_be = 1
        error_string = "type 1: {} --> count {} should = {}".format( type_slug_1, type_count, should_be )
        self.assertEqual( type_count, should_be, msg = error_string )

    #-- END test method test_set_entity_identifier_type() --#


    def test_filter_entities( self ):
        
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
        me = "test_filter_entities"
        my_entity = None
        result_qs = None
        result_count = None
        result_entity = None
        result_entity_id = None
        bad_identifier_type = None
        
        # declare variables - Entity info.
        my_entity_id = None
        my_entity_identifier = None
        my_entity_name = None
        my_entity_type_slug = None
        my_entity_type = None
        my_entity_type_qs = None

        # declare variables - Entity_Identifier info.
        my_identifier_id = None
        my_identifier_name = None
        my_identifier_uuid = None
        my_identifier_id_type = None
        my_identifier_source = None
        my_identifier_entity_id_type = None
        my_identifier_notes = None        
        
        # declare variables - test values
        test_entity_type_slug = None
        test_entity_type = None
        
        # init debug
        debug_flag = self.DEBUG
        eiqs = None
        
        # init
        test_entity_type_slug = TestHelper.ENTITY_TYPE_SLUG_PERSON
        test_identifier_type_name = TestHelper.ID_TYPE_NAME_PERSON_SOURCENET_ID
                
        # create test entity, with test identifier.
        my_entity = TestHelper.create_test_entity()
        my_entity_type_slug = test_entity_type_slug
        my_entity_type = my_entity.add_entity_type( my_entity_type_slug )
        my_entity_id = my_entity.id
        
        # create identifier
        my_entity_identifier = TestHelper.create_test_entity_identifier( my_entity )
        
        # set type and update identifier from it (must then save())
        my_identifier_type = my_entity_identifier.set_identifier_type_from_name( test_identifier_type_name, do_use_to_update_fields_IN = True )
        my_entity_identifier.save()

        # identifier details
        my_identifier_id = my_entity_identifier.id
        my_identifier_uuid = my_entity_identifier.uuid
        my_identifier_name = my_entity_identifier.name
        my_identifier_source = my_entity_identifier.source
        my_identifier_id_type = my_entity_identifier.id_type
        my_identifier_entity_id_type = my_entity_identifier.entity_identifier_type
        my_identifier_notes = my_entity_identifier.notes
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        print( "my_entity_identifier: {}".format( my_entity_identifier ) )


        #======================================================================#
        # ! ----> filter different ways.
        #======================================================================#
        
        
        #----------------------------------------------------------------------#
        # ! --------> Just Entity Type Slug

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - entity type slug: {}".format( my_entity_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.filter_entities( entity_type_slug_IN = my_entity_type_slug )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for type slug: {}, should return {}, instead returned {}.".format( my_entity_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        

        #----------------------------------------------------------------------#
        # ! --------> Just Entity Type

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - entity type: {}".format( my_entity_type ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.filter_entities( entity_type_IN = my_entity_type )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for type: {}; should return {}, instead returned {}.".format( my_entity_type, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        
        #----------------------------------------------------------------------#
        # ! --------> Entity Type Slug + Entity Type

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - entity type slug: {}".format( my_entity_type_slug ) )
            print( " - entity type: {}".format( my_entity_type ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.filter_entities( entity_type_IN = my_entity_type,
                                            entity_type_slug_IN = my_entity_type_slug )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for type: {}, type slug: {}; should return {}, instead returned {}.".format( my_entity_type, my_entity_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
                

    #-- END test method test_add_entity_type() --#
        
    
    def test_get_entity_for_identifier( self ):
        
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
        me = "test_get_entity_for_identifier"
        my_entity = None
        my_entity_id = None
        my_entity_identifier = None
        result_entity = None
        result_entity_id = None
        
        # declare variables - identifier details
        my_identifier_uuid = None
        my_identifier_name = None
        my_identifier_type = None
        my_identifier_source = None
        my_identifier_id_type = None
        my_identifier_notes = None
        
        # declare variables - test values
        bad_identifier_type = None
        test_id_uuid = None
        test_id_name = None
        test_id_source = None
        test_id_type = None
        test_id_id_type = None
        
        # debug
        debug_flag = self.DEBUG
        eiqs = None
        
        # create test entity, with test identifier.
        my_entity = TestHelper.create_test_entity()
        my_entity_id = my_entity.id
        
        # create identifier
        my_entity_identifier = TestHelper.create_test_entity_identifier( my_entity )
        
        # set type and update identifier from it (must then save())
        my_identifier_type = my_entity_identifier.set_identifier_type_from_name( TestHelper.ID_TYPE_NAME_PERSON_SOURCENET_ID, do_use_to_update_fields_IN = True )
        my_entity_identifier.save()

        # identifier details
        my_identifier_uuid = my_entity_identifier.uuid
        my_identifier_name = my_entity_identifier.name
        my_identifier_source = my_entity_identifier.source
        my_identifier_id_type = my_entity_identifier.id_type
        my_identifier_notes = my_entity_identifier.notes
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        print( "my_entity_identifier: {}".format( my_entity_identifier ) )

        #======================================================================#
        # ! DEBUG - try to get entity - manual test
        #======================================================================#
        
        # DEBUG
        if ( debug_flag == True ):

            eiqs = Entity_Identifier.objects.all()
            print( "- record count: {}".format( eiqs.count() ) )
            
            for entity_id in eiqs:
                
                print( "    - {}".format( entity_id ) )
                
            #-- END loop over entity ids. --#
            
            eiqs = eiqs.filter( uuid = my_identifier_uuid )
            print( "- record count: {}".format( eiqs.count() ) )
            
            eiqs = eiqs.filter( name = my_identifier_name )
            print( "- record count: {}".format( eiqs.count() ) )
            
            eiqs = eiqs.filter( source = my_identifier_source )
            print( "- record count: {}".format( eiqs.count() ) )
            
            eiqs = eiqs.filter( entity_identifier_type = my_identifier_type )
            print( "- record count: {}".format( eiqs.count() ) )
            
        #-- END DEBUG --#
        
        #======================================================================#
        # ! ----> try to get entity - good matches
        #======================================================================#
        
        #----------------------------------------------------------------------#        
        # ! --------> Just UUID

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
        #-- END DEBUG --#

        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid )
        
        # instance should not be None
        error_string = "Getting entity for uuid: {}, should return Entity instance, not None.".format( my_identifier_uuid )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Returned Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> UUID + ID name

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
        #-- END DEBUG --#

        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid,
                                                          id_name_IN = my_identifier_name )
        
        # instance should not be None
        error_string = "Getting entity for uuid: {} and name: {}, should return Entity instance, not None.".format( my_identifier_uuid, my_identifier_name )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> UUID + ID name + source

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
        #-- END DEBUG --#
        
        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source )
        
        # instance should not be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {}, should return Entity instance, not None.".format( my_identifier_uuid, my_identifier_name, my_identifier_source )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> UUID + ID name + source + type instance

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
        #-- END DEBUG --#
        
        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = my_identifier_type )
        
        # instance should not be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and id type: {}, should return Entity instance, not None.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_type )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> UUID + ID name + source + type instance + id_type

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
        #-- END DEBUG --#
        
        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = my_identifier_type,
                                                          id_id_type_IN = my_identifier_id_type )        

        # instance should not be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {} and id_type {}; should return Entity instance, not None.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_type, my_identifier_id_type )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> UUID + ID name + source + type instance + id_type + notes

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
            print( " - notes: {}".format( my_identifier_notes ) )
        #-- END DEBUG --#
        
        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = my_identifier_type,
                                                          id_id_type_IN = my_identifier_id_type,
                                                          id_notes_IN = my_identifier_notes )

        # instance should not be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {} and id_type {} and notes: {}; should return Entity instance, not None.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_type, my_identifier_id_type, my_identifier_notes )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #======================================================================#
        # ! ----> try to get entity - bad matches
        #======================================================================#
        
        #----------------------------------------------------------------------#        
        # ! --------> Just UUID
        test_id_uuid = TestHelper.ENTITY_ID_UUID_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( test_id_uuid ) )
        #-- END DEBUG --#

        result_entity = Entity.get_entity_for_identifier( test_id_uuid )
        
        # instance should be None
        error_string = "Getting entity for uuid: {}, should return None, not Entity instance.".format( test_id_uuid )
        self.assertIsNone( result_entity, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> UUID + ID name
        test_id_name = TestHelper.ENTITY_ID_NAME_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( test_id_name ) )
        #-- END DEBUG --#

        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid,
                                                          id_name_IN = test_id_name )
        
        # instance should be None
        error_string = "Getting entity for uuid: {} and name: {}, should return None, not Entity instance.".format( my_identifier_uuid, test_id_name )
        self.assertIsNone( result_entity, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> UUID + ID name + source
        test_id_source = TestHelper.ENTITY_ID_SOURCE_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( test_id_source ) )
        #-- END DEBUG --#
        
        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = test_id_source )
        
        # instance should be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {}, should return None, not Entity instance.".format( my_identifier_uuid, my_identifier_name, test_id_source )
        self.assertIsNone( result_entity, msg = error_string )

        #----------------------------------------------------------------------#        
        # ! --------> UUID + ID name + source + type instance
        bad_identifier_type = Entity_Identifier_Type.get_type_for_name( TestHelper.ID_TYPE_NAME_ARTICLE_NEWSBANK_ID )

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( bad_identifier_type ) )
        #-- END DEBUG --#
        
        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = bad_identifier_type )
        
        # instance should be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and id type: {}; should return None, not Entity instance.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, bad_identifier_type )
        self.assertIsNone( result_entity, msg = error_string )

        #----------------------------------------------------------------------#        
        # ! --------> UUID + ID name + source + type instance + id_type
        test_id_id_type = TestHelper.ENTITY_ID_ID_TYPE_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
            print( " - id_type: {}".format( test_id_id_type ) )
        #-- END DEBUG --#
        
        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = my_identifier_type,
                                                          id_id_type_IN = test_id_id_type )        
        
        # instance should be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and id type: {} and id_type: {}; should return None, not Entity instance.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_type, test_id_id_type )
        self.assertIsNone( result_entity, msg = error_string )

        #----------------------------------------------------------------------#        
        # ! --------> UUID + ID name + source + type instance + id_type + notes
        test_id_notes = TestHelper.ENTITY_ID_NOTES_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
            print( " - notes: {}".format( test_id_notes ) )
        #-- END DEBUG --#
        
        result_entity = Entity.get_entity_for_identifier( my_identifier_uuid,
                                                          id_name_IN = my_identifier_name,
                                                          id_source_IN = my_identifier_source,
                                                          id_entity_id_type_IN = my_identifier_type,
                                                          id_id_type_IN = my_identifier_id_type,
                                                          id_notes_IN = test_id_notes )
        # instance should be None
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and id type: {} and id_type: {} and notes: {}; should return None, not Entity instance.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_type, my_identifier_id_type, test_id_notes )
        self.assertIsNone( result_entity, msg = error_string )

    #-- END test method test_get_entity_for_identifier --#
        
    
    def test_get_entity_trait( self ):

        '''
        Things to test passing to the method:

            get_entity_trait( self,
                              name_IN,
                              slug_IN = None,
                              label_IN = None,
                              entity_type_trait_IN = None ):        
        '''

        # declare variables
        me = "test_get_entity_trait"
        entity_instance = None
        entity_type = None
        trait_name = None
        trait_instance = None
        entity_type_trait = None
        my_trait_id = None
        my_trait_name = None
        my_trait_slug = None
        my_trait_label = None
        result_trait = None
        result_trait_id = None
        
        # declare variables - test values
        test_trait_name = None
        test_trait_slug = None
        test_trait_label = None
        test_trait_type = None
        
        # debug
        debug_flag = self.DEBUG

        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )

        # build a "person" entity.
        entity_instance = TestHelper.create_test_entity()
        entity_type = entity_instance.add_entity_type( TestHelper.ENTITY_TYPE_SLUG_PERSON )
        
        # add a test trait
        trait_instance = TestHelper.create_test_entity_trait( entity_instance )
        
        # set a type on the trait.
        entity_type_trait = entity_type.get_trait_spec( TestHelper.ENTITY_TRAIT_NAME_FIRST_NAME )
        trait_instance.set_entity_type_trait( entity_type_trait )
        trait_instance.save()
        
        # trait details
        my_trait_id = trait_instance.id
        my_trait_name = trait_instance.name
        my_trait_slug = trait_instance.slug
        my_trait_label = trait_instance.label
        
        print( "trait_instance: {}".format( trait_instance ) )

        #======================================================================#
        # ! try to get entity trait - good matches
        #======================================================================#
        
        # ==> Just name

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( my_trait_name ) )
        #-- END DEBUG --#

        result_trait = entity_instance.get_entity_trait( my_trait_name )
        
        # instance should not be None
        error_string = "Getting trait for name: {}, should return Entity_Trait instance, not None.".format( my_trait_name )
        self.assertIsNotNone( result_trait, msg = error_string )

        # trait ID should match my_trait_id.
        result_trait_id = result_trait.id
        should_be = my_trait_id
        error_string = "Returned Trait has ID {}, should have ID {}".format( result_trait_id, should_be )
        self.assertEqual( result_trait_id, should_be, msg = error_string )
        
        # ==> name + slug

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( my_trait_name ) )
            print( " - slug: {}".format( my_trait_slug ) )
        #-- END DEBUG --#

        result_trait = entity_instance.get_entity_trait( my_trait_name,
                                                         slug_IN = my_trait_slug )
        
        # instance should not be None
        error_string = "Getting entity for name: {} and slug: {}, should return Entity instance, not None.".format( my_trait_name, my_trait_slug )
        self.assertIsNotNone( result_trait, msg = error_string )

        # trait ID should match my_trait_id.
        result_trait_id = result_trait.id
        should_be = my_trait_id
        error_string = "Returned Trait has ID {}, should have ID {}".format( result_trait_id, should_be )
        self.assertEqual( result_trait_id, should_be, msg = error_string )
        
        # ==> name + slug + label

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( my_trait_name ) )
            print( " - slug: {}".format( my_trait_slug ) )
            print( " - label: {}".format( my_trait_label ) )
        #-- END DEBUG --#
        
        result_trait = entity_instance.get_entity_trait( my_trait_name,
                                                         slug_IN = my_trait_slug,
                                                         label_IN = my_trait_label )
        
        # instance should not be None
        error_string = "Getting entity for name: {}, slug: {} and label: {}, should return Entity instance, not None.".format( my_trait_name, my_trait_slug, my_trait_label )
        self.assertIsNotNone( result_trait, msg = error_string )

        # trait ID should match my_trait_id.
        result_trait_id = result_trait.id
        should_be = my_trait_id
        error_string = "Returned Trait has ID {}, should have ID {}".format( result_trait_id, should_be )
        self.assertEqual( result_trait_id, should_be, msg = error_string )
        
        # ==> name + slug + label + Entity_Type_Trait instance

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( my_trait_name ) )
            print( " - slug: {}".format( my_trait_slug ) )
            print( " - label: {}".format( my_trait_label ) )
            print( " - Entity_Type_Trait: {}".format( entity_type_trait ) )
        #-- END DEBUG --#
        
        result_trait = entity_instance.get_entity_trait( my_trait_name,
                                                         slug_IN = my_trait_slug,
                                                         label_IN = my_trait_label,
                                                         entity_type_trait_IN = entity_type_trait )
        
        # instance should not be None
        error_string = "Getting entity for name: {}, slug: {}, label: {}, and Entity_Type_Trait: {}, should return Entity instance, not None.".format( my_trait_name, my_trait_slug, my_trait_label, entity_type_trait )
        self.assertIsNotNone( result_trait, msg = error_string )

        # trait ID should match my_trait_id.
        result_trait_id = result_trait.id
        should_be = my_trait_id
        error_string = "Returned Trait has ID {}, should have ID {}".format( result_trait_id, should_be )
        self.assertEqual( result_trait_id, should_be, msg = error_string )
                
        #======================================================================#
        # ! try to get entity trait - bad matches
        #======================================================================#
        
        # ==> Just name
        test_trait_name = TestHelper.ENTITY_TRAIT_NAME_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( test_trait_name ) )
        #-- END DEBUG --#

        result_trait = entity_instance.get_entity_trait( test_trait_name )
        
        # instance should not be None
        error_string = "Getting trait for name: {}, should return None, not Entity_Trait instance.".format( test_trait_name )
        self.assertIsNone( result_trait, msg = error_string )

        # ==> name + slug
        test_trait_slug = TestHelper.ENTITY_TRAIT_SLUG_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( my_trait_name ) )
            print( " - slug: {}".format( test_trait_slug ) )
        #-- END DEBUG --#

        result_trait = entity_instance.get_entity_trait( my_trait_name,
                                                         slug_IN = test_trait_slug )
        
        # instance should not be None
        error_string = "Getting entity for name: {} and slug: {}, should return Entity instance, not None.".format( my_trait_name, test_trait_slug )
        self.assertIsNone( result_trait, msg = error_string )

        # ==> name + slug + label
        test_trait_label = TestHelper.ENTITY_TRAIT_LABEL_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( my_trait_name ) )
            print( " - slug: {}".format( my_trait_slug ) )
            print( " - label: {}".format( test_trait_label ) )
        #-- END DEBUG --#
        
        result_trait = entity_instance.get_entity_trait( my_trait_name,
                                                         slug_IN = my_trait_slug,
                                                         label_IN = test_trait_label )
        
        # instance should not be None
        error_string = "Getting entity for name: {}, slug: {} and label: {}, should return Entity instance, not None.".format( my_trait_name, my_trait_slug, test_trait_label )
        self.assertIsNone( result_trait, msg = error_string )

        # ==> name + slug + label + Entity_Type_Trait instance
        test_entity_type_trait = entity_type.get_trait_spec( TestHelper.ENTITY_TRAIT_NAME_LAST_NAME )

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( my_trait_name ) )
            print( " - slug: {}".format( my_trait_slug ) )
            print( " - label: {}".format( my_trait_label ) )
            print( " - Entity_Type_Trait: {}".format( test_entity_type_trait ) )
        #-- END DEBUG --#
        
        result_trait = entity_instance.get_entity_trait( my_trait_name,
                                                         slug_IN = my_trait_slug,
                                                         label_IN = my_trait_label,
                                                         entity_type_trait_IN = test_entity_type_trait )
        
        # instance should not be None
        error_string = "Getting entity for name: {}, slug: {}, label: {}, and Entity_Type_Trait: {}, should return Entity instance, not None.".format( my_trait_name, my_trait_slug, my_trait_label, test_entity_type_trait )
        self.assertIsNone( result_trait, msg = error_string )
        
    #-- END test method test_get_entity_trait() --#


    def test_get_identifier( self ):
        
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
        me = "test_get_identifier"
        my_entity = None
        my_entity_id = None
        my_entity_identifier = None
        my_identifier_id = None
        my_identifier_uuid = None
        my_identifier_name = None
        my_identifier_source = None
        my_identifier_id_type = None
        my_identifier_notes = None
        result_identifier = None
        result_identifier_id = None
        bad_identifier_type = None
        bad_identifier_id_type = None
        
        # declare variables - test values
        test_id_name = None
        test_id_source = None
        test_id_type = None
                
        # debug
        debug_flag = self.DEBUG
        eiqs = None
        
        # create test entity, with test identifier.
        my_entity = TestHelper.create_test_entity()
        my_entity_id = my_entity.id
        
        # create identifier
        my_entity_identifier = TestHelper.create_test_entity_identifier( my_entity )
        
        # set type and update identifier from it (must then save())
        my_identifier_type = my_entity_identifier.set_identifier_type_from_name( TestHelper.ID_TYPE_NAME_PERSON_SOURCENET_ID, do_use_to_update_fields_IN = True )
        my_entity_identifier.save()

        # identifier details
        my_identifier_id = my_entity_identifier.id
        my_identifier_uuid = my_entity_identifier.uuid
        my_identifier_name = my_entity_identifier.name
        my_identifier_source = my_entity_identifier.source
        my_identifier_id_type = my_entity_identifier.id_type
        my_identifier_notes = my_entity_identifier.notes
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        print( "my_entity_identifier: {}".format( my_entity_identifier ) )

        #======================================================================#
        # ! ----> try to get identifier - good matches
        #======================================================================#
        
        #----------------------------------------------------------------------#        
        # ! --------> ID name

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( my_identifier_name ) )
        #-- END DEBUG --#

        result_identifier = my_entity.get_identifier( my_identifier_name )
        
        # instance should not be None
        error_string = "Getting identifier for name: {}, should return Entity_Identifier instance, not None.".format( my_identifier_name )
        self.assertIsNotNone( result_identifier, msg = error_string )

        # entity identifier ID should match my_entity_id.
        found = result_identifier.id
        should_be = my_identifier_id
        error_string = "identifier has ID {}, should have ID {}".format( found, should_be )
        self.assertEqual( found, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> ID name + source

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
        #-- END DEBUG --#
        
        result_identifier = my_entity.get_identifier( my_identifier_name,
                                                      id_source_IN = my_identifier_source )
        
        # instance should not be None
        error_string = "Getting identifier for name: {} and source: {}, should return Entity_Identifier instance, not None.".format( my_identifier_name, my_identifier_source )
        self.assertIsNotNone( result_identifier, msg = error_string )

        # entity identifier ID should match my_entity_id.
        found = result_identifier.id
        should_be = my_identifier_id
        error_string = "identifier has ID {}, should have ID {}".format( found, should_be )
        self.assertEqual( found, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> ID name + source + type instance

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
        #-- END DEBUG --#
        
        result_identifier = my_entity.get_identifier( my_identifier_name,
                                                      id_source_IN = my_identifier_source,
                                                      id_type_IN = my_identifier_type )
        
        # instance should not be None
        error_string = "Getting entity for name: {} and source: {} and id type: {}, should return Entity_Identifier instance, not None.".format( my_identifier_name, my_identifier_source, my_identifier_type )
        self.assertIsNotNone( result_identifier, msg = error_string )

        # entity identifier ID should match my_entity_id.
        found = result_identifier.id
        should_be = my_identifier_id
        error_string = "identifier has ID {}, should have ID {}".format( found, should_be )
        self.assertEqual( found, should_be, msg = error_string )

        #----------------------------------------------------------------------#        
        # ! --------> ID name + source + type instance + id_type

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
        #-- END DEBUG --#
        
        result_identifier = my_entity.get_identifier( my_identifier_name,
                                                      id_source_IN = my_identifier_source,
                                                      id_type_IN = my_identifier_type,
                                                      id_id_type_IN = my_identifier_id_type )
        
        # instance should not be None
        error_string = "Getting entity for name: {} and source: {} and id type: {}, should return Entity_Identifier instance, not None.".format( my_identifier_name, my_identifier_source, my_identifier_type )
        self.assertIsNotNone( result_identifier, msg = error_string )

        # entity identifier ID should match my_entity_id.
        found = result_identifier.id
        should_be = my_identifier_id
        error_string = "identifier has ID {}, should have ID {}".format( found, should_be )
        self.assertEqual( found, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> ID name + source + type instance + id_type + notes

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
            print( " - notes: {}".format( my_identifier_notes ) )
        #-- END DEBUG --#
        
        result_identifier = my_entity.get_identifier( my_identifier_name,
                                                      id_source_IN = my_identifier_source,
                                                      id_type_IN = my_identifier_type,
                                                      id_id_type_IN = my_identifier_id_type,
                                                      id_notes_IN = my_identifier_notes )
        
        # instance should not be None
        error_string = "Getting entity for name: {} and source: {} and id type: {}, should return Entity_Identifier instance, not None.".format( my_identifier_name, my_identifier_source, my_identifier_type )
        self.assertIsNotNone( result_identifier, msg = error_string )

        # entity identifier ID should match my_entity_id.
        found = result_identifier.id
        should_be = my_identifier_id
        error_string = "identifier has ID {}, should have ID {}".format( found, should_be )
        self.assertEqual( found, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> ID name + source + type instance + id_type + notes + uuid

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
            print( " - notes: {}".format( my_identifier_notes ) )
            print( " - uuid: {}".format( my_identifier_uuid ) )
        #-- END DEBUG --#
        
        result_identifier = my_entity.get_identifier( my_identifier_name,
                                                      id_source_IN = my_identifier_source,
                                                      id_type_IN = my_identifier_type,
                                                      id_id_type_IN = my_identifier_id_type,
                                                      id_notes_IN = my_identifier_notes,
                                                      id_uuid_IN = my_identifier_uuid )
        
        # instance should not be None
        error_string = "Getting entity for name: {} and source: {} and id type: {}, should return Entity_Identifier instance, not None.".format( my_identifier_name, my_identifier_source, my_identifier_type )
        self.assertIsNotNone( result_identifier, msg = error_string )

        # entity identifier ID should match my_entity_id.
        found = result_identifier.id
        should_be = my_identifier_id
        error_string = "identifier has ID {}, should have ID {}".format( found, should_be )
        self.assertEqual( found, should_be, msg = error_string )
        
        #======================================================================#
        # ! ----> try to get identifier - bad matches
        #======================================================================#
        
        #----------------------------------------------------------------------#        
        # ! --------> ID name
        test_id_name = TestHelper.ENTITY_ID_NAME_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( test_id_name ) )
        #-- END DEBUG --#

        result_identifier = my_entity.get_identifier( test_id_name )
        
        # instance should be None
        error_string = "Getting entity identifier for name: {}, should return None, not Entity_Identifier instance.".format( my_identifier_uuid, test_id_name )
        self.assertIsNone( result_identifier, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> ID name + source
        test_id_source = TestHelper.ENTITY_ID_SOURCE_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( test_id_source ) )
        #-- END DEBUG --#
        
        result_identifier = my_entity.get_identifier( my_identifier_name,
                                                      id_source_IN = test_id_source )
        
        # instance should be None
        error_string = "Getting entity identifier for name: {} and source: {}, should return None, not Entity_Identifier instance.".format( my_identifier_name, test_id_source )
        self.assertIsNone( result_identifier, msg = error_string )

        #----------------------------------------------------------------------#        
        # ! --------> ID name + source + type instance
        bad_identifier_type = Entity_Identifier_Type.get_type_for_name( TestHelper.ID_TYPE_NAME_ARTICLE_NEWSBANK_ID )

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( bad_identifier_type ) )
        #-- END DEBUG --#
        
        result_identifier = my_entity.get_identifier( my_identifier_name,
                                                      id_source_IN = my_identifier_source,
                                                      id_type_IN = bad_identifier_type )
        
        # instance should be None
        error_string = "Getting entity identifier for name: {} and source: {} and type: {}, should return None, not Entity_Identifier instance.".format( my_identifier_name, my_identifier_source, bad_identifier_type )
        self.assertIsNone( result_identifier, msg = error_string )

        #----------------------------------------------------------------------#        
        # ! --------> ID name + source + type instance + id_type
        bad_identifier_id_type = TestHelper.ENTITY_ID_ID_TYPE_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
            print( " - id_type: {}".format( bad_identifier_id_type ) )
        #-- END DEBUG --#
        
        result_identifier = my_entity.get_identifier( my_identifier_name,
                                                      id_source_IN = my_identifier_source,
                                                      id_type_IN = my_identifier_type,
                                                      id_id_type_IN = bad_identifier_id_type )
        
        # instance should be None
        error_string = "Getting entity identifier for name: {} and source: {} and type: {}, and id_type: {} should return None, not Entity_Identifier instance.".format( my_identifier_name, my_identifier_source, my_identifier_type, bad_identifier_id_type )
        self.assertIsNone( result_identifier, msg = error_string )
        
        #----------------------------------------------------------------------#        
        # ! --------> ID name + source + type instance + id_type + notes
        bad_identifier_notes = TestHelper.ENTITY_ID_NOTES_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
            print( " - notes: {}".format( bad_identifier_notes ) )
        #-- END DEBUG --#
        
        result_identifier = my_entity.get_identifier( my_identifier_name,
                                                      id_source_IN = my_identifier_source,
                                                      id_type_IN = my_identifier_type,
                                                      id_id_type_IN = my_identifier_id_type,
                                                      id_notes_IN = bad_identifier_notes )
        
        # instance should be None
        error_string = "Getting entity identifier for name: {} and source: {} and type: {}, and id_type: {}, and notes: {} should return None, not Entity_Identifier instance.".format( my_identifier_name, my_identifier_source, bad_identifier_type, my_identifier_id_type, bad_identifier_notes )
        self.assertIsNone( result_identifier, msg = error_string )

        #----------------------------------------------------------------------#        
        # ! --------> ID name + source + type instance + id_type + notes + uuid
        bad_identifier_uuid = TestHelper.ENTITY_ID_UUID_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity identifier based on:" )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - type: {}".format( my_identifier_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
            print( " - notes: {}".format( my_identifier_notes ) )
            print( " - uuid: {}".format( bad_identifier_uuid ) )
        #-- END DEBUG --#
        
        result_identifier = my_entity.get_identifier( my_identifier_name,
                                                      id_source_IN = my_identifier_source,
                                                      id_type_IN = my_identifier_type,
                                                      id_id_type_IN = my_identifier_id_type,
                                                      id_notes_IN = my_identifier_notes,
                                                      id_uuid_IN = bad_identifier_uuid )
        
        # instance should be None
        error_string = "Getting entity identifier for name: {} and source: {} and and type: {}, and id_type: {}, and notes: {}, and UUID: {} should return None, not Entity_Identifier instance.".format( my_identifier_name, my_identifier_source, my_identifier_type, my_identifier_id_type, my_identifier_notes, bad_identifier_uuid )
        self.assertIsNone( result_identifier, msg = error_string )

    #-- END test method test_get_identifier --#
        
    
    def test_get_my_entity_type( self ):
        
        # declare variables
        me = "test_get_my_entity_type"
        entity_instance = None
        type_slug_1 = None
        type_slug_2 = None
        type_1 = None
        type_1_id = None
        type_2 = None
        type_2_id = None
        type_qs = None
        type_count = None
        should_be = None
        test_type = None
        test_type_id = None

        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )

        # create test entity
        entity_instance = TestHelper.create_test_entity()
        
        #----------------------------------------------------------------------#
        # ! ----> add a type to an entity using slug.
        #----------------------------------------------------------------------#

        type_slug_1 = TestHelper.ENTITY_TYPE_SLUG_ARTICLE
        type_1 = entity_instance.add_entity_type( type_slug_1 )
        type_1_id = type_1.id
        
        # make sure it is present in the entity's type set.
        type_qs = entity_instance.my_entity_types.filter( slug = type_slug_1 )
        type_count = type_qs.count()
        should_be = 1
        error_string = "type 1: {} --> count {} should = {}".format( type_slug_1, type_count, should_be )
        self.assertEqual( type_count, should_be, msg = error_string )
        
        # --------> use get_my_entity_type() with no argument to retrieve it.
        test_type = entity_instance.get_my_entity_type()
        
        # Should not be None
        error_string = "None returned from no-argument call to get_my_entity_type(), should have returned something."
        self.assertIsNotNone( test_type, msg = error_string )
        
        # type ID should equal the ID of type_1.
        test_type_id = test_type.id
        test_value = test_type_id
        should_be = type_1_id
        error_string = "no-argument call to get_my_entity_type() returned type with ID: {}, should be {}".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # --------> use get_my_entity_type() with slug to retrieve it.
        test_type = entity_instance.get_my_entity_type( slug_IN = type_slug_1 )
        
        # Should not be None
        error_string = "None returned from call to get_my_entity_type(), slug_IN = {}, should have returned something.".format( type_slug_1 )
        self.assertIsNotNone( test_type, msg = error_string )
        
        # type ID should equal the ID of type_1.
        test_type_id = test_type.id
        test_value = test_type_id
        should_be = type_1_id
        error_string = "call to get_my_entity_type(), slug_IN = {}, returned type with ID: {}, should be {}".format( type_slug_1, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> add a second.
        #----------------------------------------------------------------------#

        type_slug_2 = TestHelper.ENTITY_TYPE_SLUG_NEWSPAPER
        type_2 = entity_instance.add_entity_type( type_slug_2 )
        type_2_id = type_2.id
        
        # make sure it is present in the entity's type set.
        type_qs = entity_instance.my_entity_types.filter( slug = type_slug_2 )
        type_count = type_qs.count()
        should_be = 1
        error_string = "type 2: {} --> count {} should = {}".format( type_slug_2, type_count, should_be )
        self.assertEqual( type_count, should_be, msg = error_string )
        
        # make sure the first one is stil there.
        type_qs = entity_instance.my_entity_types.filter( slug = type_slug_1 )
        type_count = type_qs.count()
        should_be = 1
        error_string = "type 1: {} --> count {} should = {}".format( type_slug_1, type_count, should_be )
        self.assertEqual( type_count, should_be, msg = error_string )

        # --------> try get_my_entity_type() with no argument.
        test_type = entity_instance.get_my_entity_type()
        
        # Should be None
        error_string = "Something returned from no-argument call to get_my_entity_type() when multiple types, should be None."
        self.assertIsNone( test_type, msg = error_string )
        
        # --------> use get_my_entity_type() with type_slug_1 to retrieve it.
        test_type = entity_instance.get_my_entity_type( slug_IN = type_slug_1 )
        
        # Should not be None
        error_string = "None returned from call to get_my_entity_type(), slug_IN = {}, should have returned something.".format( type_slug_1 )
        self.assertIsNotNone( test_type, msg = error_string )
        
        # type ID should equal the ID of type_1.
        test_type_id = test_type.id
        test_value = test_type_id
        should_be = type_1_id
        error_string = "call to get_my_entity_type(), slug_IN = {}, returned type with ID: {}, should be {}".format( type_slug_1, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # --------> use get_my_entity_type() with type_slug_2 to retrieve it.
        test_type = entity_instance.get_my_entity_type( slug_IN = type_slug_2 )
        
        # Should not be None
        error_string = "None returned from call to get_my_entity_type(), slug_IN = {}, should have returned something.".format( type_slug_1 )
        self.assertIsNotNone( test_type, msg = error_string )
        
        # type ID should equal the ID of type_1.
        test_type_id = test_type.id
        test_value = test_type_id
        should_be = type_2_id
        error_string = "call to get_my_entity_type(), slug_IN = {}, returned type with ID: {}, should be {}".format( type_slug_1, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
    #-- END test method test_set_entity_identifier_type() --#


    def test_lookup_entities( self ):
        
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
        me = "test_lookup_entities"
        my_entity = None
        result_qs = None
        result_count = None
        result_entity = None
        result_entity_id = None
        bad_identifier_type = None
        
        # declare variables - Entity info.
        my_entity_id = None
        my_entity_identifier = None
        my_entity_name = None
        my_entity_type_slug = None
        my_entity_type = None
        my_entity_type_qs = None

        # declare variables - Entity_Identifier info.
        my_identifier_id = None
        my_identifier_name = None
        my_identifier_uuid = None
        my_identifier_id_type = None
        my_identifier_source = None
        my_identifier_entity_id_type = None
        my_identifier_notes = None        
        
        # declare variables - test values
        test_entity_type_slug = None
        test_entity_type = None
        test_identifier_type_name = None
        test_id_uuid = None
        test_id_name = None
        test_id_source = None
        test_id_entity_id_type = None
        test_id_id_type = None
        test_id_notes = None
        
        # init debug
        debug_flag = self.DEBUG
        eiqs = None
        
        # init
        test_entity_type_slug = TestHelper.ENTITY_TYPE_SLUG_PERSON
        test_identifier_type_name = TestHelper.ID_TYPE_NAME_PERSON_SOURCENET_ID
                
        # create test entity, with test identifier.
        my_entity = TestHelper.create_test_entity()
        my_entity_type_slug = test_entity_type_slug
        my_entity_type = my_entity.add_entity_type( my_entity_type_slug )
        my_entity_id = my_entity.id
        
        # create identifier
        my_entity_identifier = TestHelper.create_test_entity_identifier( my_entity )
        
        # set type and update identifier from it (must then save())
        my_identifier_type = my_entity_identifier.set_identifier_type_from_name( test_identifier_type_name, do_use_to_update_fields_IN = True )
        my_entity_identifier.save()

        # identifier details
        my_identifier_id = my_entity_identifier.id
        my_identifier_uuid = my_entity_identifier.uuid
        my_identifier_name = my_entity_identifier.name
        my_identifier_source = my_entity_identifier.source
        my_identifier_id_type = my_entity_identifier.id_type
        my_identifier_entity_id_type = my_entity_identifier.entity_identifier_type
        my_identifier_notes = my_entity_identifier.notes
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        print( "my_entity_identifier: {}".format( my_entity_identifier ) )


        #======================================================================#
        # ! ----> filter different ways.
        #======================================================================#
        
        
        #----------------------------------------------------------------------#
        # ! --------> Just Entity Type Slug

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - entity type slug: {}".format( my_entity_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( entity_type_slug_IN = my_entity_type_slug )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for type slug: {}, should return {}, instead returned {}.".format( my_entity_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        

        #----------------------------------------------------------------------#
        # ! --------> Just Entity Type

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - Entity_Type: {}".format( my_entity_type ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( entity_type_IN = my_entity_type )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for type: {}; should return {}, instead returned {}.".format( my_entity_type, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        
        #----------------------------------------------------------------------#
        # ! --------> Entity Type Slug + Entity Type

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - entity type slug: {}".format( my_entity_type_slug ) )
            print( " - Entity_Type: {}".format( my_entity_type ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( entity_type_IN = my_entity_type,
                                            entity_type_slug_IN = my_entity_type_slug )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for type: {}, type slug: {}; should return {}, instead returned {}.".format( my_entity_type, my_entity_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
                
        
        #----------------------------------------------------------------------#
        # ! --------> Entity Type Slug + Entity Type + UUID

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - entity type slug: {}".format( my_entity_type_slug ) )
            print( " - Entity_Type: {}".format( my_entity_type ) )
            print( " - id UUID: {}".format( my_identifier_uuid ) )
        #-- END DEBUG --#

        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( entity_type_IN = my_entity_type,
                                            entity_type_slug_IN = my_entity_type_slug,
                                            id_uuid_IN = my_identifier_uuid )
        result_count = result_qs.count()
        result_entity = result_qs.get()
        
        # instance should not be None
        error_string = "Getting entity for type: {}, type slug: {}, uuid: {}; should return Entity instance, not None.".format( my_entity_type, my_entity_type_slug, my_identifier_uuid )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Returned Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! --------> Entity Type Slug + Entity Type + UUID + ID name

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - entity type slug: {}".format( my_entity_type_slug ) )
            print( " - Entity_Type: {}".format( my_entity_type ) )
            print( " - id UUID: {}".format( my_identifier_uuid ) )
            print( " - id name: {}".format( my_identifier_name ) )
        #-- END DEBUG --#

        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( entity_type_IN = my_entity_type,
                                            entity_type_slug_IN = my_entity_type_slug,
                                            id_uuid_IN = my_identifier_uuid,
                                            id_name_IN = my_identifier_name )
        result_count = result_qs.count()
        result_entity = result_qs.get()
        
        # instance should not be None
        error_string = "Getting entity for type: {}, type slug: {}, uuid: {}, id name: {}; should return Entity instance, not None.".format( my_entity_type, my_entity_type_slug, my_identifier_uuid, my_identifier_name )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Returned Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! --------> Entity Type Slug + Entity Type + UUID + ID name + source

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - entity type slug: {}".format( my_entity_type_slug ) )
            print( " - Entity_Type: {}".format( my_entity_type ) )
            print( " - id UUID: {}".format( my_identifier_uuid ) )
            print( " - id name: {}".format( my_identifier_name ) )
            print( " - id source: {}".format( my_identifier_source ) )
        #-- END DEBUG --#

        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( entity_type_IN = my_entity_type,
                                            entity_type_slug_IN = my_entity_type_slug,
                                            id_uuid_IN = my_identifier_uuid,
                                            id_name_IN = my_identifier_name,
                                            id_source_IN = my_identifier_source )
        result_count = result_qs.count()
        result_entity = result_qs.get()
        
        # instance should not be None
        error_string = "Getting entity for type: {}, type slug: {}, uuid: {}, id name: {}, id source: {}; should return Entity instance, not None.".format( my_entity_type, my_entity_type_slug, my_identifier_uuid, my_identifier_name, my_identifier_source )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Returned Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
                
        #----------------------------------------------------------------------#
        # ! --------> Entity Type Slug + Entity Type + UUID + ID name + source + type instance

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - entity type slug: {}".format( my_entity_type_slug ) )
            print( " - Entity_Type: {}".format( my_entity_type ) )
            print( " - id UUID: {}".format( my_identifier_uuid ) )
            print( " - id name: {}".format( my_identifier_name ) )
            print( " - id source: {}".format( my_identifier_source ) )
            print( " - id Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
        #-- END DEBUG --#

        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( entity_type_IN = my_entity_type,
                                            entity_type_slug_IN = my_entity_type_slug,
                                            id_uuid_IN = my_identifier_uuid,
                                            id_name_IN = my_identifier_name,
                                            id_source_IN = my_identifier_source,
                                            id_entity_id_type_IN = my_identifier_entity_id_type )
        result_count = result_qs.count()
        result_entity = result_qs.get()
        
        # instance should not be None
        error_string = "Getting entity for type: {}, type slug: {}, uuid: {}, id name: {}, id source: {}, Entity_Identifier_Type: {}; should return Entity instance, not None.".format( my_entity_type, my_entity_type_slug, my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Returned Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! --------> Entity Type Slug + Entity Type + UUID + ID name + source + type instance + id_type

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - entity type slug: {}".format( my_entity_type_slug ) )
            print( " - Entity_Type: {}".format( my_entity_type ) )
            print( " - id UUID: {}".format( my_identifier_uuid ) )
            print( " - id name: {}".format( my_identifier_name ) )
            print( " - id source: {}".format( my_identifier_source ) )
            print( " - id Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
            print( " - id id_type: {}".format( my_identifier_id_type ) )
        #-- END DEBUG --#

        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( entity_type_IN = my_entity_type,
                                            entity_type_slug_IN = my_entity_type_slug,
                                            id_uuid_IN = my_identifier_uuid,
                                            id_name_IN = my_identifier_name,
                                            id_source_IN = my_identifier_source,
                                            id_entity_id_type_IN = my_identifier_entity_id_type,
                                            id_id_type_IN = my_identifier_id_type )
        result_count = result_qs.count()
        result_entity = result_qs.get()
        
        # instance should not be None
        error_string = "Getting entity for type: {}, type slug: {}, uuid: {}, id name: {}, id source: {}, Entity_Identifier_Type: {}, id_type: {}; should return Entity instance, not None.".format( my_entity_type, my_entity_type_slug, my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type, my_identifier_id_type )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Returned Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )

        
        #----------------------------------------------------------------------#
        # ! --------> Entity Type Slug + Entity Type + UUID + ID name + source + type instance + id_type + notes

        if ( debug_flag == True ):
            print( "\n--------> Filter Entities based on:" )
            print( " - entity type slug: {}".format( my_entity_type_slug ) )
            print( " - Entity_Type: {}".format( my_entity_type ) )
            print( " - id UUID: {}".format( my_identifier_uuid ) )
            print( " - id name: {}".format( my_identifier_name ) )
            print( " - id source: {}".format( my_identifier_source ) )
            print( " - id Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
            print( " - id id_type: {}".format( my_identifier_id_type ) )
            print( " - id notes: {}".format( my_identifier_notes ) )
        #-- END DEBUG --#

        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( entity_type_IN = my_entity_type,
                                            entity_type_slug_IN = my_entity_type_slug,
                                            id_uuid_IN = my_identifier_uuid,
                                            id_name_IN = my_identifier_name,
                                            id_source_IN = my_identifier_source,
                                            id_entity_id_type_IN = my_identifier_entity_id_type,
                                            id_id_type_IN = my_identifier_id_type,
                                            id_notes_IN = my_identifier_notes )
        result_count = result_qs.count()
        result_entity = result_qs.get()
        
        # instance should not be None
        error_string = "Getting entity for type: {}, type slug: {}, uuid: {}, id name: {}, id source: {}, Entity_Identifier_Type: {}, id_type: {}, id notes: {}; should return Entity instance, not None.".format( my_entity_type, my_entity_type_slug, my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type, my_identifier_id_type, my_identifier_notes )
        self.assertIsNotNone( result_entity, msg = error_string )

        # entity ID should match my_entity_id.
        result_entity_id = result_entity.id
        should_be = my_entity_id
        error_string = "Returned Entity has ID {}, should have ID {}".format( result_entity_id, should_be )
        self.assertEqual( result_entity_id, should_be, msg = error_string )

                
        #======================================================================#
        # ! ----> try to get entity - bad matches
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! --------> Just UUID
        test_id_uuid = TestHelper.ENTITY_ID_UUID_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - id UUID: {}".format( test_id_uuid ) )
        #-- END DEBUG --#

        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( id_uuid_IN = test_id_uuid )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {}, should return {}, instead returned {}.".format( my_identifier_uuid, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! --------> UUID + ID name
        test_id_name = TestHelper.ENTITY_ID_NAME_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - id UUID: {}".format( my_identifier_uuid ) )
            print( " - id name: {}".format( test_id_name ) )
        #-- END DEBUG --#

        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( id_uuid_IN = my_identifier_uuid,
                                            id_name_IN = test_id_name )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {} and name: {}; should return {}, instead returned {}.".format( my_identifier_uuid, test_id_name, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! --------> UUID + ID name + source
        test_id_source = TestHelper.ENTITY_ID_SOURCE_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - id UUID: {}".format( my_identifier_uuid ) )
            print( " - id name: {}".format( my_identifier_name ) )
            print( " - id source: {}".format( test_id_source ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( id_uuid_IN = my_identifier_uuid,
                                            id_name_IN = my_identifier_name,
                                            id_source_IN = test_id_source )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {} and name: {} and source: {}; should return {}, instead returned {}.".format( my_identifier_uuid, my_identifier_name, test_id_source, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! --------> UUID + ID name + source + Entity_Identifier_Type
        bad_identifier_type = Entity_Identifier_Type.get_type_for_name( TestHelper.ID_TYPE_NAME_ARTICLE_NEWSBANK_ID )

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - id UUID: {}".format( my_identifier_uuid ) )
            print( " - id name: {}".format( my_identifier_name ) )
            print( " - id source: {}".format( my_identifier_source ) )
            print( " - id Entity_Identifier_Type: {}".format( bad_identifier_type ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( id_uuid_IN = my_identifier_uuid,
                                            id_name_IN = my_identifier_name,
                                            id_source_IN = my_identifier_source,
                                            id_entity_id_type_IN = bad_identifier_type )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {}; should return {}, instead returned {}.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! --------> UUID + ID name + source + Entity_Identifier_Type + id_type
        test_id_id_type = TestHelper.ENTITY_ID_ID_TYPE_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - id UUID: {}".format( my_identifier_uuid ) )
            print( " - id name: {}".format( my_identifier_name ) )
            print( " - id source: {}".format( my_identifier_source ) )
            print( " - id Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
            print( " - id id_type: {}".format( test_id_id_type ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( id_uuid_IN = my_identifier_uuid,
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
        # ! --------> UUID + ID name + source + Entity_Identifier_Type + id_type + notes
        test_id_notes = TestHelper.ENTITY_ID_NOTES_NO_MATCH

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
            print( " - notes: {}".format( test_id_notes ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( id_uuid_IN = my_identifier_uuid,
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


        #----------------------------------------------------------------------#
        # ! --------> UUID + ID name + source + Entity_Identifier_Type + id_type + notes + entity type slug
        test_entity_type_slug = TestHelper.ENTITY_TYPE_SLUG_ARTICLE

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
            print( " - notes: {}".format( my_identifier_notes ) )
            print( " - entity type slug: {}".format( test_entity_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( id_uuid_IN = my_identifier_uuid,
                                            id_name_IN = my_identifier_name,
                                            id_source_IN = my_identifier_source,
                                            id_entity_id_type_IN = my_identifier_entity_id_type,
                                            id_id_type_IN = my_identifier_id_type,
                                            id_notes_IN = my_identifier_notes,
                                            entity_type_slug_IN = test_entity_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {} and id_type: {} and notes: {} and entity type slug: {}; should return {}, instead returned {}.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type, my_identifier_id_type, my_identifier_notes, test_entity_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )


        #----------------------------------------------------------------------#
        # ! --------> UUID + ID name + source + Entity_Identifier_Type + id_type + notes + entity type
        test_entity_type_slug = TestHelper.ENTITY_TYPE_SLUG_ARTICLE
        test_entity_type = Entity_Type.objects.get( slug = test_entity_type_slug )

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
            print( " - notes: {}".format( my_identifier_notes ) )
            print( " - Entity_Type: {}".format( test_entity_type ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( id_uuid_IN = my_identifier_uuid,
                                            id_name_IN = my_identifier_name,
                                            id_source_IN = my_identifier_source,
                                            id_entity_id_type_IN = my_identifier_entity_id_type,
                                            id_id_type_IN = my_identifier_id_type,
                                            id_notes_IN = my_identifier_notes,
                                            entity_type_IN = test_entity_type )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {} and id_type: {} and notes: {} and Entity_Type: {}; should return {}, instead returned {}.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type, my_identifier_id_type, my_identifier_notes, test_entity_type, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )


        #----------------------------------------------------------------------#
        # ! --------> UUID + ID name + source + Entity_Identifier_Type + id_type + notes + entity type slug + entity type
        test_entity_type_slug = TestHelper.ENTITY_TYPE_SLUG_ARTICLE
        test_entity_type = Entity_Type.objects.get( slug = test_entity_type_slug )

        if ( debug_flag == True ):
            print( "\n--------> Retrieve entity based on:" )
            print( " - UUID: {}".format( my_identifier_uuid ) )
            print( " - ID name: {}".format( my_identifier_name ) )
            print( " - source: {}".format( my_identifier_source ) )
            print( " - Entity_Identifier_Type: {}".format( my_identifier_entity_id_type ) )
            print( " - id_type: {}".format( my_identifier_id_type ) )
            print( " - notes: {}".format( my_identifier_notes ) )
            print( " - entity type slug: {}".format( my_entity_type_slug ) )
            print( " - Entity_Type: {}".format( test_entity_type ) )
        #-- END DEBUG --#
        
        # get Entity QuerySet.
        result_qs = Entity.lookup_entities( id_uuid_IN = my_identifier_uuid,
                                            id_name_IN = my_identifier_name,
                                            id_source_IN = my_identifier_source,
                                            id_entity_id_type_IN = my_identifier_entity_id_type,
                                            id_id_type_IN = my_identifier_id_type,
                                            id_notes_IN = my_identifier_notes,
                                            entity_type_slug_IN = my_entity_type_slug,
                                            entity_type_IN = test_entity_type )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for uuid: {} and name: {} and source: {} and Entity_Identifier_Type: {} and id_type: {} and notes: {} and entity type slug: {} and Entity_Type: {}; should return {}, instead returned {}.".format( my_identifier_uuid, my_identifier_name, my_identifier_source, my_identifier_entity_id_type, my_identifier_id_type, my_identifier_notes, test_entity_type_slug, test_entity_type, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )


    #-- END test method test_lookup_entities --#
        
    
    def test_set_entity_trait( self ):

        '''
        Things to test passing to the method:
            set_entity_trait( self,
                          name_IN,
                          value_IN,
                          slug_IN = None,
                          value_json_IN = None,
                          label_IN = None,
                          description_IN = None,
                          trait_type_IN = None,
                          term_IN = None,
                          entity_type_trait_IN = None ):

        
        '''

        # declare variables
        me = "test_set_entity_trait"
        entity_instance = None
        entity_type = None
        trait_name = None
        trait_instance = None
        trait_stored_name = None
        trait_stored_value = None
        trait_stored_slug = None
        trait_stored_label = None
        trait_id = None
        trait_qs = None
        trait_count = None
        entity_type_trait = None
        original_trait_id = None
        original_trait_value = None

        # declare variables - trait properties

        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )

        # build a "person" entity.
        entity_instance = TestHelper.create_test_entity()
        entity_type = entity_instance.add_entity_type( TestHelper.ENTITY_TYPE_SLUG_PERSON )
        
        # add a new trait from scratch (flibble_glibble_pants).
        trait_name = TestHelper.ENTITY_TRAIT_NAME_GIBBERISH
        trait_instance = entity_instance.set_entity_trait( trait_name, value_IN = "Jonathan" )
        trait_stored_name = trait_instance.name
        
        # instance should not be None
        error_string = "Creating trait should return Entity_Trait instance, not None"
        self.assertIsNotNone( trait_instance, msg = error_string )

        # retrieve trait
        trait_qs = entity_instance.entity_trait_set.filter( name = trait_name )
        trait_count = trait_qs.count()
        should_be = 1
        error_string = "trait with name {} --> count {} should = {}".format( trait_name, trait_count, should_be )
        self.assertEqual( trait_count, should_be, msg = error_string )

        # create a trait with a type specification.  Make sure the meta-information was updated.
        trait_name = "first_name_string"
        trait_value = "Jonathan"
        original_trait_value = trait_value
        entity_type_trait = entity_type.get_trait_spec( TestHelper.ENTITY_TRAIT_NAME_FIRST_NAME )
        trait_instance = entity_instance.set_entity_trait( trait_name, value_IN = trait_value, entity_type_trait_IN = entity_type_trait )
        original_trait_id = trait_instance.id
        trait_stored_name = trait_instance.name
        trait_stored_value = trait_instance.value
        trait_stored_slug = trait_instance.slug
        trait_stored_label = trait_instance.label
        
        # check trait count
        trait_qs = entity_instance.entity_trait_set.all()
        trait_count = trait_qs.count()
        should_be = 2
        error_string = "trait count {} should = {}".format( trait_count, should_be )
        self.assertEqual( trait_count, should_be, msg = error_string )

        # stored name, slug, and label should be set from specification.
        should_be = entity_type_trait.name
        error_string = "trait name {} --> should be {}".format( trait_stored_name, should_be )
        self.assertEqual( trait_stored_name, should_be, msg = error_string )
        
        # slug
        should_be = entity_type_trait.slug
        error_string = "trait slug {} --> should be {}".format( trait_stored_slug, should_be )
        self.assertEqual( trait_stored_slug, should_be, msg = error_string )
        
        # label
        should_be = entity_type_trait.label
        error_string = "trait label {} --> should be {}".format( trait_stored_label, should_be )
        self.assertEqual( trait_stored_label, should_be, msg = error_string )
        
        # value should be set, too.
        should_be = trait_value
        error_string = "trait value {} --> should be {}".format( trait_stored_value, should_be )
        self.assertEqual( trait_stored_value, should_be, msg = error_string )
        
        # update the trait's value.  Make sure the value changes.
        trait_name = entity_type_trait.name
        trait_value = "Percy"
        trait_instance = entity_instance.set_entity_trait( trait_name, value_IN = trait_value, entity_type_trait_IN = entity_type_trait )
        trait_stored_id = trait_instance.id
        trait_stored_name = trait_instance.name
        trait_stored_value = trait_instance.value
        trait_stored_slug = trait_instance.slug
        trait_stored_label = trait_instance.label
        
        # check trait count
        trait_qs = entity_instance.entity_trait_set.all()
        trait_count = trait_qs.count()
        should_be = 2
        error_string = "trait count {} should = {}".format( trait_count, should_be )
        self.assertEqual( trait_count, should_be, msg = error_string )

        # stored id, name, slug, and label should be set from specification.
        should_be = entity_type_trait.name
        error_string = "trait name {} --> should be {}".format( trait_stored_name, should_be )
        self.assertEqual( trait_stored_name, should_be, msg = error_string )
                
        # id
        should_be = original_trait_id
        error_string = "trait id {} --> should be {}".format( trait_stored_id, should_be )
        self.assertEqual( trait_stored_id, should_be, msg = error_string )

        # slug
        should_be = entity_type_trait.slug
        error_string = "trait slug {} --> should be {}".format( trait_stored_slug, should_be )
        self.assertEqual( trait_stored_slug, should_be, msg = error_string )
        
        # label
        should_be = entity_type_trait.label
        error_string = "trait label {} --> should be {}".format( trait_stored_label, should_be )
        self.assertEqual( trait_stored_label, should_be, msg = error_string )
        
        # value should be set, too.
        should_be = trait_value
        error_string = "trait value {} --> should be {}".format( trait_stored_value, should_be )
        self.assertEqual( trait_stored_value, should_be, msg = error_string )

        # and value should not be original value.
        should_not_be = original_trait_value
        error_string = "trait value {} --> should NOT be {}".format( trait_stored_value, should_not_be )
        self.assertNotEqual( trait_stored_value, should_not_be, msg = error_string )

        # add a trait with a trait type that includes a vocabulary, and then a term...?
        
    #-- END test method test_set_entity_trait() --#


    def test_set_identifier( self ):

        # declare variables
        me = "test_set_identifier"
        entity_instance = None
        entity_type = None
        id_name = None
        id_uuid = None
        id_instance = None
        id_stored_name = None
        id_stored_uuid = None
        id_stored_source = None
        id_id = None
        id_qs = None
        id_count = None
        entity_identifier_type = None
        original_id_id = None
        original_id_uuid = None

        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )

        # build a "person" entity.
        entity_instance = TestHelper.create_test_entity()
        entity_type = entity_instance.add_entity_type( TestHelper.ENTITY_TYPE_SLUG_PERSON )
        
        # add a new identifier from scratch (nickname).
        id_name = self.TEST_IDENTIFIER_NAME
        id_uuid = "Jon-a-no-fun"
        id_instance = entity_instance.set_identifier( id_uuid, name_IN = id_name )
        id_stored_name = id_instance.name
        
        # instance should not be None
        error_string = "Creating identifier should return Entity_Identifier instance, not None"
        self.assertIsNotNone( id_instance, msg = error_string )

        # retrieve identifier
        id_qs = entity_instance.entity_identifier_set.filter( name = id_name )
        id_count = id_qs.count()
        should_be = 1
        error_string = "identifier with name {} --> count {} should = {}".format( id_name, id_count, should_be )
        self.assertEqual( id_count, should_be, msg = error_string )

        # ! ----> create an identifier with a type.
        
        # create an identifier with a type.  Make sure the meta-information was updated.
        id_name = "SSN"
        id_uuid = "123456789"
        original_id_uuid = id_uuid
        entity_identifier_type = Entity_Identifier_Type.get_type_for_name( TestHelper.ID_TYPE_NAME_SOURCENET )
        id_instance = entity_instance.set_identifier( id_uuid, name_IN = id_name, entity_identifier_type_IN = entity_identifier_type )
        original_id_id = id_instance.id
        id_stored_name = id_instance.name
        id_stored_source = id_instance.source
        id_stored_uuid = id_instance.uuid
        
        # check id count
        id_qs = entity_instance.entity_identifier_set.all()
        id_count = id_qs.count()
        should_be = 2
        error_string = "identifier count {} should = {}".format( id_count, should_be )
        self.assertEqual( id_count, should_be, msg = error_string )

        # stored name, source, and id_type should be set from specification.
        should_be = entity_identifier_type.name
        error_string = "identifier name {} --> should be {}".format( id_stored_name, should_be )
        self.assertEqual( id_stored_name, should_be, msg = error_string )
        
        # source
        should_be = entity_identifier_type.source
        error_string = "identifier source {} --> should be {}".format( id_stored_source, should_be )
        self.assertEqual( id_stored_source, should_be, msg = error_string )
        
        # value should be set, too.
        should_be = id_uuid
        error_string = "identifier UUID {} --> should be {}".format( id_stored_uuid, should_be )
        self.assertEqual( id_stored_uuid, should_be, msg = error_string )
        
        # ! ----> update the identifier's UUID.  Make sure the value changes.
        id_name = entity_identifier_type.name
        id_uuid = "6"
        id_instance = entity_instance.set_identifier( id_uuid, name_IN = id_name, entity_identifier_type_IN = entity_identifier_type )
        id_stored_id = id_instance.id
        id_stored_name = id_instance.name
        id_stored_source = id_instance.source
        id_stored_uuid = id_instance.uuid
        
        # check id count
        id_qs = entity_instance.entity_identifier_set.all()
        id_count = id_qs.count()
        should_be = 2
        error_string = "identifier count {} should = {}".format( id_count, should_be )
        self.assertEqual( id_count, should_be, msg = error_string )

        # stored name, source, and id_type should be set from specification, id
        #     should be same as last time.
        should_be = entity_identifier_type.name
        error_string = "identifier name {} --> should be {}".format( id_stored_name, should_be )
        self.assertEqual( id_stored_name, should_be, msg = error_string )
        
        # source
        should_be = entity_identifier_type.source
        error_string = "identifier source {} --> should be {}".format( id_stored_source, should_be )
        self.assertEqual( id_stored_source, should_be, msg = error_string )
        
        # value should be set, too.
        should_be = id_uuid
        error_string = "identifier UUID {} --> should be {}".format( id_stored_uuid, should_be )
        self.assertEqual( id_stored_uuid, should_be, msg = error_string )

        # id
        should_be = original_id_id
        error_string = "identifier id {} --> should be {} (same record, different value)".format( id_stored_id, should_be )
        self.assertEqual( id_stored_id, should_be, msg = error_string )

        # and value should not be original value.
        should_not_be = original_id_uuid
        error_string = "trait value {} --> should NOT be {}".format( id_stored_uuid, should_not_be )
        self.assertNotEqual( id_stored_uuid, should_not_be, msg = error_string )

        # ! ----> create an identifier with a type, override source.
        
        # create an identifier with a type.  Make sure the meta-information was updated.
        id_name = "opencalais_ID"
        id_uuid = "1234567abcdefgjlmnqrswz"
        id_source = "all_trains"
        original_id_uuid = id_uuid
        entity_identifier_type = Entity_Identifier_Type.get_type_for_name( TestHelper.ID_TYPE_NAME_OPENCALAIS )
        id_instance = entity_instance.set_identifier( id_uuid, name_IN = id_name, source_IN = id_source, entity_identifier_type_IN = entity_identifier_type )
        original_id_id = id_instance.id
        id_stored_name = id_instance.name
        id_stored_source = id_instance.source
        id_stored_uuid = id_instance.uuid
        
        # check id count
        id_qs = entity_instance.entity_identifier_set.all()
        id_count = id_qs.count()
        should_be = 3
        error_string = "identifier count {} should = {}".format( id_count, should_be )
        self.assertEqual( id_count, should_be, msg = error_string )

        # stored name, source, and id_type should be set from specification.
        should_be = entity_identifier_type.name
        error_string = "identifier name {} --> should be {}".format( id_stored_name, should_be )
        self.assertEqual( id_stored_name, should_be, msg = error_string )
        
        # source
        should_be = id_source
        error_string = "identifier source {} --> should be {}".format( id_stored_source, should_be )
        self.assertEqual( id_stored_source, should_be, msg = error_string )
        
        # value should be set, too.
        should_be = id_uuid
        error_string = "identifier UUID {} --> should be {}".format( id_stored_uuid, should_be )
        self.assertEqual( id_stored_uuid, should_be, msg = error_string )
        
        # ! TODO - add a trait with a trait type that includes a vocabulary, and then a term...?
        
    #-- END test method test_set_identifier() --#


#-- END test class EntityModelTest --#
