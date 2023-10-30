import openai

# Set your API key
openai.api_key = "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"

# Test the API key by making a ping request
response = openai.api.Ping.get()

# Check the response
if response["data"] == "Pong!":
    print("API key is working")
else:
    print("API key is not working")
