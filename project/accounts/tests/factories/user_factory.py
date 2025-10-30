import factory
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    user_type = "buyer"

    @factory.post_generation
    def password(obj, create, extracted, **kwargs):
        password = extracted or "test1234"
        obj.set_password(password)
        if create:
            obj.save()
