from numpy.distutils.core import Extension, setup
from pathlib import Path

def readme():
    with open('README.md') as f:
        return f.read()

CCF_1d = Extension('crosscorr._CCF_1d', sources=['crosscorr/CCF_1d.f'])
CCF_3d = Extension('crosscorr._CCF_3d', sources=['crosscorr/CCF_3d.f'])
CCF_pix = Extension('crosscorr._CCF_pix', sources=['crosscorr/CCF_pix.f'])

setup(
    name='crosscorr',
    version='0.1.2',
    description='Calculate Binary Cross Correlation Functions',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/gummiks/crosscorr/',
    author='Gudmundur Stefansson, Te Han',
    author_email='gummiks@gmail.com, tehanhunter@gmail.com',
    install_requires=['numpy==1.24.3', 'barycorrpy', 'h5py', 'seaborn'],
    packages=['crosscorr'],
    license_files='LICENSE',  # Ensure you have a LICENSE file
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
    keywords='Spectra Astronomy',
    package_data={
        'crosscorr': [
            'data/espresso/masks/*',
            'data/harps/masks/G2.mas',
            'data/hpf/masks/gj699_combined_stellarframe.mas',
            'data/hpf/masks/specmatch_mask.mas',
        ],
    },
    include_package_data=True,
    ext_modules=[CCF_1d, CCF_3d, CCF_pix],
)