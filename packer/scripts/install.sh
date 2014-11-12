#!/bin/sh

echo "updating"
sudo apt-get update

echo "getting git"
sudo apt-get install -y git

echo "installing python dev libraries"
sudo apt-get install -y libpq-dev
sudo apt-get install -y python-dev

echo "setting up virtualenv"
sudo apt-get install python-pip -y
sudo pip install virtualenvwrapper
echo "export WORKON_HOME=~/Envs" >> ~/.profile
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
source ~/.profile
mkdir -p $WORKON_HOME
mkvirtualenv 10watchers
add2virtualenv /home/ubuntu


echo "setting up nginx"
sudo apt-get install nginx -y
sudo mv /home/ubuntu/packer/nginx/tenwatchers.conf /etc/nginx/conf.d/
sudo sed -i.bak '/include \/etc\/nginx\/sites.*/d' /etc/nginx/nginx.conf
sudo service nginx restart
nginx -s reload


echo "installing"
/home/ubuntu/Envs/10watchers/bin/pip install -r /home/ubuntu/requirements.txt
cat /home/ubuntu/packer/scripts/startup.sh | sudo tee /etc/rc.local