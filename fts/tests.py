from collections import namedtuple
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PollInfo = namedtuple('PollInfo', ['question', 'choices'])
POLL1 = PollInfo(
    question='How awesome is Test-Driven Development?',
    choices=[
        'Very awesome',
        'Quite awesome',
        'Moderately awesome'
    ],
)
POLL2 = PollInfo(
    question='Which workshop treat do you prefer?',
    choices=[
        'Beer',
        'Pizza',
        'The Acquisition of Knowledge'
    ],
)


class PollTest(LiveServerTestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):
        # AJ opens her web browser and goes to the admin page
        self.browser.get(self.live_server_url + '/admin/')

        # She sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # She types in her username and password and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # Her username and password are accepted and she is taken to the Site Administration page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # She now sees a couple of hyperlinks named "Polls"
        polls_links = self.browser.find_elements_by_link_text('Polls')
        self.assertEquals(len(polls_links), 2)

        # She sees a link to add a new poll so she clicks it
        new_poll_links = self.browser.find_elements_by_link_text('Add')

        for link in new_poll_links:
            if 'poll' in link.get_attribute('href'):
                new_poll_link = link
                break

        new_poll_link.click()

        # She sees some input fields for "Question" and "Publish date"
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Question:', body.text)
        self.assertIn('Publish date:', body.text)

        # She types in an interesting question for the poll
        question_field = self.browser.find_element_by_name('question')
        question_field.send_keys('How awesome is Test-Driven Development?')

        # She sets the date and time of publication
        date_field = self.browser.find_element_by_name('pub_date_0')
        date_field.send_keys('01/01/12')
        time_field = self.browser.find_element_by_name('pub_date_1')
        time_field.send_keys('10:30')

        # She enters choices for the poll
        choice_1 = self.browser.find_element_by_name('choice_set-0-choice')
        choice_1.send_keys('Very awesome')
        choice_2 = self.browser.find_element_by_name('choice_set-1-choice')
        choice_2.send_keys('Quite awesome')
        choice_3 = self.browser.find_element_by_name('choice_set-2-choice')
        choice_3.send_keys('Moderately awesome')

        # AJ clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()

        # She is returned to the "Polls" listing where she can see her new poll listed as a clickable link
        new_poll_links = self.browser.find_elements_by_link_text('How awesome is Test-Driven Development?')
        self.assertEquals(len(new_poll_links), 1)

        # Satisfied, she goes back to sleep

    def _setup_polls_via_admin(self):
        # AJ logs into the admin site
        self.browser.get(self.live_server_url + '/admin/')

        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)

        # She has a number of polls to enter. For each one, she:
        for poll_info in [POLL1, POLL2]:
            # Follows the link to the Polls app and adds a new poll
            self.browser.find_elements_by_link_text('Polls')[1].click()
            self.browser.find_element_by_link_text('Add poll').click()

            # Enters his name and uses the 'today' and 'now' buttons to set the publish date
            question_field = self.browser.find_element_by_name('question')
            question_field.send_keys(poll_info.question)
            self.browser.find_element_by_link_text('Today').click()
            self.browser.find_element_by_link_text('Now').click()

            # Sees she can enter choices for the poll on this same page, so she does
            for i, choice_text in enumerate(poll_info.choices):
                choice_field = self.browser.find_element_by_name('choice_set-%d-choice' % i)
                choice_field.send_keys(choice_text)

            # Saves her new poll
            save_button = self.browser.find_element_by_css_selector("input[value='Save']")
            save_button.click()

            # Is returned to the polls listing where she can see her new poll listed as a clickable link by its name
            new_poll_links = self.browser.find_elements_by_link_text(poll_info.question)
            self.assertEquals(len(new_poll_links), 1)

            # She goes back to the root of the admin site
            self.browser.get(self.live_server_url + '/admin/')

        # She logs out of the admin site
        self.browser.find_element_by_link_text('Log out').click()

    def test_voting_on_a_new_poll(self):
        # First, AJ logs into the admin site and creates a coupe of new polls and their response choices
        self._setup_polls_via_admin()

        # Now, Randy (the regular user) goes to the site's homepage. He sees a list of polls.
        self.browser.get(self.live_server_url)
        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(heading.text, 'Polls')

        # He clicks on the link to the first poll which is called 'How awesome is Test-Driven Development?'
        first_poll_title = 'How awesome is Test-Driven Development?'
        self.browser.find_element_by_link_text(first_poll_title).click()

        # He is taken to a poll results page which says 'no-one has voted on this poll yet'
        main_heading = self.browser.find_element_by_tag_name('h1')
        self.assertequals(main_heading.text, 'Poll Results')
        sub_heading = self.browser.find_element_by_tag_name('h2')
        self.assertEquals(sub_heading.text, first_poll_title)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(body.text, 'No-one has voted on this poll yet')

        self.fail('TODO')
