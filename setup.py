import setuptools


# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="recutils",
    version="0.0.1",
    author="Tyler M Kontra",
    author_email="tyler@tylerkontra.com",
    description="GNU Recutils implemented in python3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Source': 'https://github.com/ttymck/python-recutils',
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[],
)