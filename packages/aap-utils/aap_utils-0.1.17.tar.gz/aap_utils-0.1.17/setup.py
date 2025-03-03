from setuptools import setup, find_packages

setup(
    name="aap_utils",  # The name of your library
    version="0.1.17",
    description="A Python library for registering an IP address for AAP",
    author="Minh Dang",
    author_email="danghoangminh86@gmail.com",
    packages=find_packages(),  # Auto-find packages in the directory
    install_requires=[
        "requests",  # Any external dependencies (e.g., 'requests')        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
