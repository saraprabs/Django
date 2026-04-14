# Cloud-Integrated Employee Portal
#### Project Description
The Cloud-Integrated Employee Portal is a hybrid web application built with Django that streamlines the management of employee professional profiles. Unlike traditional applications that rely on a single database, this system utilizes a multi-cloud architecture. It separates core identity management (handled locally) from flexible, high-scale profile metadata (handled via Azure Cosmos DB) and binary assets (handled via Azure Blob Storage).

The portal allows employees to register, upload profile pictures, and provide external portfolio links, creating a centralized, scalable directory for the organization.

## Architecture
The system follows a Layered Service Architecture where the Django application acts as the orchestrator between local storage and cloud services.
**Components:**
- **Web Layer:** Django Views & Forms (Handles input and routing).

- **Service Layer:** Dedicated modules (cosmos_service.py, storage_service.py) that abstract the Azure SDK logic.

- **Identity Store (SQL):** SQLite manages the relational data for User authentication.

- **Profile Store (NoSQL):** Azure Cosmos DB stores JSON-based employee metadata.

- **Object Storage:** Azure Blob Storage hosts profile images to keep the database light.

## 📂 Project Structure
```
Django/
│
├── .env                    # Secret keys (Cosmos Key, Storage String)
├── .gitignore              # Files to ignore (e.g., .env, __pycache__, db.sqlite3)
├── manage.py               # Django management script
├── requirements.txt        # List of dependencies (django, azure-cosmos, etc.)
│
├── Employee_Portal/                 # Project Configuration Folder
│   ├── __init__.py
│   ├── settings.py         # Main project settings
│   ├── urls.py             # Main routing (includes employee_app.urls)
│   └── wsgi.py
│
└── employee_app/           # Main Application Folder
    ├── __init__.py
    ├── admin.py            # Local SQL Admin registration
    ├── apps.py
    ├── forms.py            # Django User and Profile forms
    ├── models.py           # SQL Models (User and UserProfileInfo)
    ├── urls.py             # App-specific routing
    ├── views.py            # View logic (The "Orchestrator")
    │
    ├── services/           # The Service Layer (Azure Integration)
    │   ├── __init__.py
    │   ├── cosmos_service.py   # CosmosService Class (create_item, get_items)
    │   └── storage_service.py  # Blob Storage logic (upload_profile_picture)
    │
    └── templates/
        └── employee_app/
            ├── base.html           # Shared layout
            ├── index.html          # Homepage
            ├── registration.html   # Enrollment form
            └── employee_list.html  # Directory (Fetching from Cosmos)
```

## Setup Instructions
**Prerequisites**
Python 3.10 or higher.

An active Azure Subscription.

Azure Cosmos DB account (SQL API) and a Storage Account.

#### Step 1: Clone and Environment Prep
Install the necessary SDKs and tools:
```bash
pip install django azure-cosmos azure-storage-blob python-dotenv
```
#### Step 2: Configure Credentials
Create a .env file in the root directory. Do not commit this file to version control.
```
# Azure Cosmos DB
COSMOS_ENDPOINT="https://<your-account>.documents.azure.com:443/"
COSMOS_KEY="<your-primary-key>"

# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=...<your-string>"
```
#### Step 3: Database Initialization
Apply Django migrations to set up the local SQL tables for user accounts:
```bash
python manage.py makemigrations
python manage.py migrate
```
**Step 4: Run the Application**
```bash
python manage.py runserver
```

## Technical Justification
#### Why a Hybrid (SQL + NoSQL) Approach?
Using a hybrid model provides the "best of both worlds." We use SQL for authentication because relational databases are built for the strict ACID compliance required for passwords and security. We use NoSQL (Cosmos DB) for profiles because employee data is often "sparse" and "unstructured"—some employees may have many social links, while others have none. Cosmos DB handles this variability without the need for empty table columns or complex migrations.

#### Scalability and Performance
The system is designed for Horizontal Scaling:

**Partitioning:** By using email as a Partition Key in Cosmos DB, data is distributed across multiple physical shards, ensuring the system doesn't slow down as the employee count grows.

**Asset Offloading:** By storing images in Blob Storage rather than the database, we reduce database load and cost. This allows the application to serve images via a Content Delivery Network (CDN) in the future.

#### Security & Maintainability
**Security:** Credentials are never hardcoded; they are injected via environment variables at runtime.

**Service Layer:** By wrapping Azure logic in a CosmosService class, the application becomes "Cloud Agnostic." If the organization decided to move to AWS, only the service layer would need to be updated—the core Django views would remain unchanged.

## 📝 Reflection

#### Why NoSQL (Cosmos DB)?
We chose NoSQL for profile metadata because it allows for a flexible schema. As employee profile requirements evolve (e.g., adding social media links or skills), we can update JSON documents without performing complex SQL migrations. Additionally, Cosmos DB provides Horizontal Scaling via Partition Keys (partitioned by email).

#### Scaling
The system scales by offloading heavy assets (images) to Blob Storage and utilizing a partitioned NoSQL database for metadata. This prevents the primary SQL database from becoming a bottleneck as the user base grows.