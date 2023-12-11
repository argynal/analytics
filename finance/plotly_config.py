import os
from django_plotly_dash.consumers import send

PLOTLY_DASH = {
    "ws_route": os.path.join(send, "ws", "myapp"),
    "routes": [
        # Добавьте маршруты для ваших графиков здесь
    ],
}
