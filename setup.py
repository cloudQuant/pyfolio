import setuptools

setuptools.setup(
    name="pyfolio",
    version="0.9.6",
    author="quantopian、cloudQuant",
    author_email="yunjinqi@gmail.com",
    description="pyfolio packages",
    long_description="pyfolio packages modified by yunjinqi",
    long_description_content_type="text/markdown",
    url="https://gitee.com/yunjinqi/pyfolio",
    packages=setuptools.find_packages(exclude=['docs', 'docs2', 'samples']),
    include_package_data=True,  # Include all files specified in MANIFEST.in
    package_data={
        'pyfolio': ['datas/*', 'templates/*']  # Include datas and templates directories
    },
    install_requires=[
        'flask>=2.0.0',
        'ipython>=7.0.0',
        'matplotlib>=3.0.0',
        'numpy>=1.20.0',
        'pandas>=1.3.0',
        'pytz>=2019.3',
        'scikit-learn>=0.22.0',
        'scipy>=1.5.0',
        'seaborn>=0.10.0',
        # Note: empyrical must be installed separately from GitHub/Gitee
        # 'empyrical @ git+https://github.com/cloudQuant/empyrical.git',
    ],
    dependency_links=[
        'git+https://github.com/cloudQuant/empyrical.git#egg=empyrical',
        'git+https://gitee.com/yunjinqi/empyrical.git#egg=empyrical',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires='>=3.8',
    extras_require={
        'test': [
            'pytest>=6.0.0',
            'pytest-cov>=2.10.0',
            'pytest-xdist>=2.0.0',
            'parameterized>=0.7.0',
        ],
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.10.0',
            'pytest-xdist>=2.0.0',
            'parameterized>=0.7.0',
            'flake8>=3.8.0',
            'black>=21.0',
            'isort>=5.0.0',
        ],
    },
)
