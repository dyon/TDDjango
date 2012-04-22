from django.test import TestCase
from django.utils import timezone
from polls.models import Poll

class PollModelTest(TestCase):

    def test_creating_a_new_poll_and_saving_it_to_the_database(self):
        # Start by creating a new Poll object with its "question" set
        poll = Poll()
        poll.question = "What's up?"
        poll.pub_date = timezone.now()

        # Check if we can save it to the database
        poll.save()

        # Now check if we can find it in the database again
        all_polls_in_database = Poll.objects.all()
        self.assertEquals(len(all_polls_in_database), 1)
        only_poll_in_database = all_polls_in_database[0]
        self.assertEquals(only_poll_in_database, poll)

        # Check if it saved its two attributes: question and pub_date
        self.assertEquals(only_poll_in_database.question, "What's up?")
        self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)
