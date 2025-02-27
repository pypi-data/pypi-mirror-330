from setuptools import setup, find_packages

setup(
    name='xtrapnet',
    version='0.1.2',  # Update version to 0.1.2
    packages=find_packages(),  # Auto-detects submodules
    install_requires=[
        'torch>=2.0.0',
        'numpy',
        'scipy'
    ],
    author='cykurd',
    author_email='cykurd@gmail.com',
    description='A robust package for extrapolation control in neural networks',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',  # Ensure PyPI formats it correctly
    url='https://github.com/YourUser/xtrapnet',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
