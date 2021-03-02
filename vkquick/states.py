import os


# Флаг, означающий, что квик рабоатает максимально оптимизированно,
# исключая дополнительную ифнормацию дебага
# Используется в моментах, в которых можно сделать оптимизации.
# Например, выключение дебаггера. Вы также можете строить
# логику у себя, основываясь на этом флаге
VKQUICK_RELEASE = os.getenv("VKQUICK_RELEASE")
if VKQUICK_RELEASE is not None and VKQUICK_RELEASE.isdigit():
    VKQUICK_RELEASE = int(VKQUICK_RELEASE)
VKQUICK_RELEASE = bool(VKQUICK_RELEASE)
