from flask import Response
from flask_login import login_required
from flask_login import current_user
from functools import wraps
from .utils import add_user_role, handle_authz_failure


def roles_accepted(*accepted_roles) -> Response:
    """
    Decorator which specifies that a user must have at least one of the specified roles
    example::

        @app.post('/protected_menu')
        @roles_accepted('admin_61', 'kontraktor')
        def protected_menu_view():
            return "Only accessible if you have 'admin_61' role OR 'kontraktor' role"

    :param accepted_roles: The possible roles.
    """

    def wrapper(fn):
        @login_required
        @wraps(fn)
        def inner(*args, **kwargs):
            nonlocal accepted_roles
            add_user_role(accepted_roles)

            if not any(ar in current_user.roles for ar in accepted_roles):
                return handle_authz_failure(
                    f"Akun anda wajib terdaftar dalam salah satu role berikut: <b>{accepted_roles}</b>"
                )

            return fn(*args, **kwargs)

        return inner

    return wrapper


def roles_required(*required_roles) -> Response:
    """
    Decorator which specifies that a user must have all the specified roles
    example::

        @app.post('/protected_menu')
        @roles_required('admin_61', 'Z001')
        def protected_menu_view():
            return "Only accessible if you have 'admin_61' role AND work at 'Z001'."

    :param required_roles: The required roles.
    """

    def wrapper(fn):
        @login_required
        @wraps(fn)
        def inner(*args, **kwargs):
            nonlocal required_roles
            add_user_role(required_roles)

            if not all(rr in current_user.roles for rr in required_roles):
                return handle_authz_failure(
                    f"Hanya user dengan role <b>{required_roles}</b> yang boleh!"
                )

            return fn(*args, **kwargs)

        return inner

    return wrapper
