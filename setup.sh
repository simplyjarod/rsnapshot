#!/bin/bash

# Instalacion de rsync:
yum install rsync -y


# Instalacion de rsnapshot:
rpm -ivh rsnapshot-1.3.0-1.noarch.rpm

\cp rsnapshot.conf /etc/rsnapshot.conf

chmod 600 /etc/rsnapshot.conf


# setup cron jobs
echo "CRON JOBS SETUP REQUIRED"
