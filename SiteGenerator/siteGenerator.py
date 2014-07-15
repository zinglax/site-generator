'''
SITE GENERATOR

PURPOSE: To automically generate a django site and configure it.
'''
import os
import fileinput
import sys
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
sitesFolder = dname + '/sites'


def ensure_dir(f):
    if not os.path.exists(f):
        return True
    return False


def start_django_project(name):
    # Changes directory to Sites
    os.chdir(dname + '/sites')
    
    siteFolder = dname + '/sites/' + name 
    

    if ensure_dir(siteFolder):
        # Runs Django Start Project command
        command = "django-admin.py startproject " + name
        os.system(command)
        print "## NEW SITE CREATED: " + name
    else:
        print "## SITE ALREADY EXISTS. NOTHING CREATED"
    

def setup_database(dbType, siteName):
    settingsPath = sitesFolder +"/" + siteName + "/" + siteName + "/settings.py"
    
    # Changes Type Of Database
    databaseString = """'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'."""
    newDatabaseString = """'ENGINE': 'django.db.backends.""" + dbType + """', # THIS LINE WAS EDITED BY SITEGENERATOR
    """
    replaceAll(settingsPath, databaseString, newDatabaseString)
    
    # Inserts Database Name
    databaseString = """'NAME': '',                      # Or path to database file if using sqlite3."""
    newDatabaseString = "'NAME': PATH_TO_FILE + '/" + siteName + ".db', # THIS LINE WAS EDITED BY SITEGENERATOR"
    replaceAll(settingsPath, databaseString, newDatabaseString)


def setup_initial(siteName, timeZone):
    settingsPath = sitesFolder +"/" + siteName + "/" + siteName + "/settings.py"

    pathInfo =  '''import os

PATH_TO_FILE = os.path.abspath(os.path.dirname(__file__))
PATH_TO_APP = os.path.dirname(os.path.dirname(PATH_TO_FILE))
'''
    file_insert_beginning(settingsPath, pathInfo)
    
    # Changes TIME_ZONE
    time_zone = """TIME_ZONE = 'America/Chicago'"""
    newTime_zone = """TIME_ZONE = 'America/""" + timeZone + """' # THIS LINE WAS EDITED BY SITEGENERATOR"""
    replaceAll(settingsPath, time_zone, newTime_zone)
    

def setup_media(siteName):
    siteFolder = sitesFolder +"/" + siteName + "/" + siteName
    settingsPath = siteFolder + "/settings.py"
    media_folder = siteFolder + "/media"
    
    # Changes Media Root
    old_media_root = """MEDIA_ROOT = ''"""
    new_media_root =  'MEDIA_ROOT = PATH_TO_FILE + "/media"  # THIS LINE WAS EDITED BY SITEGENERATOR'
    replaceAll(settingsPath, old_media_root, new_media_root)
    
    # Changes media url
    old_media = "MEDIA_URL = ''"
    new_media = "MEDIA_URL =  '/media/'  # THIS LINE WAS EDITED BY SITEGENERATOR"
    replaceAll(settingsPath, old_media, new_media)
    
    # Create Media Folder
    if ensure_dir(media_folder):
        os.makedirs(media_folder)

def setup_templates(siteName):
    siteFolder = sitesFolder +"/" + siteName + "/" + siteName
    settingsPath = siteFolder + "/settings.py"     
    template_folder = siteFolder + "/templates"
    
    
    old_templates = '# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".'
    new_templates = "os.path.join(PATH_TO_FILE, 'templates'),  # THIS LINE WAS EDITED BY SITEGENERATOR"
    
    replaceAll(settingsPath, old_templates, new_templates)
    
    # Create Templates Folder
    if ensure_dir(template_folder):
        os.makedirs(template_folder)    
    

def file_insert_beginning(file_name, insertString):
    ''' Inserts someting in the begining of the file'''
    for line in fileinput.input(file_name, inplace=1):
        if (fileinput.filelineno() == 1):
            sys.stdout.write(insertString)            
        sys.stdout.write(line)           

def file_insert_end(file_name, insert_string):
    for line in fileinput.input(file_name, inplace=1):
        sys.stdout.write(line)
    sys.stdout.write(insertString)
            

def replaceAll(file_name,searchExp,replaceExp):
    for line in fileinput.input(file_name, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


def generate_site(name, time_zone, database_type):
    start_django_project(name)
    setup_initial(name, time_zone)
    setup_database(database_type, name)
    setup_media(name)
    setup_templates(name)    

'''
name = "raw"
start_django_project(name)
setup_initial(name, 'New_York')
setup_database("sqlite3", name)
setup_media(name)
setup_templates(name)
'''