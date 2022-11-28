import uvicorn

from server.app import app, os, x


@app.on_event("shutdown")
def shutdown_event():
    for file in os.listdir(x):
        os.remove(os.path.join(x, file))
        print(f"File {file} deleted")


if __name__ == "__main__":
    uvicorn.run("server.app:app", host="127.0.0.1", port=8000, reload=True)
