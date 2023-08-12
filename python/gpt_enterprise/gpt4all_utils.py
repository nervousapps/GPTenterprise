"""
GPT4ALL utils
"""
import gpt4all

class GPT4ALLUtils:
    """
    GPT4ALLUtils class binds gpt4all library to be called as openai one in order 
    to use seemlessly openai or gpt4all
    """

    def __init__(self, model_name: str, model_path: str = None, model_type: str = None, allow_download: bool = True):
        """_summary_

        Args:
            model_name (str): _description_
            model_path (str): _description_
            model_type (str): _description_
            allow_download (bool): _description_
        """
        self.gpt = gpt4all.GPT4All(
            model_name=model_name,
            model_path=model_path,
            model_type=model_type,
            allow_download=allow_download)
        
        self.ChatCompletion = self.InnerChatCompletion(gpt=self.gpt)
        self.Image = self.InnerImage(self.gpt)
        
    class InnerChatCompletion:
        """
        ChatCompletion defines a create function as openai one
        """
        def __init__(self, gpt) -> None:
            """_summary_

            Args:
                gpt (_type_): _description_
            """
            self.gpt = gpt
            
        def create(self, model: str, messages: list[dict], temperature: float = 1.0):
            """_summary_

            Args:
                model (str): _description_
                messages (list[dict]): _description_
                temperature (float, optional): _description_. Defaults to 1.0.

            Returns:
                _type_: _description_
            """
            return self.gpt.chat_completion(
                messages,
                default_prompt_header=False,
                default_prompt_footer=False,
                streaming=False
            )
        
    class InnerImage:
        """
        ChatCompletion defines a create function as openai one
        """
        def __init__(self, gpt) -> None:
            """_summary_

            Args:
                gpt (_type_): _description_
            """
            self.gpt = gpt
            
        def create(self, prompt: str, n: int, size: str):
            """_summary_

            Args:
                model (str): _description_
                messages (list[dict]): _description_
                temperature (float, optional): _description_. Defaults to 1.0.

            Returns:
                _type_: _description_
            """
            # return self.gpt.chat_completion(prompt)
            return []
         