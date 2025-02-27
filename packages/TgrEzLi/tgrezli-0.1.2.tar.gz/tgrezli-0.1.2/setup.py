from setuptools import setup, find_packages

setup(
    name='TgrEzLi',
    version='0.1.2',
    description='Easy-to-use synchronous interface for telegram-bot library with async backend and intuitive handlers.',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    author='eaannist',
    author_email='eaannist@gmail.com',
    url='https://github.com/eaannist/TgrEzLi',
    packages=find_packages(),
    install_requires=["python-telegram-bot>=20.0","requests>=2.28.0","PyCypherLib>=1.3.5"],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)