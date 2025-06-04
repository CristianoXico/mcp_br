# protocol/jsonrpc.py
from protocol.handlers import call_tool

async def handle_rpc(data):
    method = data.get("method")
    params = data.get("params", {})
    id_ = data.get("id")

    try:
        result = await call_tool(method, params)
        return {"jsonrpc": "2.0", "result": result, "id": id_}
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32000, "message": str(e)},
            "id": id_,
        }