from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
      long_description = fh.read()

setup(
      name="Func3DCad",
      version="1.3.2",
      packages=["Func3DCad"],
      author="sergey.winston",
      author_email="sergey.winston@bk.ru",
      zip_safe=False,
      long_description=long_description,
      long_description_content_type="text/markdown",
      description="A Python library for parametric 3D modeling and CAD operations.",
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      readme="README.md",
)
