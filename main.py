from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title="N100 Financial Intelligence Platform API")


# Add this root redirect handler:
@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")