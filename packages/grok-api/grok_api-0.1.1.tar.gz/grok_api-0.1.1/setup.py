import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="grok-api",
    version="0.1.1",
    author="K",
    author_email="109984658+savasoglu@users.noreply.github.com",
    description="A simple Python wrapper for interacting with the unofficial Grok API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/savasoglu/grok-api",
    py_modules=["grok_api"],
    install_requires=["requests", "curl_cffi"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
