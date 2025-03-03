import os
import dill as pickle
import logging

from pywander.pathlib import normalized_path

logger = logging.getLogger(__name__)

def get_models_path(*args, app_name='test'):
    """
    获取模型文件路径
    """
    if not args:
        raise Exception('please input the model filename.')

    path = normalized_path(os.path.join('~', 'Pywander', app_name, 'models', *args))

    return path


def load_model(*args, app_name='test'):
    """

    """
    model_path = get_models_path(*args, app_name=app_name)

    with open(model_path, 'rb') as f:
        # 将自动检测所使用的协议版本，因此我们
        # 不需要指定它。
        model = pickle.load(f)

    logger.info(f'load model from: {model_path}')
    return model


def save_model(model, *args, app_name='test'):
    """

    """
    model_path = get_models_path(*args, app_name=app_name)

    with open(model_path, 'wb') as f:
        # 使用最高版本可用协议进行 pickle
        pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)

    logger.info(f'model has saved to: {model_path}')