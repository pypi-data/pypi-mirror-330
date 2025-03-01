from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rajniwebdeveloper",
    version="0.1.2",
    author="Rajni Web Developer",
    author_email="rajnikantmahato33435@gmail.com",
    description="All tools From Rajni web developer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rajniwebdeveloper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'flask>=2.0.0',
        'selenium>=4.0.0',
        'webdriver_manager>=3.8.0',
        'pandas>=1.3.0',
        'openpyxl>=3.0.0',
        'requests>=2.26.0'
    ],
    python_requires='>=3.7',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'court-challan=rajniwebdeveloper.court_challan.flaskg:main',
        ],
    }
)
