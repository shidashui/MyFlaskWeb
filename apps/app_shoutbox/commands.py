import click
from apps.app_shoutbox import app, db
from apps.app_shoutbox.models import Message

@app.cli.command()
@click.option('--count', default=20, help='Quantity of messages default is 20.')
def forge(count):
    from faker import Faker
    db.drop_all()
    db.create_all()
    fake = Faker()
    click.echo('Working...')

    for i in range(count):
        message = Message(
            name=fake.name(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(message)
    db.session.commit()
    click.echo('Created %d fake message.'%count)