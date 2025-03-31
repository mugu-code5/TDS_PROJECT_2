from fastapi import FastAPI, Query, File, UploadFile, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from app.utils.save_files import save_file
from app.models.LLM_response import chatgpt
import logging
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

# Create FastAPI app instance
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(filename)s %(threadName)s %(message)s",
    encoding="utf-8"  
)
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@ app.api_route("/Tds_ques/", methods=["POST", "GET"])
async def UI_api_endpoint(
    request: Request,
    question: str = Form(..., description="A question string"),
    file: Optional[UploadFile] = File(None)
):
    try:
        logging.debug(f"API endpoint (Tds_ques) accessed with question: {question}")
        file_path = None
        if file and file.filename:
            logging.debug(f"Received file: {file.filename}")
            file_path = save_file(file)

        # Fetch response from chatgpt
        response = await chatgpt(query=question, file_loc=file_path)
        logging.debug(f"Raw response from ChatGPT: {response}")

        # Ensure response is a dictionary and extract the "answer" field
        try:
            response_dict = json.loads(response["answer"]) #if isinstance(response, str) else response
            # parsed_detail = response_dict.get("answer", "No 'answer' key found.")
            parsed_detail = response_dict
            
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON: {e}")
            parsed_detail= response["answer"]
            
        except Exception as e:
            # parsed_detail = "Error parsing response. Is it valid JSON?"
            parsed_detail=response["answer"]
            
        return templates.TemplateResponse("index.html", {
            "request": request,
            "response": json.dumps(response, indent=4),  # Properly formatted original response
            "parsed_json": json.dumps(parsed_detail, indent=4),  # Properly formatted parsed response
            "question": question
        })

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

    
@app.api_route("/api/", methods=["POST", "GET"])
async def api_endpoint(
    question: str = Query(..., description="A question string"),
    file: Optional[UploadFile] = File(None)
):
    try:
        logging.debug(f"API endpoint (/api/) accessed with question: {question}")
        file_path = save_file(file) if file else None
        response = await chatgpt(query=question, file_loc=file_path)
        return response

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

if __name__ == "__main__":
    import uvicorn
    import os
    print(os.getlogin())  # Who is running the app?

    logging.info("Starting server...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


#venv\Scripts\activate 
#python -m app.main