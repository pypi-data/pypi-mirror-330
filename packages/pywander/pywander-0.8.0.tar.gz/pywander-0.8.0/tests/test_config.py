def test_config():
    from pywander.config import config

    assert config['APP_NAME'] == 'pywander'


