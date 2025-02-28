from django.conf import settings

def dynamic_login_settings(request):
    """
    Returns dynamic settings for the login page (logo, heading, etc.)
    These can be overridden in settings.py as needed.
    """
    return {
        # Fallback to a default if not found in settings
        "LOGIN_PAGE_LOGO": getattr(settings, "LOGIN_PAGE_LOGO", "images/FamilyTime Logo-1200 x 1200.png"),
        "LOGIN_PAGE_HEADING": getattr(settings, "LOGIN_PAGE_HEADING", "WELCOME TO FAMILYTIME <br>(MDM REQUESTS)"),
    }
