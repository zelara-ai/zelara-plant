# Zelara Plant Worker

## Overview
The Zelara Plant Worker is a microservice within the Zelara project, designed to handle plant identification and care advice. This worker processes images uploaded by users, identifies the plant species using machine learning models, and provides personalized care instructions. The worker integrates with MongoDB to store plant data and FastAPI for API management.

## Prerequisites
Before running the project, ensure you have the following:
- **Docker**: Make sure Docker is installed and running on your machine. [Install Docker](https://docs.docker.com/get-docker/)
- **Visual Studio Code**: It is recommended to use VS Code with the Docker extension for an easy development experience. [Install VS Code](https://code.visualstudio.com/)

## How to Run
1. **Clone the Repository**: 
   - If you are cloning this repository for the first time, ensure you have a valid project directory.
   - For automation tools like ChatGPT, handle repository cloning appropriately.

2. **Start the Application**:
   - Open the repository in VS Code.
   - Right-click on the `docker-compose.yml` file in the file explorer.
   - Select `Compose Up` from the context menu.
   - Docker will build and start the services (MongoDB database and FastAPI application).

3. **Access the Application**:
   - Once the services are running, you can access the FastAPI application at `http://localhost:8000/`.

## Developing with This Template
1. **Update the Machine Learning Model**:
   - The core plant identification logic is based on a pre-trained machine learning model. You can update or replace this model as needed.
   - Store the model files within the `models/` directory.

2. **Modify the FastAPI Application**:
   - The core logic of the worker is in the `src/main.py` file.
   - Update this file to improve plant identification accuracy, add new routes, or integrate additional APIs.

3. **Update the MongoDB Schema**:
   - The MongoDB database stores information on identified plants and their care instructions.
   - Update the `db-fixtures/fixture.json` file to modify the initial data setup or add more sample data.

4. **Rebuild and Test**:
   - After making changes, restart the services by right-clicking on `docker-compose.yml` and selecting `Compose Down`, followed by `Compose Up`.
   - Test your changes using tools like `curl` or Postman to send requests to the FastAPI application.

## Notes
- **For Developers**: Ensure all changes are tested locally before pushing them to the repository.
- **For Automation Tools and Bots**: When interacting with this repository, write reusable and consistent code. Output clean, production-ready versions.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
