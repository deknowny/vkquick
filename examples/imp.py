@vq.Template()
def carousel():
        titles = [
            'Морковь',
            'Картошка',
            'Ягоды'
        ]
        # Описания для элементов. Порядок долже сохраниться
        descs = [
            'Вытянутый оранжевый овощ. Любимец кроликов',
            'Кусок крахмала, но вкусный до безумия в пюрешке',
            'Просто наборчик полезных сладостей'
        ]
        # Клавиатура для элемента
        keyboards = [
                Button.text(
                    label='Купить',
                    payload={"name": name.lower()}
                ) for name in titles
        ]
        # Просто проходимся фором по каждому из элементов
        for title, desc, kb in zip(titles, descs, keyboards):
            # Создаем экземпляр Element(**kwargs)
            elem = Element(
                title=title,
                description=desc,
                buttons=kb
            )
            # Yield'им элемент, не забывая добавлять событие,
            # которое должно случиться при нажатии на элемент.
            # Все описано в документации вк
            yield elem.open_link('https://google.com')
