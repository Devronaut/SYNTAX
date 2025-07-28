from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import router
import scheduler

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Start the reminder scheduler when the app starts"""
    print("🚀 Starting reminder scheduler...")

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the reminder scheduler when the app shuts down"""
    print("🛑 Stopping reminder scheduler...")
    scheduler.reminder_scheduler.stop()

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    # Assume the incoming message text is in data['message'] (adjust as needed for actual payload)
    message = data.get('message', '')
    response = router.route_message(message)
    return JSONResponse(content={"reply": response}) 