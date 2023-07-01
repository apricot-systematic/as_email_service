#!/usr/bin/env python
#
"""
Model tests.
"""
# system imports
#

# 3rd party imports
#
import pytest
from django.contrib.auth import get_user_model
from faker import Faker

# Project imports
#


User = get_user_model()
fake = Faker()

pytestmark = pytest.mark.django_db


####################################################################
#
def test_email_account_set_check_password(email_account_factory):
    ea = email_account_factory()
    password = fake.pystr(min_chars=8, max_chars=32)
    assert ea.check_password(password) is False
    ea.set_password(password)
    assert ea.check_password(password)


####################################################################
#
def test_email_account_valid_email_address(email_account_factory):
    """
    The `email_address` must have the same domain name as the
    associated server.
    """
    # The factory by default creates an email_address that is valid.
    #
    ea = email_account_factory()
    assert ea.clean()
    assert ea.clean_all()
    ea.save()
