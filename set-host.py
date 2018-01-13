#!/usr/bin/python
# version 2018-01-13
import fileinput, os, re, subprocess, sys, uuid

configFile = '/etc/rsnapshot.conf'


# WHAT TO DO: ===================================================
action = "unknown"

while action != "ADD" and action != "REMOVE":
	action = raw_input("Do you want to ADD or REMOVE elements to rsnapshot? ").upper()
	if (action != "ADD" and action != "REMOVE"):
		print "Please, type ADD or REMOVE to add or remove elements: "

print "OK, let's " + action + " some elements"



# ADDING CONFIG: ===================================================
if action == "ADD":

	print "Please, specify the following data:"
	host = raw_input("- domain or ip of the remote host: ")
	user = raw_input("- ssh username in the remote host: ")
	local_folder = raw_input("- local folder to store the backup (e.g. myweb.com): ")
	local_folder = os.path.join(local_folder, '') # adds the trailing slash if missing

	# Ask to backup an entire folder or just a single file
	backup_type = 'none'
	while backup_type != "FILE" and backup_type != "FOLDER" and backup_type != "SQL":
		backup_type = raw_input("- Do you want to backup a complete FOLDER or an SQL database? ").upper() # TODO: tambien permitir a single FILE
		if (backup_type != "FILE" and backup_type != "FOLDER" and backup_type != "SQL"):
			print "Please, type FILE, FOLDER or SQL: (file does not work currently) "
	
	# FOLDER BACKUP: -------------------------------------------------
	if backup_type == 'FOLDER':
		remote_path = raw_input("- absolute path (e.g. /home/user/www) of the remote folder to backup: ")
		remote_path = os.path.join(remote_path, "") # adds the trailing slash if it's not already there

		# TODO: if exists local_folder: ask wether reuse it or not!

		# SSH connection to add backup.pub to ~/.ssh/authorized_keys in the remote host
		# TODO: only necessary whether this is the first time for this user AND host (ssh with public key previously installed?)
		print "ssh password could be asked. It won't be stored. You can change it afterwards"
		# read the backup.pub key content:
		with open("backup.pub", "r") as keyFile:
			key=keyFile.read()
		# the commands to execute on the remote host via ssh:
		# permissions 700 for .ssh and 600 for .ssh/authorized_keys are needed in order to work
		ssh_cmd = "grep ' root@backup' .ssh/authorized_keys || (mkdir -p .ssh && echo '"+key+"' >> .ssh/authorized_keys && chmod 700 .ssh && chmod 600 .ssh/authorized_keys)"
		# the connection and commands execution:
		ssh = subprocess.Popen("ssh -t -o ConnectTimeout=5 "+user+"@"+host+" \""+ssh_cmd+"\"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout,stderr = ssh.communicate()

		if (len(stderr) == 0 or ("Connection to " in stderr and " closed." in stderr)): # connection OK
			with open(configFile, 'a') as file:
				file.write('backup	'+user+'@'+host+':'+remote_path + '	' + local_folder+'\n') # 3 blocks separated by a TAB
				print "FOLDER BACKUP CONFIGURATION SAVED"

		else: # error
			print "ERROR: "+stderr
			print "FOLDER BACKUP CONFIGURATION COULD NOT BE SAVED, please, try again"


	# MYSQL BACKUP: -------------------------------------------------
	elif backup_type == 'SQL':

		# TODO: check ssh connection and key

		db_name = raw_input("- database name: ")
		db_user = raw_input("- database user: ")
		db_pass = raw_input("- database password: ")

		unusedA = "unused_" + str(uuid.uuid4().get_hex().upper()[0:6])
		unusedB = "unused_" + str(uuid.uuid4().get_hex().upper()[0:6])

		with open(configFile, 'a') as file:
			# 3 lines. Each one with 3 blocks separated by a TAB
			file.write('backup_script	/usr/bin/ssh '+user+'@'+host+' \"mysqldump -u'+db_user+' -p'+db_pass+' '+db_name+' | gzip > /tmp/'+db_name+'.sql.gz\"	'+unusedA+'\n')
			file.write('backup	'+user+'@'+host+':/tmp/'+db_name+'.sql.gz	'+local_folder+'\n')
			file.write('backup_script	/usr/bin/ssh '+user+'@'+host+' \"\\rm /tmp/'+db_name+'.sql.gz\"	'+unusedB+'\n')
			print "SQL BACKUP CONFIGURATION SAVED"



# REMOVING CONFIG: ===================================================
if action == "REMOVE":
	matches = []

	# Regex para mostrar los backups ya configurados:
	for line in fileinput.input(configFile):
		match = re.search(r'^backup	(.*@.*:.*)	.*', line) # mind the tabs!
		if match:
			lineno = fileinput.lineno()
			matches.append([lineno, match.group(1)])

	print "This is what I found available to remove:"
	for i, match in enumerate(matches):
		print str(i) + ': ' + match[1]

	# Si no existen backups configurados se acaba el programa:
	if not matches:
		print "Sorry, there is nothing available to remove"
		sys.exit()

	# Pedimos cuales de los mostrados se quieren eliminar:
	strIndexesToRemove = raw_input('Please, choose the number/s to remove (e.g. "1,3,5"): ')
	indexesToRemove = str.split(strIndexesToRemove, ',')

	# Cuando se trate de ficheros .sql.gz tendremos que borrar tambien los scripts:
	linesToRemove = []
	for i in indexesToRemove:
		i = int(i)
		linesToRemove.append(matches[i][0]) # la linea en cuestion
		# si la linea en cuestion es un .sql.gz borraremos los backup_script
		sql_match = re.search(r'.*@.*:.*\.sql\.gz$', matches[i][1])
		if sql_match:
			linesToRemove.append(matches[i][0]-1) # script previo
			linesToRemove.append(matches[i][0]+1) # script posterior

	for line in fileinput.input(configFile, inplace=True):
		if fileinput.lineno() not in linesToRemove:
			sys.stdout.write(line)

	print "Element/s removed from rsnapshot config file"



subprocess.call(['rsnapshot', 'configtest']) 
