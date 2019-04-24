from django.shortcuts import render

# import django authentication code.
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Import objects from the django.http library.
#from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect

# import django code for csrf security stuff.
from django.template.context_processors import csrf

# python_utilities
from python_utilities.django_utils.django_view_helper import DjangoViewHelper


#================================================================================
# ! ==> Shared variables and functions
#================================================================================

def get_request_data( request_IN ):
    
    '''
    Accepts django request.  Based on method, grabs the container for incoming
        parameters and returns it:
        - for method "POST", returns request_IN.POST
        - for method "GET", returns request_IN.GET
    '''
    
    # return reference
    request_data_OUT = None

    # call method in DjangoViewHelper
    request_data_OUT = DjangoViewHelper.get_request_data( request_IN )
    
    return request_data_OUT
    
#-- END function get_request_data() --#


DEBUG = True
LOGGER_NAME = "context.views"

def output_debug( message_IN, method_IN = "", indent_with_IN = "", logger_name_IN = "" ):
    
    '''
    Accepts message string.  If debug is on, logs it.  If not,
       does nothing for now.
    '''
    
    # declare variables
    my_logger_name = ""
    
    # got a logger name?
    my_logger_name = LOGGER_NAME
    if ( ( logger_name_IN is not None ) and ( logger_name_IN != "" ) ):
    
        # use logger name passed in.
        my_logger_name = logger_name_IN
        
    #-- END check to see if logger name --#

    # call DjangoViewHelper method.
    DjangoViewHelper.output_debug( message_IN,
                                   method_IN = method_IN,
                                   indent_with_IN = indent_with_IN,
                                   logger_name_IN = my_logger_name,
                                   debug_flag_IN = DEBUG )

#-- END method output_debug() --#


#===============================================================================
# ! ==> view action methods (in alphabetical order)
#===============================================================================


@login_required
def index( request_IN ):
    
    # return reference
    me = "index"
    response_OUT = None
    response_dictionary = {}
    default_template = ''

    # initialize response dictionary
    response_dictionary = {}
    response_dictionary.update( csrf( request_IN ) )

    # set my default rendering template
    default_template = 'context/index.html'

    # add on the "me" property.
    response_dictionary[ 'current_view' ] = me        

    # render response
    response_OUT = render( request_IN, default_template, response_dictionary )

    return response_OUT

#-- END view method index() --#


def logout( request_IN ):

    # declare variables
    me = "context.views.logout"
    request_data = None
    redirect_path = ""
    
    # initialize redirect_path
    redirect_path = "/"
    
    # do we have input parameters?
    request_data = get_request_data( request_IN )
    if ( request_data is not None ):
    
        # we do.  See if we have redirect.
        redirect_path = request_data.get( "post_logout_redirect", "/" )

    #-- END check to see if we have request data. --#

    # log out the user.
    auth.logout( request_IN )

    # Redirect to server home page for now.
    return HttpResponseRedirect( redirect_path )
    
#-- END view method logout() --#


