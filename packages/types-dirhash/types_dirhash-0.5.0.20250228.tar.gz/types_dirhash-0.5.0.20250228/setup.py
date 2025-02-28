from setuptools import setup

name = "types-dirhash"
description = "Typing stubs for dirhash"
long_description = '''
## Typing stubs for dirhash

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`dirhash`](https://github.com/andhus/dirhash-python) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `dirhash`. This version of
`types-dirhash` aims to provide accurate annotations for
`dirhash==0.5.*`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/dirhash`](https://github.com/python/typeshed/tree/main/stubs/dirhash)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`b0c6fffe287d4c0a923eeaaa1dd7caa02cba2c9e`](https://github.com/python/typeshed/commit/b0c6fffe287d4c0a923eeaaa1dd7caa02cba2c9e).
'''.lstrip()

setup(name=name,
      version="0.5.0.20250228",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/dirhash.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['dirhash-stubs'],
      package_data={'dirhash-stubs': ['__init__.pyi', 'cli.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
