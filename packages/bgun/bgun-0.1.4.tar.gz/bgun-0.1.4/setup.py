from setuptools import setup, find_packages

setup(
    name="bgun",
    version="0.1.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "bgun=bgun.bgun:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"bgun": ["bgun.json"]},  # Ensures `bgun.json` is included
)

