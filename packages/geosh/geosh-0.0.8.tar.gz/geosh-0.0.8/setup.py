"""A setuptools based setup module."""

from setuptools import setup, find_packages


def parse_meta(path_to_metadata):
    with open(path_to_metadata) as f:
        metadata = {}
        for line in f.readlines():
            if line.startswith("__version__"):
                metadata["__version__"] = line.split('"')[1]
    return metadata


metadata = parse_meta("geosh/metadata.py")


#RELATIVE_TO_ABSOLUTE_FIGURES = {
#    '![Single window example a.](./figs/singlewindow_a.png)': '<img src="https://github.com/jpvantassel/hvsrpy/blob/main/figs/singlewindow_a.png?raw=true" width="425">',
#}


with open("README.md", encoding="utf8") as f:
    long_description = f.read()
    #for old_text, new_text in RELATIVE_TO_ABSOLUTE_FIGURES.items():
        #long_description = long_description.replace(old_text, new_text)

setup(
    name='geosh',
    version=metadata['__version__'],
    description='A Python package for Geo Utilities Plugin',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Adre17/geosh',
    author='Grechi Umberto',
    author_email='umberto.grechi@sofhare.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',

        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Programming Language :: Python :: 3.12',
    ],
    keywords='horizontal-to-vertical spectral ratio hv hvsr',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['numpy==1.26', 'scipy==1.15.2', 'obspy==1.4.1',
                      'pandas==2.2.3', 'shapely==2.0.7', 'termcolor==2.5.0', 'matplotlib==3.10.0',
                      'click>8.0.0', 'numba==0.61.0', 'PyQt5','Pillow==11.1.0','psycopg2==2.9.10','reportlab==4.3.1',
                      'segyio==1.9.13','opencv-python==4.11.0.86','openpyxl==3.1.5','opencv-contrib-python','xlrd==2.0.1',
                      'pyproj==3.7.1','cython==3.0.12','ipython==8.32.0'
                      ],
    extras_require={
        'dev': ['tox', 'coverage', 'sphinx', 'sphinx_rtd_theme', 'sphinx-click', 'autopep8'],
    },
    include_package_data=True,
    package_data={
        "geosh": ["*.pyd"],  # Includi tutti i file .pyd nella directory my_package
    },
    data_files=[
    ],
    entry_points={
        'console_scripts': [
            'hvsrpy = hvsrpy.cli:cli'
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/Adre17/geosh',
        'Source': 'https://github.com/Adre17/geosh',
        'Docs': 'https://github.com/Adre17/geosh',
    },
)
