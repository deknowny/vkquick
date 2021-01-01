import vkquick as vq


def test_serializable():
    photo = vq.Photo({"owner_id": 1, "id": 1})
    doc = vq.Document({"owner_id": 1, "id": 1, "access_key": 123})
    assert photo.api_param_representation() == "photo1_1"
    assert doc.api_param_representation() == "doc1_1_123"