import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urlparse, parse_qs


class InstalingClient:
    def __init__(self):
        self.base_url = "https://instaling.pl"
        self.session = requests.Session()
        self.student_id = None
        self.session_completed = False

    def login(self, email, password):
        """
        Log into Instaling with provided credentials.
        
        Args:
            email (str): User's email address
            password (str): User's password
            
        Returns:
            bool: True if login was successful
            
        Raises:
            ValueError: If credentials are invalid
            requests.exceptions.HTTPError: If HTTP request fails
        """
        login_url = f"{self.base_url}/teacher.php?page=teacherActions"
        data = {
            'action': 'login',
            'from': '',
            'log_email': email,
            'log_password': password
        }

        response = self.session.post(login_url, data=data)
        response.raise_for_status()

        parsed_url = urlparse(response.url)
        query_params = parse_qs(parsed_url.query)
        if "student_id" in query_params:
            self.student_id = query_params["student_id"][0]
        else:
            raise ValueError("Invalid username or password.")

        soup = BeautifulSoup(response.text, 'html.parser')
        session_completed = soup.find('h4', string='Dzisiejsza sesja wykonana')
        self.session_completed = bool(session_completed)
        
        return True

    def initiate_session(self):
        """
        Initiate a new learning session. (Not needed to start the quiz, but is used by the website)
        
        Raises:
            ValueError: If not logged in
            requests.exceptions.HTTPError: If HTTP request fails
        """
        if not self.student_id:
            raise ValueError("Student ID not set. Please login first.")

        url = f"{self.base_url}/ling2/server/actions/init_session.php"
        data = {
            'child_id': self.student_id,
            'repeat': '',
            'start': '',
            'end': ''
        }

        response = self.session.post(url, data=data)
        response.raise_for_status()

    def solve_quiz(self):
        """
        Solve the quiz by repeating words until the session is complete.
        
        Raises:
            ValueError: If not logged in
            requests.exceptions.HTTPError: If HTTP request fails
        """
        if not self.student_id:
            raise ValueError("Student ID not set. Please login first.")

        self.initiate_session()
        words_to_repeat = self.get_words_to_repeat()

        while True:
            delay = random.uniform(1, 5)
            time.sleep(delay)

            url = f"{self.base_url}/ling2/server/actions/generate_next_word.php"
            data = {
                'child_id': self.student_id,
                'date': int(time.time() * 1000)
            }

            response = self.session.post(url, data=data)
            response.raise_for_status()

            if "Dni pracy w tym tygodniu" in response.text:
                break

            word_data = response.json()
            word_id = word_data.get('id')
            polish_translation = self.get_polish_translation(word_id, words_to_repeat)
            self.save_answer(word_id, polish_translation)

    def get_words_to_repeat(self, group_id=0, limit=300):
        """
        Get a list of words that need to be repeated.
        
        Args:
            group_id (int): ID of the group
            limit (int): Maximum number of words to retrieve
            
        Returns:
            list: List of words to repeat
            
        Raises:
            ValueError: If not logged in or response is invalid
            requests.exceptions.HTTPError: If HTTP request fails
        """
        if not self.student_id:
            raise ValueError("Student ID not set. Please login first.")

        url = f"{self.base_url}/learning/repeat_words_ajax.php"
        params = {
            "action": "getWordsToRepeat",
            "student_id": self.student_id,
            "group_id": group_id,
            "limit": limit,
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            raise ValueError("Response is not in JSON format")

    def get_polish_translation(self, word_id, words_to_repeat):
        """
        Get the Polish translation for a given word ID.
        
        Args:
            word_id (int): ID of the word
            words_to_repeat (list): List of words to search in
            
        Returns:
            str: Polish translation of the word
        """
        for word in words_to_repeat:
            if word.get('word_id') == word_id:
                return word.get('word')

        return "Default Polish Translation"

    def save_answer(self, word_id, polish_translation):
        """
        Save the answer for a given word.
        
        Args:
            word_id (int): ID of the word
            polish_translation (str): Polish translation to submit
            
        Returns:
            dict: JSON response from the server
            
        Raises:
            requests.exceptions.HTTPError: If HTTP request fails
        """
        url = f"{self.base_url}/ling2/server/actions/save_answer.php"
        data = {
            'child_id': self.student_id,
            'word_id': word_id,
            'answer': polish_translation
        }

        response = self.session.post(url, data=data)
        response.raise_for_status()

        return response.json()

    def get_textbook_words_lists(self, textbook_id=33522):
        """
        Get words lists for a specific textbook.
        
        Args:
            textbook_id (int): ID of the textbook
            
        Returns:
            str: Response text containing the word lists
            
        Raises:
            ValueError: If not logged in or response is invalid
            requests.exceptions.HTTPError: If HTTP request fails
        """
        if not self.student_id:
            raise ValueError("Student ID not set. Please login first.")

        url = f"{self.base_url}/learning/repeat_words_ajax.php"
        params = {
            "action": "getTextbookWordsLists",
            "textbook_id": textbook_id,
        }

        response = self.session.get(url, json=params)
        response.raise_for_status()

        try:
            return response.text
        except ValueError:
            raise ValueError("Response is not in JSON format")
