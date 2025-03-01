import requests
import uuid

class JujiDesign:
    def __init__(self, api_key: str, platform_url: str = "https://juji.ai"):
        """
        Initialize the JujiDesign class.
        Args:
            api_key: Juji API key
            platform_url: Juji platform URL (defaults to https://juji.ai)
        """
        self.JUJI_API_KEY = api_key
        self.JUJI_PLATFORM_URL = platform_url

    def set_browser_key(self, engagement_id: str | uuid.UUID, browser_key: str | uuid.UUID | None = None):
        """
        Set the browser key for the chatbot.
        Args:
            engagement_id: the engagement id to set the browser key for.
            browser_key: the browser key to set.
        """
        if not isinstance(engagement_id, uuid.UUID):
            engagement_id = uuid.UUID(engagement_id)
        
        if browser_key is None:
            browser_key = uuid.uuid4()
        elif not isinstance(browser_key, uuid.UUID):
            browser_key = uuid.UUID(browser_key)

        mutation = """
        mutation SetBrowserKey($input: SetBrowserKeyInput!) {
            setBrowserKey(input: $input) {
                message
                success
            }
        }
        """

        variables = {
            "input": {
                "browserKey": str(browser_key),
                "engagementId": str(engagement_id)
            }
        }

        response = requests.post(
            f"{self.JUJI_PLATFORM_URL}/api/graphql",
            json={
                "query": mutation,
                "variables": variables
            },
            headers={
                "Content-Type": "application/json"
            },
            auth=("apikey", self.JUJI_API_KEY)
        )

        response.raise_for_status()
        print(response.json())

        parsed_response = response.json()["data"]["setBrowserKey"]
        parsed_response["browser_key"] = browser_key

        return parsed_response

    def get_brands(self):
        """
        Get all brands. By default, there is only one brand associated with a Juji account.
        """

        query = """
        query GetBrands {
            getBrands {
                name
                email
            }
        }
        """

        response = requests.post(
            f"{self.JUJI_PLATFORM_URL}/api/graphql",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            auth=("apikey", self.JUJI_API_KEY)
        )

        response.raise_for_status()
        print(response.json())

        parsed_response = response.json()["data"]["getBrands"]
        return parsed_response

    def add_faq(self, questions: list[str], answers: list[str], engagement_id: str | uuid.UUID, browser_key: str | uuid.UUID | None = None):
        """
        Add a FAQ to the chatbot. The first question in the list will be the primary question.
        Args:
            questions: list of questions.
            answers: list of answers
            engagement_id: the engagement id to add the FAQ to
            browser_key: the browser key to use for the FAQ update. It should be a UUID.
        """
        
        if not isinstance(engagement_id, uuid.UUID):
            engagement_id = uuid.UUID(engagement_id)
        
        if browser_key is None:
            browser_key = uuid.uuid4()

        # set browser key
        set_browser_key_response = self.set_browser_key(engagement_id, browser_key)

        if not set_browser_key_response["success"]:
            raise Exception(set_browser_key_response["message"])
        
        # get brand
        brand_name = self.get_brands()[0]["name"]

        # add faq
        mutation = """
        mutation addNewEngagementFaqs($input: AddNewEngagementFaqsInput!) {
            addNewEngagementFaqs(input: $input) {
                message
                success
                sha1
            }
        }
        """
        faq_obj = {
            "question": questions[0],
            "answers": answers,
            "new" : True
        }
        if len(questions) > 1:
            faq_obj["questionParaphrases"] = questions[1:]

        variables = {
            "input": {
                "browserKey": str(browser_key),
                "engagementId": str(engagement_id),
                "brand": brand_name,
                "filledUnansweredQuestions": [faq_obj]
            }
        }

        response = requests.post(
            f"{self.JUJI_PLATFORM_URL}/api/graphql",
            json={"query": mutation, "variables": variables},
            headers={"Content-Type": "application/json"},
            auth=("apikey", self.JUJI_API_KEY)
        )

        response.raise_for_status()
        print(response.json())

        parsed_response = response.json()["data"]["addNewEngagementFaqs"]
        return parsed_response