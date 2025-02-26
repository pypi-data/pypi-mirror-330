from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="en2th-transliterator",
    version="0.1.0",
    author="Thodsaporn Chay-intr",
    author_email="t.chayintr@gmail.com",
    description=
    "A Python package for transliterating English text to Thai using a ByT5 model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tchayintr/en2th-transliterator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.6",
    install_requires=[
        "transformers>=4.0.0",
        "torch>=1.7.0",
        "numpy>=1.19.0",
        "sentencepiece>=0.1.95",  # Required for ByT5 tokenizer
        "tqdm>=4.50.0",  # For progress bars
        # Add other dependencies
    ],
    entry_points={
        "console_scripts": [
            "en2th-transliterate=en2th_transliterator.cli:main",
        ],
    },
    include_package_data=True,
)
