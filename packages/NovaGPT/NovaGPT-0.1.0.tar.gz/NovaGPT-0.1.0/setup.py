from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="NovaGPT",
    version="0.1.0",
    author="Mohamed Medjahdi",
    author_email="medjahdi.mohamed@outlook.com",
    description="A Python-based implementation of a conversational AI model designed to simulate a highly proficient, amoral programmer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/medjahdi/NovaGPT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "requests",
        "httpx",
        "PyYAML",
        "pynput",
        "pyaudio",
        "pygame",
        "ecapture",
        "mysql-connector-python",
        "sympy",
        "pyfiglet",
        "Pillow",
        "bleak",
        "beautifulsoup4",
        "pytube",
        "GoogleNews",
    ],
)