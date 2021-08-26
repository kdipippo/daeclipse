# Development

## Python-Related Code Development

### Overview
The `/daeclipse` folder contains the contents of the `daeclipse` Python package. The purpose of the package is to conveniently wrap DeviantArt Eclipse API calls, similar to an SDK. `poetry` is used for Python dependency management and packaging.

### Development
To get started, make sure to install poetry dependencies at the root.

```
poetry install
```

### Testing
`pytest` is used for unit testing, with all code written in the `tests/` directory. All coverage reports are sent to `codecov`. This is also automatically checked and sent via the GitHub Actions workflow [test-python.yml](https://github.com/Pepper-Wood/daeclipse/blob/main/.github/workflows/test-python.yml).

To run tests locally:
```
poetry run pytest test
```

To run tests locally with a coverage report returned in the terminal:
```
poetry run pytest --cov=daeclipse test
```

To run tests locally with a coverage report returned as xml:
```
poetry run pytest --cov=daeclipse --cov-report=xml test
```

### Linting
Code for all of the above follows the [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide) guidelines. This is also automatically checked via the GitHub Actions workflow [lint-python.yml](https://github.com/Pepper-Wood/daeclipse/blob/main/.github/workflows/lint-python.yml).

Linting can be run locally via the below command at root, although the local linter is more restrictive than the GitHug Actiions linter:

```
flake8
```

### Documentation
`pdoc` is used for automated Python documentation generation. All documentation is generated on the `main` branch into a `build/python/` folder, which is then deployed to the `gh-pages` branch via the GitHub Actions workflow [gh-pages.yml](https://github.com/Pepper-Wood/daeclipse/blob/main/.github/workflows/gh-pages.yml).

### Publishing
The GitHub Actions workflow [pypi.yml](https://github.com/Pepper-Wood/daeclipse/blob/main/.github/workflows/pypi.yml) uses `JRubics/poetry-publish` to publish the `daeclipse` folder contents to pypi.org. Releases are published after a release is tagged on GitHub, formatted as `v*.*.*`.

## OpenAPI Spec Development

### Overview
The `/spec` folder contains the modularized OpenAPI spec to document how the DeviantArt Eclipse API behaves. Implementation is based on [dgarcia360/openapi-boilerplate](https://github.com/dgarcia360/openapi-boilerplate).

### Development
To get started, make sure to install node dependencies at the root.

```
npm install
```

The below command bundles the spec as one ``.yaml`` file.

```
npm run build
```

The minified document is stored in ``_build/api/openapi.yaml``.

### Testing
The below command checks if the document follows the OpenAPI 3.0 Specification.

```
npm run test
```

The below command builds a docs site so that you can view the rendering on your local browser.

```
npm run preview
```

The server starts on http://127.0.0.1:8080

You can optionally also generate the HTML and view `index.html`.

```
npm run html
```

### Linting
Courtesy of the boilerplate repo, the OpenAPI Spec is linted using [Spectral](https://github.com/stoplightio/spectral). This is also automatically checked via the GitHub Actions workflow [lint-openapi.yml](https://github.com/Pepper-Wood/daeclipse/blob/main/.github/workflows/lint-openapi.yml).

OpenAPI linting can also be performed locally by running the below command to check if the document follows the OpenAPI 3.0 Specification.

```
npm run test
```

### Documentation
`redoc` is used for automated OpenAPI documentation generation, courtesy of the boilerplate. All documentation is generated on the `main` branch into a `build/api/` folder, which is then deployed to the `gh-pages` branch via the GitHub Actions workflow [gh-pages.yml](https://github.com/Pepper-Wood/daeclipse/blob/main/.github/workflows/gh-pages.yml).

### Publishing
The OpenAPI ReDoc documentation is deployed to the `gh-pages` branch via the GitHub Actions workflow [gh-pages.yml](https://github.com/Pepper-Wood/daeclipse/blob/main/.github/workflows/gh-pages.yml).

## Docs

### Overview
The documentation that links to the separate specific documentation is stored as Markdown files in `docs/`. `mkdocs` takes the contents and formats as a helpful documentation site via GitHub Pages and  the GitHub Actions workflow [gh-pages.yml](https://github.com/Pepper-Wood/daeclipse/blob/main/.github/workflows/gh-pages.yml).

### Testing
To preview the `docs/` folder as the HTML site locally:

```
mkdocs build
```

The command will generate a `build/` folder containing the website contents.


### Publishing
The full documentation is deployed to the `gh-pages` branch via the GitHub Actions workflow [gh-pages.yml](https://github.com/Pepper-Wood/daeclipse/blob/main/.github/workflows/gh-pages.yml).
