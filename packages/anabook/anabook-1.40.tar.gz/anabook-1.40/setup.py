from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="anabook",
    version="1.40",
    packages=find_packages(include=["anabook", "anabook.*"]),
    description="This library facilitates exploratory data analysis (EDA), streamlining access to key functions for univariate and bivariate analysis of continuous and categorical variables.",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    author="Freddy Alvarado",
    author_email="freddy.alvarado.b1@gmail.com",
    url="https://github.com/FreddyAlvarado/anabook",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
   
)

