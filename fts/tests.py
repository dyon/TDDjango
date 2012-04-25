from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


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

        # AJ clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()

        # She is returned to the "Polls" listing where she can see her new poll listed as a clickable link
        new_poll_links = self.browser.find_elements_by_link_text('How awesome is Test-Driven Development?')
        self.assertEquals(len(new_poll_links), 1)

        # TODO: Finish the test
        self.fail('Finish this test')
