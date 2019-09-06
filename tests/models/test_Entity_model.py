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


class EntityModelTest( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ----> Constants-ish
    #----------------------------------------------------------------------------


    # CLASS NAME
    CLASS_NAME = "EntityModelTest"

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
    
    # Entity Type slugs
    ENTITY_TYPE_SLUG_PERSON = "person"
    ENTITY_TYPE_SLUG_ARTICLE = "article"
    ENTITY_TYPE_SLUG_NEWSPAPER = "newspaper"
    
    # Entity Trait names
    TEST_ENTITY_TRAIT_NAME = "flibble_glibble_pants"
    ENTITY_TRAIT_NAME_FIRST_NAME = "first_name"
    ENTITY_TRAIT_NAME_MIDDLE_NAME = "middle_name"
    ENTITY_TRAIT_NAME_LAST_NAME = "last_name"
    
    # Identifier names
    TEST_IDENTIFIER_NAME = "nickname"
    
    # identifier type names
    ID_TYPE_NAME_SOURCENET = "person_sourcenet_id"
    ID_TYPE_NAME_OPENCALAIS = "person_open_calais_uuid"


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
        
        print( '====> In {}.{}'.format( self.CLASS_NAME, me ) )
        
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
        type_qs = None
        type_count = None
        should_be = None

        print( '====> In {}.{}'.format( self.CLASS_NAME, me ) )

        # create test entity
        entity_instance = TestHelper.create_test_entity()
        
        # add a type to an entity.
        type_slug_1 = self.ENTITY_TYPE_SLUG_ARTICLE
        entity_instance.add_entity_type( type_slug_1 )
        
        # make sure it is present in the entity's type set.
        type_qs = entity_instance.my_entity_types.filter( slug = type_slug_1 )
        type_count = type_qs.count()
        should_be = 1
        error_string = "type 1: {} --> count {} should = {}".format( type_slug_1, type_count, should_be )
        self.assertEqual( type_count, should_be, msg = error_string )
        
        # add a second.
        type_slug_2 = self.ENTITY_TYPE_SLUG_NEWSPAPER
        entity_instance.add_entity_type( type_slug_2 )
        
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


    def test_set_entity_trait( self ):

        '''
        Things to test passing to the method:
            def set_entity_trait( self,
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

        print( '====> In {}.{}'.format( self.CLASS_NAME, me ) )

        # build a "person" entity.
        entity_instance = TestHelper.create_test_entity()
        entity_type = entity_instance.add_entity_type( self.ENTITY_TYPE_SLUG_PERSON )
        
        # add a new trait from scratch (flibble_glibble_pants).
        trait_name = self.TEST_ENTITY_TRAIT_NAME
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
        entity_type_trait = entity_type.get_trait_spec( self.ENTITY_TRAIT_NAME_FIRST_NAME )
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

        print( '====> In {}.{}'.format( self.CLASS_NAME, me ) )

        # build a "person" entity.
        entity_instance = TestHelper.create_test_entity()
        entity_type = entity_instance.add_entity_type( self.ENTITY_TYPE_SLUG_PERSON )
        
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

        # create an identifier with a type.  Make sure the meta-information was updated.
        id_name = "SSN"
        id_uuid = "123456789"
        original_id_uuid = id_uuid
        entity_identifier_type = Entity_Identifier_Type.get_type_for_name( self.ID_TYPE_NAME_SOURCENET )
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
        
        # update the identifier's UUID.  Make sure the value changes.
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

        # add a trait with a trait type that includes a vocabulary, and then a term...?
        
    #-- END test method test_set_identifier() --#


#-- END test class Entity_Identifier_TypeModelTest --#
