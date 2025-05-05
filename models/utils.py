import secrets
import os
from PIL import Image
from flask import current_app

def save_file(form_file):
     #  generate a random filname and use the same extension as the originl filename
     randon_file_name = secrets.token_hex(8)
     f_name, f_ext = os.path.splitext(form_file.filename)
     new_filename = randon_file_name+f_ext
     
     #set the full path, resize the image, and store(save) the resized image.
     new_file_path = os.path.join(current_app.root_path, 'static/images/user-pics', new_filename)
     #resize the image
     image_new_size= (150,150)
     i= Image.open(form_file)
     i.thumbnail(image_new_size)
     i.save(new_file_path)
     return new_filename