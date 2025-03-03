from setuptools import setup, find_packages

setup(
    name="gladify",
    version="0.1.4",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "gladify.GladUI.assets": ["GladUI.ico"],  # Correct path
    },
    install_requires=[],
    author="Navthej",
    author_email="gladgamingstudio@gmail.com",
    description="A Python package for various utilities",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)