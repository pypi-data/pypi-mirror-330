from setuptools import setup, find_packages

setup(
    name="MidoWebLib",
    version="0.1.3",
    author="Mohammed Ahmed Ghanam",
    author_email="mghanam883@outlook.com",
    description="A library for Mido Web Website",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://midoghanam2.pythonanywhere.com/",
    TelegramChannel = "https://t.me/mido_team",
    TelegramAccount = "https://t.me/midoghanam",
    Whatsapp = "https://wa.me/201101023681",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.6",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)