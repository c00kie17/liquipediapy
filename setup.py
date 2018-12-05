from setuptools import setup, find_packages


with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='liquipediapy',
    version = '1.0.0',
    description= 'api for liquipedia.net',
    author = 'c00kie17',
    author_email = 'anshul1708@gmail.com',
    url = 'https://github.com/c00kie17/liquipediapy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'beautifulsoup4>=4.6.3',
        'requests>=2.20.1',
        'urllib3>=1.23'
    ],
)