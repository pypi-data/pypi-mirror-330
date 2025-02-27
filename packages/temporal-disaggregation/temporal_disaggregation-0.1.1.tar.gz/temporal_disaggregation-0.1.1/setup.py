from setuptools import setup, find_packages

setup(
    name="temporal-disaggregation",
    version="0.1.1",
    author="Jaime Vera",
    author_email="your-email@example.com",
    description="A Python library for temporal disaggregation of time series data",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jaimevera1107/temporal-disaggregation",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scipy",
        "matplotlib",
        "scikit-learn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.7",
)
