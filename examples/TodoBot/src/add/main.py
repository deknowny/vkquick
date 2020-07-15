import vkquick as vq

from . import config


@vq.Cmd(prefs=config.PREFS, names=config.NAMES)
@vq.Reaction("message_new")
def add(text: str, sender: vq.Sender()):
    """
    Добавляет заметку в базу данных
    """
    note = vq.current.Notes(
        owner_id=sender.id,
        text=text,
    )
    vq.current.session.add(note)
    vq.current.session.commit()
    return config.ANSWER.format(
        id=note.id,
        text=text
    )
