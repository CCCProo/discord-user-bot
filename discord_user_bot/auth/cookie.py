"""
A class to get CloudFlare cookies.
"""

class CookieGenerator:
    def __init__(self, requester, url="https://discord.com"):
        self.requester = requester
        self.url = url

    async def compile(self):
        res = await self.requester.fetch_noparse(self.url)
        cookies_header = res.headers.get("set-cookie")
        
        if cookies_header is None:
            return ""

        cookies = cookies_header.split(";")
        values = [f"__{cookie.split('__')[1].strip()}" for cookie in cookies if "__" in cookie]

        compiled = "; ".join(values)
        return f"{compiled}; locale=en-US"

# This line makes the class available for import
__all__ = ["CookieGenerator"]
