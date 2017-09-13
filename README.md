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


## Configuración incial (una sola vez)
*1. Debemos crear/obtener las claves RSA en el servidor*  
Necesitamos la clave pública del servidor donde se vayan a almacenar los backups.  
Para ello:  
```bash
ssh-keygen -t rsa
#(dejaremos el lugar donde se almacenen con la opción por defecto)   
#(si ya existiesen nos preguntará si queremos sobreescribirlas. Diremos que NO)
#(NO escribiremos ninguna passphrase para crearlas)
```
*2. Instalación de rsnapshot*  

*3. Configurar rsnapshot*
Editaremos el fichero /etc/rsnapshot.conf  
Atención a los requisitos del fichero: Finalizar directorios con '/' y usar tabuladores en vez de espacios.


## Configurar (añadir o eliminar) una copia de seguridad remota
