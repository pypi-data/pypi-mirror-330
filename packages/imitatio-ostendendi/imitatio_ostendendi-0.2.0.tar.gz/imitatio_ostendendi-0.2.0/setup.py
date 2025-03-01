from setuptools import setup, find_packages

setup(
    name="imitatio_ostendendi",
    version="0.2.0",
    description="Mock widgets for tkinter/ttk testing (Latin: Display Imitation)",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Codeium Engineering Team",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: User Interfaces",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ]
)
