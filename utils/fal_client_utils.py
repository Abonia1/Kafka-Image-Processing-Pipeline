import aiohttp


async def submit_request(model_name, arguments):
    url = f"https://api.fal.ai/v1/{model_name}/process"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=arguments) as response:
            return await response.json()
