import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tabdeal",
    version="0.1.0",
    author="Amin Basiri",
    author_email="amin.bsr99@gmail.com",
    description="unofficial python package to use Tabdeal API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amin-bs/tabdeal",
    project_urls={
        "Bug Tracker": "https://github.com/amin-bs/tabdeal/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "tabdeal"},
    packages=setuptools.find_packages(where="tabdeal"),
    python_requires=">=3.8",
)
