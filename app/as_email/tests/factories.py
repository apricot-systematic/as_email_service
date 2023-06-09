#!/usr/bin/env python
#
"""
Factories for testing all of our models and related code
"""
# system imports
#
from pathlib import Path
from typing import Any, Sequence

# 3rd party imports
#
import factory
import factory.fuzzy
from django.contrib.auth import get_user_model
from factory import post_generation
from factory.django import DjangoModelFactory
from faker import Faker

# Project imports
#
from ..models import (
    BlockedMessage,
    EmailAccount,
    MessageFilterRule,
    Provider,
    Server,
)

User = get_user_model()
fake = Faker()


########################################################################
########################################################################
#
class UserFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("first_name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = extracted if extracted else fake.password(length=16)
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)


########################################################################
########################################################################
#
class ProviderFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Provider {n}")

    class Meta:
        model = Provider
        django_get_or_create = ("name",)


########################################################################
########################################################################
#
class ServerFactory(DjangoModelFactory):
    domain_name = factory.Sequence(lambda n: f"srvr{n}.example.com")
    provider = factory.SubFactory(ProviderFactory)

    class Meta:
        model = Server
        django_get_or_create = ("domain_name", "provider")


########################################################################
########################################################################
#
class EmailAccountFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    server = factory.SubFactory(ServerFactory)
    email_address = factory.LazyAttribute(
        lambda o: f"{fake.profile()['username']}@{o.server.domain_name}"
    )
    mail_dir = factory.LazyAttribute(
        lambda o: str(Path(fake.file_path(depth=5)).parent)
    )

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = extracted if extracted else fake.password(length=16)
        self.set_password(password)

    class Meta:
        model = EmailAccount
        django_get_or_create = ("user", "email_address", "server")


########################################################################
########################################################################
#
class BlockedMessageFactory(DjangoModelFactory):
    email_account = factory.SubFactory(EmailAccountFactory)
    message_id = factory.Sequence(lambda n: n)
    status = "Blocked"
    subject = factory.Faker("sentence")
    from_address = factory.Faker("email")
    cc = factory.Faker("email")
    blocked_reason = factory.Faker("sentence")

    class Meta:
        model = BlockedMessage


########################################################################
########################################################################
#
class MessageFilterRuleFactory(DjangoModelFactory):
    email_account = factory.SubFactory(EmailAccountFactory)
    pattern = factory.Faker("email")
    header = factory.fuzzy.FuzzyChoice(
        [x[0] for x in MessageFilterRule.HEADER_CHOICES]
    )

    class Meta:
        model = MessageFilterRule
