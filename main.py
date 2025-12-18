from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import uuid
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

os.makedirs("output", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
def generate(
    sport_name: str = Form(...),
    match_duration: int = Form(...),
    num_teams: int = Form(...),
    players_per_team: int = Form(...)
):
    # -----------------------------
    # VALIDATION — Sport Config
    # -----------------------------
    if not sport_name.strip():
        return {"error": "Sport name cannot be empty"}

    if match_duration <= 0:
        return {"error": "Match duration must be greater than 0"}

    # -----------------------------
    # CONFIG SHEET
    # -----------------------------
    df_config = pd.DataFrame({
        "Parameter": [
            "Sport Name",
            "Match Duration (minutes)",
            "Number of Teams",
            "Players per Team"
        ],
        "Value": [
            sport_name,
            match_duration,
            num_teams,
            players_per_team
        ]
    })

    # -----------------------------
    # EXISTING SUMMARY SHEET
    # -----------------------------
    df_summary = pd.DataFrame({
        "Sport": [sport_name],
        "Match Duration (min)": [match_duration],
        "Teams": [num_teams],
        "Players per Team": [players_per_team]
    })

    filename = f"tournament_{uuid.uuid4()}.xlsx"
    filepath = f"output/{filename}"

    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        df_config.to_excel(writer, sheet_name="Config", index=False)
        df_summary.to_excel(writer, sheet_name="Summary", index=False)

    return FileResponse(
        filepath,
        filename="Tournament.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
