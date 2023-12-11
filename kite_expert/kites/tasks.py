import os
from celery import shared_task
from PIL import Image

from .models import Kite, Expert
from kite_expert.settings import MAX_IMAGE_SIZE


@shared_task
def resize_photo_kite(pk):
    kite = Kite.objects.get(pk=pk)
    for photo in (kite.photo1, kite.photo2, kite.photo3, kite.photo4):
        if photo:
            resize_image(photo)


@shared_task
def resize_photo_expert(pk):
    expert = Expert.objects.get(pk=pk)
    if expert.photo:
        resize_image(expert.photo)


def resize_image(photo_object):
    img_path = os.path.join('media', photo_object.name)
    try:
        im = Image.open(img_path)
        print('file loaded: %s' % img_path)
    except:
        return

    max_size = MAX_IMAGE_SIZE
    w, h = im.size
    cut = abs(w - h) // 2
    if w >= h: 
        box = (cut, 0, w - cut, h)
    else: 
        box = (0, cut, w, h - cut)
    im = im.crop(box=box)
    if im.width > max_size:
        im = im.resize(size=(max_size, max_size))
    im.save(img_path)
    