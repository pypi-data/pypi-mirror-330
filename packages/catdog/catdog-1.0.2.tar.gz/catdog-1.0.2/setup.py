from setuptools import setup, find_packages

setup(
    name="catdog",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        "torch",
        "torchvision",
        "Pillow",
    ],
    author="Julfy",
    author_email="bahdan.suchko@yandex.by",
    description="A simple library for cat and dog image classification",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/BogdanSuchko/catdog",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    package_data={
        'catdog': ['models/*.pth', '*.py'],
    },
) 