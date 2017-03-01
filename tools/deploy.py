import click
import subprocess


@click.command()
@click.option('--user', '-u', type=click.STRING, default='ubuntu')
@click.option('--host', '-x', type=click.STRING, default='52.59.215.242')
def deploy(user, host):
    kwargs = dict(
        user=user,
        host=host
    )
    click.secho('Calling deploy.sh with arguments:\n{}'.format(kwargs), fg='green')
    call_args = '{user} {host}'.format(**kwargs)
    subprocess.call('bash deploy.sh {}'.format(call_args), shell=True)


if __name__ == '__main__':
    deploy()
