import vkquick as vq

from . import config


@vq.Cmd(names=config.NAMES)
@vq.Reaction("message_new")
def greet():

    @vq.Template()
    def carousel():
        titles = [
            'Морковь',
            'Картошка',
            'Ягоды'
        ]
        descs = [
            'Вытянутый оранжевый овощ. Любимец кроликов',
            'Кусок крахмала, но вкусный до безумия в пюрешке',
            'Просто наборчик полезных сладостей'
        ]
        keyboards = [
            [vq.Button.text(
                label='Купить',
                payload={"name": name.lower()}
            )] for name in titles
        ]
        for title, desc, kb in zip(titles, descs, keyboards):
            elem = vq.Element(
                title=title,
                description=desc,
                buttons=kb
            )
            yield elem.open_link('https://google.com')

    return vq.Message(message="Hello", template=carousel)
