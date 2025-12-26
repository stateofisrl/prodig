def user_balance(request):
    """Provide current user's balance to all templates when authenticated."""
    try:
        if request.user.is_authenticated:
            return {'balance': request.user.balance}
    except Exception:
        pass
    return {}
