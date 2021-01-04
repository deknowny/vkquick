# VK Quick
[![Downloads](https://static.pepy.tech/personalized-badge/vkquick?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/vkquick)

> Хорошие инструменты порождают не только творения, но и идеи

Можно много говорить о VK Quick, но сразу перейдем к созданию бота ВК.

# Установка
```bash
python -m pip install vkquick
```

### До релиза 1.0:
```bash
python -m pip install git+https://github.com/Rhinik/vkquick@1.0 --upgrade
```

# Hello-бот

Насколько VK Quick позволяет быть ленивым?

```python
import vkquick as vq


bot =  vq.Bot.init_via_token("token")


@bot.add_command(names="hello")
def hello():
    return "hi!"


bot.run()
```

Документация появится чуть позже.