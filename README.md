# 🔗 Related Repos
https://github.com/lugosidomotor/infra-spatially

https://github.com/lugosidomotor/app-1-spatially


# 💻 app-2-spatially

## Overview

This Flask-based web application securely retrieves configuration from Kubernetes and Azure Key Vault, reads data from a local file, stores it in Azure Blob Storage, and displays it on a web page, demonstrating a cloud-native approach to data handling and web serving.

## Application Flow

1. Start the application
2. Initialize storage:
3. Retrieve encoded Key Vault address from Kubernetes secret
4. Retrieve storage account name and key from Key Vault
5. Read data from local 'data.txt' file
6. Write data to Azure Blob Storage
7. Start Flask web server
8. Display data on webpage

# 🔄 Continuous Integration (CI) Workflow

This README describes the CI workflow defined in the GitHub Actions YAML file.

## Overview

This CI workflow automates the process of building, tagging, and pushing Docker images, as well as updating Kubernetes configuration files with the new image tag. It can be triggered manually for specific environments or automatically on pushes to the main branch.

## Trigger Events

1. Manual trigger (`workflow_dispatch`) with environment selection:
   - Options: dev, qa, prod
   - Default: dev

2. Automatic trigger on push to the `main` branch

## Workflow Steps

1. **Checkout Repository**: Fetches the latest code from the repository.

2. **Docker Hub Login**: Authenticates with Docker Hub using provided credentials.

3. **Generate Short SHA**: Creates a short version of the Git commit SHA for tagging.

4. **Determine Environment File**: Selects the appropriate environment file based on the trigger event.

5. **Build and Push Docker Image**: 
   - Builds a Docker image using the Dockerfile in the root directory.
   - Tags the image with the short SHA.
   - Pushes the image to Docker Hub.

6. **Update Kubernetes Resources**:
   - Updates the specified environment YAML file in the `config` directory.
   - Replaces the old image tag with the new one (short SHA).

7. **Commit Changes**: Commits the updated Kubernetes configuration file.

8. **Push Changes**: Pushes the committed changes back to the repository.

## Environment Variables and Secrets

The workflow uses the following secrets:
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_TOKEN`: Docker Hub access token
- `DOCKER_REPO`: Docker repository name
- `GITHUB_TOKEN`: Automatically provided by GitHub for authentication

## File Structure

The workflow assumes the following file structure:
- Dockerfile in the root directory
- Environment-specific YAML files in subdirectories (e.g., `./dev/dev.yml`)
- Kubernetes configuration files in the `config` directory

## Usage

- For manual triggers, select the desired environment from the workflow dispatch menu.
- For automatic triggers, simply push to the `main` branch.

The workflow will build the Docker image, push it to Docker Hub, update the relevant Kubernetes configuration file, and commit the changes back to the repository.
