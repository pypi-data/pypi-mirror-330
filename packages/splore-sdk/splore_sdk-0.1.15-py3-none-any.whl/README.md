# Splore Python SDK  

The Splore Python SDK simplifies the process of interacting with the Splore document processing platform. Use it to upload files, process documents, and retrieve extracted data with minimal setup.

---

## 📌 Table of Contents  

- [Features](#features)  
- [Installation](#installation)  
- [Getting Started](#getting-started)  
- [Modules Overview](#modules-overview)  
  - [Agent Management](#agent-management)  
  - [Extractions](#extractions)  
  - [File Upload](#file-upload)  
  - [AWS Integration](#aws-integration)  
- [Advanced Usage](#advanced-usage)  
- [FAQ](#faq)  
- [Support](#support)  
- [License](#license)  

---

## 🚀 Features  

- **Agent Management**: Create, update, retrieve, and delete agents.  
- **File Upload**: Upload documents for processing.  
- **Extractions**: Extract structured data from documents.  
- **AWS S3 Integration**: Process files directly from S3.  
- **Task Monitoring**: Track the progress of extraction jobs.  
- **Error Handling**: Provides meaningful errors and retry mechanisms.  

---

## 📥 Installation  

Install the SDK via pip:  

```bash
pip install splore-sdk
```

For optional example dependencies:  

```bash
pip install splore-sdk[examples]
```

---

## 🏁 Getting Started  

### Prerequisites  

1. **API Key and Base ID**: Obtain these from the Splore console.  
2. **Python 3.9+**: Ensure Python is installed.  

### Quick Start Example  

```python
from splore_sdk import SploreSDK
from time import sleep

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Get all agents
agents = sdk.agents.get_agents()
agent_id = agents[0]["id"]  # Adjust as needed

# Initialize agent
extraction_agent = sdk.init_agent(agent_id=agent_id)

# use unix based file path.
upload_response = extraction_agent.file_uploader.upload_file(file_path="path/to/file.pdf")

file_id = upload_response.get("fileId")
print("File uploaded with ID:", file_id)

# Start extraction
extraction_agent.extractions.start(file_id=file_id)

# Monitor extraction status
while True:
    status = extraction_agent.extractions.processing_status(file_id=file_id)
    if status.get("fileProcessingStatus") == "COMPLETED":
        break
    sleep(10)  # Wait before checking again

# Retrieve extracted data
extracted_data = extraction_agent.extractions.extracted_response(file_id=file_id)
print("Extracted Data:", extracted_data)
```

---

## 📦 Modules Overview  

### 🔹 [Agent Management](#agent-management)  

Manage agents for document processing.  

#### Example Usage  

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Create an agent
agent_payload = {"name": "Test Agent", "config": {"key": "value"}}
create_response = sdk.create_agent(agent_payload)
print("Create Agent Response:", create_response)

# Get agent details
agent_id = create_response.get("id")
get_response = sdk.agents.get_agents(agentId=agent_id)
print("Get Agent Response:", get_response)

# Get all agents
all_agents = sdk.agents.get_agents()
print("All Agents:", all_agents)

# Update the agent
update_payload = {"name": "Updated Agent Name"}
update_response = sdk.agents.update_agent(agent_payload=update_payload)
print("Update Agent Response:", update_response)

# Delete the agent
delete_response = sdk.agents.delete_agents(agentId=agent_id)
print("Delete Agent Response:", delete_response)
```

---

### 🔹 [Extractions](#extractions)  

Handle document processing and extraction.  

#### Example Usage  

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Initialize Agent for extraction
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")

# Basic extraction flow
extracted_response = extraction_agent.extract(file_path="absolute_file_path")
print(extracted_response)

# advanced extraction flow

# Upload file
with open("sample.pdf", "rb") as file:
    file_response = extraction_agent.file_uploader.upload_file(file)

# store file ids for next steps
file_id = file_response.get("fileId")
print("File uploaded with ID:", file_id)

# Start extraction
start_response = extraction_agent.extractions.start(file_id=file_id)
print("Extraction started:", start_response)

# Check processing status and look for status_response is COMPLETED.
status_response = extraction_agent.extractions.processing_status(file_id=file_id)
print("Processing status:", status_response)

# Get extracted response once status is COMPLETED
extracted_data = extraction_agent.extractions.extracted_response(file_id=file_id)
print("Extracted Data:", extracted_data)
```

---

### 🔹 [File Upload](#file-upload)  

Upload files to Splore for processing.  

#### Example Usage
- example-1: Open and upload file for extraction

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# use unix based file path.
with open("path/to/your/file.pdf", "rb") as file:
    response = sdk.file_uploader.upload_file(file_stream=file)
    print("Upload Response:", response)
```
- example-2: Open and upload file for normal extraction

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

metadata = {
    "file_name": "your_file_name", # it will be saved as 
    "customeExtractionEnabled": "false", # it will be uploaded for normal extraction
}
# use unix based file path.
with open("path/to/your/file.pdf", "rb") as file:
    response = sdk.file_uploader.upload_file(file_stream=file, metadata=metadata)
    print("Upload Response:", response)
```

- example-3: Open and upload file for other than data points.

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")
metadata = {
    "file_name": "your_file_name", # it will be saved as 
    "customeExtractionEnabled": "false",
    "isDataFile": "false",  # it will be uploaded as normal file. can't be used for extraction.
}
# use unix based file path.
with open("path/to/your/file.pdf", "rb") as file:
    response = sdk.file_uploader.upload_file(file_stream=file, metadata=metadata)
    print("Upload Response:", response)

```

---

### 🔹 [AWS Integration](#aws-integration)  

Download files from AWS S3 for extraction.  

#### Example Usage  

```python
from splore_sdk import SploreSDK
from examples.aws import download_from_s3

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Initialize extraction agent
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")

# Create a temporary file destination
file_ref = sdk.file_uploader.create_temp_file_destination(file_extension=".pdf")
s3_uri = "s3://abc/def/abc.pdf"

# Download file from S3
download_from_s3(s3_uri, file_ref)

# Start extraction
response = extraction_agent.extract(file_path=file_ref)
print(response)
```

---

## ⚙️ Advanced Usage  

### 🔸 Polling Interval Configuration  

Customize the polling interval for extraction status checks.  

```python
while True:
    status = sdk.extractions.processing_status(file_id=file_id)
    if status.get("fileProcessingStatus") == "COMPLETED":
        break
    sleep(5)  # Set custom polling interval
```

---

### 🔸 Error Handling  

Handle errors gracefully for better debugging.  

```python
try:
    sdk.extractions.upload_file("path/to/file.pdf")
except Exception as e:
    print("Error uploading file:", str(e))
```

---

## ❓ FAQ  

### 1️⃣ How do I get an API Key?  
Sign up on the Splore console and navigate to the API section to generate a key.  

### 2️⃣ Can I use this SDK asynchronously?  
Asynchronous support will be added in a future release.  

### 3️⃣ Which file formats are supported?  
Currently, only **PDF files** are supported.  

---

## 🔗 Support  

For any questions or issues, please:  

- Open a ticket on [GitHub Issues](https://github.com/splorehq/splore-sdk-py/issues)  
- Email us at **support@splore.com**  

---

## 📜 License  

This SDK is licensed under the MIT License. See [LICENSE](LICENSE) for details.  
