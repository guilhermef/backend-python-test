import factory
import factory.fuzzy

from alayatodo import db
from alayatodo.models import User, Todo

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.Sequence(lambda n: f"user{n}")

class TodoFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Todo
        sqlalchemy_session = db.session

    user = factory.SubFactory(UserFactory)
    description = factory.fuzzy.FuzzyText(length=12)


def create():
    users = UserFactory.create_batch(3)
    for user in users:
        TodoFactory.create_batch(50, user=user)
    db.session.commit()
