import sys

from fastapi.templating import Jinja2Templates

from sql_app.core.websockets import ConnectionManager
sys.path.append("..")


from fastapi import Request, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="web")
 

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


 


manager = ConnectionManager()


@router.get("/",response_class=HTMLResponse)
async def get(request: Request):
     context = {'request': request}
     return  HTMLResponse(html)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


# async def get_cookie_or_token(
#     websocket: WebSocket,
#     session: Union[str, None] = Cookie(default=None),
#     token: Union[str, None] = Query(default=None),
# ):
#     if session is None and token is None:
#         raise HTTPException(status_code=status.http_403)
#         # raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
#     return session or token


# @router.websocket("/get_agent_status")
# async def get_agent_status_fun(websocket: WebSocket, db: Session = Depends(get_db)):
#     await websocket.accept()
#     while True:
#         try:
#             token = websocket.cookies.get("access_token")
#             _, param = get_authorization_scheme_param(token)
#             data = get_agent_status(token=param, db=db)
#             jsondata = {"status_id": data.status_id,  "status_change_time": date_handler(data.status_change_time), "status": data.status}
#             await websocket.send_json(jsondata)
#         except Exception as e:
#             print(e)
#             break
#         finally:
#             await asyncio.sleep(10)


# in some case json wont be able to serialise datetime format so manually convert it.
def date_handler(obj):
 return obj.isoformat() if hasattr(obj, 'isoformat') else obj 

