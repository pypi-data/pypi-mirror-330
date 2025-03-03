from setuptools import setup, find_packages

setup(
    name="adversarial-attacks",  # PyPI package name
    version="0.1",
    packages=find_packages(),
    install_requires=["torch", "numpy"],
    author="Santhoshkumar",
    description="A lightweight adversarial attack library for PyTorch",
    url="https://github.com/yourgithub/adversarial-attacks",  # Replace with your repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
