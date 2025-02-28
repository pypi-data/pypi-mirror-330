from setuptools import setup, find_packages

setup(
    name="htree",
    version="2.3.5",  # Adjust your version accordingly
    description="A library for tree reading, embedding, and analysis of phylogenetic trees",
    author="Puoya Tabaghi",
    author_email="ptabaghi@ucsd.edu",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy>=2.2.3",
        "scipy>=1.15.2",
        "matplotlib>=3.10.0",
        "scikit-learn>=1.6.1",
        "seaborn>=0.13.2",
        "torch>=2.6.0",
        "treeswift>=1.1.45",
        "tqdm>=4.67.1",
        "imageio>=2.37.0",
        "imageio-ffmpeg>=0.6.0"
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.10.16",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    # Remove the `license_files` line, as it's causing issues
    # license_files=["LICENSE"],  # Remove this line
)
