from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='neidspecmatch',
    version='0.1.1',
    description='Matching NEID Spectra',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/gummiks/hpfspecmatch/',
    author='Te Han, Gudmundur Stefansson (author of HPFSpecMatch)',
    author_email='gummiks@gmail.com',
    install_requires=[
        'barycorrpy',
        'emcee',
        'lmfit',
        'neidspec',
        'crosscorr',
        'pyde',
        'astroquery',
        'glob2',
    ],
    packages=find_packages(),  # Automatically find packages in the directory
    license_files='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
    keywords='NEID Spectra Astronomy',
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    zip_safe=False,  # Ensure the package is not installed as a zip file
)