#!/usr/bin/env python
# -*-coding:utf-8-*-

import pytest
from click.testing import CliRunner
from pywander.image.__main__ import main

@pytest.mark.skip('i have test it')
def test_resize_command(tempfolder):
    runner = CliRunner()

    result = runner.invoke(main, ['resize', '--width', '30',
                                  'test_images/test.png', '-V'])

    assert result.exit_code == 0
    assert 'done' in result.output
