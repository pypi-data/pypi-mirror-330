from setuptools import setup

setup(
    name="makertiles",
    version="0.1.0",
    description="Reserved package name for MakerTiles.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="MakerTiles",
    # author_email="contact",
    url="https://github.com/yourusername/makertiles",
    packages=["makertiles"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)