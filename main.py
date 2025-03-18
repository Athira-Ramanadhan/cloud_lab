import webbrowser
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

# Mount static files (CSS & images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template setup
templates = Jinja2Templates(directory="templates")

# Sample in-memory database
quotes = {
    1: "Believe in yourself!",
    2: "Stay positive, work hard, make it happen.",
    3: "The only limit is your mind."
}
quote_id_counter = 4  # Next ID

# Home page - Display all quotes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "quotes": quotes})

# Add new quote
@app.post("/add")
async def add_quote(name: str = Form(...)):
    global quote_id_counter
    quotes[quote_id_counter] = name
    quote_id_counter += 1
    return RedirectResponse(url="/", status_code=303)

# Update a quote (PUT)
@app.post("/update/{quote_id}")
async def update_quote(quote_id: int, new_text: str = Form(...)):
    if quote_id in quotes:
        quotes[quote_id] = new_text
        return RedirectResponse(url="/", status_code=303)
    return {"error": "Quote not found"}

# Modify a quote (PATCH)
@app.post("/modify/{quote_id}")
async def modify_quote(quote_id: int, partial_text: str = Form(...)):
    if quote_id in quotes:
        quotes[quote_id] += " " + partial_text
        return RedirectResponse(url="/", status_code=303)
    return {"error": "Quote not found"}

# Delete a quote
@app.post("/delete/{quote_id}")
async def delete_quote(quote_id: int):
    if quote_id in quotes:
        del quotes[quote_id]
        return RedirectResponse(url="/", status_code=303)
    return {"error": "Quote not found"}

if __name__ == "__main__":
    url = "http://127.0.0.1:8000"
    print(f"\n🚀 FastAPI is running! Open your browser or click: \"{url}\"\n")

    # Automatically open the link in the default web browser
    webbrowser.open(url)

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
