from esmerald import UJSON, APIView, Esmerald, Gateway, Request, get, post, status


class World(APIView):
    @get(path="/{url}")
    async def home(self, request: Request, url: str) -> UJSON:
        return UJSON(content=f"URL: {url}")

    @post(path="/{url}", status_code=status.HTTP_201_CREATED)
    async def mars(self, request: Request, url: str) -> UJSON:
        ...


app = Esmerald(routes=[Gateway("/world", handler=World)])
