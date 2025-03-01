from setuptools import setup, find_packages

setup(
    name="attention_paper",
    version="0.1.1",  # Increment the version since PyPI doesn't allow re-uploads of the same version
    author="Raktim Kalita",
    author_email="raktmxx@gmail.com",
    description="Easily open the 'Attention Is All You Need' paper",
    url="https://github.com/Rktim/attention",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],  # No dependencies needed
    entry_points={
        "console_scripts": [
            "attention=attention_paper.open_paper:open_attention_paper",
        ],
    },
    package_data={
        "attention_paper": ["data/attentionalluneed.pdf"],  # Keeps local PDF support if available
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
