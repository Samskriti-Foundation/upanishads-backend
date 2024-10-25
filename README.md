# Upanishads Backend

## Overview
Upanishads frontend repository is a React frontend for Upanishads Mangement Portal which is a one stop data management portal for upanishad apps developed by Samskriti Foundation, Mysore.

## Links to Related Repositories:
- Ishavasyopanishad: https://github.com/Samskriti-Foundation/ishavasyopanishad
  
- Upanishads Frontend: https://github.com/Samskriti-Foundation/upanishads-frontend

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Samskriti-Foundation/upanishads-backend
   ```

2. **Navigate to the project directory:**

   ```bash
   cd upanishads-backend
   ```

3. **Install dependencies using a Virtual Environment:**

   a. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

   b. Activate the virtual environment:

   - **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
      venv\Scripts\activate
     ```

   c. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the backend server

1. Start the server using FastAPI CLI:

```bash
fastapi dev
```

## Run tests

1. Run tests with Pytest:

```bash
pytest -v
```

## API Documentation

The API documentation can be accessed at: `http://localhost:8000/docs`
