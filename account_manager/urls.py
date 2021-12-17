"""account_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from account_manager import views

urlpatterns = [
    path('',views.list_options, name='index'),

    path(
        'account_manager/change_pass/',
        views.change_pass, 
        name='change_pass'
    ),
    path(
        'account_manager/recover_password/',
        views.recover_password, 
        name='recover_pass'
    ),
    path(
        'account_manager/activate_account/',
        views.activate_account, 
        name='activate_account'
    ),
    path(
        'account_manager/remember_email_inst/',
        views.remember_email_inst, 
        name='remember_email_inst'
    ),
    path(
        'account_manager/alternate_email_change/',
        views.alternate_email_change, 
        name='alternate_email_change'
    ),

    # path(
    #     'account_manager/activate_account/',
    #     views.activate_account, 
    #     name='activate_account'
    # ),
]
