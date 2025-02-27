import re

from httpx import AsyncClient

from .catalogue import Catalogue


class AnimeSama:
    def __init__(self, site_url: str, client: AsyncClient | None = None) -> None:
        self.site_url = site_url
        self.client = client or AsyncClient()

    async def search(self, query: str) -> list[Catalogue]:
        response = await self.client.post(
            f"{self.site_url}template-php/defaut/fetch.php", data={"query": query}
        )

        links = re.findall(r'href="(.+?)"', response.text)
        names = re.findall(r">(.+?)<\/h3>", response.text)

        return [
            Catalogue(url=link, name=name, client=self.client)
            for link, name in zip(links, names)
        ]

    async def all_catalogues(self) -> list[Catalogue]:
        raise NotImplementedError
