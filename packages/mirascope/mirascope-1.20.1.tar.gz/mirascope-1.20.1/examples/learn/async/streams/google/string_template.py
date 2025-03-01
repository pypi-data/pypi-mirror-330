import asyncio

from mirascope.core import google, prompt_template


@google.call("gemini-1.5-flash", stream=True)
@prompt_template("Recommend a {genre} book")
async def recommend_book(genre: str): ...


async def main():
    stream = await recommend_book("fantasy")
    async for chunk, _ in stream:
        print(chunk.content, end="", flush=True)


asyncio.run(main())
