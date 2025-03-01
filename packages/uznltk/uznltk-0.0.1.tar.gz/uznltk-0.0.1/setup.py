import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uznltk",
    version="0.0.1",
    author="Ulugbek Salaev",
    author_email="ulugbek0302@gmail.com",
    description="uznltk | The Uzbek Natural Language Toolkit (NLTK) is a Python package for natural language processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UlugbekSalaev/uznltk",
    project_urls={
        "Bug Tracker": "https://github.com/UlugbekSalaev/uznltk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['nltk', 'mophology', 'uzbek-language', 'pos tagging', 'morphological tagging'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["UzMorphAnalyser", "pandas"],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={"": ["*.csv", "*.png"]},
    #package_data={"": ["cyr_exwords.csv", "lat_exwords.csv"],},
)