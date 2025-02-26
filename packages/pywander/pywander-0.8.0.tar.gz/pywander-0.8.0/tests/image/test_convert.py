#!/usr/bin/env python
# -*-coding:utf-8-*-

import pytest
from click.testing import CliRunner
from pywander.image.__main__ import main


#@pytest.mark.skipif(bool(not shutil.which('pdftocairo')), reason='there is not pdftocairo')
@pytest.mark.skip('i have test it')
def test_multi_folder_convert_command(tempfolder):
    runner = CliRunner()

    result = runner.invoke(main,
                           ['convert', '--outputdir', 'other_folder',
                            'test_images/other_folder/test2.pdf', '-V'])
    assert result.exit_code == 0
    assert 'done' in result.output
    result = runner.invoke(main,
                           ['convert', '--outputdir', 'other_folder',
                            'test_images/other_folder/test3.pdf', '-V'])
    assert result.exit_code == 0
    assert 'done' in result.output
    result = runner.invoke(main,
                           ['convert', '--outputdir', 'other_folder/other_folder2',
                            'test_images/other_folder/other_folder2/test4.pdf',
                            '-V'])
    assert result.exit_code == 0
    assert 'done' in result.output
    result = runner.invoke(main,
                           ['convert', '--outputdir', 'other_folder/other_folder2',
                            'test_images/other_folder/other_folder2/test5.pdf',
                            '-V'])
    assert result.exit_code == 0
    assert 'done' in result.output
