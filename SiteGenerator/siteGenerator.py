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

def startDjangoProject(name):
    # Changes directory to Sites
    os.chdir(dname + '/sites')
    
    siteFolder = dname + '/sites/' + name 
    
    if ensure_dir(siteFolder):
        # Runs Django Start Project command
        command = "django-admin.py startproject " + name
        os.system(command)
        print "## NEW SITE CREATED: " + name
    else:
        print "## SITE ALREADY EXISTS. NOTHING DONE"
    

def configureDatabase(dbType, siteName):
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



def initialSettingsSetup(siteName, timeZone):
    settingsPath = sitesFolder +"/" + siteName + "/" + siteName + "/settings.py"

    pathInfo =  '''import os

PATH_TO_FILE = os.path.abspath(os.path.dirname(__file__))
PATH_TO_APP = os.path.dirname(os.path.dirname(PATH_TO_FILE))
'''
    insertBeginning(settingsPath, pathInfo)
    
    # Changes TIME_ZONE
    time_zone = """TIME_ZONE = 'America/Chicago'"""
    newTime_zone = """TIME_ZONE = 'America/""" + timeZone + """' # THIS LINE WAS EDITED BY SITEGENERATOR"""
    replaceAll(settingsPath, time_zone, newTime_zone)
    

def insertBeginning(path, insertString):
    for line in fileinput.input(path, inplace=1):
        if (fileinput.filelineno() == 1):
            sys.stdout.write(insertString)
        sys.stdout.write(line)


def replaceAll(path,searchExp,replaceExp):
    for line in fileinput.input(path, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

name = "DylansFirst"
startDjangoProject(name)
initialSettingsSetup(name, 'New_York')
configureDatabase("sqlite3", name)