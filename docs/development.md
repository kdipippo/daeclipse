# Development

## Python-Related Code Development

### Overview
There are 2 different components of the Python work in this repo:
- `daeclipse` - The Python package that conveniently wraps around DeviantArt Eclipse API Calls.
- `cli.py` - A CLI script to make calls to API behavior. Functions called by the CLI are kept in the [daeclipsecli folder](https://github.com/Pepper-Wood/daeclipse/tree/main/daeclipsecli).

`poetry` is used for Python dependency management and packaging, specifically for the `daeclipse` project. The CLI is a handy add-on for local testing.

### Development
To get started, make sure to install poetry dependencies at the root.

```
poetry install
```

### Testing
There are no tests for any of the above written code yet.

### Linting
Code for all of the above follows the [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide) guidelines. This is also automatically checked via the GitHub Actions workflow [linter-python.yml](https://github.com/Pepper-Wood/daeclipse/blob/main/.github/workflows/linter-python.yml).

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
Courtesy of the boilerplate repo, the OpenAPI Spec is linted using [Spectral](https://github.com/stoplightio/spectral). This is also automatically checked via the GitHub Actions workflow [linter-openapi.yml](https://github.com/Pepper-Wood/daeclipse/blob/main/.github/workflows/linter-openapi.yml).

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
