from io import open

from setuptools import setup

from i18trans import __version__ as version

setup(
    name="i18trans",
    version=version,
    url="https://www.codehemu.com/p/jsontrans.html",
    license="MIT",
    author="Hemanta Gayen",
    description="",
    long_description="".join(open("README.md", encoding="utf-8").readlines()),
    long_description_content_type="text/markdown",
    project_urls={
        "Source Code": "https://github.com/hemucode/i18trans",
        "Bug Tracker": "https://github.com/hemucode/i18trans/issues",
        "Changelog": "https://github.com/hemucode/i18trans/blob/master/CHANGELOG.md",
    },
    keywords=["gui", "executable"],
    packages=["i18trans"],
    include_package_data=True,
    install_requires=["tk>=0.1.0","googletrans==4.0.0-rc1"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    entry_points={
        "console_scripts": ["i18trans=i18trans.__main__:run"],
    }
)
