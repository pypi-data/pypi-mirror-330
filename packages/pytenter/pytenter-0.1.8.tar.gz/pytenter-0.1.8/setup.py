from setuptools import setup, find_packages

setup(
    name="pytenter",
    use_scm_version=True,  # Auto-fetch version from Git
    setup_requires=["setuptools_scm"],  # Required for versioning
    description="pdfjinja fork with updated libraries",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Timothy",
    url="https://github.com/boiledsteak/pytenter",
    packages=find_packages(),
    install_requires=[
        "jinja2==3.1.5",
        "pdfminer.six==20240706",
        "pypdf==5.3.0",
        "Pillow==11.1.0",
        "reportlab==4.3.1",
        "fdfgen==0.16.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
