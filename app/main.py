"""
To shut down the surver use c command: taskkill /F /PID {process_id}
In case you don't remember the process number use folowing comands:
    (Get-NetTCPConnection -LocalPort {port_number}).OwningProcess
    and then
    wmic process where ("ParentProcessId={received_owning_process_number}") get Caption,ProcessId
"""

from fastapi import FastAPI
from .journal.api.api import api_router

app = FastAPI()

app.include_router(router=api_router)


@app.get("/")
async def root():
    return "The server is running."
