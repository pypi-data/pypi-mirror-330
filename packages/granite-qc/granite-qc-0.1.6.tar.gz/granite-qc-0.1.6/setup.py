from setuptools import setup, find_packages

setup(
    name="granite-qc",
    version="0.1.6", 
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "torch",
        "torch_geometric",
        "networkx",
        "numpy"
    ],
    package_data={"granite_qc": ["trained_model.pkl"]},  # Include the model file
    description="A package for graph-based energy optimization using a trained model.",
    author="Bao Tran",
    author_email="tranq3@vcu.edu",
    url="https://github.com/quocbao0603/granite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
