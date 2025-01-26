import requests

# Define the API endpoint and payload
url = "http://localhost:5000/process-images/"
payload = {
    "images": [
        "https://i.ibb.co/RNKnqMh/algea.jpg",
        # "https://i.ibb.co/0cCYDLF/burger.jpg",
        # "https://i.ibb.co/WckBR2q/cake.jpg",
        # "https://i.ibb.co/tbKz4MR/chicken.jpg",
        # "https://i.ibb.co/TPyrZ9h/chorizzo.jpg",
        # "https://i.ibb.co/ZmgW665/coffee.jpg",
        # "https://i.ibb.co/ZN0gX1q/fries.jpg",
        # "https://i.ibb.co/XD0V1Yh/nuggets.jpg",
        # "https://i.ibb.co/ssyh7fF/panini.jpg",
        # "https://i.ibb.co/m6PD5Fg/pasta.jpg",
        # "https://i.ibb.co/1TQ74mB/sashimi.jpg",
        # "https://i.ibb.co/frsXCb3/shrimps.jpg",
        # "https://i.ibb.co/XSkGXnw/sushi.jpg",
        # "https://i.ibb.co/VVDBKVh/tiramisu.jpg"
    ]
}

# Make a POST request
response = requests.post(url, json=payload)

# Print the response
print("Response status:", response.status_code)
print("Response JSON:", response.json())
