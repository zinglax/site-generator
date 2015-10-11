#!/usr/bin/env bash

apt-get update
apt-get install -y apache2 git python2.7 python-pip python2.7-dev
# apt-get install -y nginx

pip install virtualenv
pip install virtualenvwrapper

cp /vagrant/vagrantbashrc /home/vagrant/.bashrc
source /home/vagrant/.bashrc
echo "Replaced .bashrc with vagrantbashrc"


echo "Installing Wing 5.1 32bit"
sudo dpkg -i /vagrant/wingide5_5.1.7-1_i386.deb
sudo apt-get -yf install



# Linking /vagrant to /var/www to be served
if ! [ -L /var/www ]; then
  rm -rf /var/www
  ln -fs /vagrant /var/www
fi
