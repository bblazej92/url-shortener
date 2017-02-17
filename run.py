import click

from app import create_app


@click.command()
@click.option('--host', type=click.STRING, default='0.0.0.0')
@click.option('--port', type=click.INT, default='5000')
def main(port, host):
    app = create_app()
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
