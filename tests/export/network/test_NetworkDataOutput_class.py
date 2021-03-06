"""
This file contains tests of the context NetworkDataOutput class.
"""

# base Python imports
import difflib
import json
import logging
import os
import sys

# import six
import six

# django imports
import django.test

# context imports
from context.export.network.filter_spec import FilterSpec
from context.export.network.ndo_simple_matrix import NDO_SimpleMatrix
from context.export.network.ndo_csv_matrix import NDO_CSVMatrix
from context.export.network.ndo_tab_delimited_matrix import NDO_TabDelimitedMatrix
from context.export.network.network_data_request import NetworkDataRequest
from context.export.network.network_data_output import NetworkDataOutput
from context.export.network.network_output import NetworkOutput
from context.models import Entity
from context.models import Entity_Relation
from context.models import Entity_Relation_Type
from context.shared.context_base import ContextBase
from context.tests.export.network.test_helper import TestHelper

# python_utilities
from python_utilities.booleans.boolean_helper import BooleanHelper
from python_utilities.django_utils.django_test_case_helper import DjangoTestCaseHelper
from python_utilities.exceptions.exception_helper import ExceptionHelper


class NetworkDataOutputTest( DjangoTestCaseHelper ):
    

    #----------------------------------------------------------------------------
    # ! ==> Constants-ish
    #----------------------------------------------------------------------------


    # DEBUG
    DEBUG = False
    LOGGER_NAME = "context.tests.export.network.test_NetworkDataOutput_class.py.NetworkDataOutputTest"

    # CLASS NAME
    CLASS_NAME = "NetworkDataOutputTest"
    
    # test - get()/set()
    TEST_SET_ENTITY_DICTIONARY = { 1 : None, 2 : None, 3 : None, 4 : None }
    TEST_SET_ENTITY_RELATION_TYPE_SUMMARY_DICT = { 5 : None, 6 : None, 7 : None, 8 : None }
    TEST_SET_MASTER_ENTITY_LIST = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ]
    TEST_SET_NETWORK_DATA_REQUEST = "test_set_network_data_request"
    TEST_SET_OUTPUT_FORMAT = "test_set_output_format"
    TEST_SET_OUTPUT_INFO_EVERY_X_RELATIONS = 1000
    TEST_SET_OUTPUT_STRUCTURE = "test_set_output_structure"
    TEST_SET_OUTPUT_TYPE = "test_set_output_type"
    TEST_SET_QUERY_SET = "test_set_query_set"
    TEST_SET_RELATION_MAP = { 1 : None, 2 : None, 3 : None, 4 : None, 5 : None, 6 : None, 7 : None, 8 : None }
    TEST_SET_RELATION_TYPE_SLUG_LIST = [ "a", "b", "c" ]
    TEST_SET_RELATION_TYPE_SLUG_TO_INSTANCE_MAP = { "a" : None, "b" : None, "3" : None }
    
    # ! ----> testing creating relation type role value lists
    
    TEST_RELATION_TYPE_SLUG_LIST = [ "mentioned", "quoted", "shared_byline" ]
    TEST_ROLE_LIST = [ ContextBase.RELATION_ROLES_FROM, ContextBase.RELATION_ROLES_TO, ContextBase.RELATION_ROLES_THROUGH ]
    
    # ! --------> SIMPLE
    SIMPLE_MENTIONED_FROM_GOAL_LIST = [ 2, 0, 0 ]
    SIMPLE_MENTIONED_TO_GOAL_LIST = [ 1, 0, 0 ]
    SIMPLE_MENTIONED_THROUGH_GOAL_LIST = [ 0, 0, 0 ]
    SIMPLE_QUOTED_FROM_GOAL_LIST = [ 0, 0, 0 ]
    SIMPLE_QUOTED_TO_GOAL_LIST = [ 1, 2, 0 ]
    SIMPLE_QUOTED_THROUGH_GOAL_LIST = [ 0, 0, 0 ]
    SIMPLE_SHARED_BYLINE_FROM_GOAL_LIST = [ 0, 1, 0 ]
    SIMPLE_SHARED_BYLINE_TO_GOAL_LIST = [ 0, 0, 0 ]
    SIMPLE_SHARED_BYLINE_THROUGH_GOAL_LIST = [ 0, 0, 1 ]
    
    SIMPLE_TYPE_TO_ROLES_MAP = {}
    SIMPLE_MENTIONED_ROLES_TO_LISTS_MAP = {}
    SIMPLE_MENTIONED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_FROM ] = SIMPLE_MENTIONED_FROM_GOAL_LIST
    SIMPLE_MENTIONED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_TO ] = SIMPLE_MENTIONED_TO_GOAL_LIST
    SIMPLE_MENTIONED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_THROUGH ] = SIMPLE_MENTIONED_THROUGH_GOAL_LIST
    SIMPLE_TYPE_TO_ROLES_MAP[ "mentioned" ] = SIMPLE_MENTIONED_ROLES_TO_LISTS_MAP
    SIMPLE_QUOTED_ROLES_TO_LISTS_MAP = {}
    SIMPLE_QUOTED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_FROM ] = SIMPLE_QUOTED_FROM_GOAL_LIST
    SIMPLE_QUOTED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_TO ] = SIMPLE_QUOTED_TO_GOAL_LIST
    SIMPLE_QUOTED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_THROUGH ] = SIMPLE_QUOTED_THROUGH_GOAL_LIST
    SIMPLE_TYPE_TO_ROLES_MAP[ "quoted" ] = SIMPLE_QUOTED_ROLES_TO_LISTS_MAP
    SIMPLE_SHARED_BYLINE_ROLES_TO_LISTS_MAP = {}
    SIMPLE_SHARED_BYLINE_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_FROM ] = SIMPLE_SHARED_BYLINE_FROM_GOAL_LIST
    SIMPLE_SHARED_BYLINE_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_TO ] = SIMPLE_SHARED_BYLINE_TO_GOAL_LIST
    SIMPLE_SHARED_BYLINE_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_THROUGH ] = SIMPLE_SHARED_BYLINE_THROUGH_GOAL_LIST
    SIMPLE_TYPE_TO_ROLES_MAP[ "shared_byline" ] = SIMPLE_SHARED_BYLINE_ROLES_TO_LISTS_MAP

    # ! --------> BASIC
    BASIC_MENTIONED_FROM_GOAL_LIST = [ 7, 24, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0, 0, 0 ]
    BASIC_MENTIONED_TO_GOAL_LIST = [ 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1 ]
    BASIC_MENTIONED_THROUGH_GOAL_LIST = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    BASIC_QUOTED_FROM_GOAL_LIST = [ 4, 9, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0 ]
    BASIC_QUOTED_TO_GOAL_LIST = [ 0, 0, 0, 2, 2, 2, 0, 0, 2, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0 ]
    BASIC_QUOTED_THROUGH_GOAL_LIST = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    BASIC_SHARED_BYLINE_FROM_GOAL_LIST = [ 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    BASIC_SHARED_BYLINE_TO_GOAL_LIST = [ 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    BASIC_SHARED_BYLINE_THROUGH_GOAL_LIST = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    

    BASIC_TYPE_TO_ROLES_MAP = {}
    BASIC_MENTIONED_ROLES_TO_LISTS_MAP = {}
    BASIC_MENTIONED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_FROM ] = BASIC_MENTIONED_FROM_GOAL_LIST
    BASIC_MENTIONED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_TO ] = BASIC_MENTIONED_TO_GOAL_LIST
    BASIC_MENTIONED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_THROUGH ] = BASIC_MENTIONED_THROUGH_GOAL_LIST
    BASIC_TYPE_TO_ROLES_MAP[ "mentioned" ] = BASIC_MENTIONED_ROLES_TO_LISTS_MAP
    BASIC_QUOTED_ROLES_TO_LISTS_MAP = {}
    BASIC_QUOTED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_FROM ] = BASIC_QUOTED_FROM_GOAL_LIST
    BASIC_QUOTED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_TO ] = BASIC_QUOTED_TO_GOAL_LIST
    BASIC_QUOTED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_THROUGH ] = BASIC_QUOTED_THROUGH_GOAL_LIST
    BASIC_TYPE_TO_ROLES_MAP[ "quoted" ] = BASIC_QUOTED_ROLES_TO_LISTS_MAP
    BASIC_SHARED_BYLINE_ROLES_TO_LISTS_MAP = {}
    BASIC_SHARED_BYLINE_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_FROM ] = BASIC_SHARED_BYLINE_FROM_GOAL_LIST
    BASIC_SHARED_BYLINE_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_TO ] = BASIC_SHARED_BYLINE_TO_GOAL_LIST
    BASIC_SHARED_BYLINE_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_THROUGH ] = BASIC_SHARED_BYLINE_THROUGH_GOAL_LIST
    BASIC_TYPE_TO_ROLES_MAP[ "shared_byline" ] = BASIC_SHARED_BYLINE_ROLES_TO_LISTS_MAP

    # ! --------> ENTITY_SELECTION
    ENTITY_SELECTION_MENTIONED_FROM_GOAL_LIST = [ 7, 24, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ENTITY_SELECTION_MENTIONED_TO_GOAL_LIST = [ 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ENTITY_SELECTION_MENTIONED_THROUGH_GOAL_LIST = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ENTITY_SELECTION_QUOTED_FROM_GOAL_LIST = [ 4, 9, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ENTITY_SELECTION_QUOTED_TO_GOAL_LIST = [ 0, 0, 0, 2, 2, 2, 0, 0, 2, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ENTITY_SELECTION_QUOTED_THROUGH_GOAL_LIST = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ENTITY_SELECTION_SHARED_BYLINE_FROM_GOAL_LIST = [ 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ENTITY_SELECTION_SHARED_BYLINE_TO_GOAL_LIST = [ 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    ENTITY_SELECTION_SHARED_BYLINE_THROUGH_GOAL_LIST = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

    ENTITY_SELECTION_TYPE_TO_ROLES_MAP = {}
    ENTITY_SELECTION_MENTIONED_ROLES_TO_LISTS_MAP = {}
    ENTITY_SELECTION_MENTIONED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_FROM ] = ENTITY_SELECTION_MENTIONED_FROM_GOAL_LIST
    ENTITY_SELECTION_MENTIONED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_TO ] = ENTITY_SELECTION_MENTIONED_TO_GOAL_LIST
    ENTITY_SELECTION_MENTIONED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_THROUGH ] = ENTITY_SELECTION_MENTIONED_THROUGH_GOAL_LIST
    ENTITY_SELECTION_TYPE_TO_ROLES_MAP[ "mentioned" ] = ENTITY_SELECTION_MENTIONED_ROLES_TO_LISTS_MAP
    ENTITY_SELECTION_QUOTED_ROLES_TO_LISTS_MAP = {}
    ENTITY_SELECTION_QUOTED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_FROM ] = ENTITY_SELECTION_QUOTED_FROM_GOAL_LIST
    ENTITY_SELECTION_QUOTED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_TO ] = ENTITY_SELECTION_QUOTED_TO_GOAL_LIST
    ENTITY_SELECTION_QUOTED_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_THROUGH ] = ENTITY_SELECTION_QUOTED_THROUGH_GOAL_LIST
    ENTITY_SELECTION_TYPE_TO_ROLES_MAP[ "quoted" ] = ENTITY_SELECTION_QUOTED_ROLES_TO_LISTS_MAP
    ENTITY_SELECTION_SHARED_BYLINE_ROLES_TO_LISTS_MAP = {}
    ENTITY_SELECTION_SHARED_BYLINE_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_FROM ] = ENTITY_SELECTION_SHARED_BYLINE_FROM_GOAL_LIST
    ENTITY_SELECTION_SHARED_BYLINE_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_TO ] = ENTITY_SELECTION_SHARED_BYLINE_TO_GOAL_LIST
    ENTITY_SELECTION_SHARED_BYLINE_ROLES_TO_LISTS_MAP[ ContextBase.RELATION_ROLES_THROUGH ] = ENTITY_SELECTION_SHARED_BYLINE_THROUGH_GOAL_LIST
    ENTITY_SELECTION_TYPE_TO_ROLES_MAP[ "shared_byline" ] = ENTITY_SELECTION_SHARED_BYLINE_ROLES_TO_LISTS_MAP


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
        #TestHelper.standardSetUp( self )
        TestHelper.standardSetUp( self, fixture_list_IN = TestHelper.FIXTURE_LIST_DATA )

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


    #----------------------------------------------------------------------------
    # ! ==> instance methods - shared methods
    #----------------------------------------------------------------------------


    def set_up_basic_test_instance( self ):

        # return reference
        instance_OUT = None

        # declare variables
        me = "set_up_basic_test_instance"

        # init debug
        debug_flag = self.DEBUG
        
        # call the base method, passing it the method for entity selection.
        instance_OUT = self.set_up_test_instance( request_load_function_IN = TestHelper.load_basic )
        
        return instance_OUT

    #-- END test method set_up_basic_test_instance() --#
        

    def set_up_entity_relations_details( self, do_validate_IN = False ):

        # return reference
        instance_OUT = None
        
        # declare variables
        me = "set_up_entity_relations_details"
        debug_flag = None
        test_instance = None
        current_type_slug = None
        total_entity_count = None
        total_type_count = None
        entity_type_count = None
        mentioned_type = None
        quoted_type = None
        shared_byline_type = None
        entity_id = None
        relation_type = None
        relation_role = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # ! ----> get basic test instance
        
        # use it to set up test instance.
        test_instance = self.set_up_basic_test_instance()
        
        # set master entity list
        test_instance.set_master_entity_list( [ 1, 2, 3 ] )
        
        # load relation types: "mentioned", "quoted", "shared_byline"
        mentioned_type = Entity_Relation_Type.objects.get( slug = "mentioned" )
        quoted_type = Entity_Relation_Type.objects.get( slug = "quoted" )
        shared_byline_type = Entity_Relation_Type.objects.get( slug = "shared_byline" )
        
        # ! ----> 1 - "mentioned" - FROM
        entity_id = 1
        relation_type = mentioned_type
        relation_role = ContextBase.RELATION_ROLES_FROM
        
        # update details
        test_instance.update_entity_relations_details( entity_id, relation_type, relation_role, update_relation_map_IN = True )
        
        if ( do_validate_IN == True ):
        
            # validate
            total_type_count = 1
            total_entity_count = 1
            entity_type_count = 1
            type_from_count = 1
            type_to_count = 0
            type_through_count = 0
            self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                           entity_id_IN = entity_id,
                                                           relation_type_IN = relation_type,
                                                           relation_role_IN = relation_role,
                                                           total_type_count_IN = total_type_count,
                                                           total_entity_count_IN = total_entity_count,
                                                           entity_type_count_IN = entity_type_count,
                                                           type_from_count_IN = type_from_count,
                                                           type_to_count_IN = type_to_count,
                                                           type_through_count_IN = type_through_count )
                                                           
        #-- END check to see if we validate --#

        # ! ----> 1 - "mentioned" - FROM
        entity_id = 1
        relation_type = mentioned_type
        relation_role = ContextBase.RELATION_ROLES_FROM
        
        # update details
        test_instance.update_entity_relations_details( entity_id, relation_type, relation_role, update_relation_map_IN = True )
        
        if ( do_validate_IN == True ):
        
            # validate
            total_type_count = 1
            total_entity_count = 1
            entity_type_count = 1
            type_from_count = 2
            type_to_count = 0
            type_through_count = 0
            self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                           entity_id_IN = entity_id,
                                                           relation_type_IN = relation_type,
                                                           relation_role_IN = relation_role,
                                                           total_type_count_IN = total_type_count,
                                                           total_entity_count_IN = total_entity_count,
                                                           entity_type_count_IN = entity_type_count,
                                                           type_from_count_IN = type_from_count,
                                                           type_to_count_IN = type_to_count,
                                                           type_through_count_IN = type_through_count )
    
        #-- END check to see if we validate --#

        # ! ----> 1 - "mentioned" - TO
        entity_id = 1
        relation_type = mentioned_type
        relation_role = ContextBase.RELATION_ROLES_TO
        
        # update details
        test_instance.update_entity_relations_details( entity_id, relation_type, relation_role, update_relation_map_IN = True )
        
        # validate
        total_type_count = 1
        total_entity_count = 1
        entity_type_count = 1
        type_from_count = 2
        type_to_count = 1
        type_through_count = 0
        self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                       entity_id_IN = entity_id,
                                                       relation_type_IN = relation_type,
                                                       relation_role_IN = relation_role,
                                                       total_type_count_IN = total_type_count,
                                                       total_entity_count_IN = total_entity_count,
                                                       entity_type_count_IN = entity_type_count,
                                                       type_from_count_IN = type_from_count,
                                                       type_to_count_IN = type_to_count,
                                                       type_through_count_IN = type_through_count )

        # ! ----> 1 - "quoted" - TO
        entity_id = 1
        relation_type = quoted_type
        relation_role = ContextBase.RELATION_ROLES_TO
        
        # update details
        test_instance.update_entity_relations_details( entity_id, relation_type, relation_role, update_relation_map_IN = True )
        
        if ( do_validate_IN == True ):
        
            # validate
            total_type_count = 2
            total_entity_count = 1
            entity_type_count = 2
            type_from_count = 0
            type_to_count = 1
            type_through_count = 0
            self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                           entity_id_IN = entity_id,
                                                           relation_type_IN = relation_type,
                                                           relation_role_IN = relation_role,
                                                           total_type_count_IN = total_type_count,
                                                           total_entity_count_IN = total_entity_count,
                                                           entity_type_count_IN = entity_type_count,
                                                           type_from_count_IN = type_from_count,
                                                           type_to_count_IN = type_to_count,
                                                           type_through_count_IN = type_through_count )

        #-- END check to see if we validate --#

        # ! ----> 2 - "quoted" - TO
        entity_id = 2
        relation_type = quoted_type
        relation_role = ContextBase.RELATION_ROLES_TO
        
        # update details
        test_instance.update_entity_relations_details( entity_id, relation_type, relation_role, update_relation_map_IN = True )
        
        if ( do_validate_IN == True ):
        
            # validate
            total_type_count = 2
            total_entity_count = 2
            entity_type_count = 1
            type_from_count = 0
            type_to_count = 1
            type_through_count = 0
            self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                           entity_id_IN = entity_id,
                                                           relation_type_IN = relation_type,
                                                           relation_role_IN = relation_role,
                                                           total_type_count_IN = total_type_count,
                                                           total_entity_count_IN = total_entity_count,
                                                           entity_type_count_IN = entity_type_count,
                                                           type_from_count_IN = type_from_count,
                                                           type_to_count_IN = type_to_count,
                                                           type_through_count_IN = type_through_count )
    
        #-- END check to see if we validate --#

        # ! ----> 2 - "quoted" - TO
        entity_id = 2
        relation_type = quoted_type
        relation_role = ContextBase.RELATION_ROLES_TO
        
        # update details
        test_instance.update_entity_relations_details( entity_id, relation_type, relation_role, update_relation_map_IN = True )
        
        if ( do_validate_IN == True ):
        
            # validate
            total_type_count = 2
            total_entity_count = 2
            entity_type_count = 1
            type_from_count = 0
            type_to_count = 2
            type_through_count = 0
            self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                           entity_id_IN = entity_id,
                                                           relation_type_IN = relation_type,
                                                           relation_role_IN = relation_role,
                                                           total_type_count_IN = total_type_count,
                                                           total_entity_count_IN = total_entity_count,
                                                           entity_type_count_IN = entity_type_count,
                                                           type_from_count_IN = type_from_count,
                                                           type_to_count_IN = type_to_count,
                                                           type_through_count_IN = type_through_count )

        #-- END check to see if we validate --#

        # ! ----> 2 - "shared_byline" - FROM
        entity_id = 2
        relation_type = shared_byline_type
        relation_role = ContextBase.RELATION_ROLES_FROM
        
        # update details
        test_instance.update_entity_relations_details( entity_id, relation_type, relation_role, update_relation_map_IN = True )
        
        if ( do_validate_IN == True ):
        
            # validate
            total_type_count = 3
            total_entity_count = 2
            entity_type_count = 2
            type_from_count = 1
            type_to_count = 0
            type_through_count = 0
            self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                           entity_id_IN = entity_id,
                                                           relation_type_IN = relation_type,
                                                           relation_role_IN = relation_role,
                                                           total_type_count_IN = total_type_count,
                                                           total_entity_count_IN = total_entity_count,
                                                           entity_type_count_IN = entity_type_count,
                                                           type_from_count_IN = type_from_count,
                                                           type_to_count_IN = type_to_count,
                                                           type_through_count_IN = type_through_count )

        #-- END check to see if we validate --#

        # ! ----> 3 - "shared_byline" - THROUGH
        entity_id = 3
        relation_type = shared_byline_type
        relation_role = ContextBase.RELATION_ROLES_THROUGH
        
        # update details
        test_instance.update_entity_relations_details( entity_id, relation_type, relation_role, update_relation_map_IN = True )
        
        if ( do_validate_IN == True ):
        
            # validate
            total_type_count = 3
            total_entity_count = 3
            entity_type_count = 1
            type_from_count = 0
            type_to_count = 0
            type_through_count = 1
            self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                           entity_id_IN = entity_id,
                                                           relation_type_IN = relation_type,
                                                           relation_role_IN = relation_role,
                                                           total_type_count_IN = total_type_count,
                                                           total_entity_count_IN = total_entity_count,
                                                           entity_type_count_IN = entity_type_count,
                                                           type_from_count_IN = type_from_count,
                                                           type_to_count_IN = type_to_count,
                                                           type_through_count_IN = type_through_count )
                                                       
            # ! ----> validate final state for entities 1 and 2.
            
            total_type_count = 3
            total_entity_count = 3
    
            # --------> 1 - "mentioned"
            entity_id = 1
            relation_type = mentioned_type
            relation_role = ContextBase.RELATION_ROLES_TO
            entity_type_count = 2
            type_from_count = 2
            type_to_count = 1
            type_through_count = 0
            self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                           entity_id_IN = entity_id,
                                                           relation_type_IN = relation_type,
                                                           relation_role_IN = relation_role,
                                                           total_type_count_IN = total_type_count,
                                                           total_entity_count_IN = total_entity_count,
                                                           entity_type_count_IN = entity_type_count,
                                                           type_from_count_IN = type_from_count,
                                                           type_to_count_IN = type_to_count,
                                                           type_through_count_IN = type_through_count )
            
            # --------> 1 - "quoted"
            entity_id = 1
            relation_type = quoted_type
            relation_role = ContextBase.RELATION_ROLES_TO
            entity_type_count = 2
            type_from_count = 0
            type_to_count = 1
            type_through_count = 0
            self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                           entity_id_IN = entity_id,
                                                           relation_type_IN = relation_type,
                                                           relation_role_IN = relation_role,
                                                           total_type_count_IN = total_type_count,
                                                           total_entity_count_IN = total_entity_count,
                                                           entity_type_count_IN = entity_type_count,
                                                           type_from_count_IN = type_from_count,
                                                           type_to_count_IN = type_to_count,
                                                           type_through_count_IN = type_through_count )
    
            # --------> 2 - "quoted"
            entity_id = 2
            relation_type = quoted_type
            relation_role = ContextBase.RELATION_ROLES_TO
            entity_type_count = 2
            type_from_count = 0
            type_to_count = 2
            type_through_count = 0
            self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                           entity_id_IN = entity_id,
                                                           relation_type_IN = relation_type,
                                                           relation_role_IN = relation_role,
                                                           total_type_count_IN = total_type_count,
                                                           total_entity_count_IN = total_entity_count,
                                                           entity_type_count_IN = entity_type_count,
                                                           type_from_count_IN = type_from_count,
                                                           type_to_count_IN = type_to_count,
                                                           type_through_count_IN = type_through_count )
    
            # --------> 2 - "shared_byline"
            entity_id = 2
            relation_type = shared_byline_type
            relation_role = ContextBase.RELATION_ROLES_FROM
            entity_type_count = 2
            type_from_count = 1
            type_to_count = 0
            type_through_count = 0
            self.validate_update_entity_relations_details( test_instance_IN = test_instance,
                                                           entity_id_IN = entity_id,
                                                           relation_type_IN = relation_type,
                                                           relation_role_IN = relation_role,
                                                           total_type_count_IN = total_type_count,
                                                           total_entity_count_IN = total_entity_count,
                                                           entity_type_count_IN = entity_type_count,
                                                           type_from_count_IN = type_from_count,
                                                           type_to_count_IN = type_to_count,
                                                           type_through_count_IN = type_through_count )

        #-- END check to see if we validate --#

        instance_OUT = test_instance
        
        return test_instance

    #-- END method set_up_entity_relations_details() --#
        
        
    def set_up_entity_selection_test_instance( self ):

        # return reference
        instance_OUT = None

        # declare variables
        me = "set_up_entity_selection_test_instance"

        # init debug
        debug_flag = self.DEBUG
        
        # call the base method, passing it the method for entity selection.
        instance_OUT = self.set_up_test_instance( request_load_function_IN = TestHelper.load_with_entity_selection )
        
        return instance_OUT

    #-- END method set_up_entity_selection_test_instance() --#
        

    def set_up_test_instance( self, request_IN = None, request_load_function_IN = TestHelper.load_basic ):

        # return reference
        instance_OUT = None

        # declare variables
        me = "set_up_test_instance"
        debug_flag = None
        network_output = None
        test_request = None
        relation_qs = None
        test_instance = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # ! ----> set up NetworkOutput and request
        
        # create NetworkOutput
        network_output = NetworkOutput()
        
        # initialize request
        if ( request_IN is not None ):
        
            # request passed in.  Use it.
            test_request = request_IN
        
        else:
        
            # no request passed in, use basic.
            test_request = request_load_function_IN()
            
            # remove output type and file path, so no output
            test_request.set_output_type( None )
            test_request.set_output_file_path( None )
            #test_request.set_output_file_path( TestHelper.TEST_BASIC_TSV_OUTPUT )

        #-- END check to see if request passed in. --#
        
        
        # place request in instance.
        network_output.set_network_data_request( test_request )
        
        # create entity dict
        entity_dict = test_request.process_entities()
        entity_dict_count = len( entity_dict )
        
        # and create relation QuerySet
        relation_qs = test_request.filter_relation_query_set( qs_IN = relation_qs,
                                                              use_entity_selection_IN = False )

        # ! ----> configure the NetworkDataObject child instance.

        # now, create test instance - use whatever is in request.
        test_instance = network_output.get_NDO_instance()

        # initialize it.
        test_instance.set_query_set( relation_qs )
        test_instance.set_entity_dictionary( entity_dict )

        # initialize NetworkDataOutput instance from request.
        test_instance.initialize_from_request( test_request )

        instance_OUT = test_instance
        
        return instance_OUT

    #-- END method set_up_basic_test_instance() --#
        

    def validate_create_relation_type_role_value_list( self,
                                                       test_list_IN,
                                                       goal_list_IN,
                                                       relation_type_slug_IN = None,
                                                       relation_role_IN = None ):

        # declare variables
        me = "validate_create_relation_type_role_value_list"
        debug_flag = None
        test_list = None
        test_list_count = None
        test_value = None
        should_be = None
        error_string = None
        goal_list = None
        goal_list_count = None
        list_index = None
        current_value = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # init
        test_list = test_list_IN
        test_list_count = len( test_list )
        goal_list = goal_list_IN
        goal_list_count = len( goal_list )
        
        if ( debug_flag == True ):
        
            print( "In {}(): relation type slug: {}".format( me, relation_type_slug_IN ) )
            print( "In {}(): relation type role: {}".format( me, relation_role_IN ) )
            print( "In {}(): test_list ( count = {} ): {}".format( me, test_list_count, test_list ) )
            print( "In {}(): goal_list ( count = {} ): {}".format( me, goal_list_count, goal_list ) )
            
        #-- END DEBUG --#
        
        # counts should be equal
        test_value = test_list_count
        should_be = goal_list_count
        error_string = "list count = {}, should = {} ( type: {}; role: {} ).".format( test_value, should_be, relation_type_slug_IN, relation_role_IN )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # lists should be identical
        list_index = -1
        for current_value in goal_list:
        
            # increment index
            list_index += 1
            
            # value at that index should be current_value.
            test_value = test_list[ list_index ]
            should_be = current_value
            error_string = "index: {}; value = {}, should = {} ( type: {}; role: {} ).".format( list_index, test_value, should_be, relation_type_slug_IN, relation_role_IN )
            self.assertEqual( test_value, should_be, msg = error_string )
            
        #-- END loop over items in goal list. --#

    #-- END test method validate_create_relation_type_role_value_list() --#


    def validate_register_relation_type( self,
                                         test_instance_IN = None,
                                         type_slug_IN = None,
                                         type_count_IN = None ):
                                         
        # declare variables
        me = "validate_register_relation_type"
        test_instance = None
        type_slug = None
        total_type_count = None
        test_relation_type = None
        relation_type_map = None
        relation_type_map_count = None
        relation_type_slug_list = None
        relation_type_slug_list_count = None
        test_value = None
        should_be = None
        error_string = None
        
        # initialize from inputs
        test_instance = test_instance_IN
        type_slug = type_slug_IN
        total_type_count = type_count_IN        

        # get relation type.
        test_relation_type = Entity_Relation_Type.objects.get( slug = type_slug )
        
        # get the map and the list
        relation_type_map = test_instance.get_relation_type_slug_to_instance_map()
        relation_type_map_count = len( relation_type_map )
        relation_type_slug_list = test_instance.get_relation_type_slug_list()
        relation_type_slug_list_count = len( relation_type_slug_list )
        
        # check size/length of each
        
        # map
        test_value = relation_type_map_count
        should_be = total_type_count
        error_string = "relation_type_map size: {} should be: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # list
        test_value = relation_type_slug_list_count
        should_be = total_type_count
        error_string = "relation_type_slug_list size: {} should be: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # make sure it is in the map.
        test_value = type_slug in relation_type_map
        error_string = "slug {} in relation_type_map {}?: {}".format( type_slug, relation_type_map, test_value )
        self.assertTrue( test_value, msg = error_string )
        
        # make sure it is in the list.
        test_value = type_slug in relation_type_slug_list
        error_string = "slug {} in relation_type_slug_list {}?: {}".format( type_slug, relation_type_slug_list, test_value )
        self.assertTrue( test_value, msg = error_string )

        # and make sure the instance is mapped.
        test_value = relation_type_map.get( type_slug, None )
        should_be = test_relation_type
        error_string = "relation_type: {} is not the same as what we passed in: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
    #-- END method validate_register_relation_type() --#


    def validate_relation_map( self,
                               test_instance_IN = None,
                               from_entity_id_IN = None,
                               to_entity_id_IN = None,
                               relation_dict_count_IN = None,
                               to_dict_count_IN = None,
                               relation_count_IN = None ):
                               
        # declare variables
        me = "validate_relation_map"
        test_instance = None
        relation_dictionary = None
        relation_dictionary_count = None
        to_dict = None
        to_dict_count = None
        test_relation_count = None
        
        # declare variables - configuration
        from_entity_id = None
        to_entity_id = None
        target_relation_dict_count = None
        target_to_dict_count = None
        target_relation_count = None

        # initialize from inputs
        test_instance = test_instance_IN
        from_entity_id = from_entity_id_IN
        to_entity_id = to_entity_id_IN
        target_relation_dict_count = relation_dict_count_IN
        target_to_dict_count = to_dict_count_IN
        target_relation_count = relation_count_IN

        # get relation dictionary.
        relation_dictionary = test_instance.get_relation_map()
        relation_dictionary_count = len( relation_dictionary )
        
        # Should have length...
        test_value = relation_dictionary_count
        should_be = target_relation_dict_count
        error_string = "relation_map count = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # retrieve FROM entity's TO dictionary.
        to_dict = test_instance.get_relations_for_entity( from_entity_id )
        to_dict_count = len( to_dict )
        
        # should be length...
        test_value = to_dict_count
        should_be = target_to_dict_count
        error_string = "relation_map count = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # test_relation_count.
        test_relation_count = to_dict.get( to_entity_id, None )
        test_value = test_relation_count
        should_be = target_relation_count
        error_string = "count of relations from {} to {} = {}, should = {}.".format( from_entity_id, to_entity_id, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

    #-- END method validate_relation_map() --#


    def validate_update_entity_relations_details( self,
                                                  test_instance_IN = None,
                                                  entity_id_IN = None,
                                                  relation_type_IN = None,
                                                  relation_role_IN = None,
                                                  total_type_count_IN = None,
                                                  total_entity_count_IN = None,
                                                  entity_type_count_IN = None,
                                                  type_from_count_IN = None,
                                                  type_to_count_IN = None,
                                                  type_through_count_IN = None ):

                                         
        # declare variables
        me = "validate_update_entity_relations_details"
        type_slug = None
        entity_to_relation_type_map = None
        entity_to_relation_type_map_count = None
        entity_relation_type_map = None
        entity_relation_type_map_count = None
        type_role_map = None
        type_role_map_count = None
        from_count = None
        to_count = None
        through_count = None
        test_value = None
        should_be = None
        error_string = None
        
        # validate the registering of the type
        type_slug = relation_type_IN.slug
        self.validate_register_relation_type( test_instance_IN, type_slug, total_type_count_IN )
        
        # get the map
        entity_to_relation_type_map = test_instance_IN.get_entity_relation_type_summary_dict()
        entity_to_relation_type_map_count = len( entity_to_relation_type_map )

        # map count
        test_value = entity_to_relation_type_map_count
        should_be = total_entity_count_IN
        error_string = "entity_to_relation_type_map size: {} should be: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # make sure entity ID is in the map.
        test_value = entity_id_IN in entity_to_relation_type_map
        error_string = "slug {} in entity_to_relation_type_map {}?: {}".format( type_slug, entity_to_relation_type_map, test_value )
        self.assertTrue( test_value, msg = error_string )
        
        # get the entity's map.
        entity_relation_type_map = entity_to_relation_type_map.get( entity_id_IN, None )
        entity_relation_type_map_count = len( entity_relation_type_map )

        # map count - number of relation types the entity has been a part of.
        test_value = entity_relation_type_map_count
        should_be = entity_type_count_IN
        error_string = "entity_relation_type_map size: {} should be: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # is type in the map?
        test_value = type_slug in entity_relation_type_map
        error_string = "slug {} in entity_relation_type_map {}?: {}".format( type_slug, entity_relation_type_map, test_value )
        self.assertTrue( test_value, msg = error_string )
        
        # retrieve roles map
        type_role_map = entity_relation_type_map.get( type_slug, None )
        type_role_map_count = len( type_role_map )
        
        # map count - should be three roles.
        test_value = type_role_map_count
        should_be = 3
        error_string = "type_role_map size: {} should be: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # get counts for roles, compare to counts passed in.
        from_count = type_role_map.get( ContextBase.RELATION_ROLES_FROM )
        to_count = type_role_map.get( ContextBase.RELATION_ROLES_TO )
        through_count = type_role_map.get( ContextBase.RELATION_ROLES_THROUGH )
        
        # FROM
        test_value = from_count
        should_be = type_from_count_IN
        error_string = "FROM count for relation type \"{}\": {} should be: {}.".format( type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # TO
        test_value = to_count
        should_be = type_to_count_IN
        error_string = "TO count for relation type \"{}\": {} should be: {}.".format( type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # THROUGH
        test_value = through_count
        should_be = type_through_count_IN
        error_string = "THROUGH count for relation type \"{}\": {} should be: {}.".format( type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )        

    #-- END method validate_update_entity_relations_details() --#


    #----------------------------------------------------------------------------
    # ! ==> instance methods - tests
    #----------------------------------------------------------------------------


    def test_add_directed_relation( self ):

        # declare variables
        me = "test_add_directed_relation"
        debug_flag = None
        test_instance = None
        relation_dictionary = None
        relation_dictionary_count = None
        to_dict = None
        to_dict_count = None
        test_relation_count = None
        
        # declare variables - configuration
        from_entity_id = None
        to_entity_id = None
        target_relation_dict_count = None
        target_to_dict_count = None
        target_relation_count = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # ! ----> get basic test instance
        
        test_instance = self.set_up_basic_test_instance()
        
        #----------------------------------------------------------------------#
        # ! ----> add relation from 1 to 2
        
        from_entity_id = 1
        to_entity_id = 2
        target_relation_dict_count = 1
        target_to_dict_count = 1
        target_relation_count = 1
        test_instance.add_directed_relation( from_entity_id, to_entity_id )
        
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = from_entity_id,
                                    to_entity_id_IN = to_entity_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
        
        #----------------------------------------------------------------------#
        # ! ----> add relation from 1 to 3
        
        from_entity_id = 1
        to_entity_id = 3
        target_relation_dict_count = 1
        target_to_dict_count = 2
        target_relation_count = 1
        test_instance.add_directed_relation( from_entity_id, to_entity_id )
        
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = from_entity_id,
                                    to_entity_id_IN = to_entity_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
        
        #----------------------------------------------------------------------#
        # ! ----> add relation from 1 to 2
        
        from_entity_id = 1
        to_entity_id = 3
        target_relation_dict_count = 1
        target_to_dict_count = 2
        target_relation_count = 2
        test_instance.add_directed_relation( from_entity_id, to_entity_id )
        
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = from_entity_id,
                                    to_entity_id_IN = to_entity_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
        
        #----------------------------------------------------------------------#
        # ! ----> add relation from 2 to 3

        from_entity_id = 2
        to_entity_id = 3
        target_relation_dict_count = 2
        target_to_dict_count = 1
        target_relation_count = 1
        test_instance.add_directed_relation( from_entity_id, to_entity_id )
        
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = from_entity_id,
                                    to_entity_id_IN = to_entity_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
                
    #-- END test method test_add_directed_relation() --#
        
        
    def test_add_reciprocal_relation( self ):

        # declare variables
        me = "test_add_reciprocal_relation"
        debug_flag = None
        test_instance = None
        relation_dictionary = None
        relation_dictionary_count = None
        to_dict = None
        to_dict_count = None
        test_relation_count = None
        
        # declare variables - configuration
        from_entity_id = None
        to_entity_id = None
        target_relation_dict_count = None
        target_to_dict_count = None
        target_relation_count = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # ! ----> get basic test instance
        
        test_instance = self.set_up_basic_test_instance()
        
        #----------------------------------------------------------------------#
        # ! ----> add relation from 1 to 2
        
        from_entity_id = 1
        to_entity_id = 2
        test_instance.add_reciprocal_relation( from_entity_id, to_entity_id )
        
        # validate
        target_relation_dict_count = 2
        
        # validate --> FROM
        validate_from_id = from_entity_id
        validate_to_id = to_entity_id
        target_to_dict_count = 1
        target_relation_count = 1
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = validate_from_id,
                                    to_entity_id_IN = validate_to_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
        
        # validate --> TO
        validate_from_id = to_entity_id
        validate_to_id = from_entity_id
        target_to_dict_count = 1
        target_relation_count = 1
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = validate_from_id,
                                    to_entity_id_IN = validate_to_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
        
        #----------------------------------------------------------------------#
        # ! ----> add relation from 1 to 3
        
        from_entity_id = 1
        to_entity_id = 3
        test_instance.add_reciprocal_relation( from_entity_id, to_entity_id )
        
        # validate
        target_relation_dict_count = 3
        
        # validate --> FROM
        validate_from_id = from_entity_id
        validate_to_id = to_entity_id
        target_to_dict_count = 2
        target_relation_count = 1
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = validate_from_id,
                                    to_entity_id_IN = validate_to_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
        
        # validate --> TO
        validate_from_id = to_entity_id
        validate_to_id = from_entity_id
        target_to_dict_count = 1
        target_relation_count = 1
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = validate_from_id,
                                    to_entity_id_IN = validate_to_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
        
        #----------------------------------------------------------------------#
        # ! ----> add relation from 1 to 2
        
        from_entity_id = 1
        to_entity_id = 2
        test_instance.add_reciprocal_relation( from_entity_id, to_entity_id )
        
        # validate
        target_relation_dict_count = 3
        
        # validate --> FROM
        validate_from_id = from_entity_id
        validate_to_id = to_entity_id
        target_to_dict_count = 2
        target_relation_count = 2
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = validate_from_id,
                                    to_entity_id_IN = validate_to_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
        
        # validate --> TO
        validate_from_id = to_entity_id
        validate_to_id = from_entity_id
        target_to_dict_count = 1
        target_relation_count = 2
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = validate_from_id,
                                    to_entity_id_IN = validate_to_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
        
        #----------------------------------------------------------------------#
        # ! ----> add relation from 2 to 3

        from_entity_id = 2
        to_entity_id = 3
        test_instance.add_reciprocal_relation( from_entity_id, to_entity_id )
        
        # validate
        target_relation_dict_count = 3
        
        # validate --> FROM
        validate_from_id = from_entity_id
        validate_to_id = to_entity_id
        target_to_dict_count = 2
        target_relation_count = 1
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = validate_from_id,
                                    to_entity_id_IN = validate_to_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
        
        # validate --> TO
        validate_from_id = to_entity_id
        validate_to_id = from_entity_id
        target_to_dict_count = 2
        target_relation_count = 1
        self.validate_relation_map( test_instance_IN = test_instance,
                                    from_entity_id_IN = validate_from_id,
                                    to_entity_id_IN = validate_to_id,
                                    relation_dict_count_IN = target_relation_dict_count,
                                    to_dict_count_IN = target_to_dict_count,
                                    relation_count_IN = target_relation_count )        
        
    #-- END test method test_add_reciprocal_relation() --#
        
        
    def test_create_all_relation_type_values_lists( self ):

        # declare variables
        me = "test_create_all_relation_type_values_lists"
        debug_flag = None
        test_instance = None
        test_type_to_roles_map = None
        relation_type_slug_list = None
        relation_type_slug = None
        role_list = None
        relation_role = None
        test_dict = None
        test_dict_count = None
        test_list = None
        test_value = None
        should_be = None
        error_string = None
        goal_type_to_roles_map = None
        goal_dict = None
        goal_list = None
        list_index = None
        current_value = None
        
        # init
        debug_flag = self.DEBUG
        relation_type_slug_list = self.TEST_RELATION_TYPE_SLUG_LIST
        role_list = self.TEST_ROLE_LIST
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        #----------------------------------------------------------------------#
        # ! ----> simple test

        goal_type_to_roles_map = self.SIMPLE_TYPE_TO_ROLES_MAP
        test_instance = self.set_up_entity_relations_details()

        # make all possible lists, validate each.
        test_type_to_roles_map = test_instance.create_all_relation_type_values_lists()
        
        # loop over slugs.
        for relation_type_slug in relation_type_slug_list:
        
            # get goal and test dicts
            goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
            test_dict = test_type_to_roles_map.get( relation_type_slug, None )
            test_dict_count = len( test_dict )
            
            # should be three things.
            test_value = test_dict_count
            should_be = 3
            error_string = "simple - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )

            # loop over the roles
            for relation_role in role_list:
            
                # validate role
                test_list = test_dict.get( relation_role, None )
                goal_list = goal_dict.get( relation_role, None )
                self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
                
            #-- END loop over roles --#

        #-- END loop over relation type slugs. --#
            
        #----------------------------------------------------------------------#
        # ! ----> basic test

        goal_type_to_roles_map = self.BASIC_TYPE_TO_ROLES_MAP
        test_instance = self.set_up_basic_test_instance()

        # render to set everything up
        network_data = test_instance.render()
        
        # make all possible lists, validate each.
        test_type_to_roles_map = test_instance.create_all_relation_type_values_lists()
        
        # loop over slugs.
        for relation_type_slug in relation_type_slug_list:
        
            # get goal and test dicts
            goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
            test_dict = test_type_to_roles_map.get( relation_type_slug, None )
            test_dict_count = len( test_dict )
            
            # should be three things.
            test_value = test_dict_count
            should_be = 3
            error_string = "basic - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )

            # loop over the roles
            for relation_role in role_list:
            
                # validate role
                test_list = test_dict.get( relation_role, None )
                goal_list = goal_dict.get( relation_role, None )
                self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
                
            #-- END loop over roles --#

        #-- END loop over relation type slugs. --#

        #----------------------------------------------------------------------#
        # ! ----> entity selection test

        goal_type_to_roles_map = self.ENTITY_SELECTION_TYPE_TO_ROLES_MAP
        test_instance = self.set_up_entity_selection_test_instance()

        # render to set everything up
        network_data = test_instance.render()
        
        # make all possible lists, validate each.
        test_type_to_roles_map = test_instance.create_all_relation_type_values_lists()
        
        # loop over slugs.
        for relation_type_slug in relation_type_slug_list:
        
            # get goal and test dicts
            goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
            test_dict = test_type_to_roles_map.get( relation_type_slug, None )
            test_dict_count = len( test_dict )
            
            # should be three things.
            test_value = test_dict_count
            should_be = 3
            error_string = "entity selection - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
            self.assertEqual( test_value, should_be, msg = error_string )

            # loop over the roles
            for relation_role in role_list:
            
                # validate role
                test_list = test_dict.get( relation_role, None )
                goal_list = goal_dict.get( relation_role, None )
                self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
                
            #-- END loop over roles --#

        #-- END loop over relation type slugs. --#

    #-- END test method test_create_all_relation_type_values_lists() --#


    def test_create_entity_id_list( self ):

        # declare variables
        me = "test_create_entity_id_list"
        debug_flag = None
        test_instance = None
        entity_id_list = None
        entity_id_list_count = None
        test_entity_id_list = None
        test_entity_id_list_count = None
        network_data = None
        test_value = None
        should_be = None
        error_string = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        #----------------------------------------------------------------------#
        # ! ----> simple test
        
        # create instance
        test_instance = NetworkDataOutput()
        
        # set entity_dictionary and entity relation type summary
        test_instance.set_entity_dictionary( self.TEST_SET_ENTITY_DICTIONARY )
        test_instance.set_entity_relation_type_summary_dict( self.TEST_SET_ENTITY_RELATION_TYPE_SUMMARY_DICT )
        
        # call the method.
        entity_id_list = test_instance.generate_master_entity_list()
        entity_id_list_count = len( entity_id_list )
        
        # should have 8 items.
        test_value = entity_id_list_count
        should_be = 8
        error_string = "Simple test entity list count = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # should contain IDs 1 through 8.
        for id_value in range( 1, 9 ):
        
            # id value should be in list.
            test_value = id_value in entity_id_list
            error_string = "id {} in entity_id_list {}?: {}".format( id_value, entity_id_list, test_value )
            self.assertTrue( test_value, msg = error_string )
            
        #-- END loop over IDs that should be in the list --#
        
        # get test list
        test_entity_id_list = test_instance.create_entity_id_list()
        test_entity_id_list_count = len( test_entity_id_list )
        
        # should be same length as entity_id_list
        test_value = test_entity_id_list_count
        should_be = entity_id_list_count
        error_string = "Simple test create_entity_id_list count = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # entity_id_list should contain all IDs in test_entity_id_list.
        for id_value in test_entity_id_list:
        
            # id value should be in list.
            test_value = int( id_value ) in entity_id_list
            error_string = "id {} in entity_id_list {}?: {}".format( id_value, entity_id_list, test_value )
            self.assertTrue( test_value, msg = error_string )
            
        #-- END loop over IDs that should be in the list --#
        
        # and vice versa.
        for id_value in entity_id_list:
        
            # id value should be in list.
            test_value = str( id_value ) in test_entity_id_list
            error_string = "id {} in test_entity_id_list {}?: {}".format( id_value, test_entity_id_list, test_value )
            self.assertTrue( test_value, msg = error_string )
            
        #-- END loop over IDs that should be in the list --#
        
        #----------------------------------------------------------------------#
        # ! ----> basic test

        test_instance = self.set_up_basic_test_instance()

        # render to set everything up
        network_data = test_instance.render()
        
        # call the method.
        entity_id_list = test_instance.generate_master_entity_list()
        entity_id_list_count = len( entity_id_list )

        # should have ? items.
        test_value = entity_id_list_count
        should_be = 72
        error_string = "Basic test entity list count = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # get test list
        test_entity_id_list = test_instance.create_entity_id_list()
        test_entity_id_list_count = len( test_entity_id_list )
        
        # should be same length as entity_id_list
        test_value = test_entity_id_list_count
        should_be = entity_id_list_count
        error_string = "Simple test create_entity_id_list count = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # entity_id_list should contain all IDs in test_entity_id_list.
        for id_value in test_entity_id_list:
        
            # id value should be in list.
            test_value = int( id_value ) in entity_id_list
            error_string = "id {} in entity_id_list {}?: {}".format( id_value, entity_id_list, test_value )
            self.assertTrue( test_value, msg = error_string )
            
        #-- END loop over IDs that should be in the list --#
        
        # and vice versa.
        for id_value in entity_id_list:
        
            # id value should be in list.
            test_value = str( id_value ) in test_entity_id_list
            error_string = "id {} in test_entity_id_list {}?: {}".format( id_value, test_entity_id_list, test_value )
            self.assertTrue( test_value, msg = error_string )
            
        #-- END loop over IDs that should be in the list --#
        
        #----------------------------------------------------------------------#
        # ! ----> entity selection test

        test_instance = self.set_up_entity_selection_test_instance()

        # render to set everything up
        network_data = test_instance.render()
        
        # call the method.
        entity_id_list = test_instance.generate_master_entity_list()
        entity_id_list_count = len( entity_id_list )

        # should have ? items.
        test_value = entity_id_list_count
        should_be = 153
        error_string = "Entity selection test entity list count = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # get test list
        test_entity_id_list = test_instance.create_entity_id_list()
        test_entity_id_list_count = len( test_entity_id_list )
        
        # should be same length as entity_id_list
        test_value = test_entity_id_list_count
        should_be = entity_id_list_count
        error_string = "Simple test create_entity_id_list count = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # entity_id_list should contain all IDs in test_entity_id_list.
        for id_value in test_entity_id_list:
        
            # id value should be in list.
            test_value = int( id_value ) in entity_id_list
            error_string = "id {} in entity_id_list {}?: {}".format( id_value, entity_id_list, test_value )
            self.assertTrue( test_value, msg = error_string )
            
        #-- END loop over IDs that should be in the list --#
        
        # and vice versa.
        for id_value in entity_id_list:
        
            # id value should be in list.
            test_value = str( id_value ) in test_entity_id_list
            error_string = "id {} in test_entity_id_list {}?: {}".format( id_value, test_entity_id_list, test_value )
            self.assertTrue( test_value, msg = error_string )
            
        #-- END loop over IDs that should be in the list --#
        
    #-- END test method test_create_entity_id_list() --#


    def test_create_relation_type_role_value_list( self ):

        # declare variables
        me = "test_create_relation_type_role_value_list"
        debug_flag = None
        test_instance = None
        relation_type_slug = None
        relation_role = None
        test_list = None
        test_list_count = None
        test_value = None
        should_be = None
        error_string = None
        goal_list = None
        list_index = None
        current_value = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        #----------------------------------------------------------------------#
        # ! ----> simple test

        test_instance = self.set_up_entity_relations_details()

        # make all possible lists, validate each.
        
        # --------> mentioned --> FROM
        relation_type_slug = "mentioned"
        relation_role = ContextBase.RELATION_ROLES_FROM
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.SIMPLE_MENTIONED_FROM_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> mentioned --> TO
        relation_type_slug = "mentioned"
        relation_role = ContextBase.RELATION_ROLES_TO
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.SIMPLE_MENTIONED_TO_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> mentioned --> THROUGH
        relation_type_slug = "mentioned"
        relation_role = ContextBase.RELATION_ROLES_THROUGH
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.SIMPLE_MENTIONED_THROUGH_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> quoted --> FROM
        relation_type_slug = "quoted"
        relation_role = ContextBase.RELATION_ROLES_FROM
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.SIMPLE_QUOTED_FROM_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> quoted --> TO
        relation_type_slug = "quoted"
        relation_role = ContextBase.RELATION_ROLES_TO
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.SIMPLE_QUOTED_TO_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> quoted --> THROUGH
        relation_type_slug = "quoted"
        relation_role = ContextBase.RELATION_ROLES_THROUGH
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.SIMPLE_QUOTED_THROUGH_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> shared_byline --> FROM
        relation_type_slug = "shared_byline"
        relation_role = ContextBase.RELATION_ROLES_FROM
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.SIMPLE_SHARED_BYLINE_FROM_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> shared_byline --> TO
        relation_type_slug = "shared_byline"
        relation_role = ContextBase.RELATION_ROLES_TO
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.SIMPLE_SHARED_BYLINE_TO_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> shared_byline --> THROUGH
        relation_type_slug = "shared_byline"
        relation_role = ContextBase.RELATION_ROLES_THROUGH
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.SIMPLE_SHARED_BYLINE_THROUGH_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        #----------------------------------------------------------------------#
        # ! ----> basic test

        test_instance = self.set_up_basic_test_instance()

        # render to set everything up
        network_data = test_instance.render()
        
        # make all possible lists, validate each.
        
        # --------> mentioned --> FROM
        relation_type_slug = "mentioned"
        relation_role = ContextBase.RELATION_ROLES_FROM
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.BASIC_MENTIONED_FROM_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> mentioned --> TO
        relation_type_slug = "mentioned"
        relation_role = ContextBase.RELATION_ROLES_TO
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.BASIC_MENTIONED_TO_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> mentioned --> THROUGH
        relation_type_slug = "mentioned"
        relation_role = ContextBase.RELATION_ROLES_THROUGH
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.BASIC_MENTIONED_THROUGH_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> quoted --> FROM
        relation_type_slug = "quoted"
        relation_role = ContextBase.RELATION_ROLES_FROM
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.BASIC_QUOTED_FROM_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> quoted --> TO
        relation_type_slug = "quoted"
        relation_role = ContextBase.RELATION_ROLES_TO
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.BASIC_QUOTED_TO_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> quoted --> THROUGH
        relation_type_slug = "quoted"
        relation_role = ContextBase.RELATION_ROLES_THROUGH
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.BASIC_QUOTED_THROUGH_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> shared_byline --> FROM
        relation_type_slug = "shared_byline"
        relation_role = ContextBase.RELATION_ROLES_FROM
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.BASIC_SHARED_BYLINE_FROM_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> shared_byline --> TO
        relation_type_slug = "shared_byline"
        relation_role = ContextBase.RELATION_ROLES_TO
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.BASIC_SHARED_BYLINE_TO_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> shared_byline --> THROUGH
        relation_type_slug = "shared_byline"
        relation_role = ContextBase.RELATION_ROLES_THROUGH
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.BASIC_SHARED_BYLINE_THROUGH_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        #----------------------------------------------------------------------#
        # ! ----> entity selection test

        test_instance = self.set_up_entity_selection_test_instance()

        # render to set everything up
        network_data = test_instance.render()
        
        # make all possible lists, validate each.
        
        # --------> mentioned --> FROM
        relation_type_slug = "mentioned"
        relation_role = ContextBase.RELATION_ROLES_FROM
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.ENTITY_SELECTION_MENTIONED_FROM_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> mentioned --> TO
        relation_type_slug = "mentioned"
        relation_role = ContextBase.RELATION_ROLES_TO
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.ENTITY_SELECTION_MENTIONED_TO_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> mentioned --> THROUGH
        relation_type_slug = "mentioned"
        relation_role = ContextBase.RELATION_ROLES_THROUGH
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.ENTITY_SELECTION_MENTIONED_THROUGH_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> quoted --> FROM
        relation_type_slug = "quoted"
        relation_role = ContextBase.RELATION_ROLES_FROM
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.ENTITY_SELECTION_QUOTED_FROM_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> quoted --> TO
        relation_type_slug = "quoted"
        relation_role = ContextBase.RELATION_ROLES_TO
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.ENTITY_SELECTION_QUOTED_TO_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> quoted --> THROUGH
        relation_type_slug = "quoted"
        relation_role = ContextBase.RELATION_ROLES_THROUGH
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.ENTITY_SELECTION_QUOTED_THROUGH_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> shared_byline --> FROM
        relation_type_slug = "shared_byline"
        relation_role = ContextBase.RELATION_ROLES_FROM
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.ENTITY_SELECTION_SHARED_BYLINE_FROM_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> shared_byline --> TO
        relation_type_slug = "shared_byline"
        relation_role = ContextBase.RELATION_ROLES_TO
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.ENTITY_SELECTION_SHARED_BYLINE_TO_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

        # --------> shared_byline --> THROUGH
        relation_type_slug = "shared_byline"
        relation_role = ContextBase.RELATION_ROLES_THROUGH
        test_list = test_instance.create_relation_type_role_value_list( relation_type_slug, relation_role )
        test_list_count = len( test_list )
        
        # validate
        goal_list = self.ENTITY_SELECTION_SHARED_BYLINE_THROUGH_GOAL_LIST
        self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )

    #-- END test method test_create_relation_type_role_value_list() --#


    def test_create_relation_type_value_dict( self ):

        # declare variables
        me = "test_create_relation_type_value_dict"
        debug_flag = None
        test_instance = None
        relation_type_slug = None
        role_list = None
        relation_role = None
        test_dict = None
        test_dict_count = None
        test_list = None
        test_value = None
        should_be = None
        error_string = None
        goal_type_to_roles_map = None
        goal_dict = None
        goal_list = None
        list_index = None
        current_value = None
        
        # init
        debug_flag = self.DEBUG
        role_list = self.TEST_ROLE_LIST
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        #----------------------------------------------------------------------#
        # ! ----> simple test

        goal_type_to_roles_map = self.SIMPLE_TYPE_TO_ROLES_MAP
        test_instance = self.set_up_entity_relations_details()

        # make all possible lists, validate each.
        
        # --------> mentioned
        relation_type_slug = "mentioned"
        test_dict = test_instance.create_relation_type_value_dict( relation_type_slug )
        test_dict_count = len( test_dict )
        
        # should be three things.
        test_value = test_dict_count
        should_be = 3
        error_string = "simple - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # validate
        goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
        
        # loop over the roles
        for relation_role in role_list:
        
            # validate role
            test_list = test_dict.get( relation_role, None )
            goal_list = goal_dict.get( relation_role, None )
            self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
            
        #-- END loop over roles --#
            
        # --------> quoted
        relation_type_slug = "quoted"
        test_dict = test_instance.create_relation_type_value_dict( relation_type_slug )
        test_dict_count = len( test_dict )
        
        # should be three things.
        test_value = test_dict_count
        should_be = 3
        error_string = "simple - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # validate
        goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
        
        # loop over the roles
        for relation_role in role_list:
        
            # validate role
            test_list = test_dict.get( relation_role, None )
            goal_list = goal_dict.get( relation_role, None )
            self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
            
        #-- END loop over roles --#

        # --------> shared_byline --> FROM
        relation_type_slug = "shared_byline"
        test_dict = test_instance.create_relation_type_value_dict( relation_type_slug )
        test_dict_count = len( test_dict )
        
        # should be three things.
        test_value = test_dict_count
        should_be = 3
        error_string = "simple - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # validate
        goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
        
        # loop over the roles
        for relation_role in role_list:
        
            # validate role
            test_list = test_dict.get( relation_role, None )
            goal_list = goal_dict.get( relation_role, None )
            self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
            
        #-- END loop over roles --#

        #----------------------------------------------------------------------#
        # ! ----> basic test

        goal_type_to_roles_map = self.BASIC_TYPE_TO_ROLES_MAP
        test_instance = self.set_up_basic_test_instance()

        # render to set everything up
        network_data = test_instance.render()
        
        # make all possible lists, validate each.
        
        # --------> mentioned
        relation_type_slug = "mentioned"
        test_dict = test_instance.create_relation_type_value_dict( relation_type_slug )
        test_dict_count = len( test_dict )
        
        # should be three things.
        test_value = test_dict_count
        should_be = 3
        error_string = "basic - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # validate
        goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
        
        # loop over the roles
        for relation_role in role_list:
        
            # validate role
            test_list = test_dict.get( relation_role, None )
            goal_list = goal_dict.get( relation_role, None )
            self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
            
        #-- END loop over roles --#
            
        # --------> quoted
        relation_type_slug = "quoted"
        test_dict = test_instance.create_relation_type_value_dict( relation_type_slug )
        test_dict_count = len( test_dict )
        
        # should be three things.
        test_value = test_dict_count
        should_be = 3
        error_string = "basic - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # validate
        goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
        
        # loop over the roles
        for relation_role in role_list:
        
            # validate role
            test_list = test_dict.get( relation_role, None )
            goal_list = goal_dict.get( relation_role, None )
            self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
            
        #-- END loop over roles --#

        # --------> shared_byline --> FROM
        relation_type_slug = "shared_byline"
        test_dict = test_instance.create_relation_type_value_dict( relation_type_slug )
        test_dict_count = len( test_dict )
        
        # should be three things.
        test_value = test_dict_count
        should_be = 3
        error_string = "basic - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # validate
        goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
        
        # loop over the roles
        for relation_role in role_list:
        
            # validate role
            test_list = test_dict.get( relation_role, None )
            goal_list = goal_dict.get( relation_role, None )
            self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
            
        #-- END loop over roles --#

        #----------------------------------------------------------------------#
        # ! ----> entity selection test

        goal_type_to_roles_map = self.ENTITY_SELECTION_TYPE_TO_ROLES_MAP
        test_instance = self.set_up_entity_selection_test_instance()

        # render to set everything up
        network_data = test_instance.render()
        
        # make all possible lists, validate each.
        
        # --------> mentioned
        relation_type_slug = "mentioned"
        test_dict = test_instance.create_relation_type_value_dict( relation_type_slug )
        test_dict_count = len( test_dict )
        
        # should be three things.
        test_value = test_dict_count
        should_be = 3
        error_string = "entity selection - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # validate
        goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
        
        # loop over the roles
        for relation_role in role_list:
        
            # validate role
            test_list = test_dict.get( relation_role, None )
            goal_list = goal_dict.get( relation_role, None )
            self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
            
        #-- END loop over roles --#
            
        # --------> quoted
        relation_type_slug = "quoted"
        test_dict = test_instance.create_relation_type_value_dict( relation_type_slug )
        test_dict_count = len( test_dict )
        
        # should be three things.
        test_value = test_dict_count
        should_be = 3
        error_string = "entity selection - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # validate
        goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
        
        # loop over the roles
        for relation_role in role_list:
        
            # validate role
            test_list = test_dict.get( relation_role, None )
            goal_list = goal_dict.get( relation_role, None )
            self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
            
        #-- END loop over roles --#

        # --------> shared_byline --> FROM
        relation_type_slug = "shared_byline"
        test_dict = test_instance.create_relation_type_value_dict( relation_type_slug )
        test_dict_count = len( test_dict )
        
        # should be three things.
        test_value = test_dict_count
        should_be = 3
        error_string = "entity selection - relation type value dict for type {}; count = {}, should = {}.".format( relation_type_slug, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # validate
        goal_dict = goal_type_to_roles_map.get( relation_type_slug, None )
        
        # loop over the roles
        for relation_role in role_list:
        
            # validate role
            test_list = test_dict.get( relation_role, None )
            goal_list = goal_dict.get( relation_role, None )
            self.validate_create_relation_type_role_value_list( test_list, goal_list, relation_type_slug, relation_role )
            
        #-- END loop over roles --#

    #-- END test method test_create_relation_type_value_dict() --#


    def test_generate_master_entity_list( self ):

        # declare variables
        me = "test_generate_master_entity_list"
        debug_flag = None
        test_instance = None
        entity_id_list = None
        entity_id_list_count = None
        network_data = None
        test_value = None
        should_be = None
        error_string = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        #----------------------------------------------------------------------#
        # ! ----> simple test
        
        # create instance
        test_instance = NetworkDataOutput()
        
        # set entity_dictionary and entity relation type summary
        test_instance.set_entity_dictionary( self.TEST_SET_ENTITY_DICTIONARY )
        test_instance.set_entity_relation_type_summary_dict( self.TEST_SET_ENTITY_RELATION_TYPE_SUMMARY_DICT )
        
        # call the method.
        entity_id_list = test_instance.generate_master_entity_list()
        entity_id_list_count = len( entity_id_list )
        
        # should have 8 items.
        test_value = entity_id_list_count
        should_be = 8
        error_string = "Simple test entity list count = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # should contain IDs 1 through 8.
        for id_value in range( 1, 9 ):
        
            # id value should be in list.
            test_value = id_value in entity_id_list
            error_string = "id {} in entity_id_list {}?: {}".format( id_value, entity_id_list, test_value )
            self.assertTrue( test_value, msg = error_string )
            
        #-- END loop over IDs that should be in the list --#

        #----------------------------------------------------------------------#
        # ! ----> basic test

        test_instance = self.set_up_basic_test_instance()

        # render to set everything up
        network_data = test_instance.render()
        
        # call the method.
        entity_id_list = test_instance.generate_master_entity_list()
        entity_id_list_count = len( entity_id_list )

        # should have ? items.
        test_value = entity_id_list_count
        should_be = 72
        error_string = "Basic test entity list count = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        #----------------------------------------------------------------------#
        # ! ----> entity selection test

        test_instance = self.set_up_entity_selection_test_instance()

        # render to set everything up
        network_data = test_instance.render()
        
        # call the method.
        entity_id_list = test_instance.generate_master_entity_list()
        entity_id_list_count = len( entity_id_list )

        # should have ? items.
        test_value = entity_id_list_count
        should_be = 153
        error_string = "Entity selection test entity list count = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
    #-- END test method test_generate_master_entity_list() --#


    def test_getters_and_setters( self ):

        # declare variables
        me = "test_getters_and_setters"
        debug_flag = None
        test_instance = None
        test_method = None
        original_value = None
        new_value = None
        test_value = None
        should_be = None
        error_string = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # create instance
        test_instance = NetworkDataOutput()
        
        # ! ----> test get() using set()
        
        # for each (using last loaded test instance):
        # - get original value and store
        # - set new value
        # - get value.
        # - assertEquals( get value, new value )
        # - assertNotEqual( get value, original value )
        
        # ! --------> get/set_entity_dictionary()
        test_method = "set_entity_dictionary"
        original_value = test_instance.get_entity_dictionary()
        new_value = self.TEST_SET_ENTITY_DICTIONARY
        test_instance.set_entity_dictionary( new_value )
        test_value = test_instance.get_entity_dictionary()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_entity_relation_type_summary_dict()
        test_method = "set_entity_relation_type_summary_dict"
        original_value = test_instance.get_entity_relation_type_summary_dict()
        new_value = self.TEST_SET_ENTITY_RELATION_TYPE_SUMMARY_DICT
        test_instance.set_entity_relation_type_summary_dict( new_value )
        test_value = test_instance.get_entity_relation_type_summary_dict()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_master_entity_list()
        test_method = "set_master_entity_list"
        original_value = test_instance.get_master_entity_list()

        # instance should be of expected class.
        test_value = original_value
        should_be = list
        error_string = "master entity list class: {} is not the expected one: {}.".format( test_value, should_be )
        self.assertIsInstance( test_value, should_be, msg = error_string )
        
        # should be 8.
        test_value = len( original_value )
        should_be = 8
        error_string = "master entity list length = {}, should = {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
    
        # set a new value
        new_value = self.TEST_SET_MASTER_ENTITY_LIST
        test_instance.set_master_entity_list( new_value )
        test_value = test_instance.get_master_entity_list()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_network_data_request()
        test_method = "set_network_data_request"
        original_value = test_instance.get_network_data_request()
        new_value = self.TEST_SET_NETWORK_DATA_REQUEST
        test_instance.set_network_data_request( new_value )
        test_value = test_instance.get_network_data_request()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_output_format()
        test_method = "set_output_format"
        original_value = test_instance.get_output_format()
        new_value = self.TEST_SET_OUTPUT_FORMAT
        test_instance.set_output_format( new_value )
        test_value = test_instance.get_output_format()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_output_info_every_x_relations()
        test_method = "set_output_info_every_x_relations"
        original_value = test_instance.get_output_info_every_x_relations()
        new_value = self.TEST_SET_OUTPUT_INFO_EVERY_X_RELATIONS
        test_instance.set_output_info_every_x_relations( new_value )
        test_value = test_instance.get_output_info_every_x_relations()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )        
        
        # ! --------> get/set_output_structure()
        test_method = "set_output_structure"
        original_value = test_instance.get_output_structure()
        new_value = self.TEST_SET_OUTPUT_STRUCTURE
        test_instance.set_output_structure( new_value )
        test_value = test_instance.get_output_structure()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_output_type()
        test_method = "set_output_type"
        original_value = test_instance.get_output_type()
        new_value = self.TEST_SET_OUTPUT_TYPE
        test_instance.set_output_type( new_value )
        test_value = test_instance.get_output_type()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_query_set()
        test_method = "set_query_set"
        original_value = test_instance.get_query_set()
        new_value = self.TEST_SET_OUTPUT_TYPE
        test_instance.set_query_set( new_value )
        test_value = test_instance.get_query_set()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_relation_map()
        test_method = "set_relation_map"
        original_value = test_instance.get_relation_map()
        new_value = self.TEST_SET_RELATION_MAP
        test_instance.set_relation_map( new_value )
        test_value = test_instance.get_relation_map()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_relation_type_slug_list()
        test_method = "set_relation_type_slug_list"
        original_value = test_instance.get_relation_type_slug_list()

        # instance should be of expected class.
        test_value = original_value
        should_be = list
        error_string = "master entity list class: {} is not the expected one: {}.".format( test_value, should_be )
        self.assertIsInstance( test_value, should_be, msg = error_string )
        
        # set a new value
        new_value = self.TEST_SET_RELATION_TYPE_SLUG_LIST
        test_instance.set_relation_type_slug_list( new_value )
        test_value = test_instance.get_relation_type_slug_list()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

        # ! --------> get/set_relation_type_slug_to_instance_map()
        test_method = "set_relation_type_slug_to_instance_map"
        original_value = test_instance.get_relation_type_slug_to_instance_map()

        # instance should be of expected class.
        test_value = original_value
        should_be = dict
        error_string = "master entity list class: {} is not the expected one: {}.".format( test_value, should_be )
        self.assertIsInstance( test_value, should_be, msg = error_string )
        
        # set a new value
        new_value = self.TEST_SET_RELATION_TYPE_SLUG_LIST
        test_instance.set_relation_type_slug_to_instance_map( new_value )
        test_value = test_instance.get_relation_type_slug_to_instance_map()

        # new should equal test
        should_be = new_value
        error_string = "Testing {}(), new = {}, should = {}.".format( test_method, test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
                
        # new should not equal original
        should_not_be = original_value
        error_string = "Testing {}(), new = {}, should NOT = {}.".format( test_method, test_value, should_not_be )
        self.assertNotEqual( test_value, should_not_be, msg = error_string )

    #-- END test method test_getters_and_setters() --#


    def test_initialize_from_request( self ):

        # declare variables
        me = "test_initialize_from_request"
        debug_flag = None
        eval_request = None
        eval_output_format = None
        eval_output_structure = None
        eval_output_type = None
        relation_qs = None
        test_instance = None
        network_data = None
        network_data_char_count = None
        reference_data_file_path = None
        test_request = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # ! ----> get basic test instance
        
        # make request instance
        eval_request = TestHelper.load_basic()
        
        # get test values
        eval_output_format = eval_request.get_output_format()
        eval_output_structure = eval_request.get_output_structure()
        eval_output_type = eval_request.get_output_type()
        
        # use it to set up test instance.
        test_instance = self.set_up_test_instance( request_IN = eval_request )
        
        # part of set up is call to initialize from request.
        
        # ! ----> validate.
        
        # first, retrieve request and make sure it is the right type.
        test_request = test_instance.get_network_data_request()
        
        # instance should be of expected class.
        test_value = test_request
        should_be = NetworkDataRequest
        error_string = "nested request instance: {} is not of class {}.".format( test_value, should_be )
        self.assertIsInstance( test_value, should_be, msg = error_string )
        
        # instance should be the one we passed in.
        test_value = test_request
        should_be = eval_request
        error_string = "nested request instance: {} is not the same as what we passed in: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # make sure that the things set in the instance from the request match.
        
        # output_format
        test_value = test_instance.get_output_format()
        should_be = eval_output_format
        error_string = "Output format \"{}\" is not the same as what we passed in: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )
        
        # output_structure
        test_value = test_instance.get_output_structure()
        should_be = eval_output_structure
        error_string = "Output structure \"{}\" is not the same as what we passed in: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )

        # output_type
        test_value = test_instance.get_output_type()
        should_be = eval_output_type
        error_string = "Output type \"{}\" is not the same as what we passed in: {}.".format( test_value, should_be )
        self.assertEqual( test_value, should_be, msg = error_string )        

    #-- END test method test_initialize_from_request() --#
        
        
    def test_register_relation_type( self ):

        # declare variables
        me = "test_register_relation_type"
        debug_flag = None
        test_instance = None
        current_type_slug = None
        total_type_count = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # ! ----> get basic test instance
        
        # use it to set up test instance.
        test_instance = self.set_up_basic_test_instance()
        
        # Add "mentioned", "qouted", "shared_byline"
        
        # ! ----> "mentioned"
        current_type_slug = "mentioned"
        total_type_count = 1
        
        # get relation type.
        test_relation_type = Entity_Relation_Type.objects.get( slug = current_type_slug )
        
        # register it
        test_instance.register_relation_type( test_relation_type )
        
        # validate
        self.validate_register_relation_type( test_instance, current_type_slug, total_type_count )

        # ! ----> "quoted"
        current_type_slug = "quoted"
        total_type_count = 2
        
        # get relation type.
        test_relation_type = Entity_Relation_Type.objects.get( slug = current_type_slug )
        
        # register it
        test_instance.register_relation_type( test_relation_type )
        
        # validate
        self.validate_register_relation_type( test_instance, current_type_slug, total_type_count )

        # ! ----> "shared_byline"
        current_type_slug = "shared_byline"
        total_type_count = 3
        
        # get relation type.
        test_relation_type = Entity_Relation_Type.objects.get( slug = current_type_slug )
        
        # register it
        test_instance.register_relation_type( test_relation_type )
        
        # validate
        self.validate_register_relation_type( test_instance, current_type_slug, total_type_count )
        
        # ! ----> "quoted" again
        current_type_slug = "quoted"
        total_type_count = 3
        
        # get relation type.
        test_relation_type = Entity_Relation_Type.objects.get( slug = current_type_slug )
        
        # register it
        test_instance.register_relation_type( test_relation_type )
        
        # validate
        self.validate_register_relation_type( test_instance, current_type_slug, total_type_count )

    #-- END test method test_register_relation_type() --#
        
        
    def test_render( self ):

        # declare variables
        me = "test_render"
        debug_flag = None
        network_output = None
        test_request = None
        relation_qs = None
        test_instance = None
        network_data = None
        network_data_char_count = None
        reference_data_file_path = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # ! ----> set up NetworkDataObject child instance.

        test_instance = self.set_up_basic_test_instance()

        # ! ----> render and evaluate

        # render and return the result.
        network_data = test_instance.render()
        network_data_char_count = len( network_data )
        
        # validate against test file.
        reference_data_file_path = TestHelper.FILE_PATH_NETWORK_DATA_REQUEST_BASIC_TSV_OUTPUT
        self.validate_string_against_file_contents( network_data, reference_data_file_path )

    #-- END test method test_render() --#
        
        
    def test_update_entity_relations_details( self ):

        '''
        def update_entity_relations_details( self,
                                             entity_id_IN,
                                             relation_type_IN,
                                             relation_role_IN,
                                             relation_instance_IN = None,
                                             update_relation_map_IN = False ):
        '''

        # declare variables
        me = "test_update_entity_relations_details"
        debug_flag = None
        test_instance = None
        
        # init debug
        debug_flag = self.DEBUG
        
        # print test header
        TestHelper.print_test_header( self.CLASS_NAME, me )
        
        # ! ----> call set up method, includes validation.
        
        test_instance = self.set_up_entity_relations_details( do_validate_IN = True )
        
    #-- END test method test_update_entity_relations_details() --#
        
        
#-- END test class NetworkDataOutputTest --#
