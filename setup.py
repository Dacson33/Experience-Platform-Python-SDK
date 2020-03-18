import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="experience-SDK", # Replace with your own username
    version="0.0.1",
    author="Benson Condie, Dakoda Richardson, Adam Ure, Nick Cummings, Lance Haderlie",
    author_email="",
    description="A package for the Adobe Experience Platform SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dacson33/Experience-Platform-Python-SDK/tree/master",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)