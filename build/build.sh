#!/bin/bash


install_rec(){
	yum  install gcc python27-devel postgresql-devel -y
}

install_redis () {
sudo rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm 
sudo rpm -Uvh http://rpms.remirepo.net/enterprise/remi-release-6.rpm 
sudo yum --enablerepo=epel install jemalloc -y
sudo yum --enablerepo=remi install redis -y
sudo service redis start
sudo chkconfig redis on
echo "Redis OK"
}

install_rec
install_redis

