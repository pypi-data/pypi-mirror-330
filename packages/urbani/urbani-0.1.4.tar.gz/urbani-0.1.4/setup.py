from setuptools import setup, find_packages

setup(
    name="urbani",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    author="Mohamed Ibrahim",
    author_email="contact@urban-i.ai",
    description="URBAN-i API client library",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/urbanist-ai/urbani_api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)