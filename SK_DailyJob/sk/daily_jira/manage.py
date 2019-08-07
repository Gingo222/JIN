import click


@click.group()
def cli():
    pass


@cli.command()
def run_api_server():
    from daily_jira.flask_app import create_app
    from gevent.pywsgi import WSGIServer
    app = create_app()
    http_server = WSGIServer(('', 5004), app)
    http_server.serve_forever()


@cli.command()
def init_mysql_env():
    from daily_jira.migrateions.init_mysql import init_app_env
    init_app_env()


if __name__ == '__main__':
    cli()
