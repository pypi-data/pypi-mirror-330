How to import rabino's library is as follows:

<< from rabino import rubino>>

An example:

		
from rabino import rubino
import asyncio
async def main():
    async with rubino("auth") as bot:
        
        data = await bot.search_username("@super_god1")
        print(data)
asyncio.run(main())


