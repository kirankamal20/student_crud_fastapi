from fastapi import APIRouter
 
from sql_app.apis import crudapis
# from sql_app.apis import chat
from sql_app.apis import authentication
# from sql_app.apis import websocket_check

router = APIRouter( )


# router.include_router( websocket_check.router)
router.include_router( authentication.router)
router.include_router( crudapis.router)
# router.include_router( chat.router)
 
 
 