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
   python3 -m venv env
   ```

3. Activate the virtual environment. 
   For macOS:
   ```
   source env/bin/activate
   ```
   For Windows (using Command Prompt):
   ```
   env\Scripts\activate
   ```

4. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Start the API Gateway:

    ```
    uvicorn server_api:app --host localhost --port 5000
    ```

2. Navigate to the frontend application URL (starlite_fe) to start using!~
