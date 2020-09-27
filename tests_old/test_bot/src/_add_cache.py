import pathlib


def cache(string):
    with open(pathlib.Path() / "tests" / "test_bot" / ".cache", "a") as cache:
        cache.write(f"{string}\n")
