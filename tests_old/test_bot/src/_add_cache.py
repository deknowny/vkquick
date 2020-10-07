import pathlib


def cache(string):
    with open(pathlib.Path() / "tests_old" / "test_bot" / ".cache", "a") as cache:
        cache.write(f"{string}\n")
