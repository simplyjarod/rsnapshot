#!/bin/bash

centos_version=$(rpm -qa \*-release | grep -Ei "oracle|redhat|centos" | cut -d"-" -f3)


if [ "$centos_version" -eq 6 ]; then

	yum install rsync -y  # Instalacion de rsync

	rpm -ivh rsnapshot-1.3.0-1.noarch.rpm  # Instalacion de rsnapshot

	\cp rsnapshot.conf /etc/rsnapshot.conf

	chmod 600 /etc/rsnapshot.conf

	# setup cron jobs
	echo "CRON JOBS SETUP REQUIRED"
	
	# run "crontab -e" and add these lines:
	# 0  */4  *  *  *  /usr/bin/rsnapshot hourly
	# 30  4   *  *  *  /usr/bin/rsnapshot daily
	# 0   5   *  *  7  /usr/bin/rsnapshot weekly
	# 30  5   1  *  *  /usr/bin/rsnapshot monthly

else

	yum install rsnapshot -y # Instalacion de rsnapshot
	sed -i "s|#cmd_cp		/usr/bin/cp|cmd_cp		/usr/bin/cp|g" /etc/rsnapshot.conf
	
	mkdir /.snapshots
	
	sed -i "s|alpha|hourly|g" /etc/rsnapshot.conf
	sed -i "s|beta|daily|g" /etc/rsnapshot.conf
	sed -i "s|gamma|weekly|g" /etc/rsnapshot.conf
	sed -i "s|#retain	delta|retain	monthly|g" /etc/rsnapshot.conf
	
	(crontab -l ; echo "09 */4  *  *  *  /usr/bin/rsnapshot hourly") | crontab -
	(crontab -l ; echo "39  4   *  *  *  /usr/bin/rsnapshot daily") | crontab -
	(crontab -l ; echo "09  5   *  *  7  /usr/bin/rsnapshot weekly") | crontab -
	(crontab -l ; echo "39  5   1  *  *  /usr/bin/rsnapshot monthly") | crontab -

fi
