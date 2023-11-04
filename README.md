# starlite
A project aimed to help student's course planning!

## Table of Contents
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)

## Repository Structure
- `starlite_be/`: Contains all the frontend code built with React
- `starlite_fe/`: Holds all the backend code, including the API Gateway and the main Backend service
    
Each of these folders has its own README file to describe in detail how to setup and run their individual components.

## Getting Started

Here's a quick guide to navigate through the different parts of the project and run it on your local machine:

1. **Clone the repository**
   Use the following command to clone this repository:
    ```
    https://github.com/xlatios1/starlite.git

    ```

2. **Clone the submodule starlite_fe**
   Use the following command to clone this repository:
    ```
    git submodule init
    git submodule update
    ```

3. **Navigate to the individual components** 
   
    As described above, each major component has its own directory. Visit each of them for specific instructions on how to get started with that component:

    - Frontend: `starlite_fe/`
    - Backend: `starlite_be/`
    
    Each directory contains a README file with specific instructions on setting up the respective component. Be sure to follow these        instructions to ensure a successful setup.

After each component has been set up following the steps above, an easy way to start up all required environments would be to modify and run .vscode/tasks.json (ctrl-shift-b) to start up all environments required.

<em>Project done by: Woon Yi Jun