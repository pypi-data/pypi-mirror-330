from setuptools import setup, find_packages

setup(
    name="kinpfn",
    version="1.0.0",
    author="Dominik Scheuer",
    author_email="dom.scheuer@gmail.com",
    description="A package for KinPFN, the novel prior-data fitted network (PFN) for the approximation of kinetic RNA folding time distributions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/automl/KinPFN",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "torch",
        "scipy",
        "matplotlib",
        "scikit-learn",
        "pandas",
        "polars",
        "neural-pipeline-search",
        "tqdm",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license="Apache-2.0",
)
