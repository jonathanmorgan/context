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


class NetworkRequestClassTest( django.test.TestCase ):
    

    #----------------------------------------------------------------------------
    # ! ==> Constants-ish
    #----------------------------------------------------------------------------


    # DEBUG
    DEBUG = True

    # CLASS NAME
    CLASS_NAME = "NetworkRequestClassTest"
    

    #----------------------------------------------------------------------
    # ! ==> class methods
    #----------------------------------------------------------------------


    #---------------------------------------------------------------------------
    # ! ==> overridden built-in methods
    #---------------------------------------------------------------------------


    #----------------------------------------------------------------------------
    # ! ==> instance methods - setup
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


    #----------------------------------------------------------------------------
    # ! ==> instance methods - shared methods
    #----------------------------------------------------------------------------


    def validate_relation( self,
                           relation_IN,
                           from_IN,
                           to_IN,
                           through_IN = None,
                           type_IN = None,
                           type_slug_IN = None,
                           trait_dict_IN = None,
                           id_should_be_IN = None,
                           id_should_not_be_IN = None,
                           check_pub_date_IN = True,
                           pub_date_should_be_IN = None,
                           pub_date_should_not_be_IN = None,
                           match_trait_dict_IN = None ):

        # declare variables
        error_string = None
        created_relation = None
        created_relation_id = None
        trait_dict = None
        result_qs = None
        result_count = None
        relation = None
        should_be = None
        stored_relation_id = None
        stored_relation_from = None
        stored_relation_to = None
        stored_relation_through = None
        stored_relation_type = None
        stored_relation_type_slug = None
        trait_qs = None
        trait_count = None
        
        # init from input parameters
        trait_dict = trait_dict_IN
        created_relation = relation_IN
        created_relation_id = created_relation.id
        
        # ! ----> lookup the relation
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = from_IN,
                                                      to_IN = to_IN,
                                                      through_IN = through_IN,
                                                      type_IN = type_IN,
                                                      type_slug_IN = type_slug_IN,
                                                      match_trait_dict_IN = match_trait_dict_IN )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( from_IN, to_IN, through_IN, type_IN, type_slug_IN, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )

        # get() the relation
        relation = result_qs.get()

        # ! ----> get stored relation values
        stored_relation_id = relation.id
        stored_relation_from = relation.relation_from
        stored_relation_to = relation.relation_to
        stored_relation_through = relation.relation_through
        stored_relation_type = relation.relation_type
        stored_relation_type_slug = None

        # ! ----> validate the values
 
        # ID
        should_be = created_relation_id
        error_string = "lookup-ed relation ID = {} --> should match created ID {}".format( stored_relation_id, should_be )
        self.assertEqual( stored_relation_id, should_be, msg = error_string )
        
        # additional ID check - ID should be X?
        if ( id_should_be_IN is not None ):
        
            # more ID
            should_be = id_should_be_IN
            error_string = "lookup-ed relation ID = {} --> should also match {}".format( stored_relation_id, should_be )
            self.assertEqual( stored_relation_id, should_be, msg = error_string )
    
        #-- END check for id_should_be_IN --#            
        
        # additional ID check - ID should NOT be X?
        if ( id_should_not_be_IN is not None ):
        
            # more ID
            should_not_be = id_should_not_be_IN
            error_string = "lookup-ed relation ID = {} --> should NOT match {}".format( stored_relation_id, should_not_be )
            self.assertNotEqual( stored_relation_id, should_not_be, msg = error_string )
    
        #-- END check for id_should_be_IN --#            
        
        # relation_from
        should_be = from_IN
        error_string = "relation_from = {} --> should be {}".format( stored_relation_from, should_be )
        self.assertEqual( stored_relation_from, should_be, msg = error_string )
        
        # relation_to
        should_be = to_IN
        error_string = "relation_to = {} --> should be {}".format( stored_relation_to, should_be )
        self.assertEqual( stored_relation_to, should_be, msg = error_string )
        
        # relation_through
        should_be = through_IN
        error_string = "relation_through = {} --> should be {}".format( stored_relation_through, should_be )
        self.assertEqual( stored_relation_through, should_be, msg = error_string )
        
        # type should be associated.
        should_be = type_IN
        error_string = "relation type = {} --> should be {}".format( stored_relation_type, should_be )
        self.assertEqual( stored_relation_type, should_be, msg = error_string )
        
        if ( stored_relation_type is not None ):
        
            # slugs should match, as well.
            stored_relation_type_slug = stored_relation_type.slug
            should_be = type_slug_IN
            error_string = "relation type slug = {} --> should be {}".format( stored_relation_type_slug, should_be )
            self.assertEqual( stored_relation_type_slug, should_be, msg = error_string )
                        
        #-- END check to see if trait spec found --#
        
        # ! ----> validate traits
        
        # check trait count from instance.
        trait_qs = relation.entity_relation_trait_set.all()
        trait_count = trait_qs.count()
        should_be = len( trait_dict )
        error_string = "trait count {} should = {}".format( trait_count, should_be )
        self.assertEqual( trait_count, should_be, msg = error_string )

        # Evaluate trait values
        self.validate_relation_traits( relation,
                                       trait_dict,
                                       check_pub_date_IN = check_pub_date_IN,
                                       pub_date_should_be_IN = pub_date_should_be_IN,
                                       pub_date_should_not_be_IN = pub_date_should_not_be_IN )

    #-- END method validate_relation() --#


    def validate_relation_traits( self,
                                  relation_IN, 
                                  trait_dict_IN,
                                  check_pub_date_IN = True,
                                  pub_date_should_be_IN = None,
                                  pub_date_should_not_be_IN = None ):
        
        # declare variables
        relation = None
        relation_type = None
        trait_dict = None
        trait_name_list = None
        trait_name = None
        trait_value = None
        trait_spec = None
        trait_qs = None
        trait_count = None
        should_be = None
        should_not_be = None
        error_string = None
        trait_instance = None
        trait_stored_id = None
        trait_stored_name = None
        trait_stored_value = None
        trait_stored_slug = None
        trait_stored_label = None
        trait_stored_spec = None
        
        # init from inputs
        relation = relation_IN
        trait_dict = trait_dict_IN
        
        # get relation type
        relation_type = relation.relation_type
        
        # create trait name list.
        if ( trait_dict is not None ):
            
            # there is a trait dict - get list of keys.
            trait_name_list = list( six.iterkeys( trait_dict_IN ) )
            
        else:
        
            # no dict, empty list (and why even call this method?)
            trait_name_list = []
            
        #-- END check to see if trait dictionary passed in. --#
        
        # ! ----> evaluate traits by looping over name list
        for trait_name in trait_name_list:

            # get trait information.
            trait_value = trait_dict.get( trait_name, None )
            
            # got a relation type?
            if ( relation_type is not None ):
    
                # we do - look for trait spec.
                trait_spec = relation_type.get_trait_spec( trait_name )
                
            else:
            
                # no type, no trait spec
                trait_spec = None
                
            #-- END check to see if relation type. --#
            
            # lookup trait
            trait_qs = relation.entity_relation_trait_set.filter( name = trait_name )
            trait_count = trait_qs.count()
            should_be = 1
            error_string = "trait with name {} --> count {} should = {}".format( trait_name, trait_count, should_be )
            self.assertEqual( trait_count, should_be, msg = error_string )
            
            # get trait_instance
            trait_instance = trait_qs.get()
            
            # retrieve values from instance.
            trait_stored_id = trait_instance.id
            trait_stored_name = trait_instance.name
            trait_stored_value = trait_instance.value
            trait_stored_slug = trait_instance.slug
            trait_stored_label = trait_instance.label
            trait_stored_spec = trait_instance.entity_relation_type_trait

            # stored name and value should be set from dict.
            should_be = trait_name
            error_string = "trait name {} --> should be {}".format( trait_stored_name, should_be )
            self.assertEqual( trait_stored_name, should_be, msg = error_string )
            
            # check value
            
            # is this pub_date?
            if ( trait_name == TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE ):

                # compare pub_date in instance to dict?
                if ( ( check_pub_date_IN is not None ) and ( check_pub_date_IN == True ) ):

                    # check value
                    should_be = trait_value
                    error_string = "trait value {} --> should be {}".format( trait_stored_value, should_be )
                    self.assertEqual( trait_stored_value, should_be, msg = error_string )
                
                #-- END check to see if we do a straight check of pub_date --#
                
                # pub_date - do we have a "should_be" value?
                if ( pub_date_should_be_IN is not None ):
                
                    # pub_date should be...
                    should_be = pub_date_should_be_IN
                    error_string = "pub_date value {} --> should be {}".format( trait_stored_value, should_be )
                    self.assertEqual( trait_stored_value, should_be, msg = error_string )
                    
                #-- END check to see if pub date should be. --#
            
                # pub_date - do we have a "should_not_be" value?
                if ( pub_date_should_not_be_IN is not None ):
                
                    # pub_date should not be...
                    should_not_be = pub_date_should_not_be_IN
                    error_string = "pub_date value {} --> should NOT be {}".format( trait_stored_value, should_not_be )
                    self.assertNotEqual( trait_stored_value, should_not_be, msg = error_string )
                    
                #-- END check to see if pub date should NOT be. --#
                    
            else:
            
                # not pub_date - check value
                should_be = trait_value
                error_string = "trait value {} --> should be {}".format( trait_stored_value, should_be )
                self.assertEqual( trait_stored_value, should_be, msg = error_string )
                
            #-- END check to see if pub date. --#
            
            # if we found a spec, it should be associated.
            should_be = trait_spec
            error_string = "trait spec {} --> should be {}".format( trait_stored_spec, should_be )
            self.assertEqual( trait_stored_spec, should_be, msg = error_string )
            
            if ( trait_spec is not None ):
            
                # stored name should match spec name.
                should_be = trait_spec.name
                error_string = "trait name {} --> should be {}".format( trait_stored_name, should_be )
                self.assertEqual( trait_stored_name, should_be, msg = error_string )
                
                # stored slug should match spec name.
                should_be = trait_spec.slug
                error_string = "trait name {} --> should be {}".format( trait_stored_name, should_be )
                self.assertEqual( trait_stored_slug, should_be, msg = error_string )
                
            else:
            
                # slug
                should_be = None
                error_string = "trait slug {} --> should be {}".format( trait_stored_slug, should_be )
                self.assertEqual( trait_stored_slug, should_be, msg = error_string )
            
            #-- END check to see if trait spec found --#

        #-- END loop over traits. --#
          
    #-- END method validate_relation_traits() --#


    #----------------------------------------------------------------------------
    # ! ==> instance methods - tests
    #----------------------------------------------------------------------------


    def test_create_entity_relation_1( self ):
        
        '''
        Test method that accepts details of a relation, creates it.  Signature:

        @classmethod
        d e f create_entity_relation( cls,
                                    from_IN,
                                    to_IN,
                                    through_IN = None,
                                    type_IN = None,
                                    type_slug_IN = None,
                                    trait_name_to_value_map_IN = None ):

        '''
        
        # declare variables
        me = "test_create_entity_relation_1"
        relation_instance = None
        entity_type = None
        trait_dict = None
        trait_name_list = None
        trait_name = None
        trait_value = None

        # declare variables - create relation
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        result_qs = None
        result_count = None
        created_relation = None
        created_relation_id = None
        original_relation_id = None
        
        # declare variables - validation values
        original_pub_date = None


        # debug
        debug_flag = self.DEBUG

        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )
        
        # create test relation data.
        TestHelper.create_test_relations()
        
        # ! ----> test 1 - create from scratch

        # create relation
        # FROM 3 TO 1 THROUGH 4 - type "quoted" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        
        # init relation properties
        relation_from = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        relation_type_slug = relation_type.slug
        
        # set up traits
        trait_dict = {}
        trait_name_list = []
        
        # add a new trait from scratch (flibble_glibble_pants).
        trait_name = TestHelper.ENTITY_TRAIT_NAME_GIBBERISH
        trait_value = "Jonathan"
        trait_name_list.append( trait_name )
        trait_dict[ trait_name ] = trait_value
        
        # trait with a type specification.  Make sure the meta-information was updated.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
        trait_value = "1923-05-21"
        original_pub_date = trait_value
        trait_name_list.append( trait_name )
        trait_dict[ trait_name ] = trait_value
        
        if ( debug_flag == True ):
            print( "\n--------> Create Entity_Relation:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - relation trait_dict: {}".format( trait_dict ) )
        #-- END DEBUG --#
        
        # ! --------> create relation using slug
        created_relation = Entity_Relation.create_entity_relation( relation_from,
                                                                   relation_to,
                                                                   through_IN = relation_through,
                                                                   type_slug_IN = relation_type_slug,
                                                                   trait_name_to_value_map_IN = trait_dict )
        
        # instance should not be None
        error_string = "None returned creating relation for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}, trait dict: {}".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, trait_dict )
        self.assertIsNotNone( created_relation, msg = error_string )
        
        # store ID for testing.
        created_relation_id = created_relation.id
        original_relation_id = created_relation_id
        
        # ! --------> validate relation        
        self.validate_relation( created_relation,
                                relation_from,
                                relation_to,
                                through_IN = relation_through,
                                type_IN = relation_type,
                                type_slug_IN = relation_type_slug,
                                trait_dict_IN = trait_dict )
                
        # ! ----> test 2 - create again with updated traits
        
        # ! --------> update the pub_date trait's value.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
        trait_value = "2019-11-14"
        trait_dict[ trait_name ] = trait_value

        if ( debug_flag == True ):
            print( "\n--------> Create Entity_Relation:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - relation trait_dict: {}".format( trait_dict ) )
        #-- END DEBUG --#
        
        # ! --------> create relation using type
        created_relation = Entity_Relation.create_entity_relation( relation_from,
                                                                   relation_to,
                                                                   through_IN = relation_through,
                                                                   type_IN = relation_type,
                                                                   trait_name_to_value_map_IN = trait_dict )
        
        # instance should not be None
        error_string = "None returned creating relation for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}, trait dict: {}".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, trait_dict )
        self.assertIsNotNone( created_relation, msg = error_string )
        
        # store ID for testing.
        created_relation_id = created_relation.id
        
        # ! --------> validate relation        
        self.validate_relation( created_relation,
                                relation_from,
                                relation_to,
                                through_IN = relation_through,
                                type_IN = relation_type,
                                type_slug_IN = relation_type_slug,
                                trait_dict_IN = trait_dict,
                                id_should_be_IN = original_relation_id,
                                check_pub_date_IN = False,
                                pub_date_should_be_IN = original_pub_date )
            
    #-- END method test_create_entity_relation_1() --#
        
    
    def test_create_entity_relation_2( self ):
        
        '''
        Test method that accepts details of a relation, creates it.  Signature:

        @classmethod
        d e f create_entity_relation( cls,
                                    from_IN,
                                    to_IN,
                                    through_IN = None,
                                    type_IN = None,
                                    type_slug_IN = None,
                                    trait_name_to_value_map_IN = None ):

        '''
        
        # declare variables
        me = "test_create_entity_relation_2"
        relation_instance = None
        entity_type = None
        trait_dict = None
        trait_name_list = None
        trait_name = None
        trait_value = None

        # declare variables - create relation
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        result_qs = None
        result_count = None
        created_relation = None
        created_relation_id = None
        original_relation_id = None

        # debug
        debug_flag = self.DEBUG

        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )
        
        # create test relation data.
        TestHelper.create_test_relations()
        
        # ! ----> create relation - FROM 3 TO 1 THROUGH 4, no type
        
        # init relation properties
        relation_from = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = None
        relation_type_slug = None
        
        # set up traits
        trait_dict = {}
        trait_name_list = []
        
        # add a new trait from scratch (flibble_glibble_pants).
        trait_name = TestHelper.ENTITY_TRAIT_NAME_GIBBERISH
        trait_value = "Jonathan"
        trait_name_list.append( trait_name )
        trait_dict[ trait_name ] = trait_value
        
        # trait with a type specification.  Make sure the meta-information was updated.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
        trait_value = "1923-05-21"
        original_pub_date = trait_value
        trait_name_list.append( trait_name )
        trait_dict[ trait_name ] = trait_value
        
        if ( debug_flag == True ):
            print( "\n--------> Create Entity_Relation:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - relation trait_dict: {}".format( trait_dict ) )
        #-- END DEBUG --#
        
        # create relation using slug
        created_relation = Entity_Relation.create_entity_relation( relation_from,
                                                                   relation_to,
                                                                   through_IN = relation_through,
                                                                   type_slug_IN = relation_type_slug,
                                                                   trait_name_to_value_map_IN = trait_dict )
        
        # instance should not be None
        error_string = "None returned creating relation for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}, trait dict: {}".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, trait_dict )
        self.assertIsNotNone( created_relation, msg = error_string )
        
        # store ID for testing.
        created_relation_id = created_relation.id
        original_relation_id = created_relation_id
        
        # ! ----> validate relation        
        self.validate_relation( created_relation,
                                relation_from,
                                relation_to,
                                through_IN = relation_through,
                                type_IN = relation_type,
                                type_slug_IN = relation_type_slug,
                                trait_dict_IN = trait_dict )
                
    #-- END method test_create_entity_relation_2() --#
        
    
    def test_create_entity_relation_3( self ):
        
        '''
        Test method that accepts details of a relation, creates it.  Signature:

        @classmethod
        d e f create_entity_relation( cls,
                                    from_IN,
                                    to_IN,
                                    through_IN = None,
                                    type_IN = None,
                                    type_slug_IN = None,
                                    trait_name_to_value_map_IN = None ):

        '''
        
        # declare variables
        me = "test_create_entity_relation_3"
        relation_instance = None
        entity_type = None
        trait_dict = None
        trait_name_list = None
        trait_name = None
        trait_value = None

        # declare variables - create relation
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        result_qs = None
        result_count = None
        created_relation = None
        created_relation_id = None
        original_relation_id = None

        # debug
        debug_flag = self.DEBUG

        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )
        
        # create test relation data.
        TestHelper.create_test_relations()
        
        # ! ----> create relation - FROM 3 TO 1 THROUGH 4, type, no traits
        
        # init relation properties
        relation_from = TestHelper.test_entity_number_to_instance_map[ 3 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_through = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        relation_type_slug = relation_type.slug
        
        # set up traits
        trait_dict = {}
        trait_name_list = []
                
        if ( debug_flag == True ):
            print( "\n--------> Create Entity_Relation:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - relation trait_dict: {}".format( trait_dict ) )
        #-- END DEBUG --#
        
        # create relation using slug
        created_relation = Entity_Relation.create_entity_relation( relation_from,
                                                                   relation_to,
                                                                   through_IN = relation_through,
                                                                   type_slug_IN = relation_type_slug,
                                                                   trait_name_to_value_map_IN = trait_dict )
        
        # instance should not be None
        error_string = "None returned creating relation for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}, trait dict: {}".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, trait_dict )
        self.assertIsNotNone( created_relation, msg = error_string )
        
        # store ID for testing.
        created_relation_id = created_relation.id
        original_relation_id = created_relation_id
        
        # ! ----> validate relation        
        self.validate_relation( created_relation,
                                relation_from,
                                relation_to,
                                through_IN = relation_through,
                                type_IN = relation_type,
                                type_slug_IN = relation_type_slug,
                                trait_dict_IN = trait_dict )
                        
    #-- END method test_create_entity_relation_3() --#
        
    
    def test_create_entity_relation_filter_traits( self ):
        
        '''
        Test method that accepts details of a relation, creates it.  This test
            validates including trait values in check to see if a Relation
            already exists - so not just looking for matching FROM, TO, THROUGH,
            etc., but also looking for matching trait values.

        Signature:

        @classmethod
        d e f create_entity_relation( cls,
                                    from_IN,
                                    to_IN,
                                    through_IN = None,
                                    type_IN = None,
                                    type_slug_IN = None,
                                    trait_name_to_value_map_IN = None,
                                    match_trait_dict_IN = None ):

        '''
        
        # declare variables
        me = "test_create_entity_relation_filter_traits"
        relation_instance = None
        entity_type = None
        trait_dict = None
        trait_name_list = None
        trait_name = None
        trait_value = None

        # declare variables - create relation
        test_relation_qs = None
        test_relation_count = None
        test_relation = None
        test_relation_id = None
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        result_qs = None
        result_count = None
        created_relation = None
        created_relation_id = None
        original_relation_id = None

        # debug
        debug_flag = self.DEBUG

        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )
        
        # create test relation data.
        TestHelper.create_test_relations()
        
        # ! ----> create relation - FROM 3 TO 1 THROUGH 4, type "author", pub_date "1923-05-22"
        
        # init relation properties
        relation_from = TestHelper.test_entity_number_to_instance_map[ 4 ]
        relation_to = TestHelper.test_entity_number_to_instance_map[ 1 ]
        relation_through = None
        relation_type = Entity_Relation_Type.get_type_for_slug( TestHelper.CONTEXT_RELATION_TYPE_SLUG_AUTHOR )
        relation_type_slug = relation_type.slug
        relation_trait_filter_dict = {}
        
        # set up traits
        trait_dict = {}
        trait_name_list = []
        
        # add a new trait from scratch (flibble_glibble_pants).
        trait_name = TestHelper.ENTITY_TRAIT_NAME_GIBBERISH
        trait_value = "Jonathan"
        trait_name_list.append( trait_name )
        trait_dict[ trait_name ] = trait_value
        
        # trait with a type specification.  Make sure the meta-information was updated.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
        trait_value = "1923-05-22"
        original_pub_date = trait_value
        trait_name_list.append( trait_name )
        trait_dict[ trait_name ] = trait_value
        relation_trait_filter_dict[ trait_name ] = trait_value
        
        # ! ----> get count of FROM 3 TO 1 THROUGH 4, type "author", any pub_date
        
        # get match to everything but the trait value
        test_relation_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                             to_IN = relation_to,
                                                             through_IN = relation_through,
                                                             type_IN = relation_type,
                                                             type_slug_IN = relation_type_slug )
        test_relation_count = test_relation_qs.count()

        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, test_relation_count )
        self.assertEqual( test_relation_count, should_be, msg = error_string )

        # get instance and ID.        
        test_relation = test_relation_qs.get()
        test_relation_id = test_relation.id
        
        if ( debug_flag == True ):
            print( "\n--------> Create Entity_Relation:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - relation trait_dict: {}".format( trait_dict ) )
            print( " - relation filter trait_dict: {}".format( relation_trait_filter_dict ) )
        #-- END DEBUG --#
        
        # create relation using slug
        created_relation = Entity_Relation.create_entity_relation( relation_from,
                                                                   relation_to,
                                                                   through_IN = relation_through,
                                                                   type_slug_IN = relation_type_slug,
                                                                   trait_name_to_value_map_IN = trait_dict,
                                                                   match_trait_dict_IN = relation_trait_filter_dict )
        
        # instance should not be None
        error_string = "None returned creating relation for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}, trait dict: {}".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, trait_dict )
        self.assertIsNotNone( created_relation, msg = error_string )
        
        # store ID for testing.
        created_relation_id = created_relation.id
        original_relation_id = created_relation_id
        
        # ! ----> validate relation        
        self.validate_relation( created_relation,
                                relation_from,
                                relation_to,
                                through_IN = relation_through,
                                type_IN = relation_type,
                                type_slug_IN = relation_type_slug,
                                trait_dict_IN = trait_dict,
                                id_should_not_be_IN = test_relation_id,
                                match_trait_dict_IN = relation_trait_filter_dict )
                
        # ! ----> get count of FROM 3 TO 1 THROUGH 4, type "author", any pub_date
                
        # get match to everything but the trait value
        test_relation_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                             to_IN = relation_to,
                                                             through_IN = relation_through,
                                                             type_IN = relation_type,
                                                             type_slug_IN = relation_type_slug )
        test_relation_count = test_relation_qs.count()

        # count should be 2.
        should_be = 2
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, test_relation_count )
        self.assertEqual( test_relation_count, should_be, msg = error_string )

    #-- END method test_create_entity_relation_filter_traits() --#
        
    
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
        # ! ----> MATCH - FROM 1 TO 3 THROUGH 4 - type "quoted" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! --------> FROM 1
        
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
        # ! --------> FROM 1, TO 3
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4, type slug "quoted"
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4, type "quoted"
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4, type "quoted", type slug "quoted"
        
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
        # ! ----> NO MATCH
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! --------> FROM 1, TO 3, THROUGH 4, type "quoted", type slug "mentioned"
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4, type "same-article-subjects"
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4, type slug "same-article-subjects"
        
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
        # ! --------> FROM 1, TO 3, THROUGH 2
        
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
        # ! --------> FROM 1, TO 4
        
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
        # ! --------> FROM 3
        
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
        # ! ----> test within existing query
        #======================================================================#
        

        #----------------------------------------------------------------------#
        # ! --------> Create test QuerySet - FROM 1
        
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
        # ! --------> MATCH - FROM 1, TO 3, THROUGH 4, type "quoted", type slug "quoted"
        
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
        # ! --------> NO MATCH - FROM 1, TO 3, THROUGH 4, type "same-article-subjects"
        
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
        # ! ----> try to get trait - good matches
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! --------> Just name
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
        # ! --------> name + slug
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
        # ! --------> name + slug + label
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
        # ! --------> name + slug + label + Entity_Relation_Type_Trait instance
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
        # ! ----> try to get trait - bad matches
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! --------> Just name
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
        # ! --------> name + slug
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
        # ! --------> name + slug + label
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
        # ! ----> MATCH - FROM 1 TO 3 THROUGH 4 - type "quoted" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! --------> FROM 1
        
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
        # ! --------> FROM 1, TO 3
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4, type slug "quoted"
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4, type "quoted"
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4, type "quoted", type slug "quoted"
        
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
        # ! ----> NO MATCH
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! --------> FROM 1, TO 3, THROUGH 4, type "quoted", type slug "mentioned"
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4, type "same-article-subjects"
        
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
        # ! --------> FROM 1, TO 3, THROUGH 4, type slug "same-article-subjects"
        
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
        # ! --------> FROM 1, TO 3, THROUGH 2
        
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
        # ! --------> FROM 1, TO 4
        
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
        # ! --------> FROM 3
        
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
        # ! ----> test within existing query
        #======================================================================#
        

        #----------------------------------------------------------------------#
        # ! --------> Create test QuerySet - FROM 1
        
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
        # ! --------> MATCH - FROM 1, TO 3, THROUGH 4, type "quoted", type slug "quoted"
        
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
        # ! --------> NO MATCH - FROM 1, TO 3, THROUGH 4, type "same-article-subjects"
        
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
        
    
    def test_lookup_relations_traits( self ):
        
        '''
        Test using the test relation data created in
            TestHelper.create_test_relations().
        '''
        
        # declare variables
        me = "test_lookup_relations_traits"
        result_qs = None
        result_count = None
        
        # declare variables - Lookup info
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        relation_traits = None
        trait_name = None
        trait_value = None
        
        # declare variables - test values
        test_entity_type_slug = None
        test_entity_type = None
        
        # init debug
        debug_flag = self.DEBUG
        
        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )

        # init - test relation data
        TestHelper.create_test_relations()
        
        #======================================================================#
        # ! ----> MATCHES
        #======================================================================#
        
        #----------------------------------------------------------------------#
        # ! --------> pub_date = "1923-05-22" (1)
        
        # init filter parameters
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        relation_traits = {}
        
        # trait with a type specification.  Make sure the meta-information was updated.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
        trait_value = "1923-05-22"
        relation_traits[ trait_name ] = trait_value

        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - relation_traits: {}".format( relation_type_slug ) )            
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug,
                                                      match_trait_dict_IN = relation_traits )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )
        

        #----------------------------------------------------------------------#
        # ! --------> pub_date = "1923-05-21" (2)
        
        # init filter parameters
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        relation_traits = {}
        
        # trait with a type specification.  Make sure the meta-information was updated.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
        trait_value = "1923-05-21"
        relation_traits[ trait_name ] = trait_value

        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - relation_traits: {}".format( relation_type_slug ) )            
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug,
                                                      match_trait_dict_IN = relation_traits )
        result_count = result_qs.count()
        
        # count should be 2.
        should_be = 2
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )


        #----------------------------------------------------------------------#
        # ! --------> pub_date = "1923-05-21" and sourcenet-Newspaper-ID = 123456 (2)
        
        # init filter parameters
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        relation_traits = {}
        
        # trait with a type specification.  Make sure the meta-information was updated.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
        trait_value = TestHelper.TRAIT_VALUE_19230521
        relation_traits[ trait_name ] = trait_value

        # second trait, should not further limit.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_NEWSPAPER_ID
        trait_value = TestHelper.TRAIT_VALUE_123456
        relation_traits[ trait_name ] = trait_value

        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - relation_traits: {}".format( relation_type_slug ) )            
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug,
                                                      match_trait_dict_IN = relation_traits )
        result_count = result_qs.count()
        
        # count should be 2.
        should_be = 2
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )


        #----------------------------------------------------------------------#
        # ! --------> pub_date = "1923-05-21" and sourcenet-Newspaper-ID = 123456 and flibble_glibble_pants = "glarbleblarg" (2)
        
        # init filter parameters
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        relation_traits = {}
        
        # trait with a type specification.  Make sure the meta-information was updated.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
        trait_value = TestHelper.TRAIT_VALUE_19230521
        relation_traits[ trait_name ] = trait_value

        # second trait, should not further limit.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_NEWSPAPER_ID
        trait_value = TestHelper.TRAIT_VALUE_123456
        relation_traits[ trait_name ] = trait_value
        
        # third trait - should limit to 1
        trait_name = TestHelper.TRAIT_NAME_GIBBERISH
        trait_value = TestHelper.TRAIT_VALUE_GIBBERISH
        relation_traits[ trait_name ] = trait_value

        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - relation_traits: {}".format( relation_type_slug ) )            
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug,
                                                      match_trait_dict_IN = relation_traits )
        result_count = result_qs.count()
        
        # count should be 1.
        should_be = 1
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )


        #----------------------------------------------------------------------#
        # ! --------> pub_date = "1923-05-23" (0)
        
        # init filter parameters
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        relation_traits = {}
        
        # trait with a type specification.  Make sure the meta-information was updated.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
        trait_value = "1923-05-23"
        relation_traits[ trait_name ] = trait_value

        if ( debug_flag == True ):
            print( "\n--------> Lookup Entity_Relation based on:" )
            print( " - relation_from: {}".format( relation_from ) )
            print( " - relation_to: {}".format( relation_to ) )
            print( " - relation_through: {}".format( relation_through ) )
            print( " - relation_type: {}".format( relation_type ) )
            print( " - relation_type_slug: {}".format( relation_type_slug ) )
            print( " - relation_traits: {}".format( relation_type_slug ) )            
        #-- END DEBUG --#
        
        # get Entity_Relation QuerySet.
        result_qs = Entity_Relation.lookup_relations( from_IN = relation_from,
                                                      to_IN = relation_to,
                                                      through_IN = relation_through,
                                                      type_IN = relation_type,
                                                      type_slug_IN = relation_type_slug,
                                                      match_trait_dict_IN = relation_traits )
        result_count = result_qs.count()
        
        # count should be 0.
        should_be = 0
        error_string = "Getting entity for FROM: {}, TO: {}, THROUGH:{}, Entity_Relation_Type: {}, type slug: {}; should_be {}, instead returned {}.".format( relation_from, relation_to, relation_through, relation_type, relation_type_slug, should_be, result_count )
        self.assertEqual( result_count, should_be, msg = error_string )


    #-- END method test_lookup_relations_traits() --#
    
                
    def test_set_basic_traits_from_dict( self ):
        
        '''
        Test method that accepts a map of name value trait pairs, looks each up
            to see if there is a trait for the current type, then adds each as a
            trait.
        '''
        
        # declare variables
        me = "test_set_basic_traits_from_dict"
        relation_instance = None
        entity_type = None
        trait_dict = None
        trait_name_list = None
        trait_name = None
        trait_value = None
        trait_count = None
        trait_qs = None
        original_pub_date = None

        # declare variables - lookup relation
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        result_qs = None
        result_count = None   

        # debug
        debug_flag = self.DEBUG

        print( '\n\n====> In {}.{}\n'.format( self.CLASS_NAME, me ) )
        
        # create test relation data.
        TestHelper.create_test_relations()
        
        # ! ----> get Entity_Relation.

        # retrieve one of the relations
        # FROM 1 TO 3 THROUGH 4 - type "quoted" ( TestHelper.CONTEXT_RELATION_TYPE_SLUG_QUOTED )
        
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
        
        # ! ----> create trait dictionary
        
        trait_dict = {}
        trait_name_list = []

        # add a new trait from scratch (flibble_glibble_pants).
        trait_name = TestHelper.ENTITY_TRAIT_NAME_GIBBERISH
        trait_value = "Jonathan"
        trait_name_list.append( trait_name )
        trait_dict[ trait_name ] = trait_value
        
        # create a trait with a type specification.  Make sure the meta-information was updated.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
        trait_value = "1923-05-21"
        original_pub_date = trait_value
        trait_name_list.append( trait_name )
        trait_dict[ trait_name ] = trait_value

        # ! ----> set these traits in the relation.
        trait_count = relation.set_basic_traits_from_dict( trait_dict )
        
        # count from call to method should be 2.
        should_be = len( trait_dict )
        error_string = "After set_basic_traits_from_dict(), trait count returned is {}, should be {}".format( trait_count, should_be )
        self.assertEqual( trait_count, should_be, msg = error_string )

        # check trait count from instance.
        trait_qs = relation.entity_relation_trait_set.all()
        trait_count = trait_qs.count()
        should_be = len( trait_dict )
        error_string = "trait count {} should = {}".format( trait_count, should_be )
        self.assertEqual( trait_count, should_be, msg = error_string )

        # ! ----> evaluate traits by looping over name list
        self.validate_relation_traits( relation, trait_dict )
        
        # ! ----> update the trait's value.  Make sure the value changes.
        trait_name = TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE
        trait_value = "2019-11-14"
        trait_dict[ trait_name ] = trait_value

        # update these traits in the relation.
        trait_count = relation.set_basic_traits_from_dict( trait_dict )
        
        # count from call to method should be 2.
        should_be = len( trait_dict )
        error_string = "After set_basic_traits_from_dict(), trait count returned is {}, should be {}".format( trait_count, should_be )
        self.assertEqual( trait_count, should_be, msg = error_string )

        # check trait count from instance.
        trait_qs = relation.entity_relation_trait_set.all()
        trait_count = trait_qs.count()
        should_be = len( trait_dict )
        error_string = "trait count {} should = {}".format( trait_count, should_be )
        self.assertEqual( trait_count, should_be, msg = error_string )

        # ! ----> evaluate traits by looping over name list
        self.validate_relation_traits( relation, trait_dict, pub_date_should_not_be_IN = original_pub_date )
                
    #-- END method test_set_basic_traits_from_dict() --#
        
    
    def test_set_trait( self ):

        '''
        Things to test passing to the method:
            set_trait( self,
                       name_IN,
                       value_IN,
                       slug_IN = None,
                       value_json_IN = None,
                       label_IN = None,
                       description_IN = None,
                       trait_type_IN = None,
                       term_IN = None,
                       child_type_trait_IN = None ):

        
        '''

        # declare variables
        me = "test_set_trait"
        relation_instance = None
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
        entity_relation_type_trait = None
        original_trait_id = None
        original_trait_value = None

        # declare variables - lookup relation
        relation_from = None
        relation_to = None
        relation_through = None
        relation_type = None
        relation_type_slug = None
        result_qs = None
        result_count = None   

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

        # add a new trait from scratch (flibble_glibble_pants).
        trait_name = TestHelper.ENTITY_TRAIT_NAME_GIBBERISH
        trait_instance = relation.set_trait( trait_name, value_IN = "Jonathan" )
        trait_stored_name = trait_instance.name
        
        # instance should not be None
        error_string = "Creating trait should return Entity_Relation_Trait instance, not None"
        self.assertIsNotNone( trait_instance, msg = error_string )

        # retrieve trait
        trait_qs = relation.entity_relation_trait_set.filter( name = trait_name )
        trait_count = trait_qs.count()
        should_be = 1
        error_string = "trait with name {} --> count {} should = {}".format( trait_name, trait_count, should_be )
        self.assertEqual( trait_count, should_be, msg = error_string )

        # create a trait with a type specification.  Make sure the meta-information was updated.
        trait_name = "pub_date_string"
        trait_value = "1923-05-21"
        original_trait_value = trait_value
        entity_relation_type_trait = relation_type.get_trait_spec( TestHelper.ENTITY_RELATION_TRAIT_NAME_PUB_DATE )
        trait_instance = relation.set_trait( trait_name, value_IN = trait_value, child_type_trait_IN = entity_relation_type_trait )
        original_trait_id = trait_instance.id
        trait_stored_name = trait_instance.name
        trait_stored_value = trait_instance.value
        trait_stored_slug = trait_instance.slug
        trait_stored_label = trait_instance.label
        
        # check trait count
        trait_qs = relation.entity_relation_trait_set.all()
        trait_count = trait_qs.count()
        should_be = 2
        error_string = "trait count {} should = {}".format( trait_count, should_be )
        self.assertEqual( trait_count, should_be, msg = error_string )

        # stored name, slug, and label should be set from specification.
        should_be = entity_relation_type_trait.name
        error_string = "trait name {} --> should be {}".format( trait_stored_name, should_be )
        self.assertEqual( trait_stored_name, should_be, msg = error_string )
        
        # slug
        should_be = entity_relation_type_trait.slug
        error_string = "trait slug {} --> should be {}".format( trait_stored_slug, should_be )
        self.assertEqual( trait_stored_slug, should_be, msg = error_string )
        
        # label
        should_be = entity_relation_type_trait.label
        error_string = "trait label {} --> should be {}".format( trait_stored_label, should_be )
        self.assertEqual( trait_stored_label, should_be, msg = error_string )
        
        # value should be set, too.
        should_be = trait_value
        error_string = "trait value {} --> should be {}".format( trait_stored_value, should_be )
        self.assertEqual( trait_stored_value, should_be, msg = error_string )
        
        # update the trait's value.  Make sure the value changes.
        trait_name = entity_relation_type_trait.name
        trait_value = "2019-11-14"
        trait_instance = relation.set_trait( trait_name, value_IN = trait_value, child_type_trait_IN = entity_relation_type_trait )
        trait_stored_id = trait_instance.id
        trait_stored_name = trait_instance.name
        trait_stored_value = trait_instance.value
        trait_stored_slug = trait_instance.slug
        trait_stored_label = trait_instance.label
        
        # check trait count
        trait_qs = relation.entity_relation_trait_set.all()
        trait_count = trait_qs.count()
        should_be = 2
        error_string = "trait count {} should = {}".format( trait_count, should_be )
        self.assertEqual( trait_count, should_be, msg = error_string )

        # stored id, name, slug, and label should be set from specification.
        should_be = entity_relation_type_trait.name
        error_string = "trait name {} --> should be {}".format( trait_stored_name, should_be )
        self.assertEqual( trait_stored_name, should_be, msg = error_string )
                
        # id
        should_be = original_trait_id
        error_string = "trait id {} --> should be {}".format( trait_stored_id, should_be )
        self.assertEqual( trait_stored_id, should_be, msg = error_string )

        # slug
        should_be = entity_relation_type_trait.slug
        error_string = "trait slug {} --> should be {}".format( trait_stored_slug, should_be )
        self.assertEqual( trait_stored_slug, should_be, msg = error_string )
        
        # label
        should_be = entity_relation_type_trait.label
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
        
    #-- END test method test_set_trait() --#


#-- END test class NetworkRequestClassTest --#
