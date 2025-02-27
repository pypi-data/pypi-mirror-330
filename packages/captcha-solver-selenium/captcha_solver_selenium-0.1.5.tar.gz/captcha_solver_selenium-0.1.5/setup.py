from setuptools import setup, find_packages

setup(
    name="captcha_solver_selenium", 
    version="0.1.5",
    author="DENO",
    author_email="your.email@example.com",
    description="A package for solving Google reCAPTCHA using Selenium and Speech Recognition",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=["captcha_solver"],
    install_requires=[
        "selenium",
        "selenium-wire",
        "requests",
        "speechrecognition",
        "pyaudio"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
