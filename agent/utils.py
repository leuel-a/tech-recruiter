import getpass
import os


def add_to_environ(key: str, prompt: str) -> None: 
    """Adds an environment variable if it does not already exist.

    :param key: The name of the environment variable.
    :param message: The message to display when prompting for the value.
    """
    if key not in os.environ: 
        os.environ[key] = getpass.getpass(prompt=prompt) 

        if key == "LANGSMITH_PROJECT" and not os.environ.get(key):
            os.environ["LANGSMITH_PROJECT"] = "default"
    return
