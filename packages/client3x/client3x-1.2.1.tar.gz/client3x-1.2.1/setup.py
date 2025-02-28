from setuptools import setup, find_packages

setup(
    name="client3x",
    version="1.2.1",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.11.11",
        "requests>=2.32.3",
    ],
    author="Wert-Rar",
    author_email="wert-rar@mail.ru",
    description="A python Client for 3X-UI client",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wert-rar/ThreeX-Python-Client.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)