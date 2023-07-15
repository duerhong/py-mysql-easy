from time import time
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="pysucculent",
    version="1.0.0",
    author="duer",
    author_email="1186969412@qq.com",
    description="mysql crud exends",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/duerhong/py-mysql-easy",
    project_urls={
        "Bug Tracker": "https://github.com/duerhong/py-mysql-easy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)