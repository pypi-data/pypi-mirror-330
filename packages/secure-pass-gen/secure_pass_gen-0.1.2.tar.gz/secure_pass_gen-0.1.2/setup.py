from setuptools import setup, find_packages

setup(
    name="secure_pass_gen",
    version="0.1.2",
    author="NIL MAKVANA",
    author_email="neel327.rejoice@gmail.com",
    description="A simple Python package to generate strong passwords.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NIL327/password_generator",  # Update with your GitHub repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)


