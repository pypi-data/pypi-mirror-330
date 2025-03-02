# Usage
A third-party RunPod GraphQL client in Python generated using Ariadne.
The author is not affiliated with RunPod. This package will be updated to match the API on a best effort basis.

# Development
To regenerate the package:
1) Install dev dependencies: `pip install -r pyproject.toml --extra dev` 
1) Fetch https://graphql-spec.runpod.io/ and convert it to markdown to reduce the size
2) Ask your favorite AI to convert it into a valid GraphQL schema `runpod.schema`
4) Run `ariadne-codegen`

# Deployment
This package uses GitHub Actions to automatically deploy to PyPI when a new release is created, using PyPI's trusted publishing feature.

To deploy a new version:
1. Update the version in `pyproject.toml`
2. Create a new release on GitHub with a tag matching the version (e.g., `v0.1.0`)
3. The GitHub Action will automatically build and publish the package to PyPI