from setuptools import setup, find_packages

setup(
    name='auto_easy',  # 打包后的名称
    version='0.1.6',  # 版本号
    author='Jefung',
    author_email='jefung865424525@gmail.com',
    description='make automated script development easier',
    long_description=open('README.md', encoding='utf-8').read(),  # 从README.md中读取详细描述
    long_description_content_type='text/markdown',
    url='https://github.com/Jefung/auto_easy',  # 项目的URL
    packages=find_packages(),  # 自动发现所有的���
    classifiers=[  # 根据您的许可证调整
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',  # 最低Python版本
)
