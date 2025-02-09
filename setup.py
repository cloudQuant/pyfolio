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
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.3',
)
