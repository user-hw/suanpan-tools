import click

@click.command()
@click.option("-name", default='world', help="姓名", type=str)
def hello(name):
    click.echo('hello {name}'.format(name=name))

if __name__ == '__main__':
    hello()