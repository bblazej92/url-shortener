import click

from app import create_app


@click.command()
@click.option('--host', '-h', type=click.STRING, default='0.0.0.0')
@click.option('--port', '-p', type=click.INT, default='5000')
@click.option('--config', '-c', type=click.STRING, default='default')
def main(port, host, config):
    app = create_app(config_name=config)
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
