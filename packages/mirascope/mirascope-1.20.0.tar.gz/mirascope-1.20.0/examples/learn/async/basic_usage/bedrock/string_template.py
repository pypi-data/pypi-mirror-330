import asyncio

from mirascope.core import bedrock, prompt_template


@bedrock.call(model="anthropic.claude-3-haiku-20240307-v1:0")
@prompt_template("Recommend a {genre} book")
async def recommend_book(genre: str): ...


async def main():
    response = await recommend_book("fantasy")
    print(response.content)


asyncio.run(main())
