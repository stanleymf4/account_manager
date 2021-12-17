# Utility functions

from django.core.mail import send_mail


def send_reset_password_email(email, from_email, full_name, reset_link, pwd_temp):
    """
    Send password reset email
    :param email:
    :param from_email:
    :param full_name: 
    :param reset_link: 
    :param app_name: 
    :return: 
    """
    tpl = """
        Hola {full_name},
        ¡Hemos desbloqueado tu cuenta institucional!

        Tu contraseña de recuperación es: {pwd_temp}

        Esta contraseña debes modificarla ingresando a {reset_link} y seleccionar la opción 'cambio de contraseña'.
        
        Este mensaje es informativo.

        ¿Algun inconveniente con tu cuenta?

        Contáctanos a través del portal: htts://ejemplo.edu.co

        """
    subject = 'Instrucciones de Recuperación de Contraseña'
    msg_map = { 'full_name': full_name, 'reset_link': reset_link, 'pwd_temp': pwd_temp }
    message = tpl.format_map(msg_map)

    send_mail(subject, message, from_email, [email])

def send_activate_account_email(email, from_email, full_name, reset_link, pwd_temp):
    """
    Activacion de cuenta
    :param email:
    :param from_email:
    :param full_name: 
    :param reset_link: 
    :param app_name: 
    :return: 
    """
    tpl = """
        Hola {full_name},

        ¡Hemos activado tu cuenta institucional!

        Tu contraseña de temporal es: {pwd_temp}

        Esta contraseña debes modificarla ingresando a {reset_link} y seleccionar la opción 'cambio de contraseña'.
        
        Este mensaje es informativo.

        ¿Algun inconveniente con tu cuenta?

        Contáctanos a través del portal: htts://ejemplo.edu.co

        """
    subject = 'Activación de cuenta'
    msg_map = { 'full_name': full_name, 'reset_link': reset_link, 'pwd_temp': pwd_temp }
    message = tpl.format_map(msg_map)

    send_mail(subject, message, from_email, [email])


def send_newly_registered_email(email, from_email, full_name, activate_link, app_name):
    """
    Send notification for new registrations with activation link
    :param email: 
    :param from_email: 
    :param full_name: 
    :param activate_link: 
    :param app_name: 
    :return: 
    """
    tpl = """
    Welcome {full_name}!
    The first step is to verify your email address. Please click the link or paste the URL into your web browser:
    {activate_link}
    -- {app_name}
    """
    subject = 'Welcome to ' + app_name + '!'
    msg_map = { 'full_name': full_name, 'activate_link': activate_link, 'app_name': app_name }
    message = tpl.format_map(msg_map)

    send_mail(subject, message, from_email, [email])

def send_remember_email_inst(email, from_email, full_name, email_inst):
    """
    Send password reset email
    :param email:
    :param from_email:
    :param full_name: 
    :param reset_link: 
    :param app_name: 
    :return: 
    """
    tpl = """
        Hola {full_name},

        Te recordamos que tu cuenta de correo institucional es:

        {email_inst}
        
        Este mensaje es informativo.

        ¿Algun inconveniente con tu cuenta?

        Contáctanos a través del portal: https://ejemplo.edu.co

        """
    subject = 'Recodatorio correo institucional'
    msg_map = { 'full_name': full_name, 'email_inst': email_inst }
    message = tpl.format_map(msg_map)

    send_mail(subject, message, from_email, [email])


