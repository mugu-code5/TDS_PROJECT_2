fastapi_project/
├── app/
│   ├── __init__.py              
│   ├── main.py              # The entry point for your FastAPI application.
│   ├── data/
│   ├── models/
│   │   ├── __init__.py      # Makes this folder a package.
│   │   ├── LLM_response.py
│   ├── utils/
│   │   ├── __init__.py      # Makes this folder a package.
│   │   ├── function_calls.py       
│   │   ├── function.py       
│   │   ├── save_files.py    
├── tests/
│   ├── q1_eval.py    # Test cases for function logic.
│   ├── data/
|          |--all the data files
├── requirements.txt         # Python dependencies.
├── README.md                # Project documentation.
├── .env                     # Environment variables for sensitive data.
├── .gitignore               # Files to ignore in version control.


# """
# python -m venv venv
# venv\Scripts\activate   (windows)
# source venv/bin/activate     (linux, mac)
# deactivate
# """