import setuptools

setuptools.setup(
    name="pyfolio",
    version="0.9.2",
    author="quantopian",
    author_email="yunjinqi@qq.com",
    description="pyfolio packages",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url="https://gitee.com/yunjinqi/pyfolio",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: MacOS :: MacOS X"
    ],
    python_requires='>=3.6.3',
    
)