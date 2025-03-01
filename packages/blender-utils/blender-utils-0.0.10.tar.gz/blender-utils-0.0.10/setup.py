from setuptools import setup, find_packages

setup(
  name = "blender-utils",
  version = "0.0.10",
  packages = find_packages(),
  author = "Zhang Meixue",
  author_email = "3385842328@qq.com",
  description = "",
  long_description = open('README.md', encoding = 'utf-8').read(),
  long_description_content_type = 'text/markdown',
  url = "https://github.com/xnorain001/blender-utils",
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires = '>=3.11.9',
)