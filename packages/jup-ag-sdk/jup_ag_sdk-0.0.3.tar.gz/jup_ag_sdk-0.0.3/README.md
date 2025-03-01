# **Jup-Ag-SDK**

A Python SDK for interacting with Jupiter Exchange APIs.

## **Installation**
To install the SDK globally from PyPI, run:
```sh
pip install jup-ag-sdk
```

## **Local Development**
If you want to make changes to the SDK and test it locally:

1. In this project's directory, install the package in editable mode by running:
   ```sh
   pip install -e .
   ```

2. To use this library in another project while making changes to it, install the package from its local path in that project:
   ```sh
   pip install -e /path/to/jup-ag-sdk
   ```

   Replace `/path/to/jup-ag-sdk` with the absolute or relative path to this project directory.

By installing in editable mode, any changes you make to the SDK will immediately reflect in your tests without needing to reinstall the package.

## **Making a New Release**
To create and publish a new release of the package to PyPI:

1. **Update the Version:**
   - Update the version in your `pyproject.toml` file following [semantic versioning](https://semver.org/), e.g., `0.0.1` → `0.1.0` for a minor update.

2. **Commit the Changes:**
   - Commit and push the version update to the main branch:
     ```sh
     git add pyproject.toml
     git commit -m "Bump version to vX.Y.Z"
     git push origin main
     ```

3. **Create a Tag:**
   - Tag the commit with the new version:
     ```sh
     git tag vX.Y.Z
     git push origin vX.Y.Z
     ```

   Replace `vX.Y.Z` with the actual version number.

4. **GitHub Actions Workflow:**
   - When the tag is pushed, the `release.yml` GitHub Actions workflow will automatically:
      - Build the package using Poetry.
      - Publish the package to PyPI.

5. **Confirm the Release:**
   - Check [PyPI](https://pypi.org/project/jup-ag-sdk/) to ensure the new version has been published successfully.

## **Disclaimer**
🚨 **This project is a work in progress and should not be used in production systems.**  
Expect breaking changes as the SDK evolves.