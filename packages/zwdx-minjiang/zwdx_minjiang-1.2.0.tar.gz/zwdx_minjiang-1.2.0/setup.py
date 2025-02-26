from setuptools import setup,find_packages

setup(
    name = 'zwdx_minjiang',
    version = '1.2.0',
    description = 'Quantum Measurement and Control Driver',
    author = 'zwdx',
    license = 'MIT',
    packages = find_packages(),
    zip_safe = False,
    include_package_data = True,
    install_requires = [
        'pyvisa>=1.13.0',
        'numpy>=1.25.1',
        'zerorpc>=0.6.3',
        'matplotlib>=3.7.2',
        'pandas>=2.0.3',
        'seaborn>=0.13.2',
        'scipy>=1.11.1',
        'ipympl>=0.9.4',
        'grpcio>=1.70.0',
        'protobuf>=5.27.2'
    ],
    keywords='instrument Master',
    classifiers=[
        "Natural Language :: Chinese (Simplified)",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities"
    ],
)