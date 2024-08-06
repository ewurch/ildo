from sqlalchemy.orm import Session
from fastapi import FastAPI, Form, Request, File, UploadFile, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
from starlette.responses import HTMLResponse
import json

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up the static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up the templates directory
templates = Jinja2Templates(directory="templates")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
def upload_csv(
    request: Request,
    db: Session = Depends(get_db),
    file: UploadFile = File(...)
) -> HTMLResponse:
    df = pd.read_csv(file.file)
    file.file.close()

    columns = df.columns.to_list()
    meta = {"columns": columns}

    # Save to database
    obj = models.Object(
        filename=file.filename,
        raw_data=df.to_json(),
        meta=json.dumps(meta),
    )
    db.add(obj)
    db.commit()

    return templates.TemplateResponse(
        "columns.html", 
        {
            "request": request, 
            "columns": columns,
            "file_id": obj.id,
        }
    )


@app.get("/columns/{file_id}")
async def select_feature_columns(
    request: Request,
    file_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    obj = db.query(models.Object).filter(models.Object.id == file_id).first()
    meta = json.loads(obj.meta)
    print(meta)
    return templates.TemplateResponse(
        "columns.html", 
        {
            "request": request,
            "file_id": file_id,
            "columns": meta["columns"],
            "feature_columns": meta.get("feature_columns", []),
        }
    )

@app.get("/target/{file_id}")
async def select_target_column(
    request: Request,
    file_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    obj = db.query(models.Object).filter(models.Object.id == file_id).first()
    meta = json.loads(obj.meta)
    return templates.TemplateResponse(
        "target.html", 
        {
            "request": request, 
            "file_id": file_id,
            "columns": meta["columns"],
            "feature_columns": meta.get("feature_columns", []),
        }
    )


@app.post("/columns/{file_id}")
async def select_columns(
    request: Request,
    file_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    obj = db.query(models.Object).filter(models.Object.id == file_id).first()
    meta = json.loads(obj.meta)
    form_data = await request.form()
    meta["feature_columns"] = [key for key in form_data.keys()]

    obj.meta = json.dumps(meta)
    db.add(obj)
    db.commit()

    return templates.TemplateResponse(
        "target.html", 
        {
            "request": request, 
            "columns": meta["columns"],
            "feature_columns": meta["feature_columns"],
        }
    )


@app.get("/confirm/{file_id}")
async def confirm(
    request: Request,
    file_id: int,
    db: Session = Depends(get_db),
) -> HTMLResponse:
    obj = db.query(models.Object).filter(models.Object.id == file_id).first()
    meta = json.loads(obj.meta)
    return templates.TemplateResponse(
        "confirm.html", 
        {
            "request": request, 
            "feature_columns": meta["feature_columns"],
            "target_column": meta["target_column"],
        }
    )

@app.post("/target/{file_id}")
def confirm(
    request: Request,
    file_id: int,
    target: str = Form(...),
    db: Session = Depends(get_db),
) -> HTMLResponse:
    obj = db.query(models.Object).filter(models.Object.id == file_id).first()
    meta = json.loads(obj.meta)
    meta["target_column"] = target
    obj.meta = json.dumps(meta)
    db.add(obj)
    db.commit()

    return RedirectResponse(url=f"/confirm/{file_id}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
