import setuptools

with open("requirements/base.txt", "r", encoding="utf-8") as fh:
    requirements = fh.readlines()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="tabdeal-python",
    version="0.3.1",
    author="Amin Basiri",
    author_email="amin.bsr99@gmail.com",
    description="Official python package to use Tabdeal API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tabdeal-Exchange/tabdeal-python",
    project_urls={
        "Bug Tracker": "https://github.com/Tabdeal-Exchange/tabdeal-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),
    install_requires=[req for req in requirements],
    python_requires=">=3.6",
    include_package_data=True,
)
