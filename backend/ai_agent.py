from langchain.tools import tool
from tools import query_medgemma

import googlemaps
from config import GOOGLE_MAPS_API_KEY
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
@tool
def ask_mental_health_specialist(query: str) -> str:
   
    """Therapeutic response for emotional/mental health queries."""
    print("ask_mental_health_specialist")
    return query_medgemma(query)


@tool
def emergency_call_tool() -> None:
     
    """ONLY for explicit suicidal ideation or immediate self-harm intent."""
    print("emergency_call_tool")
    pass

    
@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds real therapists near the specified location using Google Maps API.
    
    Args:
        location (str): The city or area to search.
    
    Returns:
        str: A list of therapist names, addresses, and phone numbers.
    """
    geocode_result = gmaps.geocode(location)
    lat_lng = geocode_result[0]['geometry']['location']
    lat, lng = lat_lng['lat'], lat_lng['lng']
    places_result = gmaps.places_nearby(
            location=(lat, lng),
            radius=5000,
            keyword="Psychotherapist"
        )
    output = [f"Therapists near {location}:"]
    top_results = places_result['results'][:5]
    for place in top_results:
            name = place.get("name", "Unknown")
            address = place.get("vicinity", "Address not available")
            details = gmaps.place(place_id=place["place_id"], fields=["formatted_phone_number"])
            phone = details.get("result", {}).get("formatted_phone_number", "Phone not available")

            output.append(f"- {name} | {address} | {phone}")

    
    return "\n".join(output)

# Step1: Create an AI Agent & Link to backend
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from config import GROQ_API_KEY


tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location]
 
llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0,   
    api_key=GROQ_API_KEY
)
graph = create_agent(llm, tools=tools)

SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
You may respond directly to the user when no tool is required.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `find_nearby_therapists_by_location`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `emergency_call_tool`: ONLY if user says something like 'I want to kill myself' or 'I will hurt myself' — explicit stated intent only. Sadness, stress, or failure are NOT emergencies.

Always take necessary action. Respond kindly, clearly, and supportively.
 
"""
def parse_response(stream):
    tool_called_name = "None"
    final_response = None

    for s in stream:
        # Check if a tool was called
        model_data = s.get('model')
        if model_data:
            messages = model_data.get('messages')
            if messages and isinstance(messages, list):
                for msg in messages:
                    # check for tool calls
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for call in msg.tool_calls:
                            tool_called_name = call['name']
                    # check for final response
                    if hasattr(msg, 'content') and msg.content:
                        final_response = msg.content

    return tool_called_name, final_response

 
# if __name__ == "__main__":
#     while True:
#         user_input = input("User: ")
        
#         inputs = {
#             "messages": [
#                 ("system", SYSTEM_PROMPT),
#                 ("user", user_input),
#             ]
#         }
        
#         stream = graph.stream(inputs, stream_mode="updates")
        
#         for s in stream:
#             print("STREAM CHUNK:", s)  # see what's coming out
        
#         # then call parse
#         stream = graph.stream(inputs, stream_mode="updates")  # re-stream since first was consumed
#         result = parse_response(stream)
#         print("ANSWER:", result[1])
#         print("TOOL CALLED:", result[0])
