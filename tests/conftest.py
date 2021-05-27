import pytest
import vkquick


@pytest.fixture
async def user_api():
    api = vkquick.API("$GROUP_TOKEN", token_owner=vkquick.TokenOwner.GROUP)
    async with api:
        yield api
