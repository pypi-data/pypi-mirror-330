from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='neidspecmatch',
    version='0.1.2',
    description='Matching NEID Spectra',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/gummiks/hpfspecmatch/',
    author='Te Han, Gudmundur Stefansson (author of HPFSpecMatch)',
    author_email='gummiks@gmail.com',
    install_requires=[
        'numpy',
        'barycorrpy',
        'emcee',
        'lmfit',
        'neidspec',
        'crosscorr',
        'pyde',
        'astroquery',
        'glob2',
        'celerite',
        'numba',
    ],
    packages=find_packages(),
    license_files='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
    keywords='NEID Spectra Astronomy',
    include_package_data=True,
    zip_safe=False,
)