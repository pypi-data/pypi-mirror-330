from setuptools import setup, find_packages

setup(
    name='optimation',
    version='2.0',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,  
    author='Sourceduty',
    author_email='sourceduty@gmail.com',
    description='A Python library for iterative variable weighting and optimation',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT",
)
