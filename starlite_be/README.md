# Starlite Backend

Starlite Backend holds the algorithm used to support the platform. <WIP>

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Microservices](#microservices)

## Prerequisites
- Python 3.11
- pip (Python package installer)

## Installation

1. Navigate to the server directory:
    ```
    cd .\starlite_be\
    ```

2. Create a new virtual environment in the cloned directory. 
   ```
   conda create -n starlite_env
   ```

3. Activate the virtual environment. 
   ```
   conda activate starlite_env
   ```

4. Install the required dependencies:

    ```
    conda env update --file environment.yml --prune
    ```

## Usage

1. Start the API Gateway:

    ```
    uvicorn server_api:app --host localhost --port 5000
    ```