import vkquick as vq


def test_carousel():
    carousel = vq.Carousel.build(
        vq.Element(
            title="a",
            description="b",
            buttons=[vq.Button.text("a")],
            photo_id="123",
        ).open_link("google.com"),
        vq.Element(
            title="a",
            description="b",
            buttons=[vq.Button.text("a")],
            photo_id=vq.Photo({"id": 1, "owner_id": 1}),
        ).open_photo(),
    )
    assert carousel().scheme == {
        "elements": [
            {
                "action": {"link": "google.com", "type": "open_link"},
                "buttons": [
                    {
                        "action": {
                            "label": "a",
                            "payload": None,
                            "type": "text",
                        }
                    }
                ],
                "description": "b",
                "photo_id": "123",
                "title": "a",
            },
            {
                "action": {"type": "open_photo"},
                "buttons": [
                    {
                        "action": {
                            "label": "a",
                            "payload": None,
                            "type": "text",
                        }
                    }
                ],
                "description": "b",
                "photo_id": "photo1_1",
                "title": "a",
            },
        ],
        "type": "carousel",
    }
