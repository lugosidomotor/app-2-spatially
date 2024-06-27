from flask import Flask
import os
import base64
from kubernetes import client, config
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

def get_kubernetes_secret(secret_name, key_name, namespace='default'):
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    try:
        secret = v1.read_namespaced_secret(secret_name, namespace)
        if key_name in secret.data:
            return secret.data[key_name]
        else:
            raise KeyError(f"Key '{key_name}' not found in secret '{secret_name}'")
    except Exception as e:
        print(f"Error accessing secret {secret_name}: {e}")
        raise

def decode_base64_twice(encoded_value):
    try:
        first_decode = base64.b64decode(encoded_value)
        second_decode = base64.b64decode(first_decode)
        return second_decode.decode('utf-8')
    except Exception as e:
        print(f"Error decoding base64 value: {e}")
        raise

def get_keyvault_secret(vault_address, secret_name):
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_address, credential=credential)
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        print(f"Error accessing key vault: {e}")
        raise

def write_to_storage(account_name, account_key, container_name, blob_name, data):
    try:
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)

        # Create the container if it does not exist
        container_client.create_container()

        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(data, overwrite=True)
        print("Data written to storage successfully.")
    except Exception as e:
        print(f"Error writing to storage: {e}")
        raise

def initialize_storage():
    try:
        encoded_vault_address = get_kubernetes_secret("keyvault-address", "address")
        print(f"Encoded vault address: {encoded_vault_address}")
        vault_address = decode_base64_twice(encoded_vault_address)
        print(f"Decoded vault address: {vault_address}")

        storage_account_name = get_keyvault_secret(vault_address, "storage-account-name")
        storage_account_key = get_keyvault_secret(vault_address, "storage-account-key")
        print(f"Storage account name: {storage_account_name}")
        print(f"Storage account key: {storage_account_key}")

        with open("data.txt", "r") as file:
            content = file.read()

        write_to_storage(storage_account_name, storage_account_key, "data", "data.txt", content)
    except Exception as e:
        print(f"Error: {str(e)}")

@app.route("/")
def hello_world():
    try:
        with open("data.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        content = "Data file not found."

    return f"<h1>app-2-spatially</h1><p>{content}</p>"

if __name__ == "__main__":
    initialize_storage()
    app.run(host='0.0.0.0', port=8080, debug=True)
