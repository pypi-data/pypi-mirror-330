import asyncio
import concurrent
import datetime
import os
import shutil
from pathlib import Path
from uuid import uuid4

from ALSTracker.alstracker import run
from fastapi import BackgroundTasks, FastAPI, HTTPException, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_202_ACCEPTED

from . import _version

HERE = os.path.realpath(os.path.dirname(__file__))

app = FastAPI()

# Directory to store uploaded files and generated PDFs
upload_dir = Path("uploads")
upload_dir.mkdir(exist_ok=True)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory=f"{HERE}/templates")
app.mount("/img", StaticFiles(directory=f"{HERE}/templates/img"), name="img")
app.mount("/tools", StaticFiles(directory=f"{HERE}/templates/tools"), name="tools")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    version = _version.version
    last_update = datetime.datetime.fromtimestamp(os.stat(_version.__file__).st_ctime)
    last_update = last_update.strftime("%Y-%m-%d")
    return templates.TemplateResponse("index.html", {"request": request, "version": version, "last_update": last_update})


async def _process_file(filepath, pdf_path, log_path):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ProcessPoolExecutor() as pool:
        await loop.run_in_executor(pool, run, filepath, pdf_path, log_path)


@app.post("/upload/", status_code=HTTP_202_ACCEPTED)
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only xlsx files are accepted.")

    unique_id = str(uuid4())

    try:
        pdf_path = upload_dir / f"{unique_id}.pdf"
        log_path = upload_dir / f"{unique_id}.log"
        filepath = upload_dir / f"{unique_id}.xlsx"
        with filepath.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    # Call the als_tool_package's `run` function with the file paths
    background_tasks.add_task(_process_file, filepath, pdf_path, log_path)

    return {"unique_id": unique_id}


@app.get("/download/{unique_id}")
async def download_file(unique_id: str):
    xlsx_path = upload_dir / f"{unique_id}.xlsx"

    if not xlsx_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    pdf_path = upload_dir / f"{unique_id}.pdf"
    log_path = upload_dir / f"{unique_id}.log"
    if not pdf_path.exists():
        html_template = """
        <html>
            <head>
                <title>Processing log</title>
                <meta http-equiv="refresh" content="5">
            </head>
            <body>
                <h1>Processing log</h1>
                <p>
                Pdf creation still in progress... This page refreshes every 5 seconds.
                </p>
                <pre>{}</pre>
            </body>
        </html>
        """
        insert = ""
        if log_path.exists():
            insert = log_path.read_text()
        return HTMLResponse(html_template.format(insert))

    creation_date = datetime.datetime.fromtimestamp(pdf_path.stat().st_mtime).strftime(
        "%Y-%m-%dT%H-%M-%S"
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"ALSTracker-report-{creation_date}.pdf",
    )
