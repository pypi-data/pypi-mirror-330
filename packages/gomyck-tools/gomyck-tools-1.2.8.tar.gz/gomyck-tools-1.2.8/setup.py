import os

from setuptools import setup, find_packages

def parse_requirements(filename):
  with open(filename, 'r') as f:
    lines = f.read().splitlines()
    return [line for line in lines if line and not line.startswith('#')]

requirements = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'))

setup(
  name="gomyck-tools",
  version="1.2.8",
  author="gomyck",
  author_email="hao474798383@163.com",
  description="A tools collection for python development by hao474798383",
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  url="https://blog.gomyck.com",
  packages=["ctools"],  # 自动发现并包含包内所有模块
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.9",
  install_requires=requirements
)

# 安装依赖, 并生成构建包
# pip install setuptools wheel twine
# rm -rf gomyck_tools.egg-info dist build && python setup.py sdist bdist_wheel && twine upload dist/* && rm -rf gomyck_tools.egg-info dist build

