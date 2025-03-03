from setuptools import setup, find_packages

setup(
    name="pytorch-adversarial-attackers",
    version="0.1",
    author="Santhoshkumar K",
    author_email="your-email@example.com",
    description="A PyTorch library for evaluating model robustness against FGSM, PGD, and CW attacks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/santhosh1705kumar/pytorch-adversarial-attackers",
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchvision",
        "numpy",
        "matplotlib",
        "Pillow"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
