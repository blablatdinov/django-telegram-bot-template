from django.test import TestCase

from bot_init.service import do_mailing


class DoMailing(TestCase):

    def test_ok(self):
        do_mailing(
            {
                358610865: 'asdf'
            }
        )
