from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="plexcontentmanager",
    version="0.1.0",
    author="Alex Boutros",
    author_email="alex@aterrible.day",
    description="A command-line tool for managing and curating Plex Media Server content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexboutros/plexcontentmanager",
    project_urls={
        "Bug Tracker": "https://github.com/alexboutros/plexcontentmanager/issues",
        "Source Code": "https://github.com/alexboutros/plexcontentmanager",
        "Documentation": "https://github.com/alexboutros/plexcontentmanager#readme",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Multimedia :: Video",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "plexapi",
        "click",
        "colorama",
        "requests>=2.25.0",
        "urllib3<2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "plexcontent=plexcontentmanager.cli:main",
        ],
    },
)
