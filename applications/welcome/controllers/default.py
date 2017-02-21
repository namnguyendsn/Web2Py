#from urllib.parse import urlparse, parse_qs #python 3
from urlparse import urlparse, parse_qs #python 2
# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if not session.counter:
        session.counter=1
    else:
        session.counter +=1
    #response.flash = T("Hello World")
    #return dict(message=T('Welcome to web2py!')
    #return "Chào nhớ, đây là app của tao (nguyennamdsn)"
    return dict(message="Đây là app của tao (nguyennamdsn)", Counter=session.counter)

def UpdateGardenInfo():
    PostBody = request.body.read() # Query string
    ConvertToDict = parse_qs(PostBody) # parse_qs: parse query string
    if len(PostBody) != 0:
        db.GardenInfo.insert(SoilMoisture=ConvertToDict["SoilMoisture"][0], 
                            AirHumidity=ConvertToDict["AirHumidity"][0],
                            Temperature=ConvertToDict["Temperature"][0],
                            RelayStatus=ConvertToDict["RelayStatus"][0])
        db.commit()
    return dict()
    
def TestDB():
    db.GardenInfo.insert(SoilMoisture=111, 
                        AirHumidity=222,
                        Temperature=333,
                        RelayStatus=444)
    db.commit()
    return dict()

def FirstPage0():
    formVar = FORM(INPUT(_name='VisitorName', requires=IS_NOT_EMPTY()),
                    INPUT(_name='VisitorCountry'),
                    INPUT(_name='VisitorAge'),
                    INPUT(_type='submit'))
    if formVar.process().accepted:
        session.VisitorName=formVar.vars.VisitorName
        session.VisitorCountry=formVar.vars.VisitorCountry
        session.VisitorAge=formVar.vars.VisitorAge
        redirect(URL(SecondPage))
    return dict(form=formVar)

def FirstPage1():
    FormSql = SQLFORM.factory(Field('VisitorName', label='お名前は?', requires=IS_NOT_EMPTY()),
                              Field('VisitorCountry', label='お国?'))
    if FormSql.process().accepted:
        session.VisitorName = FormSql.vars.VisitorName
        session.VisitorCountry=FormSql.vars.VisitorCountry
        redirect(URL(SecondPage))
    return dict(form=FormSql)

    #if request.vars.VisitorName:
    #    session.VisitorName = request.vars.VisitorName
    #    redirect(URL(SecondPage)) # Goto SecondPage.html
    #if request.vars.VisitorCountry:
    #    session.VisitorCountry = request.vars.VisitorCountry
    #    redirect(URL(FirstPage)) # Goto FirstPaga.html
    #return dict()
def SecondPage():
    maxID=db(db.GardenInfo).select(db.GardenInfo.id.max()).first()['MAX(GardenInfo.id)']
    row = db.GardenInfo(maxID)
    return dict(row=row)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
