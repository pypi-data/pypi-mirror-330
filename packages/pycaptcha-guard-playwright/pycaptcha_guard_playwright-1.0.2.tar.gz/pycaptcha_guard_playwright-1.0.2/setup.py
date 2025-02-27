from setuptools import setup, find_packages

setup(
    name="pycaptcha-guard-playwright",
    version="1.0.2",
    author="MurtazaA",
    description="Solve any kind of captcha like human",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "nopecha>=1.0.8",
        "playwright>=1.35",
        "pillow==10.1.0",
        "pyautogui==0.9.54",
        "capsolver>=1.0.7"
    ],
    python_requires=">=3.9",
    license_files=["LICENSE"]
)