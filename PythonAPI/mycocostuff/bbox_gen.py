#!/usr/bin/env python

# Author: Youngjun Kim, aiden.kim@brookhurstgarage.com
# Date: 6/17/2017

from __future__ import print_function

import os
import json
import numpy as np

from PIL import Image
from operator import itemgetter
from copy import deepcopy
from multiprocessing import Pool, cpu_count


def get_bbox(image_id):

  with open('config.json') as config_file:
    config = json.load(config_file)

  labels = config['labels']

  instance_path = "training/instances/{}.png".format(image_id)
  #instance_path = "validation/instances/{}.png".format(image_id)
  instance_image = Image.open(instance_path)
  instance_array = np.array(instance_image, dtype=np.uint16) 
  instance_label_array = np.array(instance_array / 256, dtype=np.uint8)
  instance_ids_array = np.array(instance_array % 256, dtype=np.uint8)

  objects_ = {}

  for i in xrange(instance_label_array.shape[0]):
    for j in xrange(instance_label_array.shape[1]):
      label = str(instance_label_array[i, j])
      id_ = instance_ids_array[i, j]

      #if label == '45' or label == '47':  # Pole or Utility Pole
      if labels[int(label)]['instances'] is True:
        if label not in objects_:
          objects_[label] = {}
        if id_ not in objects_[label]:
          objects_[label][id_] = []
        objects_[label][id_].append((j, i))

  objects = deepcopy(objects_)

  for label in objects_.keys():
    objects[label] = []
    for id_ in objects_[label].keys():
      objects[label].append([(min(objects_[label][id_], key = itemgetter(0))[0], min(objects_[label][id_], key = itemgetter(1))[1]), (max(objects_[label][id_], key = itemgetter(0))[0], max(objects_[label][id_], key = itemgetter(1))[1])])

  return {image_id: objects}


if __name__ == '__main__':
  image_files = os.listdir('training/instances')
  #image_files = os.listdir('validation/instances')
  image_ids = map(lambda x: os.path.splitext(x)[0], image_files)

  ncores = cpu_count()

  if ncores >= 4:
    p = Pool(ncores - 2)
    results = p.map(get_bbox, image_ids)
  else:
    results = []
    for image_id in image_ids:
      result = get_bbox(image_id)
      results.append(result)

  if os.path.exists('bbox.json'):
    with open('bbox.json') as bbox_file:
      bbox = json.load(bbox_file)
  else:
    bbox = {}

  for result in results:
    bbox.update(result)

  with open('bbox.json', 'w') as bbox_file:
    json.dump(bbox, bbox_file)


