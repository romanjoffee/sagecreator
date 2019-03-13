import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sagecreator",
    version="0.0.36",
    author="evoneutron",
    author_email="evoneutron@gmail.com",
    description="Package to provision and install architecture in AWS",
    long_description=long_description,
    long_description_content_type="text/x-rst; charset=UTF-8",
    packages=setuptools.find_packages(),
    url="https://github.com/evoneutron/sagecreator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=["ansible==2.7.2", "boto==2.49.0", "boto3==1.9.82", "botocore==1.12.82", "click==7.0"],
    entry_points={
        "console_scripts": [
            "sage=scripts.cli:cli"
        ]
    },
    include_package_data=True,
    package_dir={'sagebase': 'sagebase'},
    package_data={'sagebase': ['*']}
)
