'''
Copyright 2021 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context.

context is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context. If not, see http://www.gnu.org/licenses/.
'''

#================================================================================
# Imports
#================================================================================

# python imports
import logging

# nameparser import
# http://pypi.python.org/pypi/nameparser
from nameparser import HumanName

# Django imports
#from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Q

# python_utilities
from python_utilities.strings.string_helper import StringHelper

# context imports
from context.shared.context_error import ContextError
from context.shared.entity_models import Abstract_Person_Parent
from context.shared.entity_models import output_debug
from context.shared.entity_models import output_log_message


#================================================================================
# ! ==> Abstract Models
#================================================================================


#-------------------------------------------------------------------------------
# ! --------> Abstract Human Models
#-------------------------------------------------------------------------------


# Abstract_Person model
class Abstract_Person( Abstract_Person_Parent ):

    '''
    HumanName (from package "nameparser" ) code sample:

    from nameparser import HumanName
    >>> test = HumanName( "Jonathan Scott Morgan" )
    >>> test
    <HumanName : [
            Title: ''
            First: 'Jonathan'
            Middle: 'Scott'
            Last: 'Morgan'
            Suffix: ''
    ]>
    >>> import pickle
    >>> test2 = pickle.dumps( test )
    >>> test3 = pickle.loads( test2 )
    >>> test3.__eq__( test2 )
    False
    >>> test3.__eq__( test )
    True
    >>> test3.first
    u'Jonathan'
    >>> test3.middle
    u'Scott'
    >>> test3.last
    u'Morgan'
    >>> test3.title
    u''
    >>> test3.suffix
    u''
    >>> if ( test3 == test ):
    ...     print( "True!" )
    ... else:
    ...     print( "False!" )
    ...
    True!
    '''


    #----------------------------------------------------------------------
    # constants-ish
    #----------------------------------------------------------------------

    GENDER_CHOICES = (
        ( 'na', 'Unknown' ),
        ( 'female', 'Female' ),
        ( 'male', 'Male' )
    )

    # lookup status
    LOOKUP_STATUS_FOUND = "found"
    LOOKUP_STATUS_NEW = "new"
    LOOKUP_STATUS_NONE = "None"

    #----------------------------------------------------------------------
    # model fields and meta
    #----------------------------------------------------------------------

    first_name = models.CharField( max_length = 255, blank = True, null = True )
    middle_name = models.CharField( max_length = 255, blank = True, null = True )
    last_name = models.CharField( max_length = 255, blank = True, null = True )
    name_prefix = models.CharField( max_length = 255, blank = True, null = True )
    name_suffix = models.CharField( max_length = 255, blank = True, null = True )
    nickname = models.CharField( max_length = 255, blank = True, null = True )
    full_name_string = models.CharField( max_length = 255, blank = True, null = True )
    original_name_string = models.CharField( max_length = 255, blank = True, null = True )
    gender = models.CharField( max_length = 6, choices = GENDER_CHOICES, blank = True, null = True )
    nameparser_pickled = models.TextField( blank = True, null = True )
    is_ambiguous = models.BooleanField( default = False )

    # moved up to parent
    #notes = models.TextField( blank = True, null = True )
    #create_date = models.DateTimeField( auto_now_add = True )
    #last_modified = models.DateTimeField( auto_now = True )

    # field to store how source was captured - moved up to parent.
    # capture_method = models.CharField( max_length = 255, blank = True, null = True )


    # Meta-data for this class.
    class Meta:

        abstract = True
        ordering = [ 'last_name', 'first_name', 'middle_name' ]

    #-- END class Meta --#


    #----------------------------------------------------------------------
    # ! static methods
    #----------------------------------------------------------------------


    @staticmethod
    def HumanName_to_str( human_name_IN ):

        # return reference
        string_OUT = ""

        string_OUT += "HumanName: \"" + StringHelper.object_to_unicode_string( human_name_IN ) + "\"\n"
        string_OUT += "- title: " + human_name_IN.title + "\n"
        string_OUT += "- first: " + human_name_IN.first + "\n"
        string_OUT += "- middle: " + human_name_IN.middle + "\n"
        string_OUT += "- last: " + human_name_IN.last + "\n"
        string_OUT += "- suffix: " + human_name_IN.suffix + "\n"
        string_OUT += "- nickname: " + human_name_IN.nickname + "\n"

        return string_OUT

    #-- END static method HumanName_to_str() --#


    #----------------------------------------------------------------------
    # ! class methods
    #----------------------------------------------------------------------


    @classmethod
    def create_person_for_name( cls,
                                name_IN,
                                parsed_name_IN = None,
                                remove_periods_IN = False,
                                *args,
                                **kwargs ):

        '''
        Accepts name string.  Creates instance of cls, stores name in it, then
           returns the instance.  Eventually, might do more fancy or
           sophisticated things, but for now, not so much.
        '''

        # return reference
        instance_OUT = None

        # got a name?
        if ( ( name_IN is not None ) and ( name_IN != "" ) ):

            # create new Person!
            instance_OUT = cls()

            # store name
            instance_OUT.set_name( name_IN,
                                   parsed_name_IN = parsed_name_IN,
                                   remove_periods_IN = remove_periods_IN,
                                   *args,
                                   **kwargs )

        else:

            instance_OUT = None

        #-- END check to make sure there is a name. --#

        return instance_OUT

    #-- END class method create_person_for_name() --#


    @classmethod
    def find_person_from_name( cls, name_IN, do_strict_match_IN = True, do_partial_match_IN = False ):

        '''
        More flexible way of looking for a person than look_up_person_from_name
            (though it uses it quite extensively).  Accepts name string.  Tries
            the following to find a matching person:
            - looks for exact match.
            - if no match, checks if one word.  If just one word, looks for
                any name part that contains that one word.
            - if not one word, or no one-word match, tries non-exact lookup.
            - if no match, tries non-exact, partial lookup.

        Postconditions: returns QuerySet instance with what this method could
            find.  Might be empty.  If fatal error, returns None.
        '''

        # return reference
        query_set_OUT = None

        # declare variables
        me = "find_person_from_name"
        match_count = -1
        name_part_list = None
        name_part_count = -1

        # first, try a strict lookup.
        query_set_OUT = cls.look_up_person_from_name( name_IN, do_strict_match_IN = do_strict_match_IN, do_partial_match_IN = do_partial_match_IN )

        # got anything back?
        if ( query_set_OUT is not None ):

            # not None, do we have anything in QuerySet?
            match_count = query_set_OUT.count()
            if ( match_count == 0 ):

                # no exact matches.  Is it just one word?
                name_part_list = name_IN.split()
                name_part_count = len( name_part_list )
                if ( name_part_count == 1 ):

                    # just one word.  Try the old way, so we get either first,
                    #    middle or last.
                    query_set_OUT = cls.objects.filter( Q( first_name__icontains = name_IN ) | Q( middle_name__icontains = name_IN ) | Q( last_name__icontains = name_IN ) | Q( full_name_string__icontains = name_IN ) )

                #-- END check to see if just one word. --#

                # got anything back?
                match_count = query_set_OUT.count()
                if ( match_count == 0 ):

                    # no.  Try not strict.
                    query_set_OUT = cls.look_up_person_from_name( name_IN, do_strict_match_IN = False, do_partial_match_IN = False )

                    # got anything back?
                    match_count = query_set_OUT.count()
                    if ( match_count == 0 ):

                        # no exact matches.  Try not strict, allow partial match.
                        query_set_OUT = cls.look_up_person_from_name( name_IN, do_strict_match_IN = False, do_partial_match_IN = True )

                        # got anything back?
                        match_count = query_set_OUT.count()
                        if ( match_count == 0 ):

                            # no lookup matches.  Try the old way...
                            query_set_OUT = cls.objects.filter( Q( first_name__icontains = name_IN ) | Q( middle_name__icontains = name_IN ) | Q( last_name__icontains = name_IN ) | Q( full_name_string__icontains = name_IN ) )

                        #-- END check to see if any non-strict partial matches. --#

                    #-- END check to see if any non-strict matches. --#

                #-- END check to see if any matches for just one word. --#

            #-- END check to see if strict matches. --#

        else:

            output_debug( "In " + me + ": None returned for name {}, so returning None.".format( name_IN ) )

        #-- END check to see if None --#

        return query_set_OUT

    #-- END class method find_person_from_name() --#

    @classmethod
    def get_name_part_count_from_name( cls, name_string_IN ):

        '''
        Accepts a name string.  Returns list of name parts. This works
            with nameparser.HumanName - it parses the name using HumanName, then
            retrieves each name part that HumanName knows about and puts those
            that are not emtpy into a list. Returns the list.
        '''

        # return reference
        value_OUT = None

        # declare variables
        name_part_list = None
        name_part_count = None

        # Make sure we have a string value
        if ( ( name_string_IN is not None ) and ( name_string_IN != "" ) ):

            # get name part list
            name_part_list = cls.get_name_part_list_from_name( name_string_IN )

            # got anything back?
            if ( name_part_list is not None ):

                # get and return count.
                name_part_count = len( name_part_list )
                value_OUT = name_part_count

            else:

                # error. return None
                value_OUT = None

            #-- END check for returned name part list. --#

        else:

            # None - No string passed in, so returning None.
            value_OUT = None

        #-- END check to see if None. --#

        return value_OUT

    #-- END class method get_name_part_count_from_name() --#


    @classmethod
    def get_name_part_list_from_name( cls, name_string_IN ):

        '''
        Accepts a name string.  Returns list of name parts. This works
            with nameparser.HumanName - it parses the name using HumanName, then
            retrieves each name part that HumanName knows about and puts those
            that are not emtpy into a list. Returns the list.
        '''

        # return reference
        list_OUT = None

        # declare variables
        human_name = None
        name_part_value_list = None
        name_part_list = None
        name_part = ""
        cleaned_name_part = ""

        # init
        name_part_value_list = list()
        name_part_list = list()

        # Make sure we have a string value
        if ( ( name_string_IN is not None ) and ( name_string_IN != "" ) ):

            # parse with HumanName
            human_name = HumanName( name_string_IN )

            # make list of HumanName's name parts
            name_part_value_list.append( human_name.first )
            name_part_value_list.append( human_name.middle )
            name_part_value_list.append( human_name.last )
            name_part_value_list.append( human_name.title )  # prefix
            name_part_value_list.append( human_name.suffix )
            name_part_value_list.append( human_name.nickname )

            # loop, checking each for being empty - add any that are not empty to return list.
            for name_part in name_part_value_list:

                # got anything?
                if ( ( name_part is not None ) and ( name_part != "" ) ):

                    # clean it up - strip white space.
                    cleaned_name_part = name_part.strip()

                    # got anything now?
                    if ( cleaned_name_part != "" ):

                        # yup.  Add to return list.
                        name_part_list.append( cleaned_name_part )

                    #-- END check to see if other name parts. --#

                #-- check to see if empty. --#

            #-- loop over other name parts. --#

            # return list.
            list_OUT = name_part_list

        else:

            # None - No string passed in, so returning None.
            list_OUT = None

        #-- END check to see if None. --#

        return list_OUT

    #-- END class method get_name_part_list_from_name() --#


    @classmethod
    def get_person_for_name( cls,
                             name_IN,
                             create_if_no_match_IN = False,
                             parsed_name_IN = None,
                             do_strict_match_IN = False,
                             do_partial_match_IN = False ):

        '''
        This method accepts the full name of a person.  Uses NameParse object to
           parse name into prefix/title, first name, middle name(s), last name,
           and suffix.  Looks first for an exact person match.  If one found,
           returns it.  If none found, returns new Person instance with name
           stored in it.
        preconditions: None.
        postconditions: Looks first for an exact person match.  If one found,
           returns it.  If none found, returns new Person instance with name
           stored in it.  If multiple matches found, error, so will return None.
           If new Person instance returned, it will not have been saved.  If you
           want that person to be in the database, you have to save it yourself.
        '''

        # return reference
        instance_OUT = None

        # declare variables.
        me = "get_person_for_name"
        person_qs = None
        person_count = -1
        id_list = []

        # got a name?
        if ( name_IN ):

            # try to retrieve person for name.
            person_qs = cls.look_up_person_from_name( name_IN,
                                                      parsed_name_IN = parsed_name_IN,
                                                      do_strict_match_IN = do_strict_match_IN,
                                                      do_partial_match_IN = do_partial_match_IN )

            # got a match?
            person_count = person_qs.count()
            if ( person_count == 1 ):

                # got one match.  Return it.
                instance_OUT = person_qs.get()

                output_debug( "In " + me + ": found single match for name: " + name_IN )

            elif( person_count == 0 ):

                # no matches.  What do we do?
                if ( create_if_no_match_IN == True ):

                    # create new Person!
                    instance_OUT = cls.create_person_for_name( name_IN, parsed_name_IN = parsed_name_IN )

                    output_debug( "In " + me + ": no match for name: \"" + name_IN + "\"; so, creating new Person instance (but not saving yet)!" )

                else:

                    # return None!
                    instance_OUT = None

                    output_debug( "In " + me + ": no match for name: \"" + name_IN + "\"; so, returning None!" )

                #-- END check to see if we create on no match. --#

            else:

                # Multiple matches.  Trouble.
                id_list = []
                for person in person_qs:

                    id_list.append( person.id )

                #-- END loop over person matches. --#

                output_debug( "In " + me + ": multiple matches for name \"" + name_IN + "\" ( " + str( id_list ) + " ).  Returning None." )
                instance_OUT = None

            #-- END check count of persons returned. --#

        else:

            # No name passed in.  Nothing to return.
            output_debug( "In " + me + ": no name passed in, so returning None." )
            instance_OUT = None

        #-- END check for name string passed in. --#

        return instance_OUT

    #-- END method get_person_for_name() --#


    @classmethod
    def get_person_lookup_status( cls, person_IN ):

        # return reference
        status_OUT = ""

        # declare variables

        if ( person_IN is not None ):

            if ( ( person_IN.id ) and ( person_IN.id > 0 ) ):

                # there is an ID, so this is not a new record.
                status_OUT = cls.LOOKUP_STATUS_FOUND

            else:

                # Person returne, but no ID, so this is a new record - not found.
                status_OUT = cls.LOOKUP_STATUS_NEW

            #-- END check to see if ID present in record returned. --#

        else:

            # None - either multiple matches (eek!) or error.
            status_OUT = cls.LOOKUP_STATUS_NONE

        #-- END check to see if None. --#

        return status_OUT

    #-- END class method get_person_lookup_status() --#


    @classmethod
    def is_single_name_part( cls, name_string_IN ):

        '''
        Accepts a name string.  If name string just has a single word, returns
            True.  If not, returns False.  If error, returns None.  This works
            with nameparser.HumanName - it parses the name using HumanName, then
            checks to see if there is a value in first_name and the rest of the
            values are empty.  If that is the case, then single name part.  If
            more than one name field is populated, then not single name part.
        '''

        # return reference
        is_single_name_OUT = False

        # declare variables
        me = "is_single_name_part"
        status_message = None
        name_part_count = None

        # Make sure we have a string value
        if ( ( name_string_IN is not None ) and ( name_string_IN != "" ) ):

            # get count.
            name_part_count = cls.get_name_part_count_from_name( name_string_IN )

            # how many?
            if ( name_part_count == 1 ):

                # single name part.
                is_single_name_OUT = True

            elif ( name_part_count > 1 ):

                # more than one name part.
                is_single_name_OUT = False

            else:

                # not 1 or > 1. Error.
                is_single_name_OUT = None
                status_message = "In Abstract_Person.{me}(): name_count = {name_count}, not 1 or greater than 1, unexpected at this point.".format(
                    me = me,
                    name_count = name_part_count
                )
                raise ContexError( "status_message" )

            #-- END how many name parts found? --#

        else:

            # None - No string passed in, so returning None.
            is_single_name_OUT = None

        #-- END check to see if None. --#

        return is_single_name_OUT

    #-- END class method is_single_name_part() --#


    @classmethod
    def look_up_person_from_name( cls,
                                  name_IN = "",
                                  parsed_name_IN = None,
                                  do_strict_match_IN = False,
                                  do_partial_match_IN = False,
                                  qs_IN = None,
                                  *args,
                                  **kwargs ):

        '''
        This method accepts the full name of a person.  Uses NameParse object to
           parse name into prefix/title, first name, middle name(s), last name,
           and suffix.  Uses the result of the parse to lookup the person in
           the database by name part.  If do_strict_match_IN is True, looks for
           the exact combination of the name parts (so if a record has same
           first and last name, and a middle name, but the string passed in just
           has a middle name, no match).  If do_strict_match_IN is False, the
           above example would result in a match.  Returns QuerySet that results
           from filtering Person objects based on name string passed in.  If
           None found, returns empty QuerySet.  If error, returns None.
        preconditions: None.
        postconditions: Returns QuerySet that results from filtering Person
           objects based on name string passed in.  If None found, returns empty
           QuerySet.  If error, returns None.
        '''

        # return reference
        qs_OUT = None

        # declare variables.
        me = "look_up_person_from_name"
        parsed_name = None
        prefix = ""
        first = ""
        middle = ""
        last = ""
        suffix = ""
        nickname = ""
        strict_q = None

        # got a name or a pre-parsed name?
        if ( ( ( name_IN is not None ) and ( name_IN != "" ) )
            or ( parsed_name_IN is not None ) ):

            # Got a pre-parsed name?
            if ( parsed_name_IN is not None ):

                # yes. Use it.
                parsed_name = parsed_name_IN

            else:

                # no. Parse name_IN using HumanName class from nameparser.
                parsed_name = HumanName( name_IN )

            #-- END check to see if pre-parsed name. --#

            # Use parsed values to build a search QuerySet.  First, get values.
            prefix = parsed_name.title
            first = parsed_name.first
            middle = parsed_name.middle
            last = parsed_name.last
            suffix = parsed_name.suffix
            nickname = parsed_name.nickname

            # build up queryset.
            if ( qs_IN is not None ):

                # got one passed in, start with it.
                qs_OUT = qs_IN

            else:

                # make a new one
                qs_OUT = cls.objects.all()

            #-- END check to see if QuerySet passed in. --#

            # got a prefix?
            if ( prefix ):

                # yes - allow partial match?
                if ( do_partial_match_IN == True ):

                    # yes.
                    qs_OUT = qs_OUT.filter( name_prefix__icontains = prefix )

                else:

                    # no.
                    qs_OUT = qs_OUT.filter( name_prefix__iexact = prefix )

                #-- END check to see if we allow partial match. --#

            else:

                # are we being strict?
                if ( do_strict_match_IN == True ):

                    # yes - None or ""?
                    if ( ( prefix is None ) or ( prefix == "" ) ):

                        # for None or "", match to either NULL OR "".
                        strict_q = Q( name_prefix__isnull = True ) | Q( name_prefix__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )

                    else:

                        # for anything else, what?  Stupid Python False values...
                        pass

                    #-- END check to see what exact value of prefix is. --#

                #-- END check to see if strict. --#

            #-- END check for prefix --#

            # first name
            if ( first ):

                # allow partial match?
                if ( do_partial_match_IN == True ):

                    # yes.
                    qs_OUT = qs_OUT.filter( first_name__icontains = first )

                else:

                    # no.
                    qs_OUT = qs_OUT.filter( first_name__iexact = first )

                #-- END check to see if we allow partial match. --#

            else:

                # are we being strict?
                if ( do_strict_match_IN == True ):

                    # yes - None or ""?
                    if ( ( first is None ) or ( first == "" ) ):

                        # for None or "", match to either NULL OR "".
                        strict_q = Q( first_name__isnull = True ) | Q( first_name__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )

                    else:

                        # for anything else, what?  Stupid Python False values...
                        pass

                    #-- END check to see what exact value of first is. --#

                #-- END check to see if strict. --#

            #-- END check for first name --#

            # middle name
            if ( middle ):

                # allow partial match?
                if ( do_partial_match_IN == True ):

                    # yes.
                    qs_OUT = qs_OUT.filter( middle_name__icontains = middle )

                else:

                    # no.
                    qs_OUT = qs_OUT.filter( middle_name__iexact = middle )

                #-- END check to see if we allow partial match. --#

            else:

                # are we being strict?
                if ( do_strict_match_IN == True ):

                    # yes - None or ""?
                    if ( ( middle is None ) or ( middle == "" ) ):

                        # for None or "", match to either NULL OR "".
                        strict_q = Q( middle_name__isnull = True ) | Q( middle_name__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )

                    else:

                        # for anything else, what?  Stupid Python False values...
                        pass

                    #-- END check to see what exact value of middle is. --#

                #-- END check to see if strict. --#

            #-- END check for middle name --#

            # last name
            if ( last ):

                # allow partial match?
                if ( do_partial_match_IN == True ):

                    # yes.
                    qs_OUT = qs_OUT.filter( last_name__icontains = last )

                else:

                    # no.
                    qs_OUT = qs_OUT.filter( last_name__iexact = last )

                #-- END check to see if we allow partial match. --#

            else:

                # are we being strict?
                if ( do_strict_match_IN == True ):

                    # yes - None or ""?
                    if ( ( last is None ) or ( last == "" ) ):

                        # for None or "", match to either NULL OR "".
                        strict_q = Q( last_name__isnull = True ) | Q( last_name__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )

                    else:

                        # for anything else, what?  Stupid Python False values...
                        pass

                    #-- END check to see what exact value of last is. --#

                #-- END check to see if strict. --#

            #-- END check for last name --#

            # suffix
            if ( suffix ):

                # allow partial match?
                if ( do_partial_match_IN == True ):

                    # yes.
                    qs_OUT = qs_OUT.filter( name_suffix__icontains = suffix )

                else:

                    # no.
                    qs_OUT = qs_OUT.filter( name_suffix__iexact = suffix )

                #-- END check to see if we allow partial match. --#

            else:

                # are we being strict?
                if ( do_strict_match_IN == True ):

                    # yes - None or ""?
                    if ( ( suffix is None ) or ( suffix == "" ) ):

                        # for None or "", match to either NULL OR "".
                        strict_q = Q( name_suffix__isnull = True ) | Q( name_suffix__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )

                    else:

                        # for anything else, what?  Stupid Python False values...
                        pass

                    #-- END check to see what exact value of suffix is. --#

                #-- END check to see if strict. --#

            #-- END suffix --#

            # nickname
            if ( nickname ):

                # allow partial match?
                if ( do_partial_match_IN == True ):

                    # yes.
                    qs_OUT = qs_OUT.filter( nickname__icontains = nickname )

                else:

                    # no.
                    qs_OUT = qs_OUT.filter( nickname__iexact = nickname )

                #-- END check to see if we allow partial match. --#

            else:

                # are we being strict?
                if ( do_strict_match_IN == True ):

                    # yes - None or ""?
                    if ( ( nickname is None ) or ( nickname == "" ) ):

                        # for None or "", match to either NULL OR "".
                        strict_q = Q( nickname__isnull = True ) | Q( nickname__iexact = "" )
                        qs_OUT = qs_OUT.filter( strict_q )

                    else:

                        # for anything else, what?  Stupid Python False values...
                        pass

                    #-- END check to see what exact value of nickname is. --#

                #-- END check to see if strict. --#

            #-- END nickname --#

        else:

            # No name, returning None
            output_debug( "In " + me + ": no name passed in, returning Empty QuerySet." )
            qs_OUT = cls.objects.none()

        #-- END check to see if we have a name. --#

        return qs_OUT

    #-- END static method look_up_person_from_name() --#


    @classmethod
    def standardize_name_part( cls, name_part_IN, remove_periods_IN = False ):

        '''
        Accepts string name part, does the following to standardize it, in this
        order:
           - removes any commas.
           - strips white space from the beginning and end.
           - More to come?

        preconditions: None.

        postconditions: None.
        '''

        # return reference
        name_part_OUT = ""

        # declare variables
        working_string = ""

        # start with name part passed in.
        working_string = name_part_IN

        # first, check to see if anything passed in.
        if ( ( working_string is not None ) and ( working_string != "" ) ):

            # remove commas.
            working_string = working_string.replace( ",", "" )

            # remove periods as well?
            if ( remove_periods_IN == True ):

                # yes.
                working_string = working_string.replace( ".", "" )

            #-- END check to see if remove periods --#

            # strip white space.
            working_string = working_string.strip()

        #-- END check to see if anything passed in. --#

        # return working_string.
        name_part_OUT = working_string

        return name_part_OUT

    #-- END method standardize_name_part() --#


    #----------------------------------------------------------------------
    # ! instance methods
    #----------------------------------------------------------------------

    def __init__( self, *args, **kwargs ):

        # call parent __init()__ first.
        super().__init__( *args, **kwargs )

    #-- END method __init__() --#


    def __str__( self ):

        # return reference
        string_OUT = ''

        # declare variables
        string_list = []

        if ( self.id ):

            string_OUT = str( self.id ) + " - "

        #-- END check to see if ID --#

        string_OUT += self.last_name + ', ' + self.first_name

        # middle name?
        if ( self.middle_name ):

            string_OUT += " " + self.middle_name

        #-- END middle name check --#

        if ( ( self.title ) or ( self.organization_string ) or ( self.capture_method ) ):

            string_OUT += " ( "

            string_list = []

            if ( self.title ):

                # add title to list
                string_list.append( "title = " + self.title )

            #-- END check for title --#

            if ( self.organization_string ):

                # add title to list
                string_list.append( "organization = " + self.organization_string )

            #-- END check for title --#

            if ( self.capture_method ):

                # add capture method to the list.
                string_list.append( "capture_method = " + self.capture_method )

            #-- END check for capture_method --#

            string_OUT += "; ".join( string_list )

            string_OUT += " )"

        #-- END check to see if we have a title, organization, or capture_method. --#

        return string_OUT

    #-- END method __str__() --#


    def get_name_part_count( self ):

        '''
        Retrieves name part list from `get_name_part_list()`. Returns count.
        '''

        # return reference
        value_OUT = None

        # declare variables
        name_part_list = None
        name_part_count = None

        # get name part list
        name_part_list = self.get_name_part_list()

        # got anything back?
        if ( name_part_list is not None ):

            # get and return count.
            name_part_count = len( name_part_list )
            value_OUT = name_part_count

        else:

            # error. return None
            value_OUT = None

        #-- END check for returned name part list. --#

        return value_OUT

    #-- END class method get_name_part_count() --#


    def get_name_part_list( self ):

        '''
        Returns list of name parts, retrieved from the fields within this instance.
        '''

        # return reference
        list_OUT = None

        # declare variables
        name_part_value_list = None
        name_part_list = None
        name_part = ""
        cleaned_name_part = ""

        # init
        name_part_value_list = list()
        name_part_list = list()

        # make list of instance's name parts
        name_part_value_list.append( self.first_name )
        name_part_value_list.append( self.middle_name )
        name_part_value_list.append( self.last_name )
        name_part_value_list.append( self.name_prefix )
        name_part_value_list.append( self.name_suffix )
        name_part_value_list.append( self.nickname )

        # loop, checking each for being empty - add any that are not empty to return list.
        for name_part in name_part_value_list:

            # got anything?
            if ( ( name_part is not None ) and ( name_part != "" ) ):

                # clean it up - strip white space.
                cleaned_name_part = name_part.strip()

                # got anything now?
                if ( cleaned_name_part != "" ):

                    # yup.  Add to return list.
                    name_part_list.append( cleaned_name_part )

                #-- END check to see if other name parts. --#

            #-- check to see if empty. --#

        #-- loop over other name parts. --#

        list_OUT = name_part_list

        return list_OUT

    #-- END class method get_name_part_list() --#


    def get_name_string( self ):

        '''
        Converts current person's name into a HumanName, then call the str()
           function on that name to convert it to a string.  Returns that
           string.
        '''

        # return reference
        value_OUT = ""

        # declare variables
        my_HumanName = None

        # get human name for this instance.
        my_HumanName = self.to_HumanName()

        # if nickname, remove it so it doesn't get output at the end of the
        #    string like a last name.
        if ( my_HumanName.nickname ):

            # yes - get rid of it.
            my_HumanName.nickname = ""

        #-- END check to see if nickname. --#

        # convert that to a string.
        value_OUT = str( my_HumanName )

        return value_OUT

    #-- END method get_name_string() --#


    def is_single_name( self ):

        '''
        Retrieves count of name parts from `get_name_part_count()`. Returns
            True if 1, False if > 1, and raises ContextException otherwise.
        '''

        # return reference
        is_single_name_OUT = False

        # declare variables
        me = "is_single_name"
        status_message = None
        name_part_count = None

        # get count.
        name_part_count = self.get_name_part_count( name_string_IN )

        # how many?
        if ( name_part_count == 1 ):

            # single name part.
            is_single_name_OUT = True

        elif ( name_part_count > 1 ):

            # more than one name part.
            is_single_name_OUT = False

        else:

            # not 1 or > 1. Error.
            is_single_name_OUT = None
            status_message = "In Abstract_Person.{me}(): name_count = {name_count}, not 1 or greater than 1, unexpected at this point.".format(
                me = me,
                name_count = name_part_count
            )
            raise ContexError( "status_message" )

        #-- END how many name parts found? --#

        return is_single_name_OUT

    #-- END class method is_single_name() --#


    def standardize_name_parts( self, remove_periods_IN = False ):

        '''
        This method looks at each part of a name and for each, calls the method
           standardize_name_part() to do the following to standardize it, in this
           order:
           - removes any commas.
           - strips white space from the beginning and end.
           - More to come?  Best list is in standardize_name_part()

        preconditions: None.

        postconditions: if needed, name parts in instance are updated to be
           standardized.  Instance is not saved.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "standardize_name_parts"

        # standardize name parts.
        if ( self.name_prefix ):

            self.name_prefix = self.standardize_name_part( self.name_prefix, remove_periods_IN = remove_periods_IN )

        #-- END check to see if name_prefix.

        if ( self.first_name ):

            self.first_name = self.standardize_name_part( self.first_name, remove_periods_IN = remove_periods_IN )

        #-- END check to see if first_name.

        if ( self.middle_name ):

            self.middle_name = self.standardize_name_part( self.middle_name, remove_periods_IN = remove_periods_IN )

        #-- END check to see if middle_name.

        if ( self.last_name ):

            self.last_name = self.standardize_name_part( self.last_name, remove_periods_IN = remove_periods_IN )

        #-- END check to see if last_name.

        if ( self.name_suffix ):

            self.name_suffix = self.standardize_name_part( self.name_suffix, remove_periods_IN = remove_periods_IN )

        #-- END check to see if name_suffix.

        if ( self.nickname ):

            self.nickname = self.standardize_name_part( self.nickname, remove_periods_IN = remove_periods_IN )

        #-- END check to see if nickname.

        return instance_OUT

    #-- END method clean_up_name_parts() --#


    def save( self, *args, **kwargs ):

        '''
        Overridden save() method that automatically creates a full name string
           for a person in case one is not specified.

        Note: looks like child classes don't have to override save method.
        '''

        # declare variables.
        name_HumanName = None
        generated_full_name_string = ""

        # standardize name parts
        self.standardize_name_parts()

        # Make HumanName() instance from this Person's name parts.
        name_HumanName = self.to_HumanName()

        # use it to update the full_name_string.
        self.full_name_string = StringHelper.object_to_unicode_string( name_HumanName )

        # call parent save() method.
        super( Abstract_Person, self ).save( *args, **kwargs )

    #-- END method save() --#


    def set_name( self,
                  name_IN,
                  parsed_name_IN = None,
                  remove_periods_IN = False,
                  *args,
                  **kwargs ):

        '''
        This method accepts the full name of a person.  Uses NameParse object to
           parse name into prefix/title, first name, middle name(s), last name,
           and suffix.  Stores resulting parsed values in this instance, and also
           stores the pickled name object and the full name string.
        preconditions: None.
        postconditions: Updates values in this instance with values parsed out of
           name passed in.
        '''

        # declare variables.
        me = "set_name"
        parsed_name = None
        prefix = ""
        first = ""
        middle = ""
        last = ""
        suffix = ""
        nickname = ""
        standardized_hn = None

        # No name, returning None
        output_debug( "In " + me + ": storing name: " + str( name_IN ) )

        # got a name?
        if ( ( name_IN is not None ) and ( name_IN != "" ) ):

            # yes.  Store original name string
            self.original_name_string = name_IN

            # was parsed name passed in?
            if ( parsed_name_IN is not None ):

                # used pre-parsed name.
                parsed_name = parsed_name_IN

                # No name, returning None
                output_debug( "In " + me + ": using pre-parsed name: " + str( parsed_name_IN ) )

            else:

                # Parse it using HumanName class from nameparser.
                parsed_name = HumanName( name_IN )

            #-- END check to see if name already parsed. --#

            # Use parsed values to build a search QuerySet.  First, get values.
            prefix = parsed_name.title
            first = parsed_name.first
            middle = parsed_name.middle
            last = parsed_name.last
            suffix = parsed_name.suffix
            nickname = parsed_name.nickname

            # got a prefix?
            if ( prefix ):

                # set value
                self.name_prefix = prefix

            #-- END check for prefix --#

            # first name
            if ( first ):

                # set value
                self.first_name = first

            #-- END check for first name --#

            # middle name
            if ( middle ):

                # set value
                self.middle_name = middle

            #-- END check for middle name --#

            # last name
            if ( last ):

                # set value
                self.last_name = last

            #-- END check for last name --#

            # suffix
            if ( suffix ):

                # set value
                self.name_suffix = suffix

            #-- END suffix --#

            # nickname
            if ( nickname ):

                # set value
                self.nickname = nickname

            #-- END nickname --#

            # standardize name parts
            self.standardize_name_parts( remove_periods_IN = remove_periods_IN )

            # Finally, store the full name string (and the pickled object?).
            standardized_hn = self.to_HumanName()

            # convert name to string - different in python 2 and 3.
            self.full_name_string = StringHelper.object_to_unicode_string( standardized_hn )

            # not pickling at the moment.
            #self.nameparser_pickled = pickle.dumps( standardized_hn )

        else:

            # No name, returning None
            output_debug( "In " + me + ": no name passed in, returning None." )

        #-- END check to see if we have a name. --#

    #-- END method set_name() --#


    def to_HumanName( self ):

        '''
        This method creates a nameparser HumanName() object instance, then uses
           the values from this Abstract_Person instance to populate it.  Returns
           the HumanName instance.

        preconditions: None.
        postconditions: None.
        '''

        # return reference
        instance_OUT = None

        # declare variables
        me = "to_HumanName"

        # make HumanString instance.
        instance_OUT = HumanName()

        # Use nested values to populate HumanName.
        if ( self.name_prefix ):

            instance_OUT.title = self.name_prefix

        #-- END check to see if name_prefix.

        if ( self.first_name ):

            instance_OUT.first = self.first_name

        #-- END check to see if first_name.

        if ( self.middle_name ):

            instance_OUT.middle = self.middle_name

        #-- END check to see if middle_name.

        if ( self.last_name ):

            instance_OUT.last = self.last_name

        #-- END check to see if last_name.

        if ( self.name_suffix ):

            instance_OUT.suffix = self.name_suffix

        #-- END check to see if name_suffix.

        if ( self.nickname ):

            instance_OUT.nickname = self.nickname

        #-- END check to see if nickname.

        return instance_OUT

    #-- END method to_HumanName() --#


#== END abstract Abstract_Person Model ========================================#
