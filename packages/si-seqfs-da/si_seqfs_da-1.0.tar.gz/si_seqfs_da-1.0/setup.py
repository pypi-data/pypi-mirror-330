import setuptools

with open('README.md','r') as f:
    long_description = f.read()
setuptools.setup(
    name="si_seqfs_da",
    version="1.0",
    author="Duong Tan Loc",
    author_email="235202854@gm.uit.edu.vn",
    description="Statistical Inference for Sequential Feature Selection after Domain Adaptation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/locluclak/SI-SeqFS-DA",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
