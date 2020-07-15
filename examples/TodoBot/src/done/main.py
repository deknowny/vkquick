import vkquick as vq

from . import config


@vq.Cmd(prefs=config.PREFS, names=config.NAMES)
@vq.Reaction("message_new")
def done(id_: int, sender: vq.Sender()):
    """
    Помечает команду как "выполненное"
    """
    note = vq.current.Notes.fetch_by_id(
        id_=id_, owner_id=sender.id
    )
    if note is None:
        return config.ANSWER_NOT_EXIST.format(
            id=id_
        )

    note.done = True
    vq.current.session.add(note)
    vq.current.session.commit()

    return config.ANSWER.format(
        id=id_,
        text=note.text
    )
