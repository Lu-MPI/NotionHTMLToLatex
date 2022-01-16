import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noml",
    version="0.0.1",
    author="Lu",
    author_email="lu2github@gmail.com",
    description="(Early Dev)Convert Notion Export HTML To Latex",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lu-MPI/NotionHTMLToLatex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'noml = noml.main:main'
        ]
    },
)