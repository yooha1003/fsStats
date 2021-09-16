from setuptools import setup, find_packages

setup(
    name='fsStats',
    version='0.1.0',
    url='https://github.com/yooha1003/fsStats',
    author='Uksu, Choi',
    author_email='qtwing@naver.com',
    description='FreeSurfer Stats Extraction python script',
    packages=find_packages(),
    install_requires=['pandas', 'csv', 'argparse', 'numpy'],
)
