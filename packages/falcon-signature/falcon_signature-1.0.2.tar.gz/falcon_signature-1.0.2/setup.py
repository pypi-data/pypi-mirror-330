from setuptools import setup, find_packages

setup(
    name="falcon_signature",
    version="1.0.2",
    packages=find_packages(),
    install_requires=["numpy", "pycryptodome"],
    author="Erhan",
    author_email="senin-email@example.com",
    description="Falcon Signature implementation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tprest/falcon.py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
