#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 13:16:15 2020

@author: federiva
"""

import sys
import os

def list_html_files(path_html):
    abs_path= os.path.abspath(path_html)
    html_files= os.listdir(path_html)
    html_files= [os.path.join(abs_path, x) for x in html_files if x.endswith('.html')]
    return html_files

def generate_views(html_files):
    with open('views.py', 'w+') as viewfile:
        viewfile.write('from django.shortcuts import render\n')
        for html in html_files:
            viewfile.write(write_view(html))
        
def write_view(html_file): 
    name_view= get_name(html_file)
    view= '''\ndef render_{0}(request):\n    return render(request, '{0}.html', {{}})\n'''.format(name_view)
    return view

def write_path(html_file):
    name_view= get_name(html_file)
    url_path= '''    re_path(r'^{0}$', views.render_{0}, name='{0}'),\n'''.format(name_view)
    return url_path

def get_name(html_file):
    name_view= html_file.split('.')[0]
    name_view= os.path.split(name_view)[1]
    name_view= name_view.replace(' ', '_').lower()
    return name_view


def genereate_urls(html_files, app_name):
    with open('urls.py', 'w+') as urlfile:
        urlfile.write('from . import views\n')
        urlfile.write('from django.urls import path, re_path\n')
        urlfile.write('''app_name = '{}'\n'''.format(app_name))
        urlfile.write('''urlpatterns = [\n''')
        for html in html_files:
            urlfile.write(write_path(html))    
        urlfile.write('''    ]\n''')


if __name__ == '__main__': 
    path_html_files= sys.argv[1]
    app_name= sys.argv[2]
    html_files= list_html_files(path_html_files)
    generate_views(html_files)
    genereate_urls(html_files, app_name)    