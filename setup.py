import setuptools

setuptools.setup(
    name="pyfolio",
    version="0.9.2",
    author="quantopian",
    author_email="yunjinqi@qq.com",
    description="pyfolio packages",
    long_description="pyfolio packages modified by yunjinqi",
    long_description_content_type = "text/markdown",
    url="https://gitee.com/yunjinqi/pyfolio",
    packages=['pyfolio'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6.3',
    
)