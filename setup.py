from setuptools import setup, find_packages

setup(
    name="stingbot-ai",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["main"],
    include_package_data=True,
    install_requires=[
        "rich",
        "textual",
        "requests",
        "psutil",
        "flask",
        "flask-cors",
        "colorama",
        "docker",
        "pyautogui",
    ],
    entry_points={
        "console_scripts": [
            "stingbot=main:main",
        ],
    },
    author="subhadeep-sec",
    description="Generalist Neural Engine for Security & Productivity",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/subhadeep-sec/STINGBOT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.10",
)
