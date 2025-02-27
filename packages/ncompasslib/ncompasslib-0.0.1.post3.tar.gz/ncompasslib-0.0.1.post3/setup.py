from setuptools import setup, find_packages

setup(
    name="ncompasslib",
    version="0.0.1-post3",
    author="nCompass Technologies",
    author_email="diederik.vink@ncompass.tech",  # Replace with actual email
    description="nCompass Tools Library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nCompass-tech/ncompasslib.git",  # Replace with actual repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
    ],
    extras_require={
        'dev': [
            'python-dotenv>=1.0.0',
            'build',
            'twine',
            'pytest>=7.0.0',
        ],
    },
) 
