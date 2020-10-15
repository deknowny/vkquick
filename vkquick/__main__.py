import cleo

import vkquick.cli.new


app = cleo.Application()
app.add_commands(vkquick.cli.new.New())


if __name__ == "__main__":
    app.run()
