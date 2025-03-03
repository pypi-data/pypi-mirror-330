from setuptools import setup, find_packages

setup(
    name="cosmotalker",
    version="1.1.0",
    author="Bhuvanesh M",
    author_email="bhuvaneshm.developer@gmail.com",
    description="CosmoTalker is your gateway to the universe! Whether you're fascinated by stars, planets, or scientific phenomena, this tool brings the cosmos closer to you.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bhuvanesh-m-dev/cosmotalker",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    project_urls={
        "Portfolio": "https://bhuvaneshm.in",
        "LinkedIn": "https://www.linkedin.com/in/bhuvaneshm-developer",
        "GitHub Repository": "https://github.com/bhuvanesh-m-dev",
    },
)
