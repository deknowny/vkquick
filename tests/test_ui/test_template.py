import vkquick as vq


def test_inits():
    @vq.Template()
    def carousel(*photos):
        titles = ["Foo", "Bar"]
        descs = ["Foo desc", "Bar desc"]
        kbs = [
            [vq.Button.text("foo")],
            [vq.Button.text("bar")]
        ]
        for title, desc, photo, kb in zip(
            titles, descs, photos, kbs
        ):
            elem = vq.Element(
                title=title,
                description=desc,
                photo_id=photo,
                buttons=kb
            )
            yield elem.open_photo()


    carousel = carousel("123_456", "456_789")

    carousel_dict = {
        "type": "carousel",
        "elements": [
            {
                "title": "Foo",
                "description": "Foo desc",
                "photo_id": "123_456",
                "buttons": [
                    {
                        "action": {
                            "type": "text",
                            "label": "foo"
                        }
                    }

                ],
                "action": {
                    "type": "open_photo"
                }
            },
            {
                "title": "Bar",
                "description": "Bar desc",
                "photo_id": "456_789",
                "buttons": [
                    {
                        "action": {
                            "type": "text",
                            "label": "bar"
                        }
                    }
                ],
                "action": {
                    "type": "open_photo"
                }
            }
        ]
    }

    assert (
        carousel.info ==
        carousel_dict ==
        vq.Template.by(carousel_dict).info
    )
