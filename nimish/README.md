# Candidate Data One-time Processing

This Python script retrieves candidate data from a CosmosDB database. It encompasses features for summarizing candidate information, creating vectors, and storing them in Azure AI Search. Additionally, it logs detailed processing information, including token usage.

## Overview

The script establishes a connection with a CosmosDB database to retrieve candidate data. Leveraging GPT-3.5 Turbo, it extracts summaries of candidate profiles and generates vector embeddings using the Azure OpenAI model 'text-embedding-ada-002'. The processed data is subsequently posted and stored in an Azure AI Search index. Additionally, the script integrates seamlessly with Azure Application Insights to log detailed information on candidate processing, token usage, and any encountered exceptions

## Project Structure
<p class="has-line-data" data-line-start="0" data-line-end="5">.<br>
├── dockerfile                # Dockerfile for containerization<br>
├── bolt_fullload_candidates.py  # Python script for candidate data processing<br>
├── .env                      # Environment variables configuration file<br>
└── requirements.txt          # Dependencies version details</p>


## Setup

1. Clone the repository.
2. Ensure you have podman installed on your system.
3. Create a `.env` file with the necessary environment variables (see Configuration section).
4. Build the Docker image using the provided Dockerfile.
5. Run the podman container.

## Usage

To use the script:

1. Ensure the MongoDB database is running and accessible.
2. Configure the environment variables in the `.env` file.
3. Execute the Python script.

## Configuration

The `.env` file contains the following configuration variables:

- `OPENAI_API_KEY`: API key for accessing OpenAI services.
- `AZURE_OPENAI_API_BASE`: Base URL for Azure OpenAI API.
- `AZURE_OPENAI_API_VERSION`: Version of Azure OpenAI API.
- `NUM_CANDIDATES`: Number of candidates to process.
- `DATABASE_NAME`: Name of the MongoDB database.
- `COLLECTION_NAME`: Name of the MongoDB collection.
- `VECTOR_NAME`: Name of the Azure AI Search index.
- `BASE_URI`: Base URI for Azure services.
- `API_KEY`: API key for accessing Azure Open AI services.
- `APP_INSIGHTS_CONNECTION_STRING`: Connection string for Application Insights.
- `COSMOSDB_CONNECTION_STRING`: Connection string for Cosmos DB (MongoDB API).

## Dependencies

- pymongo
- dotenv
- openai
- requests
- opencensus-ext-azure
