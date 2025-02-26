from setuptools import setup
from tonetext import __version__

VERSION = __version__
with open("README.md", "r") as fh:
    README = fh.read()

setup(
    name="tonetext",
    version=VERSION,
    description="Colored text for terminal",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Kim Huang",
    license="MIT",
    python_requires=">=3.5",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Topic :: Terminals",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    packages=["tonetext"],
)
