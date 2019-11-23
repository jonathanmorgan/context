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
import six

# Django imports
from django.contrib.auth.models import User
from django.core.management import call_command

# import basic django configuration application.
from django_config.models import Config_Property

# python_utilities - logging
from python_utilities.exceptions.exception_helper import ExceptionHelper
from python_utilities.logging.logging_helper import LoggingHelper

# context_text imports
from context.models import Entity
from context.models import Entity_Identifier
from context.models import Entity_Relation
from context.models import Entity_Relation_Trait
from context.models import Entity_Trait

#===============================================================================
# Shared variables and functions
#===============================================================================


#===============================================================================
# classes (in alphabetical order by name)
#===============================================================================

class TestHelper( object ):

    
    #---------------------------------------------------------------------------
    # ! ==> CONSTANTS-ish
    #---------------------------------------------------------------------------


    # fixtures paths, in order they should be loaded.
    FIXTURE_UNIT_TEST_CONTEXT_METADATA = "context-sourcenet_entities_and_relations.json"
    FIXTURE_LIST = []
    FIXTURE_LIST.append( FIXTURE_UNIT_TEST_CONTEXT_METADATA )
    
    # Test user
    TEST_USER_NAME = "test_user"
    TEST_USER_EMAIL = "test@email.com"
    TEST_USER_PASSWORD = "calliope"
    
    #---------------------------------------------------------------------------
    # ! ----> Entity

    # Test Entity information
    TEST_ENTITY_NAME = "calliope"
    
    # Test Entity_Identifier default information
    TEST_ENTITY_IDENTIFIER_NAME = "calliope_type"
    TEST_ENTITY_IDENTIFIER_UUID = "123456"
    TEST_ENTITY_IDENTIFIER_ID_TYPE = "made-up"
    TEST_ENTITY_IDENTIFIER_SOURCE = "my_brain"
    TEST_ENTITY_IDENTIFIER_NOTE = "default initialization notes"

    # Entity_Identifier names
    TEST_IDENTIFIER_NAME = "nickname"    
    
    # Entity_Identifier type names
    ID_TYPE_NAME_SOURCENET = "person_sourcenet_id"
    ID_TYPE_NAME_OPENCALAIS = "person_open_calais_uuid"

    # identifier type names
    ID_TYPE_NAME_ARTICLE_NEWSBANK_ID = "article_newsbank_id"
    ID_TYPE_NAME_ARTICLE_SOURCENET_ID = "article_sourcenet_id"
    ID_TYPE_NAME_PERSON_OPEN_CALAIS_UUID = ID_TYPE_NAME_OPENCALAIS    
    ID_TYPE_NAME_PERSON_SOURCENET_ID = ID_TYPE_NAME_SOURCENET
    ID_TYPE_NAME_DOES_NOT_EXIST = "calliope_tree_frog"
    
    # map of identifier type names to test IDs
    ID_TYPE_NAME_TO_ID_MAP = {}
    ID_TYPE_NAME_TO_ID_MAP[ ID_TYPE_NAME_PERSON_SOURCENET_ID ] = 1
    ID_TYPE_NAME_TO_ID_MAP[ ID_TYPE_NAME_PERSON_OPEN_CALAIS_UUID ] = 2
    ID_TYPE_NAME_TO_ID_MAP[ ID_TYPE_NAME_ARTICLE_SOURCENET_ID ] = 3
    ID_TYPE_NAME_TO_ID_MAP[ ID_TYPE_NAME_ARTICLE_NEWSBANK_ID ] = 4

    # Entity_Identifier no-match values
    ENTITY_ID_UUID_NO_MATCH = "calliope_1234567890"
    ENTITY_ID_NAME_NO_MATCH = "hunterlane"
    ENTITY_ID_SOURCE_NO_MATCH = "chiquita_brain_fuel"
    ENTITY_ID_ID_TYPE_NO_MATCH = "shady_salads"
    ENTITY_ID_NOTES_NO_MATCH = "these notes should not match."
    
    # Test Entity_Trait default information
    TEST_ENTITY_TRAIT_NAME = "calliope_status"
    TEST_ENTITY_TRAIT_SLUG = TEST_ENTITY_TRAIT_NAME
    TEST_ENTITY_TRAIT_VALUE = "calliope_status_value"
    TEST_ENTITY_TRAIT_VALUE_JSON = '{ "calliope_status": "calliope_status_value" }'
    TEST_ENTITY_TRAIT_LABEL = "important"
    TEST_ENTITY_TRAIT_DESCRIPTION = "The calliope status for this important thing."
    
    # Entity_Trait no-match values
    ENTITY_TRAIT_NAME_NO_MATCH = "garbleflarbleflub"
    ENTITY_TRAIT_SLUG_NO_MATCH = "garbleflarbleflubstub"
    ENTITY_TRAIT_LABEL_NO_MATCH = "garbleflarbleflubstubstomp"
    
    # Entity_Type slugs
    ENTITY_TYPE_SLUG_PERSON = "person"
    ENTITY_TYPE_SLUG_ARTICLE = "article"
    ENTITY_TYPE_SLUG_NEWSPAPER = "newspaper"
    
    #---------------------------------------------------------------------------
    # ! ----> Traits    
    
    # Trait names
    TRAIT_NAME_GIBBERISH = "flibble_glibble_pants"
    ENTITY_TRAIT_NAME_GIBBERISH = TRAIT_NAME_GIBBERISH
    ENTITY_TRAIT_NAME_FIRST_NAME = "first_name"
    ENTITY_TRAIT_NAME_MIDDLE_NAME = "middle_name"
    ENTITY_TRAIT_NAME_LAST_NAME = "last_name"
    ENTITY_RELATION_TRAIT_NAME_PUB_DATE = "pub_date"
    ENTITY_RELATION_TRAIT_NAME_NEWSPAPER_ID = "sourcenet-Newspaper-ID"
    
    # Trait values
    TRAIT_VALUE_GIBBERISH = "glarbleblarg"
    TRAIT_VALUE_123456 = "123456"
    TRAIT_VALUE_19230521 = "1923-05-21"
    TRAIT_VALUE_19230522 = "1923-05-22"
    TRAIT_VALUE_19230523 = "1923-05-23"
    
    #---------------------------------------------------------------------------
    # ! ----> Entity_Relation

     # Entity_Relation_Type slugs - FROM NEWSPAPER
    CONTEXT_RELATION_TYPE_SLUG_NEWSPAPER_ARTICLE = "newspaper_article"    # FROM newspaper TO article.
    CONTEXT_RELATION_TYPE_SLUG_NEWSPAPER_REPORTER = "newspaper_reporter"  # FROM newspaper TO person (reporter) THROUGH article.
    CONTEXT_RELATION_TYPE_SLUG_NEWSPAPER_SOURCE = "newspaper_source"      # FROM newspaper TO person (source) THROUGH article.
    CONTEXT_RELATION_TYPE_SLUG_NEWSPAPER_SUBJECT = "newspaper_subject"    # FROM newspaper TO person (subject, including sources) THROUGH article.

    # Entity_Relation_Type slugs - FROM ARTICLE
    CONTEXT_RELATION_TYPE_SLUG_AUTHOR = "author"    # FROM article TO reporter.
    CONTEXT_RELATION_TYPE_SLUG_SOURCE = "source"    # FROM article TO source person.
    CONTEXT_RELATION_TYPE_SLUG_SUBJECT = "subject"  # FROM article TO subject person.
    
    # Entity_Relation_Type slugs - THROUGH ARTICLE    
    CONTEXT_RELATION_TYPE_SLUG_MENTIONED = "mentioned"                          # FROM reporter/author TO subject THROUGH article (includes subjects and sources).
    CONTEXT_RELATION_TYPE_SLUG_QUOTED = "quoted"                                # FROM reporter TO source THROUGH article.
    CONTEXT_RELATION_TYPE_SLUG_SAME_ARTICLE_SOURCES = "same_article_sources"    # FROM source person TO source person THROUGH article.
    CONTEXT_RELATION_TYPE_SLUG_SAME_ARTICLE_SUBJECTS = "same_article_subjects"  # FROM subject person TO subject person THROUGH article (includes subjects and sources).
    CONTEXT_RELATION_TYPE_SLUG_SHARED_BYLINE = "shared_byline"                  # FROM author TO author THROUGH article.

    # Test Entity Names
    ENTITY_NUMBER_TO_NAME_MAP = {}
    ENTITY_NUMBER_TO_NAME_MAP[ 1 ] = "test_entity_1"
    ENTITY_NUMBER_TO_NAME_MAP[ 2 ] = "test_entity_2"
    ENTITY_NUMBER_TO_NAME_MAP[ 3 ] = "test_entity_3"
    ENTITY_NUMBER_TO_NAME_MAP[ 4 ] = "test_entity_4"
    ENTITY_NUMBER_TO_NAME_MAP[ 5 ] = "test_entity_5"
    ENTITY_NUMBER_TO_NAME_MAP[ 6 ] = "test_entity_6"
    ENTITY_NUMBER_TO_NAME_MAP[ 7 ] = "test_entity_7"
    ENTITY_NUMBER_TO_NAME_MAP[ 8 ] = "test_entity_8"
    ENTITY_NUMBER_TO_NAME_MAP[ 9 ] = "test_entity_9"
    ENTITY_NUMBER_TO_NAME_MAP[ 10 ] = "test_entity_10"
    ENTITY_NUMBER_TO_NAME_MAP[ 11 ] = "test_entity_11"
    ENTITY_NUMBER_TO_NAME_MAP[ 12 ] = "test_entity_12"

    # Entity Types
    ENTITY_NUMBER_TO_TYPE_MAP = {}
    ENTITY_NUMBER_TO_TYPE_MAP[ 1 ] = ENTITY_TYPE_SLUG_PERSON
    ENTITY_NUMBER_TO_TYPE_MAP[ 2 ] = ENTITY_TYPE_SLUG_PERSON
    ENTITY_NUMBER_TO_TYPE_MAP[ 3 ] = ENTITY_TYPE_SLUG_PERSON
    ENTITY_NUMBER_TO_TYPE_MAP[ 4 ] = ENTITY_TYPE_SLUG_ARTICLE
    ENTITY_NUMBER_TO_TYPE_MAP[ 5 ] = ENTITY_TYPE_SLUG_PERSON
    ENTITY_NUMBER_TO_TYPE_MAP[ 6 ] = ENTITY_TYPE_SLUG_PERSON
    ENTITY_NUMBER_TO_TYPE_MAP[ 7 ] = ENTITY_TYPE_SLUG_PERSON
    ENTITY_NUMBER_TO_TYPE_MAP[ 8 ] = ENTITY_TYPE_SLUG_PERSON
    ENTITY_NUMBER_TO_TYPE_MAP[ 9 ] = ENTITY_TYPE_SLUG_PERSON
    ENTITY_NUMBER_TO_TYPE_MAP[ 10 ] = ENTITY_TYPE_SLUG_PERSON
    ENTITY_NUMBER_TO_TYPE_MAP[ 11 ] = ENTITY_TYPE_SLUG_NEWSPAPER
    ENTITY_NUMBER_TO_TYPE_MAP[ 12 ] = ENTITY_TYPE_SLUG_ARTICLE

    #----------------------------------------------------------------------------
    # ! ==> Class variables
    # - overriden by __init__() per instance if same names, but if not set
    #     there, shared!
    #----------------------------------------------------------------------------

    
    DEBUG = True
    
    # store references to relation test data.
    test_entity_number_to_instance_map = {}
    test_relation_list = []
    

    #-----------------------------------------------------------------------------
    # ! ==> class methods
    #-----------------------------------------------------------------------------


    @classmethod
    def create_test_entities( cls ):
    
        '''
        Creates test entities based on associated ENTITY_NUMBER_TO_NAME_MAP and
            ENTITY_NUMBER_TO_TYPE_MAP dictionaries which map numbers to names
            and types.  Loops over the keys in one of the maps, making an entity
            for each key.
        '''

        # declare variables
        me = "create_test_data"
        test_entity_count = None
        entity_type_slug = None
        entity_name = None
        entity_number = None
        entity_instance = None
        
        # first, see if we already have this data created.
        test_entity_count = len( cls.test_entity_number_to_instance_map )
        if ( test_entity_count == 0 ):
        
            # ! ----> create entities.
            
            # loop over the items in cls.ENTITY_NUMBER_TO_NAME_MAP
            for entity_number, entity_name in six.iteritems( cls.ENTITY_NUMBER_TO_NAME_MAP ):
            
                # get type slug
                entity_type_slug = cls.ENTITY_NUMBER_TO_TYPE_MAP[ entity_number ]
                
                # create entity
                entity_instance = TestHelper.create_test_entity( entity_type_slug_IN = entity_type_slug,
                                                                 entity_name_IN = entity_name )
    
                # store it.
                cls.test_entity_number_to_instance_map[ entity_number ] = entity_instance
                
            #-- END loop over names and indexes of entities to create --#
            
        #-- END check to see if entities already created. --#

    #-- END class method create_test_entities() --#


    @classmethod
    def create_test_entity( cls, entity_type_slug_IN = None, entity_name_IN = None, trait_dict_IN = None ):
        
        # return reference
        instance_OUT = None
        
        # declare variables
        entity_instance = None
        
        # create entity
        entity_instance = Entity()
        
        # set some values
        if ( ( entity_name_IN is not None ) and ( entity_name_IN != "" ) ):
        
            # use name passed in.
            entity_instance.name = entity_name_IN
            
        else:
        
            # use default
            entity_instance.name = cls.TEST_ENTITY_NAME
            
        #-- END check to see if name passed in. --#
            
        # save
        entity_instance.save()
        
        if ( ( entity_type_slug_IN is not None ) and ( entity_type_slug_IN != "" ) ):
        
            # we do.  Add entity type.
            entity_instance.add_entity_type( entity_type_slug_IN )
        
        #-- END check to see if we assign an entity type --#
        
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


    @classmethod
    def create_test_entity_trait( cls, entity_instance_IN ):
        
        '''
        Contents:
        
        #entity = models.ForeignKey( "Entity", on_delete = models.CASCADE )
        name = models.CharField( max_length = 255 )
        slug = models.SlugField( blank = True, null = True )
        value = models.CharField( max_length = 255, blank = True, null = True )
        value_json = JSONField( blank = True, null = True )
        label = models.CharField( max_length = 255, blank = True, null = True )
        description = models.TextField( blank = True )
    
        # context
        trait_type = models.ForeignKey( "Trait_Type", on_delete = models.SET_NULL, blank = True, null = True )
        term = models.ForeignKey( "Term", on_delete = models.SET_NULL, blank = True, null = True )
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        trait_instance = None
        
        # create entity
        trait_instance = Entity_Trait()
        
        # set some values
        trait_instance.name = cls.TEST_ENTITY_TRAIT_NAME
        trait_instance.slug = cls.TEST_ENTITY_TRAIT_SLUG
        trait_instance.value = cls.TEST_ENTITY_TRAIT_VALUE
        trait_instance.value_json = cls.TEST_ENTITY_TRAIT_VALUE_JSON
        trait_instance.label = cls.TEST_ENTITY_TRAIT_LABEL
        trait_instance.description = cls.TEST_ENTITY_TRAIT_DESCRIPTION
        trait_instance.entity = entity_instance_IN
        trait_instance.save()
        
        # return it
        instance_OUT = trait_instance
        return instance_OUT

    #-- END method create_test_entity_trait() --#


    @classmethod
    def create_test_relation_trait( cls, relation_instance_IN ):
        
        '''
        Contents:
        
        #entity = models.ForeignKey( "Entity", on_delete = models.CASCADE )
        name = models.CharField( max_length = 255 )
        slug = models.SlugField( blank = True, null = True )
        value = models.CharField( max_length = 255, blank = True, null = True )
        value_json = JSONField( blank = True, null = True )
        label = models.CharField( max_length = 255, blank = True, null = True )
        description = models.TextField( blank = True )
    
        # context
        trait_type = models.ForeignKey( "Trait_Type", on_delete = models.SET_NULL, blank = True, null = True )
        term = models.ForeignKey( "Term", on_delete = models.SET_NULL, blank = True, null = True )
        '''
        
        # return reference
        instance_OUT = None
        
        # declare variables
        trait_instance = None
        
        # create entity
        trait_instance = Entity_Relation_Trait()
        
        # set some values
        trait_instance.name = cls.TEST_ENTITY_TRAIT_NAME
        trait_instance.slug = cls.TEST_ENTITY_TRAIT_SLUG
        trait_instance.value = cls.TEST_ENTITY_TRAIT_VALUE
        trait_instance.value_json = cls.TEST_ENTITY_TRAIT_VALUE_JSON
        trait_instance.label = cls.TEST_ENTITY_TRAIT_LABEL
        trait_instance.description = cls.TEST_ENTITY_TRAIT_DESCRIPTION
        trait_instance.entity_relation = relation_instance_IN
        trait_instance.save()
        
        # return it
        instance_OUT = trait_instance
        return instance_OUT

    #-- END method create_test_relation_trait() --#


    @classmethod
    def create_test_relations( cls ):
    
        '''
        Creates 4 test entities, then the following relations:

        - FROM 4 TO 1           - type "author" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_AUTHOR )
        - FROM 4 to 2           - type "subject" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_SUBJECT )
        - FROM 4 to 3           - type "source" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_SOURCE )
        - FROM 1 TO 2 THROUGH 4 - type "mentioned" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_MENTIONED )
        - FROM 1 TO 3 THROUGH 4 - type "mentioned" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_MENTIONED )
        - FROM 1 TO 3 THROUGH 4 - type "quoted" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        - FROM 2 to 3 THROUGH 4 - type "same_article_subjects" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_SAME_ARTICLE_SUBJECTS )
        
        '''

        # declare variables
        me = "create_test_data"
        test_entity_count = None
        entity_type_slug = None
        entity_name = None
        entity_number = None
        entity_instance = None
        relation_from_number = None
        relation_to_number = None
        relation_through_number = None
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type_slug = None
        relation_traits = None
        trait_name = None
        trait_value = None
        relation_instance = None
        
        # check to see if 
        test_entity_count = len( cls.test_entity_number_to_instance_map )
        if ( test_entity_count == 0 ):
        
            # ! ----> create entities.
            cls.create_test_entities()
            
            # loop over the items in cls.ENTITY_NUMBER_TO_NAME_MAP
            for entity_number, entity_name in six.iteritems( cls.ENTITY_NUMBER_TO_NAME_MAP ):
            
                # get type slug
                entity_type_slug = cls.ENTITY_NUMBER_TO_TYPE_MAP[ entity_number ]
                
                # create entity
                entity_instance = TestHelper.create_test_entity( entity_type_slug_IN = entity_type_slug,
                                                                 entity_name_IN = entity_name )
    
                # store it.
                cls.test_entity_number_to_instance_map[ entity_number ] = entity_instance
                
            #-- END loop over names and indexes of entities to create --#
                 
            # ! ----> create relations.
            
            #----------------------------------------------------------------------#
            # ! --------> FROM 4 TO 1 - type "author" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_AUTHOR )
            relation_from_number = 4
            relation_to_number = 1
            relation_through_number = None
            relation_type_slug = cls.CONTEXT_RELATION_TYPE_SLUG_AUTHOR
            relation_traits = None
            
            # add a couple of traits
            relation_traits = {}
            
            # add a new trait from scratch (flibble_glibble_pants).
            trait_name = cls.ENTITY_RELATION_TRAIT_NAME_NEWSPAPER_ID
            trait_value = cls.TRAIT_VALUE_123456
            relation_traits[ trait_name ] = trait_value
        
            # trait with a type specification.  Make sure the meta-information was updated.
            trait_name = cls.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
            trait_value = cls.TRAIT_VALUE_19230521
            relation_traits[ trait_name ] = trait_value
            
            # pull in entities
            relation_from = cls.test_entity_number_to_instance_map.get( relation_from_number, None )
            relation_to = cls.test_entity_number_to_instance_map.get( relation_to_number, None )
            if relation_through_number is not None:
                relation_through = cls.test_entity_number_to_instance_map.get( relation_through_number, None )
            #-- END check to see if we are going THROUGH --#
    
            # create and store relation
            relation_instance = Entity_Relation.create_entity_relation( relation_from,
                                                                        relation_to,
                                                                        through_IN = relation_through,
                                                                        type_slug_IN = relation_type_slug,
                                                                        trait_name_to_value_map_IN = relation_traits )
            cls.test_relation_list.append( relation_instance )
            
            #----------------------------------------------------------------------#
            # ! --------> FROM 4 to 2 - type "subject" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_SUBJECT )
            relation_from_number = 4
            relation_to_number = 2
            relation_through_number = None
            relation_type_slug = cls.CONTEXT_RELATION_TYPE_SLUG_SUBJECT
            relation_traits = None
            
            # add a couple of traits
            relation_traits = {}
            
            # add a new trait from scratch (flibble_glibble_pants).
            trait_name = cls.ENTITY_RELATION_TRAIT_NAME_NEWSPAPER_ID
            trait_value = cls.TRAIT_VALUE_123456
            relation_traits[ trait_name ] = trait_value
        
            # add a new trait from scratch (flibble_glibble_pants).
            trait_name = cls.TRAIT_NAME_GIBBERISH
            trait_value = cls.TRAIT_VALUE_GIBBERISH
            relation_traits[ trait_name ] = trait_value

            # trait with a type specification.  Make sure the meta-information was updated.
            trait_name = cls.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
            trait_value = cls.TRAIT_VALUE_19230521
            relation_traits[ trait_name ] = trait_value
            
            # pull in entities
            relation_from = cls.test_entity_number_to_instance_map.get( relation_from_number, None )
            relation_to = cls.test_entity_number_to_instance_map.get( relation_to_number, None )
            if relation_through_number is not None:
                relation_through = cls.test_entity_number_to_instance_map.get( relation_through_number, None )
            #-- END check to see if we are going THROUGH --#
    
            # create and store relation
            relation_instance = Entity_Relation.create_entity_relation( relation_from,
                                                                        relation_to,
                                                                        through_IN = relation_through,
                                                                        type_slug_IN = relation_type_slug,
                                                                        trait_name_to_value_map_IN = relation_traits )
            cls.test_relation_list.append( relation_instance )
            
            #----------------------------------------------------------------------#
            # ! --------> FROM 4 to 3 - type "source" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_SOURCE )
            relation_from_number = 4
            relation_to_number = 3
            relation_through_number = None
            relation_type_slug = cls.CONTEXT_RELATION_TYPE_SLUG_SOURCE
            relation_traits = None
            
            # add a couple of traits
            relation_traits = {}
            
            # add a new trait from scratch (flibble_glibble_pants).
            trait_name = cls.ENTITY_RELATION_TRAIT_NAME_NEWSPAPER_ID
            trait_value = cls.TRAIT_VALUE_123456
            relation_traits[ trait_name ] = trait_value
        
            # trait with a type specification.  Make sure the meta-information was updated.
            trait_name = cls.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
            trait_value = cls.TRAIT_VALUE_19230522
            relation_traits[ trait_name ] = trait_value
            
            # pull in entities
            relation_from = cls.test_entity_number_to_instance_map.get( relation_from_number, None )
            relation_to = cls.test_entity_number_to_instance_map.get( relation_to_number, None )
            if relation_through_number is not None:
                relation_through = cls.test_entity_number_to_instance_map.get( relation_through_number, None )
            #-- END check to see if we are going THROUGH --#
    
            # create and store relation
            relation_instance = Entity_Relation.create_entity_relation( relation_from,
                                                                        relation_to,
                                                                        through_IN = relation_through,
                                                                        type_slug_IN = relation_type_slug,
                                                                        trait_name_to_value_map_IN = relation_traits )
            cls.test_relation_list.append( relation_instance )
    
            #----------------------------------------------------------------------#
            # ! --------> FROM 1 TO 2 THROUGH 4 - type "mentioned" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_MENTIONED )
            relation_from_number = 1
            relation_to_number = 2
            relation_through_number = 4
            relation_type_slug = cls.CONTEXT_RELATION_TYPE_SLUG_MENTIONED
            relation_traits = None
            
            # pull in entities
            relation_from = cls.test_entity_number_to_instance_map.get( relation_from_number, None )
            relation_to = cls.test_entity_number_to_instance_map.get( relation_to_number, None )
            if relation_through_number is not None:
                relation_through = cls.test_entity_number_to_instance_map.get( relation_through_number, None )
            #-- END check to see if we are going THROUGH --#
    
            # create and store relation
            relation_instance = Entity_Relation.create_entity_relation( relation_from,
                                                                        relation_to,
                                                                        through_IN = relation_through,
                                                                        type_slug_IN = relation_type_slug,
                                                                        trait_name_to_value_map_IN = relation_traits )
            cls.test_relation_list.append( relation_instance )
            
            #----------------------------------------------------------------------#
            # ! --------> FROM 1 TO 3 THROUGH 4 - type "mentioned" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_MENTIONED )
            relation_from_number = 1
            relation_to_number = 3
            relation_through_number = 4
            relation_type_slug = cls.CONTEXT_RELATION_TYPE_SLUG_MENTIONED
            relation_traits = None
            
            # pull in entities
            relation_from = cls.test_entity_number_to_instance_map.get( relation_from_number, None )
            relation_to = cls.test_entity_number_to_instance_map.get( relation_to_number, None )
            if relation_through_number is not None:
                relation_through = cls.test_entity_number_to_instance_map.get( relation_through_number, None )
            #-- END check to see if we are going THROUGH --#
    
            # create and store relation
            relation_instance = Entity_Relation.create_entity_relation( relation_from,
                                                                        relation_to,
                                                                        through_IN = relation_through,
                                                                        type_slug_IN = relation_type_slug,
                                                                        trait_name_to_value_map_IN = relation_traits )
            cls.test_relation_list.append( relation_instance )
    
            #----------------------------------------------------------------------#
            # ! --------> FROM 1 TO 3 THROUGH 4 - type "quoted" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
            relation_from_number = 1
            relation_to_number = 3
            relation_through_number = 4
            relation_type_slug = cls.CONTEXT_RELATION_TYPE_SLUG_QUOTED
            relation_traits = None
            
            # pull in entities
            relation_from = cls.test_entity_number_to_instance_map.get( relation_from_number, None )
            relation_to = cls.test_entity_number_to_instance_map.get( relation_to_number, None )
            if relation_through_number is not None:
                relation_through = cls.test_entity_number_to_instance_map.get( relation_through_number, None )
            #-- END check to see if we are going THROUGH --#
    
            # create and store relation
            relation_instance = Entity_Relation.create_entity_relation( relation_from,
                                                                        relation_to,
                                                                        through_IN = relation_through,
                                                                        type_slug_IN = relation_type_slug,
                                                                        trait_name_to_value_map_IN = relation_traits )
            cls.test_relation_list.append( relation_instance )
            
            #----------------------------------------------------------------------#
            # ! --------> FROM 2 to 3 THROUGH 4 - type "same_article_subjects" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_SAME_ARTICLE_SUBJECTS )
            relation_from_number = 2
            relation_to_number = 3
            relation_through_number = 4
            relation_type_slug = cls.CONTEXT_RELATION_TYPE_SLUG_SAME_ARTICLE_SUBJECTS
            relation_traits = None
            
            # pull in entities
            relation_from = cls.test_entity_number_to_instance_map.get( relation_from_number, None )
            relation_to = cls.test_entity_number_to_instance_map.get( relation_to_number, None )
            if relation_through_number is not None:
                relation_through = cls.test_entity_number_to_instance_map.get( relation_through_number, None )
            #-- END check to see if we are going THROUGH --#
    
            # create and store relation
            relation_instance = Entity_Relation.create_entity_relation( relation_from,
                                                                        relation_to,
                                                                        through_IN = relation_through,
                                                                        type_slug_IN = relation_type_slug,
                                                                        trait_name_to_value_map_IN = relation_traits )
            cls.test_relation_list.append( relation_instance )
            
        else:
        
            # already created this data.  Output a message.
            print( "In {}: data already created.".format( me ) )
            
        #-- END check to see if data already created --#

    #-- END method create_relation_data() --#


    @classmethod
    def create_test_user( cls, username_IN = "" ):

        # return reference
        user_OUT = None

        # declare variables
        test_user = None
        test_username = ""

        # do we want non-standard username?
        if ( ( username_IN is not None ) and ( username_IN != "" ) ):

            test_username = username_IN

        else:

            test_username = cls.TEST_USER_NAME

        #-- END check to see if special user name. --#

        # create new test user
        test_user = User.objects.create_user( username = test_username,
                                              email = cls.TEST_USER_EMAIL,
                                              password = cls.TEST_USER_PASSWORD )
        test_user.save()

        user_OUT = test_user

        return user_OUT

    #-- END class method create_test_user() --#


    @classmethod
    def get_test_user( cls, username_IN = "" ):

        # return reference
        user_OUT = None

        # declare variables
        test_user = None
        test_username = ""

        # do we want non-standard username?
        if ( ( username_IN is not None ) and ( username_IN != "" ) ):

            test_username = username_IN

        else:

            test_username = cls.TEST_USER_NAME

        #-- END check to see if special user name. --#

        # try a lookup
        try:

            # by username
            user_OUT = User.objects.get( username = test_username )
        
        except Exception as e:
        
            # create new test user
            user_OUT = cls.create_test_user()

        #-- END try to get existing test user. --#

        return user_OUT

    #-- END class method get_test_user() --#


    @classmethod
    def load_fixture( cls, fixture_path_IN = "", verbosity_IN = 0 ):
        
        # declare variables
        
        # got a fixture path?
        if ( ( fixture_path_IN is not None ) and ( fixture_path_IN != "" ) ):
        
            # got a path - try to load it.
            call_command( 'loaddata', fixture_path_IN, verbosity = verbosity_IN )
            
        #-- END check to make sure we have a path --#
        
    #-- END function load_fixture() --#
    
    
    @classmethod
    def output_debug( cls, message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = "", do_print_IN = False ):
        
        '''
        Accepts message string and other optional logging things.  Logs the
            debug message.
        '''
        
        # declare variables
    
        # got a message?
        if ( message_IN ):
        
            # use Logging Helper to log messages.
            LoggingHelper.output_debug( message_IN, method_IN, indent_with_IN, logger_name_IN, do_print_IN = do_print_IN )
        
        #-- END check to see if message. --#
    
    #-- END method output_debug() --#
        

    @classmethod
    def standardSetUp( cls, test_case_IN = None, fixture_list_IN = FIXTURE_LIST ):
        
        """
        setup tasks.  Call function that we'll re-use.
        """
        
        # return reference
        status_OUT = None

        # declare variables
        me = "standardSetUp"
        status_instance = None
        fixture_list = None
        current_fixture = ""
        exception_message = None
        
        print( "\n\nIn context.TestHelper." + me + "(): starting standardSetUp.\n" )
        
        # clear out maps and lists for created data
        cls.test_entity_number_to_instance_map = {}
        cls.test_relation_list = []
        
        # see if test case passed in.  If so, set status variables on it.
        if ( test_case_IN is not None ):
        
            # not None, set status variables on it.
            status_instance = test_case_IN
            
        else:
        
            # no test case passed in.  Just set on self...?  This shouldn't
            #     work.
            status_instance = self
        
        #-- END check to see if test case --#
        
        # janky way to add variables to instance since you can't override init.
        status_instance.setup_error_count = 0
        status_instance.setup_error_list = []
        
        # get fixture list
        fixture_list = fixture_list_IN
        if ( ( fixture_list is None ) or ( len( fixture_list ) <= 0 ) ):
        
            # no list passed in.  Use default.
            fixture_list = cls.FIXTURE_LIST
            
        #-- END check to see if list passed in --#
        
        if ( cls.DEBUG == True ):
            print( "----> Fixture list: {}".format( fixture_list ) )
        #-- END DEBUG --#

        # loop over fixtures in fixture_list
        for current_fixture in fixture_list:
        
            try:
            
                cls.load_fixture( current_fixture )
    
            except Exception as e:
            
                # looks like there was a problem.
                status_instance.setup_error_count += 1
                status_instance.setup_error_list.append( current_fixture )
                
                # log Exception
                exception_message = "Exception thrown loading fixture {}".format( current_fixture )
                ExceptionHelper.log_exception( e,
                                               message_IN = exception_message,
                                               method_IN = me,
                                               do_print_IN = True )
                
            #-- END try/except --#
            
        #-- END loop over cls.FIXTURE_LIST --#
                
        print( "In context.TestHelper.{}(): standardSetUp complete.".format( me ) )
        
        return status_OUT

    #-- END function standardSetUp() --#
        

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