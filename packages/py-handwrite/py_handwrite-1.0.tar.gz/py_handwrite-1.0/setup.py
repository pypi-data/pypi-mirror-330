from setuptools import find_packages, setup


setup(
    name="py_handwrite",
    packages=find_packages(),
    version="1.0",
    description="Convert Text to HandWritten Image",
    author="Jenil sheth",
    author_email="shethjeniljigneshbhai@gmail.com",
    install_requires=["pillow"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={
        "py_handwrite": ["images/*.png"],
    }
)
