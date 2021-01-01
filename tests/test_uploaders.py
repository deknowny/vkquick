import pytest
import pytest_mock
import vkquick as vq


@pytest.mark.asyncio
async def test_upload_photos_to_message(mocker: pytest_mock.MockerFixture):
    mocked_form_builed = mocker.patch("aiohttp.FormData")
    mocked_form_builed.return_value = mocked_form_builed
    mocked_form_builed.add_field = mocker.Mock()

    mocked_read = mocker.Mock(return_value=b"456")
    mocked_open = mocker.patch("vkquick.uploaders.open")
    mocked_open.return_value = mocked_open
    mocked_open.read = mocked_read

    api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
    api._make_api_request = mocker.AsyncMock(
        side_effect=[
            vq.AttrDict({"upload_url": "url"}),
            vq.AttrDict([{"photo": 1}, {"photo": 2}]),
        ]
    )
    api.async_http_session = mocker.Mock(name="session")
    api.async_http_session.return_value = api.async_http_session
    response = mocker.Mock()
    response.__aenter__ = mocker.AsyncMock(return_value=response)
    response.__aexit__ = mocker.AsyncMock(return_value=response)
    response.read = mocker.AsyncMock(return_value='{"some": "data"}')
    api.async_http_session.post = mocker.Mock(return_value=response)

    upload_data = await vq.upload_photos_to_message(
        b"123", "some/path.jpg", api=api
    )

    fileds_calls = [
        mocker.call(
            "file0",
            b"123",
            content_type="multipart/form-data",
            filename=f"a.png",
        ),
        mocker.call(
            "file1",
            b"456",
            content_type="multipart/form-data",
            filename=f"a.png",
        ),
    ]

    mocked_form_builed.add_field.assert_has_calls(fileds_calls)
    assert upload_data[0].fields() == {"photo": 1}
    assert upload_data[1].fields() == {"photo": 2}
    mocked_open.read.assert_called_once()
    mocked_open.assert_called_once_with("some/path.jpg", "rb")
    response.read.assert_called_once()
    response.__aenter__.assert_called_once()
    api.async_http_session.post.assert_called_once()

    with pytest.raises(ValueError):
        await vq.upload_photos_to_message(*["photo"] * 11, api=api)


@pytest.mark.asyncio
async def test_upload_photo_to_message(mocker: pytest_mock.MockerFixture):
    api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
    mocked_uploader = mocker.patch(
        "vkquick.uploaders.upload_photos_to_message", return_value=[0]
    )
    res = await vq.upload_photo_to_message(b"123", api=api)
    mocked_uploader.assert_called_once_with(b"123", api=api, peer_id=0)
    assert res == 0


@pytest.mark.asyncio
async def test_upload_doc_to_message(mocker: pytest_mock.MockerFixture):
    path_handler = mocker.patch("pathlib.Path")
    path_handler.return_value = path_handler
    path_handler.name = "foo.txt"
    path_handler.read_bytes = mocker.Mock(return_value="text")

    mocked_form_builed = mocker.patch("aiohttp.FormData")
    mocked_form_builed.return_value = mocked_form_builed
    mocked_form_builed.add_field = mocker.Mock()

    api = vq.API("token", token_owner=vq.TokenOwner.GROUP)
    api.async_http_session = mocker.Mock(name="session")
    api.async_http_session.return_value = api.async_http_session
    api._make_api_request = mocker.AsyncMock(
        side_effect=[
            vq.AttrDict({"upload_url": "url"}),
            vq.AttrDict({"doc": 1}),
        ]
    )
    response = mocker.Mock()
    response.__aenter__ = mocker.AsyncMock(return_value=response)
    response.__aexit__ = mocker.AsyncMock(return_value=response)
    response.read = mocker.AsyncMock(return_value='{"some": "data"}')
    api.async_http_session.post = mocker.Mock(return_value=response)
    doc = await vq.upload_doc_to_message(
        filepath="foo.txt", api=api, peer_id=0
    )
    assert doc.fields == 1
    response.read.assert_called_once()
    response.__aenter__.assert_called_once()

    with pytest.raises(ValueError):
        await vq.upload_doc_to_message(api=api, peer_id=0)

    with pytest.raises(ValueError):
        await vq.upload_doc_to_message(
            filepath="foo.txt",
            content="text",
            filename="a.txt",
            api=api,
            peer_id=0,
        )
