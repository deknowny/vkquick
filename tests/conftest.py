import pytest
import vkquick


@pytest.fixture
async def user_api():
    api = vkquick.API("$GROUP_TOKEN")
    yield api
    await api.close_session()
