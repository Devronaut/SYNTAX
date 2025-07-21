from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import router

app = FastAPI()

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    # Assume the incoming message text is in data['message'] (adjust as needed for actual payload)
    message = data.get('message', '')
    try:
        response = router.route_message(message)
        return JSONResponse(content={"reply": response})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500) 