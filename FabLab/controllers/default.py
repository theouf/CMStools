# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    
     if not session.counter:
                                session.counter = 1
     else:
                                session.counter += 1
     return dict(message="Bienvenu sur l\' Application Novar et Precidot",counter=session.counter);

def first():
   
    return dict()

def second():
    
    return dict()
