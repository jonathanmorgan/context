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
from context.models import Entity_Relation
from context.models import Entity_Relation_Type
from context.tests.test_helper import TestHelper


class Entity_RelationModelTest( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ----> Constants-ish
    #----------------------------------------------------------------------------


    # DEBUG
    DEBUG = True

    # CLASS NAME
    CLASS_NAME = "Entity_RelationModelTest"
    

    #----------------------------------------------------------------------
    # ! ----> class methods
    #----------------------------------------------------------------------


    #---------------------------------------------------------------------------
    # ! ----> overridden built-in methods
    #---------------------------------------------------------------------------


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


    def test_filter_relations( self ):
        
        '''
        Test using the test relation data created in
            TestHelper.create_test_relations().
        '''
        
        # declare variables
        me = "test_filter_relations"
        result_qs = None
        result_count = None
        
        # declare variables - Lookup info
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        
        # declare variables - test values
        test_entity_type_slug = None
        test_entity_type = None
        
        # init debug
        debug_flag = self.DEBUG
        
        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )

        # init - test relation data
        TestHelper.create_test_relations()
        
        #======================================================================#
        # ! ==> MATCH - FROM 1 TO 3 THROUGH 4 - type "quoted" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 3.
        should_be = 3
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
                
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = None
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 2.
        should_be = 2
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 2.
        should_be = 2
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type slug "quoted"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = None
        relation_type_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type "quoted"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type "quoted", type slug "quoted"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        relation_type_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #======================================================================#
        # ! ==> NO MATCH
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type "quoted", type slug "mentioned"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        relation_type_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_MENTIONED
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type "same-article-subjects"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_SAME_ARTICLE_SUBJECTS )
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type slug "same-article-subjects"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = None
        relation_type_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_SAME_ARTICLE_SUBJECTS
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 2
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 2 ]
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 4
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_through = None
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 3
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #======================================================================#
        # ! ==> test within existing query
        #======================================================================#
        

        #----------------------------------------------------------------------#
        # ! ----> Create test QuerySet - FROM 1
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        test_qs = Entity_Relation.objects.all()
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - test_qs: {}".format( test_qs ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug,
                                                      qs_IN = test_qs )
        result_count = result_qs.count()
        test_qs = result_qs
        
        # count should be 3.
        should_be = 3
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> MATCH - FROM 1, TO 3, THROUGH 4, type "quoted", type slug "quoted"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        relation_type_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - test_qs: {}".format( test_qs ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug,
                                                      qs_IN = test_qs )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> NO MATCH - FROM 1, TO 3, THROUGH 4, type "same-article-subjects"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_SAME_ARTICLE_SUBJECTS )
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - test_qs: {}".format( test_qs ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug,
                                                      qs_IN = test_qs )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

    #-- END test method test_filter_relations --#
        
    
    def test_get_trait( self ):

        '''
        Things to test passing to the method:

            get_trait( self,
                       name_IN,
                       slug_IN = None,
                       label_IN = None,
                       child_type_trait_IN = None ):        
        '''

        # declare variables
        me = "test_get_trait"
        relation_qs = None
        relation_instance = None
        relation_type = None
        trait_name = None
        trait_instance = None
        relation_type_trait = None
        my_trait_id = None
        my_trait_name = None
        my_trait_slug = None
        my_trait_label = None
        result_trait = None
        result_trait_id = None
        
        # declare variables - lookup relation
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        result_qs = None
        result_count = None   
        
        # declare variables - test values
        test_trait_name = None
        test_trait_slug = None
        test_trait_label = None
        test_trait_type = None
        
        # debug
        debug_flag = self.DEBUG

        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )

        # create test relation data.
        TestHelper.create_test_relations()
        
        # retrieve one of the relations
        # FROM 1 TO 3 THROUGH 4 - type "quoted" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        
        # get Entity_Relation.
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = None
        relation_type_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED
        
        if ( debug_flag == True ):
            print( "\n--------> Filter Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.filter_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {} ( QS query: {} ).".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count, result_qs.query )
        self.assertEqual( result_count, should_be, msg = error_string )

        # then retrieve type
        relation = result_qs.get()
        relation_type = relation.relation_type
        
        # Create trait
        trait_instance = TestHelper.create_test_relation_trait( relation )
        
        # set a type on the trait.
        relation_type_trait = relation_type.get_trait_spec( TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE )
        trait_instance.set_entity_relation_type_trait( relation_type_trait )
        trait_instance.save()
        
        # trait details
        my_trait_id = trait_instance.id
        my_trait_name = trait_instance.name
        my_trait_slug = trait_instance.slug
        my_trait_label = trait_instance.label
        
        print( '\n====> In {}.{}'.format( self.CLASS_NAME, me ) )
        print( "trait_instance: {}".format( trait_instance ) )

        #======================================================================#
        # ! ==> try to get entity trait - good matches
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! ----> Just name
        test_trait_name = my_trait_name
        test_trait_slug = None
        test_trait_label = None
        test_trait_type = None

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( test_trait_name ) )
            print( " - slug: {}".format( test_trait_slug ) )
            print( " - label: {}".format( test_trait_label ) )
            print( " - Entity_Relation_Type_Trait: {}".format( test_trait_type ) )
        #-- END DEBUG --#
        
        result_trait = relation.get_trait( test_trait_name,
                                           slug_IN = test_trait_slug,
                                           label_IN = test_trait_label,
                                           child_type_trait_IN = test_trait_type )
        
        # instance should not be None
        error_string = "Getting trait for name: {}, slug: {}, label: {}, and Entity_Relation_Type_Trait: {}, should return instance, not None.".format( test_trait_name, test_trait_slug, test_trait_label, test_trait_type )
        self.assertIsNotNone( result_trait, msg = error_string )

        # trait ID should match my_trait_id.
        result_trait_id = result_trait.id
        should_be = my_trait_id
        error_string = "Returned Trait has ID {}, should have ID {}".format( result_trait_id, should_be )
        self.assertEqual( result_trait_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> name + slug
        test_trait_name = my_trait_name
        test_trait_slug = my_trait_slug
        test_trait_label = None
        test_trait_type = None

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( test_trait_name ) )
            print( " - slug: {}".format( test_trait_slug ) )
            print( " - label: {}".format( test_trait_label ) )
            print( " - Entity_Relation_Type_Trait: {}".format( test_trait_type ) )
        #-- END DEBUG --#
        
        result_trait = relation.get_trait( test_trait_name,
                                           slug_IN = test_trait_slug,
                                           label_IN = test_trait_label,
                                           child_type_trait_IN = test_trait_type )
        
        # instance should not be None
        error_string = "Getting trait for name: {}, slug: {}, label: {}, and Entity_Relation_Type_Trait: {}, should return instance, not None.".format( test_trait_name, test_trait_slug, test_trait_label, test_trait_type )
        self.assertIsNotNone( result_trait, msg = error_string )

        # trait ID should match my_trait_id.
        result_trait_id = result_trait.id
        should_be = my_trait_id
        error_string = "Returned Trait has ID {}, should have ID {}".format( result_trait_id, should_be )
        self.assertEqual( result_trait_id, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> name + slug + label
        test_trait_name = my_trait_name
        test_trait_slug = my_trait_slug
        test_trait_label = my_trait_label
        test_trait_type = None

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( test_trait_name ) )
            print( " - slug: {}".format( test_trait_slug ) )
            print( " - label: {}".format( test_trait_label ) )
            print( " - Entity_Relation_Type_Trait: {}".format( test_trait_type ) )
        #-- END DEBUG --#
        
        result_trait = relation.get_trait( test_trait_name,
                                           slug_IN = test_trait_slug,
                                           label_IN = test_trait_label,
                                           child_type_trait_IN = test_trait_type )
        
        # instance should not be None
        error_string = "Getting trait for name: {}, slug: {}, label: {}, and Entity_Relation_Type_Trait: {}, should return instance, not None.".format( test_trait_name, test_trait_slug, test_trait_label, test_trait_type )
        self.assertIsNotNone( result_trait, msg = error_string )

        # trait ID should match my_trait_id.
        result_trait_id = result_trait.id
        should_be = my_trait_id
        error_string = "Returned Trait has ID {}, should have ID {}".format( result_trait_id, should_be )
        self.assertEqual( result_trait_id, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> name + slug + label + Entity_Relation_Type_Trait instance
        test_trait_name = my_trait_name
        test_trait_slug = my_trait_slug
        test_trait_label = my_trait_label
        test_trait_type = relation_type_trait

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( test_trait_name ) )
            print( " - slug: {}".format( test_trait_slug ) )
            print( " - label: {}".format( test_trait_label ) )
            print( " - Entity_Relation_Type_Trait: {}".format( test_trait_type ) )
        #-- END DEBUG --#
        
        result_trait = relation.get_trait( test_trait_name,
                                           slug_IN = test_trait_slug,
                                           label_IN = test_trait_label,
                                           child_type_trait_IN = test_trait_type )
        
        # instance should not be None
        error_string = "Getting trait for name: {}, slug: {}, label: {}, and Entity_Relation_Type_Trait: {}, should return instance, not None.".format( test_trait_name, test_trait_slug, test_trait_label, test_trait_type )
        self.assertIsNotNone( result_trait, msg = error_string )

        # trait ID should match my_trait_id.
        result_trait_id = result_trait.id
        should_be = my_trait_id
        error_string = "Returned Trait has ID {}, should have ID {}".format( result_trait_id, should_be )
        self.assertEqual( result_trait_id, should_be, msg = error_string )
                        
        #======================================================================#
        # ! ==> try to get entity trait - bad matches
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! ----> Just name
        test_trait_name = TestHelper.ENTITY_TRAIT_NAME_NO_MATCH
        test_trait_slug = None
        test_trait_label = None
        test_trait_type = None

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( test_trait_name ) )
            print( " - slug: {}".format( test_trait_slug ) )
            print( " - label: {}".format( test_trait_label ) )
            print( " - Entity_Relation_Type_Trait: {}".format( test_trait_type ) )
        #-- END DEBUG --#
        
        result_trait = relation.get_trait( test_trait_name,
                                           slug_IN = test_trait_slug,
                                           label_IN = test_trait_label,
                                           child_type_trait_IN = test_trait_type )
        
        # instance should be None
        error_string = "Getting trait for name: {}, slug: {}, label: {}, and Entity_Relation_Type_Trait: {}, should return None.".format( test_trait_name, test_trait_slug, test_trait_label, test_trait_type )
        self.assertIsNone( result_trait, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> name + slug
        test_trait_name = my_trait_name
        test_trait_slug = TestHelper.ENTITY_TRAIT_SLUG_NO_MATCH
        test_trait_label = None
        test_trait_type = None

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( test_trait_name ) )
            print( " - slug: {}".format( test_trait_slug ) )
            print( " - label: {}".format( test_trait_label ) )
            print( " - Entity_Relation_Type_Trait: {}".format( test_trait_type ) )
        #-- END DEBUG --#
        
        result_trait = relation.get_trait( test_trait_name,
                                           slug_IN = test_trait_slug,
                                           label_IN = test_trait_label,
                                           child_type_trait_IN = test_trait_type )
        
        # instance should be None
        error_string = "Getting trait for name: {}, slug: {}, label: {}, and Entity_Relation_Type_Trait: {}, should return None.".format( test_trait_name, test_trait_slug, test_trait_label, test_trait_type )
        self.assertIsNone( result_trait, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> name + slug + label
        test_trait_name = my_trait_name
        test_trait_slug = my_trait_slug
        test_trait_label = TestHelper.ENTITY_TRAIT_LABEL_NO_MATCH
        test_trait_type = None

        if ( debug_flag == True ):
            print( "\n--------> Retrieve trait based on:" )
            print( " - name: {}".format( test_trait_name ) )
            print( " - slug: {}".format( test_trait_slug ) )
            print( " - label: {}".format( test_trait_label ) )
            print( " - Entity_Relation_Type_Trait: {}".format( test_trait_type ) )
        #-- END DEBUG --#
        
        result_trait = relation.get_trait( test_trait_name,
                                           slug_IN = test_trait_slug,
                                           label_IN = test_trait_label,
                                           child_type_trait_IN = test_trait_type )
        
        # instance should be None
        error_string = "Getting trait for name: {}, slug: {}, label: {}, and Entity_Relation_Type_Trait: {}, should return None.".format( test_trait_name, test_trait_slug, test_trait_label, test_trait_type )
        self.assertIsNone( result_trait, msg = error_string )
        
    #-- END test method test_get_trait() --#


    def test_lookup_relations( self ):
        
        '''
        Test using the test relation data created in
            TestHelper.create_test_relations().
        '''
        
        # declare variables
        me = "test_lookup_relations"
        result_qs = None
        result_count = None
        
        # declare variables - Lookup info
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        
        # declare variables - test values
        test_entity_type_slug = None
        test_entity_type = None
        
        # init debug
        debug_flag = self.DEBUG
        
        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )

        # init - test relation data
        TestHelper.create_test_relations()
        
        #======================================================================#
        # ! ==> MATCH - FROM 1 TO 3 THROUGH 4 - type "quoted" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 3.
        should_be = 3
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
                
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = None
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 2.
        should_be = 2
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 2.
        should_be = 2
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type slug "quoted"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = None
        relation_type_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type "quoted"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type "quoted", type slug "quoted"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        relation_type_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #======================================================================#
        # ! ==> NO MATCH
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type "quoted", type slug "mentioned"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        relation_type_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_MENTIONED
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type "same-article-subjects"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_SAME_ARTICLE_SUBJECTS )
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 4, type slug "same-article-subjects"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = None
        relation_type_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_SAME_ARTICLE_SUBJECTS
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 3, THROUGH 2
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 2 ]
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 1, TO 4
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_through = None
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        
        #----------------------------------------------------------------------#
        # ! ----> FROM 3
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #======================================================================#
        # ! ==> test within existing query
        #======================================================================#
        

        #----------------------------------------------------------------------#
        # ! ----> Create test QuerySet - FROM 1
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        test_qs = Entity_Relation.objects.all()
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - test_qs: {}".format( test_qs ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug,
                                                      qs_IN = test_qs )
        result_count = result_qs.count()
        test_qs = result_qs
        
        # count should be 3.
        should_be = 3
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> MATCH - FROM 1, TO 3, THROUGH 4, type "quoted", type slug "quoted"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        relation_type_slug = TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - test_qs: {}".format( test_qs ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug,
                                                      qs_IN = test_qs )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> NO MATCH - FROM 1, TO 3, THROUGH 4, type "same-article-subjects"
        
        # init filter parameters
        relation_from = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_SAME_ARTICLE_SUBJECTS )
        relation_type_slug = None
        
        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - test_qs: {}".format( test_qs ) )
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug,
                                                      qs_IN = test_qs )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

    #-- END test method test_lookup_relations --#
        
    
#-- END test class Entity_RelationModelTest --#
