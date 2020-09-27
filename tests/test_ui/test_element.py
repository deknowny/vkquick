import vkquick as vq


def test_inits():
    """
    Test fields correcting
    """
    elem = vq.Element(
        buttons=[
            vq.Button.text("foo")
        ],
        title="Fizz",
        description="Bazz",
        photo_id="-123_123"
    ).open_photo()

    elem_dict = {
        "title": "Fizz",
        "description": "Bazz",
        "photo_id": "-123_123",
        "action": {"type": "open_photo"},
        "buttons": [
            {
                "action": {
                    "type": "text",
                    "label": "foo"
                }
            }

        ]
    }

    elem_by_dict = vq.Element.by(elem_dict)

    assert elem._info == elem_by_dict._info == elem_dict
