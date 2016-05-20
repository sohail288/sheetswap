"""
    Common tasks used throughout the controllers
"""

import os
from PIL import Image
from app.celery_creator import celery
from config import get_env_config


app_settings = get_env_config()
thumbnail_size = 400, 300


def get_thumbnail_filename(filename):
    base, ext = os.path.splitext(filename)
    return base + '.thumbnail' + ext


def save_image(file, filename, create_thumbnail=True):
    file.save(os.path.join(app_settings.UPLOAD_FOLDER, filename))

    if create_thumbnail:
        make_thumbnail.delay(filename)


@celery.task
def make_thumbnail(filename):
    im = Image.open(os.path.join(app_settings.UPLOAD_FOLDER, filename))
    im.thumbnail(thumbnail_size, Image.ANTIALIAS)
    thumbnail_filename = get_thumbnail_filename(filename)
    im.save(os.path.join(app_settings.UPLOAD_FOLDER, thumbnail_filename))

