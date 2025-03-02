# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup, find_packages


def get_version():
    v_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'vwalila', '__init__.py')
    ver_info_str = re.compile(r".*version_info = \((.*?)\)", re.S). \
        match(open(v_file_path).read()).group(1)
    return re.sub(r'(\'|"|\s+)', '', ver_info_str).replace(',', '.')

require = []
with open('requirements.txt') as require_fd:
    for req in require_fd:
        require.append(req)

setup(
    name='vwalila',
    version=get_version(),
    description="vwalila - Awesome tookit for internal",
    author='xiaohui.chang',
    author_email='cxh@dobechina.com',
    packages=find_packages(),
    tests_require=require,
    install_requires=require,

)
