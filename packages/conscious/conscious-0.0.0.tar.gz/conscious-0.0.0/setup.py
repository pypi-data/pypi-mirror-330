from setuptools import setup, find_packages

setup(
    name="conscious",
    version="0.0.0",
    packages=find_packages(),
    install_requires=[],
    author="Ami Tachibana",
    author_email="tachibana@openconsc.com",
    description="Scheduled for public release in March by OpenConscious, Japan. ",
    long_description="This package name has been reserved for a new open-source library "+ \
        "scheduled for public release in March by OpenConscious, Japan. "+ \
        "If the source code is not disclosed by December 2025, "+ \
        "we plan to relinquish this PyPI package name.",
    url="https://openconsciouss.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
