site-generator
==============

site-generator generates sites in Django for Quick Mobile web jquery sites. 

TODO:

~~Create Django Project~~

~~settings.py: Configure Database~~

~~settings.py: Configure Templates~~

~~settings.py: Configure Media~~

~~settings.py: Configure Time Zone~~

~~settings.py: Configure static files~~

~~Test for matching settings.py file~~

Test for matching directory structure

Sync Database 

~~Create Application~~

Adding a Page

Themes

Base.py	



-------------------------------------------------------------------------------
SITE-GENERATOR SETUP
=============================

## Linux Packages
[Vagrant](https://www.vagrantup.com/)
[Virtualbox](https://www.virtualbox.org/wiki/Linux_Downloads)

## Vagrantfile
- On startup will run vagrantsetup.sh
- Network connection is bridged ('public_network')
 - Must be able to obatin an IP address for the Vagrant Box (DHCP)
- Hostname = sitegenerator
- x11 forwarding for GUI is turned on

## vagrantsetup.sh
- Installs a few packages
 - apt-get install -y apache2 git python2.7 python-pip python2.7-dev
 - pip install virtualenv
 - pip install virtualenvwrapper
- Installs Wing IDE 5.1
- Simlinks /var/www to /vagrant
