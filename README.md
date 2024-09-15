# Zelara Plant Worker 

## Overview
The Zelara Plant Worker is a microservice within the Zelara project, designed to handle plant identification and care advice. Instead of building custom machine learning models, this worker leverages the **Kindwise SDK** for plant identification. By integrating with the Kindwise API, the worker can process images uploaded by users, identify plant species, and provide personalized care instructions. The worker also integrates with MongoDB to store plant data and uses FastAPI for API management.

## Prerequisites
Before running the project, ensure you have the following:
- **Docker**: Make sure Docker is installed and running on your machine. [Install Docker](https://docs.docker.com/get-docker/)
- **Visual Studio Code**: It is recommended to use VS Code with the Docker extension for an easy development experience. [Install VS Code](https://code.visualstudio.com/)
- **Kindwise API Key**: You will need an API key from [Kindwise Admin](https://admin.kindwise.com/) to use the SDK.

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
1. **Integrating the Kindwise SDK**:
   - The Kindwise SDK is already included as a submodule in this repository.
   - The worker uses this SDK to interact with the **Kindwise API** for plant identification. You can find more details about the SDK [here](https://github.com/flowerchecker/kindwise-api-client.git).
   - Modify the API integration in `src/main.py` to customize the plant identification process according to your needs.

2. **Modify the FastAPI Application**:
   - The core logic of the worker is in the `src/main.py` file.
   - Update this file to improve plant identification accuracy, add new routes, or integrate additional APIs.

3. **Update the MongoDB Schema**:
   - The MongoDB database stores information on identified plants and their care instructions.
   - Update the `db-fixtures/fixture.json` file to modify the initial data setup or add more sample data.

4. **Rebuild and Test**:
   - After making changes, restart the services by right-clicking on `docker-compose.yml` and selecting `Compose Down`, followed by `Compose Up`.
   - Test your changes using tools like `curl` or Postman to send requests to the FastAPI application.

## Production API Key Usage

In production, you need to provide the API key through the request headers using the `Authorization` header. Example:

- **Authorization Header**: `Bearer your_production_api_key_here`

For example, using Postman or cURL:

   ```
   Authorization: Bearer your_production_api_key_here
   ```

## API Documentation and Resources
- **KindWise Admin**: Access the KindWise admin portal for managing plant data. [KindWise Admin](https://admin.kindwise.com/)
- **KindWise Crop API**: Documentation for interacting with crop data and plant care information. [KindWise Crop API](https://crop.kindwise.com/docs)
- **Plant.id API**: Documentation for plant identification and related API services. [Plant.id API](https://plant.id/docs)

## Notes
- **For Developers**: Ensure all changes are tested locally before pushing them to the repository.
- **For Automation Tools and Bots**: When interacting with this repository, write reusable and consistent code. Output clean, production-ready versions.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
