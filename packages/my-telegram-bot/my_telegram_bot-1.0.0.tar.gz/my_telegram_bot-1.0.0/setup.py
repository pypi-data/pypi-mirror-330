from setuptools import setup, find_packages

setup(
    name="my_telegram_bot",
    version="1.0.0",
    author="iliya kaviyani",
    author_email="iliyakaviyani313@gmail.com",
    description="یک کتابخانه فوق سریع برای ربات تلگرام",    long_description_content_type="text/markdown",
    url="https://github.com/iliya8989/telegrampx",
    packages=find_packages(),
    install_requires=[
        "requests",
        "httpx"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
