import setuptools

import vkdev


with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

with open("requirements.txt", "r") as req_file:
    dependeces = [
        pack for pack in req_file.read().split('\n')
    ]

setuptools.setup(
    name="vkdev",
    version=vkdev.__version__,
    author="Yan",
    author_email="deknowny@gmail.com",
    description="Create your VK bot quickly and easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rhinik/vkdev",
    packages=setuptools.find_packages(),
    install_requires=dependeces,
    python_requires='>=3.8',
)
