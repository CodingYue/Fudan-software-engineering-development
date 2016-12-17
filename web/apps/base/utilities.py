"""
    This file contains useful function for image tagging,　categorizing and searching
"""
import requests
from api_keys import api_key, api_secret, authorization, categorizer_id

import os
import numpy as np
from PIL import Image, ImageChops
import time

class ApiUploadError(Exception):
    pass

class ApiTagError(Exception):
    pass

class ApiCategoryError(Exception):
    pass


"""
    upload image file to api service
    if success, return id
    if unsuccess, raise ApiUploadError
"""
def upload(img_path):
    response = requests.post('https://api.imagga.com/v1/content',
        auth=(api_key, api_secret),
        files={'image': open(img_path, 'r')}).json()

    if response['status'] != 'success':
        raise ApiUploadError

    return response['uploaded'][0]['id']


"""
    tag image use api service
    img_id is the id returns from upload
    if img_id is not provided, upload method will be called
    confidence is the threshold for selecting tag
    if success, return the tags as a list, note this list may contains zero element if there is no tag matches the confidence
    if unsuccess, raise ApiTagError
"""
def tag(img_path, confidence = 20, img_id = 0):
    if img_id == 0:
        img_id = upload(img_path)
    response = requests.get('https://api.imagga.com/v1/tagging?content=%s' % img_id, auth=(api_key, api_secret)).json()

    if 'unsuccessful' in response:
        raise ApiTagError

    results = []
    for tag in response['results'][0]['tags']:
        if tag['confidence'] > confidence:
            results.append(tag['tag'])
    return results


"""
    categorize image use api service
    img_id is the id returns from upload
    if img_id is not provided, upload method will be called
    if success, return the category as a string, note this string contains whitespace
    if unsuccess, raise ApiCategoryError
"""
def category(img_path, img_id = 0):
    if img_id == 0:
        img_id = upload(img_path)
    response = requests.get('https://api.imagga.com/v1/categorizations/%s?content=%s' % (categorizer_id, img_id), auth=(api_key, api_secret)).json()

    if 'unsuccessful' in response:
        raise ApiCategoryError

    result = {'confidence': 0, 'name': '' }
    for category in response['results'][0]['categories']:
        if category['confidence'] > result['confidence']:
            result = category

    return result['name']


"""
    returns available classfier for categorizing
"""
def classifier_list():
    response = requests.get('https://api.imagga.com/v1/categorizers',
        auth=(api_key, api_secret)).json()
    return response


"""
    caculate the difference of two images
    note the sequence of im1, im2 will influence the result
    the im1 should be the scratch image
"""
def caculate_dif(im1, im2):
    im1_r, im1_g, im1_b, im1_a = im1.split()
    im2_r, im2_g, im2_b, im2_a = im2.split()
    dif_r = np.matrix(ImageChops.difference(im1_r, im2_r))
    dif_g = np.matrix(ImageChops.difference(im1_g, im2_g))
    dif_b = np.matrix(ImageChops.difference(im1_b, im2_b))
    alpha = np.matrix(im1_a) / 255
    dif = np.multiply(dif_r, alpha).sum() \
        + np.multiply(dif_g, alpha).sum() \
        + np.multiply(dif_b, alpha).sum()
    return dif


"""
    search similar image in the category_path,
    the result will be a list contains the tuple of result image path and the difference of two image, eg:
    [('dir/a.jpg', 3433), ('dir/b.jpg', 4555)]
    the items in this list is limited to result_num
"""
def search_by_image(img_path, category_path, result_num = 10):
    results = []
    im1 = Image.open(img_path).resize((16, 16))\
        .convert("RGBA")
    for lists in os.listdir(category_path):
        f = os.path.join(category_path, lists)
        im2 = Image.open(f).resize((16, 16))\
            .convert("RGBA")
        results.append((f, caculate_dif(im1, im2)))
    results = sorted(results, key=lambda item: item[1])
    return results[:result_num]
