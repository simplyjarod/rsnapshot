# rsnapshot installation and configuration
_with interactive host adding/removing Python script_ ;)

Please, **download _all files_ before executing any script**. There are several dependencies between them. You can use:
```bash
wget https://github.com/simplyjarod/rsnapshot/archive/master.zip
unzip master.zip
cd rsnapshot-master
chmod u+x *.sh -R
chmod u+x *.py -R
```


## Pasos a seguir para configurar un nuevo host
1. Debemos crear/obtener las claves RSA en el servidor  
Necesitamos la clave pública del servidor donde se vayan a almacenar los backups.  
Para ello:  
```bash
ssh-keygen -t rsa
(el lugar donde se almacenen no importa, la opción por defecto es buen lugar)   
(si ya existiesen nos preguntará si queremos sobreescribirlas. Diremos que NO)
(NO escribiremos ninguna passphrase para crearlas)
```
