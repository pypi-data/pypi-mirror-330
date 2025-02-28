from setuptools import setup, find_packages

setup(
    name="heraldopy",
    version="1.0.0",
    author="Heraldo Almeida",
    author_email="heraldo.almeida@gmail.com",
    description="A set of automation tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/heraldopy",
    packages=find_packages(),
    install_requires=[
        "requests",
        "msal",
        "wget",
        "numpy",
        "pandas",
        "tk",
    ],
    license="MIT",  # ✅ Force correct license
    options={"metadata": {"license": "MIT"}},  # ✅ Force correct metadata
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
