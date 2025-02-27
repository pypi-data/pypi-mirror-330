from setuptools import setup, find_packages

setup(
    name="INP_Calc",
    version="0.2.2",
    author="Max Fobian Skov",
    author_email="max.fobian@gmail.com",
    description="Functions for converting frozen fraction (FF) to "
                "concentration, volume, and surface area.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'scipy>=1.7.0',
        'inspect>=3.0.0'
    ],
    python_requires=">=3.9",
)
