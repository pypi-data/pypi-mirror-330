from setuptools import setup, find_packages

setup(
    name="glebs_package",
    version="1.0.6",
    packages=find_packages(),
    install_requires=[
      "cython",
      "pybloomfiltermmap3",
      "huggingface_hub",
      "floret"
    ],  
    python_requires=">=3.7",
)
