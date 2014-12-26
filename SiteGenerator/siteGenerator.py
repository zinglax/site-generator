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

def setup_django_site(site_name, app_name, time_zone, db_type, media_root= 'PATH_TO_FILE + "/media"', media_url="'/media/'", template_dir="os.path.join(PATH_TO_FILE, 'templates'),", static_dir='PATH_TO_FILE + "/static",'):
    
    # Paths
    siteFolder = sitesFolder + site_name
    settingsPath = sitesFolder +"/" + site_name + "/" + site_name + "/settings.py"
    appFolder = sitesFolder + site_name + "/" + app_name
    static_folder = siteFolder + "/" + site_name + "/static"
    media_folder = siteFolder + "/" + site_name + "/media"
    template_folder = siteFolder + "/" + site_name + "/templates"
    app_template_folder = template_folder + "/" + app_name
        
    # Creating Django Project
    os.chdir(sitesFolder)
    if ensure_dir(siteFolder):
        command = "django-admin.py startproject " + site_name
        os.system(command)
        print "## NEW SITE CREATED: " + site_name
    else:
        print "## SITE ALREADY EXISTS. NOTHING CREATED"    

    # Creating Django Application   
    os.chdir(siteFolder)
    if  not ensure_dir(siteFolder):
        if ensure_dir(appFolder):
            # Site has already been created, create the App!
            command = "python manage.py startapp " + app_name
            os.system(command)   

            # Can Be done with file_replace_with_list at the end
            #old_app_string = """    # 'django.contrib.admindocs',"""
            #new_app_string = "    '" + app_name + "',"            
            #replaceAll(settingsPath, old_app_string, new_app_string)
        else:
            print "## App already exists in site"
    else:
        print "## SITE ALREADY EXISTS. NOTHING CREATED"
        
    # Database setup here
    
    # Setup Initial here
    view_py_string = """from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, QueryDict

# Dictionary to add objects passed to the through to the HTML
script_args = {}
script_args['theme'] = "a"
    """    
    with open(appFolder + "/views.py", 'r+') as views_py:
        views_py.write(view_py_string)
        views_py.close()
        
    # Setup Media Here
    if ensure_dir(media_folder):
        os.makedirs(media_folder)
        
    # Setup Templates here
    if ensure_dir(template_folder):
        os.makedirs(template_folder)    
    if ensure_dir(app_template_folder):
        os.makedirs(app_template_folder)    
        
    # Setup Static here
    if ensure_dir(static_folder):
        os.makedirs(static_folder)   

    # Copy Defalut settings.py to new sites settings.py
    command = "cp " + dname + "/defaultFiles/settings.py " + settingsPath
    subprocess.call(command, shell=True)
    
    # Replace values in new settings.py
    replace_list = [site_name, 
                    db_type, 
                    site_name, 
                    time_zone,
                    media_root,
                    media_url,
                    static_dir,
                    site_name,
                    site_name,
                    template_dir,
                    app_name
                    ]
    file_replace_with_list(settingsPath, replace_list)

def setup_theme_and_homepage(sitename, app_name, path_to_theme_zip):
    siteFolder = sitesFolder + sitename + "/" + sitename
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
    \n    url(r'^$', '%s.views.home', name='home'), \n""" % app_name
    file_insert_after(siteFolder + "/urls.py", search, 
                     insert)

    # Edits views.py to add home page method 
    home_method = """\n\ndef home(request):
  return render_to_response("%s/home.html", script_args)""" % app_name
    file_insert_end(app_folder + "/views.py", home_method)

    # Create default base.html and home.html pages
    templates_folder = siteFolder + "/templates/" + app_name + "/"
    command = "cp " + dname + "/defaultFiles/home.html " + templates_folder
    command2 = "cp " + dname + "/defaultFiles/base.html " + templates_folder
    subprocess.call(command, shell=True)
    subprocess.call(command2, shell=True)
    
    # Edits data to reflect site name, app name, and theme name where appropriate
    replace_list = [sitename, theme_name]
    file_replace_with_list(templates_folder + "base.html", replace_list)
    
    replace_list = [app_name]
    file_replace_with_list(templates_folder + "home.html", replace_list)


def file_insert_beginning(file_name, insertString):
    ''' Inserts someting in the begining of the file'''
    for line in fileinput.input(file_name, inplace=1):
        if (fileinput.filelineno() == 1):
            sys.stdout.write(insertString)            
        sys.stdout.write(line)           

def file_insert_end(file_name, insert_string):
    data = None
    with open (file_name, "a+") as myfile:
        #data=myfile.read()              
        #data = data + insert_string         
        myfile.write(insert_string)
        myfile.close()
            

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
        #insert_point = data.find(search_string) + len(search_string)   
        #print data
        #data = data[:insert_point] + insert_string + data[insert_point:]  
        insert_point = data.find(search_string) + len(search_string)
        myfile.seek(data.find(search_string) + len(search_string))   
        end_data = myfile.read()
        myfile.seek(insert_point)
        myfile.write(insert_string + end_data)
        #myfile.write(data)


def file_replace_with_list(file_name, replace_list):
    ''' Searchs for @@0@@, @@1@@, @@#@@, ... in file and replaces it with string at given index'''
    
    for i,j in enumerate(replace_list):
        data = None
        myfile = open(file_name, "r+")
        myfile.seek(0)
        data=myfile.read()
        replace_point = data.find('@@' + str(i) + '@@')
        end_replace_point = replace_point + len('@@' + str(i) + '@@')
        beginning_data = data[:replace_point]
        ending_data = data[end_replace_point:]
        myfile.close()
        
        myfile = open(file_name, "w+")        
        myfile.write(beginning_data + j + ending_data)
        myfile.close()
        

def generate_site():
    name = raw_input("Enter a Site Name: ")    
    app_name = raw_input("Enter an App Name: ")
    time_zone = raw_input("Enter a Time Zone, default is New_York (ex. New_York): ") or "New_York"
    database_type = raw_input("Enter a Database Type, defalut is sqlite3 (ex. sqlite3): ") or "sqlite3"
    
    setup_django_site(name, app_name, time_zone, 
                     database_type)
    
    # Setting up Theme and new homepage
    decision = raw_input("Would you like to set up a them and homepage? [Y/n]") or "Y"
    if decision in {'Y','yes','Yes','YES',"ya","yeah",'y'}:
        print "You decided to setup a theme and homepage, sweet!"
        theme_path = raw_input("Enter the where your theme .zip file is (the one Downloaded from ThemeRoller): ")
        setup_theme_and_homepage(name, app_name, theme_path)


    
    
    
    
if __name__ == '__main__':
        generate_site()