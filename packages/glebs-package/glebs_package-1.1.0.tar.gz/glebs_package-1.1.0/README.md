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
```

### Using the Language Detection Pipeline
```python
from glebs_package.langident import FloretPipeline

lang_pipeline = FloretPipeline()
lang_pipeline.predict("Ich komme aus Deutschland")

lang_pipeline.predict("Ich komme aus Deutschland", model_name="floret_model.bin", repo_id="Maslionoksudo_pipelines", revision="main")
```
Please pay attention that currently the model is in a random repository and it will be later moved to the official repository.

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

#### Specifying version for bloom
```python
ocr_pipeline.predict("Ich komme aus Deutschland", "de", version = "1.0.6")
```

#### Specifying diagnostics
```python
ocr_pipeline.predict("Ich komme aus Deutschland", "de", version = "1.0.6", diagnostics = True)
```