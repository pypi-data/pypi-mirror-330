from setuptools import find_packages, setup

setup(
    name="pruna-launch-party",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "colorama>=0.4.6",  # For colored terminal output
        "tqdm>=4.65.0",     # For progress bars
    ],
    author="Pruna Team",
    author_email="team@pruna.dev",
    description="A fun package celebrating Pruna's open-source launch!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pruna-ai/pruna",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "pruna-party=pruna_launch_party.cli:main",
        ],
    },
) 