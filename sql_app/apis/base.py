from fastapi import APIRouter
 
from sql_app.apis import crudapis
from sql_app.apis import chat
from sql_app.apis import authentication

router = APIRouter( )

router.include_router( authentication.router)
router.include_router( crudapis.router)
router.include_router( chat.router)
 
 