from example import app
from uvicorn import run

if __name__ == "__main__":
    run("example:app" ,reload=True)
