from setuptools import setup, find_packages

setup(
    name="somali_number_converter",  # Name of the package
    version="0.0.1",  # Version number
    packages=find_packages(),  # Find all packages in the current directory
    install_requires=[  # List your dependencies
        "pdfplumber",
    ],
    description="A package to convert numbers in PDFs to Somali words.",
    long_description=open('README.md').read(),  # Read from README.md
    long_description_content_type='text/markdown',  # Content type for the long description
    author="ABDOL",  # Your name
    author_email="abdoldevtra@gmail.com",  # Your email
    url="https://github.com/abdoltd/somali_number_converter",  # Link to GitHub repo
    # classifiers=[  # Classifiers help users find your package
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
)
