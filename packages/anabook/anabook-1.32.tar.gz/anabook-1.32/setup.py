from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="anabook",
    version="1.32",
    packages=find_packages(),
    description="This library facilitates exploratory data analysis (EDA), streamlining access to key functions for univariate and bivariate analysis of continuous and categorical variables.",
    long_description=long_description,
    author="Freddy Alvarado",
    author_email="freddy.alvarado.b1@gmail.com",
    url="https://github.com/FreddyAlvarado/anabook",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'pandas<=2.1.3',
        'numpy<=1.26.2',
        'matplotlib<=3.8.2',
        'seaborn<=0.13.0',
        'scipy<=1.11.4'
    ],
)
