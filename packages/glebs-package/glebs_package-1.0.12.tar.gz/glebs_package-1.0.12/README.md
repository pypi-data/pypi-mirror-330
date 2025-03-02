# Glebs Package

## How to Upload the Package to PyPI

### Install the Required Packages
```sh
pip install setuptools wheel twine
```

### Build the Package
```sh
python setup.py sdist bdist_wheel
```

### Upload the Package
```sh
twine upload dist/*
```

---

## How to Use Glebs Package

### Installation
```sh
pip install glebs_package
pip install cython pybloomfiltermmap3 huggingface_hub
pip install floret
```

### Using the Language Detection Pipeline
```python
from glebs_package.langident import FloretPipeline

lang_pipeline = FloretPipeline()
lang_pipeline.predict("Ich komme aus Deutschland")
```

### Using the QA Score Model
```python
from glebs_package.ocrqa import OCRPipeline

ocr_pipeline = OCRPipeline()
ocr_pipeline.predict("Ich komme aus Deutschland")
```

#### Specifying a Language
```python
ocr_pipeline.predict("Ich komme aus Deutschland", "de")
```

