from __future__ import unicode_literals

'''
Copyright 2010-2015 Jonathan Morgan

This file is part of http://github.com/jonathanmorgan/context.

context is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

context is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with http://github.com/jonathanmorgan/context. If not, see http://www.gnu.org/licenses/.
'''

# import djanfgo.conf.urls.defaults stuff.
#from django.conf.urls.defaults import *
from django.conf.urls import include
from django.conf.urls import url

# and import stuff to use the admin's login page for all authentication.
from django.contrib.auth import views as auth_views

# import polls from mysite
import context.views

# context_text URL settings, intended to be included in master urls.py file.
urlpatterns = [

    # index page
    url( r'^index$', context.views.index, name = "context-index" ),

    # link the default authentication page to the admin login page.
    url( r'^accounts/login/$', auth_views.LoginView.as_view( template_name = "registration/login.html" ), name = "context-login" ),
    
    # created a view to log people out that redirects to server root.    
    url( r'^accounts/logout/$', context.views.logout, name = "context-logout" ),
    
]