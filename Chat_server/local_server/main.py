import cli
import setup

def onstart():
    setup.check()


if __name__ == "__main__":
    onstart()
    cli.readrun()