import os

import numpy as np

from pywander.pathlib import normalized_path, mkdirs


def get_datasets_path(*args, app_name='test'):
    """
    获取数据集文件路径
    """
    if not args:
        raise Exception('please input the dataset filename.')

    path = normalized_path(os.path.join('~', 'Pywander', app_name, 'datasets', *args))

    if not os.path.exists(path):
        raise Exception(f'file not exists: {path}')

    if not os.path.isfile(path):
        raise Exception(f'can not find the file: {path}')

    return path

def load_mnist_csv_data(*args):
    file_path = get_datasets_path(*args)

    data = []

    with open(file_path) as f:
        for line in f:
            label = line[0]
            image_data = line[2:]
            image_data = image_data.strip()
            image_data_list = image_data.split(',')
            image_data2 = np.asarray(image_data_list, dtype=float)

            data.append((label, image_data2))

    return data
