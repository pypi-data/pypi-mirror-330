
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException,APIRouter,Request
from fastapi.responses import JSONResponse,StreamingResponse
import fastapi_cdn_host
from bilibili import BilibiliLib

from bilibili.info import InfoRouter

def serve(args):
    host = args.host 
    port = args.port
    app = FastAPI(title="bilibiliServe")
    fastapi_cdn_host.patch_docs(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)
    
    bilibiliLib = BilibiliLib()
    app.include_router(bilibiliLib.router,prefix="/v1")
    infoRouter = InfoRouter(app)
    app.include_router(infoRouter.router,prefix="")

    uvicorn.run(app, host = host, port = port)

