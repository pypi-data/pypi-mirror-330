from setuptools import setup, find_packages

setup(
    name='factorchain',
    version='1.0',
    packages=find_packages(),
    install_requires=['numpy'],
    author='Sourceduty',
    author_email='sourceduty@gmail.com',
    description='A library for multiple simultaneous computations with dynamically influencing results in complex webs of interconnected operations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://sourceduty.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
