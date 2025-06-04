# main.py
from fastapi import FastAPI, Request
from protocol.jsonrpc import handle_rpc

app = FastAPI()

@app.post("/")
async def root(request: Request):
    data = await request.json()
    return await handle_rpc(data)