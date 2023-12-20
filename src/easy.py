""" Some lovely functions to make the code more readable.
/easy.py
"""

from flask import Response

def reset_cookies(response: Response) -> Response:
    """Reset the user and session cookies."""
    response.set_cookie("session_token", "", expires=0)
    response.set_cookie("user", "", expires=0)
    return response