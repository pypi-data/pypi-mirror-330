from setuptools import setup, find_packages

setup(
    name='restauapii',  # Name of the module
    version='1.0',  # Version of the module
    # packages=find_packages(),  # Automatically find packages
    install_requires=[  # List of dependencies
        # 'numpy', 'requests', etc.
        'mysql-connector-python','restauvallues','datetime','bcrypt', 'flask'
    ],
    author='Capo Loup',  # Your name
    author_email='loupcapo4@gmail.com',  # Your email
    description='api restauu',  # Short description of your module
    # long_description=open('README.md').read(),  # Long description from the README file
    # long_description_content_type='text/markdown',  # Content type for long description
    # url='https://github.com/yourusername/my_module',  # URL to the module's repository (optional)
    # classifiers=[  # Classifiers for the package (optional but recommended)
    #     'Programming Language :: Python :: 3',
    #     'License :: OSI Approved :: MIT License',
    #     'Operating System :: OS Independent',
    # ],
)
