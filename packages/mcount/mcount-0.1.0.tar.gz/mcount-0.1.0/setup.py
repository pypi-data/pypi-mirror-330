from setuptools import setup, find_packages

setup(
    name="mcount",  # Package name
    version="0.1.0",  # Initial version
    author="Abdur Rahman Ansari",
    author_email="theabdur10@gmail.com",
    description="A lightweight tool for counting metastatic cells in cancerous tissue samples",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/abd-ur/MTC_Count",  # GitHub repo link
    packages=find_packages(),  # Automatically find all packages
    install_requires=[
        "opencv-python",
        "numpy",
        "scipy"
    ],
    entry_points={
        "console_scripts": [
            "mcount=mtc.main:count",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
