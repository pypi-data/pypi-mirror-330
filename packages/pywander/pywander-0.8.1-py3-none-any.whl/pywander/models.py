import os

from pywander.pathlib import normalized_path


def get_models_path(*args, app_name='test'):
    """
    获取模型文件路径
    """
    if not args:
        raise Exception('please input the model filename.')

    path = normalized_path(os.path.join('~', 'Pywander', app_name, 'models', *args))

    if not os.path.exists(path):
        raise Exception(f'file not exists: {path}')

    if not os.path.isfile(path):
        raise Exception(f'can not find the file: {path}')

    return path
