from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LemX",
    version="0.1.7",
    packages=find_packages(),
    install_requires=["python-Levenshtein"],
    description="A Banglish lemmatizer and word corrector using Levenshtein Distance Developped By Pronoy Kumar Mondal & Sadman Sadik Khan Under the supervision of Md. Sadekur Rahman In colaboration with DIU NLP & ML Research Lab.",
    long_description=long_description,  # Ensure this is set
    long_description_content_type="text/markdown",  # Ensure this is set
    author="Pronoy Kumar Mondal",
    author_email="pronoy15-14744@diu.edu.bd",
    url="https://github.com/yourusername/LemX",  # Update with your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={"lemx": ["dictionary.csv"]},
    python_requires=">=3.6",
)