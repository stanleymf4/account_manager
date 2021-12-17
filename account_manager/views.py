""" vista de account_manager """

# django
from django.contrib.auth import authenticate, login
from django.shortcuts import render
# from django_auth_ldap.backend import LDAPBackend
from django.contrib.auth.models import User
import ldap.modlist as modlist
import hashlib
from .passwd import PasswordUtils
from django_auth_ldap.backend import LDAPBackend, LDAPSearch
from .utils import send_reset_password_email, send_activate_account_email, send_remember_email_inst
from django.conf import settings
import ldap


# utilities
from datetime import datetime


def list_options(request):
  """ Opciones existente en el admisnitrador de cuenta de usuario """
  return render(request, 'feed.html', {'name': 'Stanley'})

def change_pass(request):
  """ Cambio de contraseña """

  passwd_util = PasswordUtils()

  if request.method == 'POST':
    username = request.POST['email']
    password = request.POST['password']
    new_password = request.POST['new_password']
    conf_password = request.POST['conf_password']

    if (new_password != conf_password):

      return render(request, 'account_manager/change_pass.html', {'error': 'Nueva contraseña invalida'})

    new_password = passwd_util.mkpasswd(new_password, hash='crypt')
    print(f'{username} {password}')
    user = authenticate(username=username, password=password)
    employeeType = 'A'
    
    if user is not None:
      
      ldif = modlist.modifyModlist(
        {'userpassword': user.ldap_user.attrs['userpassword']},
        {'userpassword':[new_password.encode()]}
      )
      user.ldap_user.connection.modify_s(user.ldap_user.dn, ldif)

      print(user.ldap_user.attrs['employeeType'])

      if user.ldap_user.attrs['employeeType'] == ['C']:
        ldif = modlist.modifyModlist(
          {'employeeType': user.ldap_user.attrs['employeeType']},
          {'employeeType':[employeeType.encode()]}
        )
        user.ldap_user.connection.modify_s(user.ldap_user.dn, ldif)

      return render(request, 'account_manager/change_pass.html', {'success': 'Su contraseña fue actualizada'})
    else:
      return render(request, 'account_manager/change_pass.html', {'error': 'usuario y contraseña invalida'})

  return render(request, 'account_manager/change_pass.html')

def activate_account(request):
  """ activacion de cuenta de usuario en openldap 
      Para activar la cuenta de un usuario en ldap. 
      Este debe estar categorizado como nuevo, por lo que en el atributo 
      employeeType debe tener el valor N.

      Esta funcionalidad le asigna una clave temporal al usuario y 
      le cambia el contenido del atributo employeeType a C. Adicionalmente,
      en el atributo initials de ldap, le carga el contenido A, 
      el cual indica que aceptó los terminos y condiciones.

      Por ultimo, para que el usuario pueda darse de alta completamente,
      debe realizar el cambio de contraseña. De está forma queda como usuario activo.
      employeeType quedará con el valor A, siemnpre que la contraseña sea 
      cambiada en la opción "cambio de contraseña"
  """
  if request.method == 'POST':
    email_inst = request.POST['email_inst']
    email_alterno = request.POST['emailAlterno']
    user = LDAPBackend().populate_user(email_inst)
    token = PasswordUtils().getsalt(length=10)
    employeeType = 'C'
    initials = 'Acepto terminos'

    print (user.ldap_user.attrs['employeeType'])

    if user.ldap_user.attrs['employeeType'] == ['N']:
      if user is not None:
        if (email_alterno == user.email):
          ldif = modlist.modifyModlist(
            {'userpassword': user.ldap_user.attrs['userpassword']},
            {'userpassword':[token.encode()]}
          )
          user.ldap_user.connection.modify_s(user.ldap_user.dn, ldif)

          ldif = modlist.modifyModlist(
            {'employeeType': user.ldap_user.attrs['employeeType']},
            {'employeeType':[employeeType.encode()]}
          )
          user.ldap_user.connection.modify_s(user.ldap_user.dn, ldif)

          ldif = modlist.modifyModlist(
            {'initials': user.ldap_user.attrs['initials']},
            {'initials':[initials.encode()]}
          )
          user.ldap_user.connection.modify_s(user.ldap_user.dn, ldif)

          send_activate_account_email(user.email, 'stanley.mf4@gmail.com',
                                    user.get_full_name(), 'https://localhost:8000', token)

          return render(
            request, 'account_manager/activate_account.html', {
              'success': 'Fue enviado un correo de activación de cuenta a su email alterno'
            }
          )
        else:
            return render(
              request, 'account_manager/activate_account.html', {
                'error': 'Email alterno no esá registrado'
              }
            )
      else:
        return render(
          request, 'account_manager/activate_account.html', {
            'error': 'Usuario no registrado'
          }
        )
    else:
      return render(request, 'account_manager/activate_account.html', {'error': 'Su cuenta ya está activa'})


  return render(request, 'account_manager/activate_account.html')

def recover_password(request):

  if request.method == 'POST':
    email_inst = request.POST['email_inst']
    email_alterno = request.POST['emailAlterno']
    user = LDAPBackend().populate_user(email_inst)
    token = PasswordUtils().getsalt(length=10)
    employeeType = 'C'

    # print (user.ldap_user.attrs['employeeType'])

    if (user.ldap_user.attrs['employeeType'] == ['A']) or (user.ldap_user.attrs['employeeType'] == ['C']):
      if user is not None:
        if (email_alterno == user.email):
          print(token)

          ldif = modlist.modifyModlist(
            {'userpassword': user.ldap_user.attrs['userpassword']},
            {'userpassword':[token.encode()]}
          )
          user.ldap_user.connection.modify_s(user.ldap_user.dn, ldif)

          
          ldif = modlist.modifyModlist(
            {'employeeType': user.ldap_user.attrs['employeeType']},
            {'employeeType':[employeeType.encode()]}
          )
          user.ldap_user.connection.modify_s(user.ldap_user.dn, ldif)

          send_reset_password_email(user.email, 'stanley.mf4@gmail.com',
                                    user.get_full_name(), 'https://localhost:8000', token)

          return render(request, 'account_manager/recover_password.html', {'success': 'Fue enviado un correo de recuperación de contraseña a su email alterno'})

        else:
          return render(request, 'account_manager/recover_password.html', {'error': 'Email alterno no esá registrado'})
      else:
        return render(request, 'account_manager/recover_password.html', {'error': 'Usuario no registrado'})
    else:
      return render(request, 'account_manager/recover_password.html', {'error': 'Usuario inactivo'})

  return render(request, 'account_manager/recover_password.html')

def remember_email_inst (request):
  """ Esta vista envia un correo electronico a la cuenta de correo alterno registrada por el estudiante,
      El contenido del correo informa el sobre la cuenta de correo institucional """

  if request.method == 'POST':
    employeeNumber = request.POST['employeeNumber']
    settings.AUTH_LDAP_USER_SEARCH = LDAPSearch(
          'ou=usuarios,dc=marvajulocal,dc=com' , 
          ldap.SCOPE_SUBTREE,
          '(employeeNumber=%(user)s)',
      ) 
    user = LDAPBackend().populate_user(employeeNumber)

    if user is not None:

      

      # settings.AUTH_LDAP_SEARCH_OU
      # settings.AUTH_LDAP_SEARCH_FILTER

      send_remember_email_inst(
        user.email, 
        'stanley.mf4@gmail.com',
        user.get_full_name(), 
        user.email_inst
      )

      return render(request, 'account_manager/remember_email_inst.html', {'success': 'Fue enviado un correo de recordatorio de correo institucional a su correo alterno'})
    else:
      return render(request, 'account_manager/remember_email_inst.html', {'error': 'Número de documento no existe'})
      
  return render(request, 'account_manager/remember_email_inst.html')


def alternate_email_change (request):
  """ Esta vista realiza el cambio de correo alterno en AD, validando correo institucional y contraseña """

  if request.method == 'POST':
    username = request.POST['email']
    password = request.POST['password']
    alternate_email = request.POST['new_email']
    alternate_email_conf = request.POST['conf_new_email']

    if (alternate_email != alternate_email_conf):
      return render(request, 'account_manager/alternate_email_change.html', {'error': 'Confirmación de correo alterno no es equivalente al correo alterno'})

    user = authenticate(username=username, password=password)  

    if user is not None:
      
      ldif = modlist.modifyModlist(
        {'displayName': user.ldap_user.attrs['displayName']},
        {'displayName':[alternate_email.encode()]}
      )
      user.ldap_user.connection.modify_s(user.ldap_user.dn, ldif)

      return render(request, 'account_manager/alternate_email_change.html', {'success': 'Su correo alterno fue actualizado'})
    else:
      return render(request, 'account_manager/alternate_email_change.html', {'error': 'usuario o contraseña invalida'})    

  return render(request, 'account_manager/alternate_email_change.html')    

