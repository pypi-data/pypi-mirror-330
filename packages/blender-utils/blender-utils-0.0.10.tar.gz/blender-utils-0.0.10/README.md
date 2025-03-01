# 安装必要的工具
pip install setuptools wheel twine

# 构建包
python setup.py sdist bdist_wheel

# 上传包到 PyPI
twine upload dist/*

# 安装
pip install blender-utils
