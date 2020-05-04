#!/usr/bin/env bash
# This script generates a Django app, its views, urlpatterns and static files 
# from an exported folder from Bootstrap Studio
# Uses python3.x, python3.x-venv, sed and pip
#
# Parameters
# ----------
# $1 Project Name
# $2 App name
# $3 PATH to Static Assets from BootstrapStudio
#
# Example Usage
# -------------
# $./create_app.sh 'ProjectName' 'SomeAppName' './exported/export_1/assets'
#
# Notes
# -----
# It does not create the include path in the main's app urls.py
#
#
root_folder=$(pwd)
# Create an app folder
mkdir app
cd app
# Create virtual environment
python3 -m venv env
source env/bin/activate
# Install django
pip install -r ../requirements.txt
# Start project and app
django-admin startproject $1
cd $1
root_project=$(pwd)
# Create templates folder
mkdir templates
templates_folder=$(echo $root_project/templates)
# settings.py path
project_settings=$(echo $root_project/$1/settings.py)
project_urls=$(echo $root_project/$1/urls.py)
echo "$project_urls"
# App path
app_folder=$(echo $root_project/$2)
#echo "$project_settings"
django-admin startapp $2
# Add static conf to the settings.py file
static_conf=$(echo "STATICFILES_DIRS = [os.path.join(BASE_DIR, '"$2"', 'static'),]")
#echo "$static_conf"
echo "$static_conf" >> "$project_settings"
sed -i "/admin.site.urls),/a path('', include('$2.urls'))," "$project_urls"
sed -i '/from django.urls import path/ s/$/, include/' "$project_urls"
cd $app_folder
# Creates static folder,
mkdir static
cd static
project_static_folder=$(pwd)
# Return to the root folder and execute python script
cd $root_folder
cp -r $3 $project_static_folder
# Edit project settings in place
sed -i  "s/'DIRS': \[\],/'DIRS': [os.path.join(BASE_DIR, 'templates'),],/g" $project_settings
# copy html files to templates folder
cd $3
cd ..
cp *.html $templates_folder
cd $root_folder
python generate_views_urls.py $templates_folder "$2"
mv urls.py $app_folder
mv views.py $app_folder
python process_html.py $templates_folder $2