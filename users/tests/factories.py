import factory
from faker import Factory as FakeFactory
from django.conf import settings
fake = FakeFactory.create()

DEFAULT_PASSWORD = 'a_password'


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Sequence(lambda n: 'username_{0}'.format(n))
    full_name = fake.name()
    color = fake.hex_color()
    email = fake.email()
    is_staff = False
    is_active = True
    date_joined = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
    password = factory.PostGenerationMethodCall('set_password', DEFAULT_PASSWORD)
