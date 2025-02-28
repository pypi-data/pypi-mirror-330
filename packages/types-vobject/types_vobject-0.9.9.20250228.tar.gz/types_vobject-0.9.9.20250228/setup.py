from setuptools import setup

name = "types-vobject"
description = "Typing stubs for vobject"
long_description = '''
## Typing stubs for vobject

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`vobject`](https://github.com/py-vobject/vobject) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
[Pyre](https://pyre-check.org/),
PyCharm, etc. to check code that uses `vobject`. This version of
`types-vobject` aims to provide accurate annotations for
`vobject~=0.9.9`.

This package is part of the [typeshed project](https://github.com/python/typeshed).
All fixes for types and metadata should be contributed there.
See [the README](https://github.com/python/typeshed/blob/main/README.md)
for more details. The source for this package can be found in the
[`stubs/vobject`](https://github.com/python/typeshed/tree/main/stubs/vobject)
directory.

This package was tested with
mypy 1.15.0,
pyright 1.1.389,
and pytype 2024.10.11.
It was generated from typeshed commit
[`b0c6fffe287d4c0a923eeaaa1dd7caa02cba2c9e`](https://github.com/python/typeshed/commit/b0c6fffe287d4c0a923eeaaa1dd7caa02cba2c9e).
'''.lstrip()

setup(name=name,
      version="0.9.9.20250228",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/vobject.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['vobject-stubs'],
      package_data={'vobject-stubs': ['__init__.pyi', 'base.pyi', 'behavior.pyi', 'change_tz.pyi', 'hcalendar.pyi', 'icalendar.pyi', 'ics_diff.pyi', 'vcard.pyi', 'win32tz.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.9",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
