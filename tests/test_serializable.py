import vkquick as vq


def test_serializable():
    photo = vq.Photo({"owner_id": 1, "id": 1})
    doc = vq.Document({"owner_id": 1, "id": 1, "access_key": 123})
    assert photo.represent_as_api_param() == "photo1_1"
    assert doc.represent_as_api_param() == "doc1_1_123"
