from django.test import TestCase
from django.contrib.auth.models import User
from ads.models import Ad
from .models import ExchangeProposal

class ExchangeProposalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.ad1 = Ad.objects.create(
            user=self.user1,
            title='Test Ad 1',
            description='Test Description'
        )
        self.ad2 = Ad.objects.create(
            user=self.user2,
            title='Test Ad 2',
            description='Test Description'
        )

    def test_proposal_creation(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='Test proposal'
        )
        self.assertEqual(proposal.status, 'pending')
        self.assertEqual(proposal.ad_sender.user.username, 'user1')
        self.assertEqual(proposal.ad_receiver.user.username, 'user2')

    def test_proposal_str(self):
        proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2
        )
        self.assertEqual(str(proposal), f"Обмен {self.ad1} на {self.ad2}")


def test_duplicate_proposal(self):
    ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2)
    with self.assertRaises(Exception):
        ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2)


def test_update_proposal_status(self):
    proposal = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad2)
    proposal.status = 'accepted'
    proposal.save()
    self.assertEqual(proposal.status, 'accepted')


def test_cannot_propose_to_own_ad(self):
    with self.assertRaises(ValueError):
        ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=self.ad1)


def test_auto_reject_on_accept(self):
    ad3 = Ad.objects.create(user=self.user2, title='Test Ad 3', description='Test')
    proposal1 = ExchangeProposal.objects.create(ad_sender=self.ad1, ad_receiver=ad3)
    proposal2 = ExchangeProposal.objects.create(ad_sender=self.ad2, ad_receiver=ad3)

    proposal1.status = 'accepted'
    proposal1.save()

    proposal2.refresh_from_db()
    self.assertEqual(proposal2.status, 'rejected')