from django.test import TestCase
from django.utils import timezone, unittest
from polls.models import Choice, Poll


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

    def test_verbose_name_for_pub_date(self):
        for field in Poll._meta.fields:
            if field.name == 'pub_date':
                self.assertEquals(field.verbose_name, 'Publish date')

    def test_poll_objects_are_named_after_their_question(self):
        p = Poll()
        p.question = 'This question is a test?'
        self.assertEquals(unicode(p), 'This question is a test?')


class ChoiceModelTest(TestCase):

    def test_creating_some_choices_for_a_poll(self):
        # Start by creating a new Poll object
        poll = Poll()
        poll.question = "What's up?"
        poll.pub_date = timezone.now()
        poll.save()

        # Now we create a Choice object
        choice = Choice()

        # Link it to our poll
        choice.poll = poll
        choice.choice = 'Doing fine...'
        choice.votes = 3
        choice.save()

        # Try retrieving from the database using the poll object's reverse lookup
        poll_choices = poll.choice_set.all()
        self.assertEquals(poll_choices.count(), 1)

        # Finally, check that its attributes have been saved
        choice_from_db = poll_choices[0]
        self.assertEquals(choice_from_db, choice)
        self.assertEquals(choice_from_db.choice, 'Doing fine...')
        self.assertEquals(choice_from_db.votes, 3)

    def test_choice_defaults(self):
        choice = Choice()
        self.assertEquals(choice.votes, 0)


class HomePageViewTest(TestCase):

    def test_root_url_shows_all_polls(self):
        # Set up some polls
        poll1 = Poll(question='6 times 7', pub_date=timezone.now())
        poll1.save()
        poll2 = Poll(question='Life, the universe and everything', pub_date=timezone.now())
        poll2.save()

        response = self.client.get('/')

        self.assertIn(poll1.question, response.content)
        self.assertIn(poll2.question, response.content)
