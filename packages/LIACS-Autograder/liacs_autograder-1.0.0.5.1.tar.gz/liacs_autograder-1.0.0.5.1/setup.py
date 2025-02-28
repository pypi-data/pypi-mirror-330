from setuptools import setup, find_packages

setup(
    name="LIACS_Autograder",
    version="1.0.0.5.1",
    packages=find_packages(),
    package_data={},
    install_requires=[
        "PyYAML>=6.0.1",
        "numpy>=1.26.4"
    ],
    include_package_data=True,
    description="A package to autograde",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/jjgsherwood/LIACS_Autograder",
    author="Jonne Goedhart; Irina Epure",
    author_email="j.j.goedhart@liacs.leidenuniv.nl",
    license="Creative Commons CC BY-NC-SA 4.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)