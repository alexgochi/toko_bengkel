from flask import current_app, request, g, flash, redirect, Response
from flask.sessions import SecureCookieSessionInterface
from flask_login import LoginManager, current_user, login_url

# setup flask login
login_manager = LoginManager()
login_manager.init_app(current_app)
login_manager.login_view = "login2"


def get_login_url() -> str:
    # Construct the URL for redirecting to the login page with the 'next' parameter in the query string
    # TODO: Pelajari dan implement ini ya: https://snyk.io/blog/secure-python-url-validation/
    return login_url(login_view=login_manager.login_view, next_url=request.url)


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get("login_via_request"):
            return None
        else:
            return super(CustomSessionInterface, self).save_session(*args, **kwargs)


# change default flask session interface
current_app.session_interface = CustomSessionInterface()


def detect_request_source() -> str:
    """
    Detects the source of the request.

    Returns:
        str: The detected source of the request, which can be one of the following:
            - 'ajax' for requests from Ajax.
            - 'browser' for requests from a web browser.
            - 'others' if the source cannot be determined (postman, cURL, etc).
    """

    # Deteksi apakah request berasal dari ajax ?
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return "ajax"

    # Deteksi apakah request berasal dari browser ?
    user_agent = request.headers.get("User-Agent", "")
    # Tiap browser 99.9% punya 3 keywords yg sama: https://webaim.org/blog/user-agent-string-history/
    browser_keywords = {"Mozilla", "Chrome", "Safari"}
    if any(bk in user_agent for bk in browser_keywords):
        return "browser"

    return "others"


def handle_authz_failure(message: str, status_code: int = 403) -> Response:
    """
    Handles authorization failure based on the request source.

    Args:
        message(str): Pesan error untuk direturn
        status_code(int): http status code

    Returns:
        Flask.Response
            If the request is from Ajax or other sources, it returns a plain text response with status_code.
            If the request is from a browser, it redirects to the login page (302).
    """
    request_source = detect_request_source()

    if request_source == "browser":
        flash(message, "info")
        return redirect(get_login_url())
    else:
        return {"message": message}, status_code


def add_user_role(roles) -> set:
    """
    An admin role is more powerful than a 'user' role. Therefore,
    we must add 'user' role for corresponding 'admin' roles in current_user.roles
    """
    for role in roles:
        if role.startswith("user_"):
            admin_role = f"admin_{role.split('_')[1]}"
            if admin_role in current_user.roles:
                current_user.roles.add(role)
                break
