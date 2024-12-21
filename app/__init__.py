# app/__init__.py  
import os  

# Set the base directory to the directory of this file  
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  

# Define paths for static and media files  
STATIC_DIR = os.path.join(BASE_DIR, "static")  
MEDIA_DIR = os.path.join(BASE_DIR, "media")