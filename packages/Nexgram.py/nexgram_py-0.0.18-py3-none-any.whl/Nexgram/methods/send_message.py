import aiohttp

class sendMessage:
  async def send_message(self, chat_id, text):
    if not self.connected: raise ConnectionError("Client is not connected, you must connect the client to send message.")
    url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    async with aiohttp.ClientSession() as x:
      async with x.post(url, json=data) as z:
        return await z.json()