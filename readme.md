# URL Shortener Service

URL shortener service built with FastAPI, SQLite, and Python.

**Author:** Anish Kr Singh

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. Clone the repository

```bash
git clone https://github.com/anishfyle/fastapi-backend.git
cd fastapi-backend
```

2. Create a virtual environment

```bash
python -m venv fastapi_venv
```

3. Activate the virtual environment

On Windows (PowerShell):
```powershell
.\fastapi_venv\Scripts\Activate.ps1
```

On Windows (Command Prompt):
```cmd
.\fastapi_venv\Scripts\activate.bat
```

On macOS/Linux:
```bash
source fastapi_venv/bin/activate
```

4. Install required dependencies

```bash
pip install fastapi uvicorn pydantic
```

5. Run the application

```bash
uvicorn main:app --reload
```

6. Access the application

- API will be available at: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs
- Alternative API documentation: http://127.0.0.1:8000/redoc

### Database

The application uses SQLite database (urls.db) which will be automatically created when the application starts for the first time.