# Step1: Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from ai_agent import graph, SYSTEM_PROMPT, parse_response

app = FastAPI()

# Step2: Receive and validate request from Frontend
class Query(BaseModel):
    message: str
    phone: str
    location: str  

from database import init_db, register_user, get_user
 # run once on startup
init_db()  

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/register")
def register(req: RegisterRequest):
    success = register_user(req.name, req.email, req.password, req.phone)
    if success:
        return {"status": "registered"}
    return {"status": "email already exists"}

@app.post("/login")
def login(req: LoginRequest):
    user = get_user(req.email, req.password)
    if user:
        return {"status": "success", "name": user[1], "phone": user[4]}
    return {"status": "invalid credentials"}
 
 


@app.post("/ask")
async def ask(query: Query):
    message_with_context = f"[User location: {query.location}] {query.message}"
    inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", message_with_context)]}
    stream = graph.stream(inputs, stream_mode="updates")
    
    for s in stream:
        print("CHUNK:", s)   
    
    stream = graph.stream(inputs, stream_mode="updates")   
    tool_called_name, final_response = parse_response(stream)
    print("TOOL CALLED:", tool_called_name)   
    if tool_called_name == "emergency_call_tool":
        from tools import call_emergency
        call_emergency(query.phone)   
    return {"response": final_response, "tool_called": tool_called_name}
         

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)






