from setuptools import setup, find_packages

setup(
    name='recommend_py',  # Project name
    version='0.1.4',  # Project version
    packages=find_packages(),  # Automatically find packages
    install_requires=[  # Required packages
        'numpy',
        'pandas',
        'scikit-learn',
        # Add other dependencies
    ],
    author='Ziqian Wang',  # Author
    author_email='1793982387@qq.com',  # Author email
    description='A library to do recommendations based on matrix',  # Project description
    long_description=open('README.md').read(),  # Detailed description
    long_description_content_type='text/markdown',
    url='https://github.com/blacker-sd/pyrecommendation',  # Project URL
    classifiers=[
        'Programming Language :: Python :: 3',  # License
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
    ],
    python_requires='>=3.6',  # Required Python version
) 