from setuptools import setup, find_packages

setup(
    name='sierpinski_hpo',
    version='0.1.0',
    author='Abhishek Pandey',
    description='A Sierpinski Triangle-based Hyperparameter Optimization algorithm.',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
