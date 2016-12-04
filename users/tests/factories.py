import factory
from django.contrib.auth.models import User
from faker import Factory as FakeFactory

fake = FakeFactory.create()

DEFAULT_PASSWORD = 'a_password'


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username_{0}'.format(n))
    first_name = fake.name().split()[0]
    last_name = fake.name().split()[1]
    email = fake.email()
    is_staff = False
    is_active = True
    date_joined = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
    password = factory.PostGenerationMethodCall('set_password', DEFAULT_PASSWORD)
