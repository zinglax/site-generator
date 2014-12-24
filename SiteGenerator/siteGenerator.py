'''
SITE GENERATOR

PURPOSE: To automically generate a django site and configure it.
'''
import os
import fileinput
import sys
import subprocess

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
sitesFolder = dname + '/sites/'

touched_by_site_generator = "# THIS LINE WAS EDITED BY SITEGENERATOR"

theme_name = None

def ensure_dir(f):
    'makes sure directory or file exists'
    if not os.path.exists(f):
        return True
    return False


def start_django_project(name):
    # Changes directory to Sites
    os.chdir(sitesFolder)
    
    siteFolder = sitesFolder + name 
    
    if ensure_dir(siteFolder):
        # Runs Django Start Project command
        command = "django-admin.py startproject " + name
        os.system(command)
        print "## NEW SITE CREATED: " + name
    else:
        print "## SITE ALREADY EXISTS. NOTHING CREATED"

def start_django_app(site_name, app_name):
    '''Creates the django application for a specific site'''
    # Changes directory to new site   
    
    settingsPath = sitesFolder +"/" + site_name + "/" + site_name + "/settings.py"        
    
    siteFolder = sitesFolder + site_name
    appFolder = sitesFolder + site_name + "/" + app_name
    
    os.chdir(siteFolder)
    
    if  not ensure_dir(siteFolder):
        if ensure_dir(appFolder):
            # Site has already been created, create the App!
            command = "python manage.py startapp " + app_name
            os.system(command)   
            
            old_app_string = """    # 'django.contrib.admindocs',"""
            
            new_app_string = "    '" + app_name + "',"
            
            replaceAll(settingsPath, old_app_string, new_app_string)
            
        else:
            print "## App already exists in site"
    else:
        print "## SITE ALREADY EXISTS. NOTHING CREATED"
        

def setup_database(dbType, siteName):
    settingsPath = sitesFolder +"/" + siteName + "/" + siteName + "/settings.py"
    
    # Changes Type Of Database
    databaseString = """'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'."""
    newDatabaseString = """'ENGINE': 'django.db.backends.""" + dbType + """', """ + touched_by_site_generator
    replaceAll(settingsPath, databaseString, newDatabaseString)
    
    # Inserts Database Name
    databaseString = """'NAME': '',                      # Or path to database file if using sqlite3."""
    newDatabaseString = "'NAME': PATH_TO_FILE + '/" + siteName + ".db', " + touched_by_site_generator
    replaceAll(settingsPath, databaseString, newDatabaseString)


def setup_initial(siteName, app_name, timeZone):
    siteNameApp_folder = sitesFolder +"/" + siteName + "/" + siteName
    settingsPath = siteNameApp_folder + "/settings.py"
    appfolder = sitesFolder +"/" + siteName + "/" + app_name

    # Inserting Path Info to settings.py
    pathInfo =  '''import os

PATH_TO_FILE = os.path.abspath(os.path.dirname(__file__))
PATH_TO_APP = os.path.dirname(os.path.dirname(PATH_TO_FILE))
'''
    file_insert_beginning(settingsPath, pathInfo)
    
    # Changes TIME_ZONE
    time_zone = """TIME_ZONE = 'America/Chicago'"""
    newTime_zone = """TIME_ZONE = 'America/""" + timeZone + touched_by_site_generator
    replaceAll(settingsPath, time_zone, newTime_zone)
    
    # Create views.py for the site and adds some imports into it
    view_py_string = """from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
"""
    with open(appfolder + "/views.py", 'w+') as views_py:
        views_py.write(view_py_string)
    
    

def setup_media(siteName):
    siteFolder = sitesFolder +"/" + siteName + "/" + siteName
    settingsPath = siteFolder + "/settings.py"
    media_folder = siteFolder + "/media"
    
    # Changes Media Root
    old_media_root = """MEDIA_ROOT = ''"""
    new_media_root =  'MEDIA_ROOT = PATH_TO_FILE + "/media"  ' + touched_by_site_generator
    replaceAll(settingsPath, old_media_root, new_media_root)
    
    # Changes media url
    old_media = "MEDIA_URL = ''"
    new_media = "MEDIA_URL =  '/media/' " + touched_by_site_generator
    replaceAll(settingsPath, old_media, new_media)
    
    # Create Media Folder
    if ensure_dir(media_folder):
        os.makedirs(media_folder)

def setup_templates(siteName, app_name):
    siteFolder = sitesFolder +"/" + siteName + "/" + siteName
    settingsPath = siteFolder + "/settings.py"     
    template_folder = siteFolder + "/templates"
    site_app_template_folder = template_folder + "/" + siteName
    app_template_folder = template_folder + "/" + app_name
    
    old_templates = '# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".'
    new_templates = "os.path.join(PATH_TO_FILE, 'templates'), " + touched_by_site_generator
    
    replaceAll(settingsPath, old_templates, new_templates)
    
    # Create Templates Folder
    if ensure_dir(template_folder):
        os.makedirs(template_folder)
        
    # Creates the app template folder
    if ensure_dir(app_template_folder):
            os.makedirs(app_template_folder)    

def setup_static(sitename):
    siteFolder = sitesFolder +"/" + sitename + "/" + sitename
    settingsPath = siteFolder + "/settings.py"     
    static_folder = siteFolder + "/static"
    
    old_static = '    # Put strings here, like "/home/html/static" or "C:/www/django/static".'
    new_static = '    PATH_TO_FILE + "/static",' + touched_by_site_generator
    
    replaceAll(settingsPath, old_static, new_static)
    
    # Create Static Folder
    if ensure_dir(static_folder):
        os.makedirs(static_folder)    
    

def file_insert_beginning(file_name, insertString):
    ''' Inserts someting in the begining of the file'''
    for line in fileinput.input(file_name, inplace=1):
        if (fileinput.filelineno() == 1):
            sys.stdout.write(insertString)            
        sys.stdout.write(line)           

def file_insert_end(file_name, insert_string):
    data = None
    with open (file_name, "r+") as myfile:
        data=myfile.read()              
        data = data + insert_string         
        myfile.write(data)
            

def replaceAll(file_name,searchExp,replaceExp):
    for line in fileinput.input(file_name, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def file_insert_after(file_name, search_string, insert_string):
    ''' Inserts a string after position of search string in a given file'''
    data = None
    with open (file_name, "r+") as myfile:
        data=myfile.read()    
        insert_point = data.find(search_string) + len(search_string)    
        data = data[:insert_point] + insert_string + data[insert_point:]        
        myfile.write(data)

def generate_site():
    name = raw_input("Enter a Site Name: ")    
    app_name = raw_input("Enter an App Name: ")
    time_zone = raw_input("Enter a Time Zone, default is New_York (ex. New_York): ") or "New_York"
    database_type = raw_input("Enter a Database Type, defalut is sqlite3 (ex. sqlite3): ") or "sqlite3"
    
    # Initial project and app creation, settings.py configuration (static, media, templates)
    start_django_project(name)
    start_django_app(name, app_name)    
    setup_initial(name, app_name, time_zone)
    setup_database(database_type, name)    
    setup_media(name)
    setup_templates(name, app_name)
    setup_static(name)
    
    # Setting up Theme and new homepage
    decision = raw_input("Would you like to set up a them and homepage? [Y/n]") or "Y"
    if decision in {'Y','yes','Yes','YES',"ya","yeah",'y'}:
        print "You decided to setup a theme and homepage, sweet!"
        theme_path = raw_input("Enter the where your theme .zip file is (the one Downloaded from ThemeRoller): ")
        setup_theme_and_homepage(name, app_name, theme_path)

'''
name = "raw"
start_django_project(name)
setup_initial(name, 'New_York')
setup_database("sqlite3", name)
setup_media(name)
setup_templates(name)
'''

def setup_theme_and_homepage(sitename, app_name, path_to_theme_zip):
    siteFolder = sitesFolder +"/" + sitename + "/" + sitename
    static_folder = siteFolder + "/static"
    app_folder = sitesFolder +"/" + sitename + "/" + app_name
    
    # extract theme zip file in static folder
    command = "unzip " + path_to_theme_zip + " -d " + static_folder
    extract_cmd_return = subprocess.call(command, shell=True)
        
    # Set Theme Path (use with {% static theme_path %} )
    themes_folder = static_folder + "/themes"
    jquery_mobile_path = themes_folder + "/jquery.mobile.icons.min.css"
    
    # get name of theme
    files = os.walk(themes_folder).next()[2]
    for f in files:
        if not (f[-8:] == ".min.css") and (f[-4:] == ".css"):
            theme_name = f[0:-4]
    
    jquery_theme_path = themes_folder + "/" + theme_name + ".min.css"
    
    # Edit urls.py to add home url
    search = """from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',"""
    insert = """
    url(r'^$', '%s.views.home', name='home'),
    """ % app_name
    file_insert_after(siteFolder + "/urls.py", search, 
                     insert)

    # Edits views.py to add home page method 
    home_method = """\n\ndef home(request):
  return render_to_response("home/home.html", script_args)"""
    file_insert_end(app_folder + "/views.py", home_method)

    # Create Basic home.html page
    home_html_file = siteFolder + "/templates/" + app_name + "/home.html"
    with open(home_html_file, "w+") as homeHTML:
        homeCode = """<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>jQuery Mobile: Theme Download</title>
	<link rel="stylesheet" href="themes/%s.min.css" />
	<link rel="stylesheet" href="themes/jquery.mobile.icons.min.css" />
	<link rel="stylesheet" href="http://code.jquery.com/mobile/1.4.5/jquery.mobile.structure-1.4.5.min.css" />
	<script src="http://code.jquery.com/jquery-1.11.1.min.js"></script>
	<script src="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script>
</head>
<body>
	<div data-role="page" data-theme="a">
		<div data-role="header" data-position="inline">
			<h1>It Worked!</h1>
		</div>
		<div data-role="content" data-theme="a">
			<p>Your theme was successfully downloaded. You can use this page as a reference for how to link it up!</p>
			<pre>
<strong>&lt;link rel=&quot;stylesheet&quot; href=&quot;themes/%s.min.css&quot; /&gt;</strong>
<strong>&lt;link rel=&quot;stylesheet&quot; href=&quot;themes/jquery.mobile.icons.min.css&quot; /&gt;</strong>
&lt;link rel=&quot;stylesheet&quot; href=&quot;http://code.jquery.com/mobile/1.4.5/jquery.mobile.structure-1.4.5.min.css&quot; /&gt;
&lt;script src=&quot;http://code.jquery.com/jquery-1.11.1.min.js&quot;&gt;&lt;/script&gt;
&lt;script src=&quot;http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js&quot;&gt;&lt;/script&gt;
			</pre>
			<p>This is content color swatch "A" and a preview of a <a href="#" class="ui-link">link</a>.</p>
			<label for="slider1">Input slider:</label>
			<input type="range" name="slider1" id="slider1" value="50" min="0" max="100" data-theme="a" />
			<fieldset data-role="controlgroup"  data-type="horizontal" data-role="fieldcontain">
			<legend>Cache settings:</legend>
			<input type="radio" name="radio-choice-a1" id="radio-choice-a1" value="on" checked="checked" />
			<label for="radio-choice-a1">On</label>
			<input type="radio" name="radio-choice-a1" id="radio-choice-b1" value="off"  />
			<label for="radio-choice-b1">Off</label>
			</fieldset>
		</div>
	</div>
</body>
</html>""" % (theme_name, theme_name)
        homeHTML.write(homeCode)

if __name__ == '__main__':
        generate_site()