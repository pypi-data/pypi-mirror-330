from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='sfs_da', 
    version='1.0.4',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'mpmath',
        'scipy',
        'scikit-learn'
    ],
    description='A package for Statistical Inference for Feature Selection after OT-based Domain Adaptation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nguyen Thang Loi',
    author_email='23520872@gm.uit.edu.vn',
    license='MIT',
    url='https://github.com/NT-Loi/SFS_DA.git'
)