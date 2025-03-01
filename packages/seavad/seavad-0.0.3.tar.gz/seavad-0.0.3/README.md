# SeaVAD

VAD module wrapping Silero with a state machine.

### How to publish this package

#### Prerequisite
1. pip install build twine

#### publish a version
1. change version in `pyproject.toml`
2. cp .pypirc.example .pypirc
3. set up token in .pypirc `password`, e.g. `pypi-...`
4. source publish_package.sh
