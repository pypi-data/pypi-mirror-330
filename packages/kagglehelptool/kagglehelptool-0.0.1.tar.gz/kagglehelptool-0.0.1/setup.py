from setuptools import setup, find_packages

setup(
    name='kagglehelptool',
    version='0.0.1',
    description='a pip-installable package kagglehelptool',
    license='MIT',
    packages=find_packages(),
    author='Fatih Karagoz',
    author_email='fatihkkaragoz@gmail.com',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=['kaggle'],
    install_requires=[
       'kagglehub>=0.2.9'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    url="https://github.com/FatihKaragoz/kagglehelptool"
)