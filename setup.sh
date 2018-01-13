#!/bin/bash

# Instalacion de rsync:
yum install rsync -y


# Instalacion de rsnapshot:
rpm -ivh rsnapshot-1.3.0-1.noarch.rpm

\cp rsnapshot.conf /etc/rsnapshot.conf

chmod 600 /etc/rsnapshot.conf


# setup cron jobs
echo "CRON JOBS SETUP REQUIRED"

# run "crontab -e" and add these lines:
# 0  */4  *  *  *  /usr/bin/rsnapshot hourly
# 30  4   *  *  *  /usr/bin/rsnapshot daily
# 0   5   *  *  7  /usr/bin/rsnapshot weekly
# 30  5   1  *  *  /usr/bin/rsnapshot monthly
