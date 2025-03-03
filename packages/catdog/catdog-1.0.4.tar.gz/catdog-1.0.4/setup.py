from setuptools import setup, find_packages
import os

# Убедимся, что все файлы на месте
print("Files in catdog directory:")
print(os.listdir("catdog"))

setup(
    name="catdog",
    version="1.0.4",  # Увеличиваем версию
    packages=['catdog'],
    package_dir={'catdog': 'catdog'},
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
        'catdog': [
            'models/*.pth',
            'model.py',
            'classifier.py',
            '__init__.py',
            'version.py',
        ],
    },
    zip_safe=False,  # Важно для правильной установки
) 