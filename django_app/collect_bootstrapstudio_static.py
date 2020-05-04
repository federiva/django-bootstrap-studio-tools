#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 12:36:35 2020

@author: federiva
"""
from django.conf import settings


settings.TEMPLATES[0]['DIRS'] += "os.path.join(BASE_DIR, 'templates'"
collect_bootstrapstudio_static

input_folder= '/home/trona/Documents/freelance/freelancer_git/contributions/django-bootstrap-studio-tools/django_app/1'
target_folder= '/home/trona/Documents/freelance/freelancer_git/contributions/django-bootstrap-studio-tools/django_app'
class staticLoader: 
    
    def __init__(self):
        pass
    



def copy_assets(input_folder, target_folder):
    folders= [x for x in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, x))]
    # look for assets folder
    asset_folder= [os.path.join(input_folder, x) for x in folders if x == 'assets']
    asset_folder= asset_folder[0] if len(asset_folder) == 1 else None
    if asset_folder is None: 
        raise Exception('There is more than one asset folder in: {}'.format(input_folder))
    else:
        shutil.copytree(src=asset_folder, dst='/home/Documents/lapala')






os.path.join(BASE_DIR, 'templates')