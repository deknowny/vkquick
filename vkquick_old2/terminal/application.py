import cleo

import commands

app = cleo.Application()
app.add(commands.create.Create())

if __name__ == "__main__":
    app.run()
