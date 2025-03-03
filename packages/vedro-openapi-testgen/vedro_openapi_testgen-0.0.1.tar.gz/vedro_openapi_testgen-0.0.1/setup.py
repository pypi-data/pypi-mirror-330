from setuptools import setup

from vedro_openapi_testgen.__version__ import __version__


def find_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="vedro-openapi-testgen",
    version=__version__,
    description="Vedro Openapi basic tests generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nikita Mikheev",
    author_email="thelol1mpo@gmail.com",
    python_requires=">=3.10",
    url="https://github.com/Lolimpo/vedro-openapi-testgen",
    packages=["vedro_openapi_testgen"],
    install_requires=find_requirements(),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Typing :: Typed",
    ],
    entry_points={
        "console_scripts": [
            "vedro-openapi-testgen = vedro_openapi_testgen:command",
        ]
    }
)
