from datetime import date


def year(request):
    """Добавляет переменную с текущим годом."""
    request = date.today().year
    return {
        'year': request
    }
