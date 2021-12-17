Descripción del proyecto:
  Este proyecto refiere a la instalación de un servidor OpenLdap y un gestor web para que los usuarios 
  administren su cuenta de usuario.

Requisitos:
  Tener instalado docker y docker-compose

Notas importantes:
  1. La implementacion para OpenLdap, se realizó con base a lo planteado en la documentación del proyecto git: https://github.com/Ramhm/openldap
  2. antes de ejecutar el docker-compose, se debe ejecutar la implementación docker de opendldap, con la red especifica opendldap2_organization
  3. Para ejecutar los contenedores:
      3.1. En ambiente de desarrollo:
           /> docker-compose -f local.yml run account_manager django-admin startproject account_manager .
              Este comando solo se ejecuta cuando quieres crear por primera vez un proyecto de django, 
              pero al clonar el proyecto desde git, no se debe ejecutar este comando
           /> docker-compose -f local.yml up
              inicia los servicios establecidos en el archivo local.yml y levanta la instancio del servidor que expone django
      3.2. En ambiente de production or produccion:
           /> docker-compose -f production.yml up
              inicia los servicios establecidos en el archivo production.yml y levanta la instancio del servidor que expone django
  4. Para que no genere errores al momento de autenticar cuentas de usuario, se debe ingresar al contenedor que despliega este proyecto (docker exec -it nombrecontenedor bash) y ejecutar las migraciones de base de datos para el modelo de usuarios nativos, con el comando (python manage.py migrate)

  5. para que podamos conectar el aplicativo con openldap, debemos validar la dirección ip por donde podemos conetaarnos con el servicio de ldap con el siguiente comando:  docker network inspect openldap2_organization y validar en que ip esta expuesto el servico  "Name": "openldap".
  Despues se coloca esta Ip en le settien del proyecto en la variable: AUTH_LDAP_SERVER_URI = 'ldap://172.22.0.2'

  6. activar aplicaciones poco seguras para envío de correo electronico: https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4MoOfHPLpMtOesbO6FLeyoKEb-lXQHMzXCXnPocV-Pz6nkqhCvJx67P_qLZtG5ydWxdGN7dT7VpHjuZgFy9yIUi72onwQ

  7. ejemplo de una configuración LDAP: https://programmerclick.com/article/8701837035/
  
           