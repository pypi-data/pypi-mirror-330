from setuptools import setup, find_packages

setup(
    name="captcha_solver_selenium", 
    version="0.1.7",
    author="DENO",
    author_email="Vinhytb3010@gmail.com",
    description="A package for solving Google reCAPTCHA using Selenium and Speech Recognition",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=["captcha_solver"],
    install_requires=[
        "selenium>=4.9.1",
        "selenium-wire>=5.0.0",
        "requests>=2.32.3",
        "SpeechRecognition",
        "pyaudio"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
