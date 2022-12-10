import dialogflow
from google.api_core.exceptions import InvalidArgument


class dialogflowSession:
    def __init__(self, DIALOGFLOW_PROJECT_ID, DIALOGFLOW_LANGUAGE_CODE, SESSION_ID):
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        self.lang_code = DIALOGFLOW_LANGUAGE_CODE
    
    def get_intent(self, query):
        text_input = dialogflow.types.TextInput(text=query, language_code=self.lang_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            intent = self.session_client.detect_intent(session=self.session, query_input=query_input)
        except InvalidArgument:
            raise
        return intent