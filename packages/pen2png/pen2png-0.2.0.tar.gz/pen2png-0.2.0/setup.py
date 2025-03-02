from setuptools import setup, find_packages

setup(
    name="pen2png",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "Pillow",
        "pillow-heif",
    ],
    entry_points={
        "console_scripts": [
            "pen2png=pen2png.cli:main",
        ],
    },
    author="Henry Hamer",
    author_email="hhame4@gmail.com",
    description="A tool to convert pen drawings to transparent PNGs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hentity/pen2png",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
