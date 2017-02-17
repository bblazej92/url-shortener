import click
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'


@click.command()
@click.option('--host', type=click.STRING, default='0.0.0.0')
@click.option('--port', type=click.INT, default='5000')
def main(port, host):
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()

