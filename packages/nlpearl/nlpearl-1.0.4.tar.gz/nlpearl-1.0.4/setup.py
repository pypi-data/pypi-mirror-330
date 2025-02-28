from setuptools import setup, find_packages
import pathlib

# Read the contents of your README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="nlpearl",  # Required

    version="1.0.4",  # Required, update this with each release

    description="A Python wrapper for the NLPearl API",  # Optional

    long_description=long_description,  # Optional, from README.md

    long_description_content_type="text/markdown",  # Optional (see note)

    author="nlpearl",  # Optional

    author_email="support@nlpearl.ai",  # Optional

    url="https://github.com/Samueleons/NLPearl-API",  # Add the GitHub repo here optional

    packages=find_packages(),  # Required

    install_requires=[
        'requests',
    ],  # Optional, add other dependencies if any

    license="BSD-3-Clause",  # Use the BSD 3-Clause License

    classifiers=[
        # Development Status
        "Development Status :: 4 - Beta",

        # Intended Audience
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",

        # Topic
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Telephony",
        "Topic :: Internet",

        # License
        "License :: OSI Approved :: BSD License",

        # Programming Language
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",

        # Operating System
        "Operating System :: OS Independent",

        # Natural Language
        "Natural Language :: English",
    ],# Optional

    keywords="nlpearl api wrapper client telephony automation python conversational-ai nlp call-handling", #optional


    python_requires='>=3.6, <4',  # Required, adjust as needed
    project_urls={  # Optional but recommended
        # 'Bug Reports': 'https://github.com/Samueleons/NLPearl-API/issues',
        'Source': 'https://github.com/Samueleons/NLPearl-API',
        'Documentation': 'https://developers.nlpearl.ai',  # Optional if you have docs
        'Homepage': 'https://www.nlpearl.ai',  # Optional
    },
)

