import os
from PIL import Image
from app import get_or_create_celery
from config import get_env_config

app_settings = get_env_config()
celery = get_or_create_celery()


thumbnail_size = 400, 300


def get_thumbnail_filename(filename):
    base, ext = os.path.splitext(filename)
    return base + '.thumbnail' + ext


def save_image(file, filename):
    file.save(os.path.join(app_settings.UPLOAD_FOLDER, filename))
    make_thumbnail.delay(filename)


@celery.task
def make_thumbnail(filename):
    im = Image.open(os.path.join(app_settings.UPLOAD_FOLDER, filename))
    im.thumbnail(thumbnail_size, Image.ANTIALIAS)
    thumbnail_filename = get_thumbnail_filename(filename)
    im.save(os.path.join(app_settings.UPLOAD_FOLDER, thumbnail_filename))

