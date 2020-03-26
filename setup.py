import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='aep_sdk',
    version='0.0.35',
    description='A SDK for the Adobe Experience Platform',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests",
        "PyJWT",
        "bitmath",
        "cryptography",
    ],
    liscense='MIT',
    url='https://github.com/Dacson33/Experience-Platform-Python-SDK/',
    author=[
        "Dakoda Richardson",
        "Benson Condie",
        "Adam Ure",
        "Nick Cummings",
        "Lance Haderlie"
    ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    packages=setuptools.find_packages(
        exclude=['Tests']
    ),
)
