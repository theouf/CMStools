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
    # Questionnaire pour récupérer le nom du fichier à ouvrir 
               form=FORM('Your file:', INPUT(_name='fichier_name', _type='file'), INPUT(_type='submit'))
        
    # Si on récupère l'information alors :    
               if form.accepts(request.vars.fichier_name):
                    response.flash = T('Thanks! The form has been submitted.')
                #Appel de la fonction pour rechercher les composants
                    composant_recherche(request.vars.fichier_name)  
    # Si on récupère pas alors Erreur :
               elif form.errors:
                       response.flash = T('Please correct the error(s).')
               else:
                       response.flash = T( 'Try again - no fields can be empty.')
return dict(form=form)

def composant_recherche(fichier_name):

    # Onverture du fichier 
    # compiler d'un façon :-composant-(.+)-package-(.+)-X-(.+)-Y-(.*)-rot-(.*)$
    # parcourir tout les lignes
    # Si composant alors on récupère la valeur comp
    
    lines = [line.strip() for line in open(request.vars.fichier_name.value)]
    p = re.compile('^-composant-(.+)-package-(.+)-X-(.+)-Y-(.*)-rot-(.*)$')
    for line in lines:
                          line = line.rstrip()
                          if "-composant-" in line:
                                m = p.match(line)
                                if m:
                                    comp = m.group(1)


    return dict(comp=session.composant)



def second():
    
    return dict()
