from distutils.core import setup

setup(name='amz_extractor',
      version='1.0.9',
      description='提取亚马逊详情页和评论信息',
      author='lonely',
      packages=['amz_extractor'],
      package_dir={'amz_extractor': 'amz_extractor'},
      install_requires=['dateparser>=1.1.4', 'pyquery>=1.4.3']
      )

"""
# 更新版本命令

python setup.py sdist bdist_wheel

twine upload dist/*

pypi-AgEIcHlwaS5vcmcCJDU1MzcyNDMzLTMxZTgtNDMwYy1iYjc1LWFkY2NmODA3YWM2NAACKlszLCJiYWRlYjNjMS1lNDE2LTQ2MzEtYjYyMy1lNGIwZTFiNzYyNTYiXQAABiCfmYnP8ub1BxGEKI3irxGj_YXv4Is8DleBm8MEUVsSuw
"""