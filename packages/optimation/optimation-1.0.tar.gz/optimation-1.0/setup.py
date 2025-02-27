from setuptools import setup, find_packages

setup(
    name='optimation',
    version='1.0',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,  # Ensures LICENSE file is included
    author='Sourceduty',
    author_email='sourceduty@gmail.com',
    description='A Python library for iterative variable weighting and optimation',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/optimation',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
