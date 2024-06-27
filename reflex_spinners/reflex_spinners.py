import reflex as rx

from .async_example import index as async_index
from .simple import index as sync_index


def index():
    return rx.tabs.root(
        rx.tabs.list(
            rx.tabs.trigger("Simple", value="Simple"),
            rx.tabs.trigger("Async", value="Async"),
        ),
        rx.tabs.content(
            sync_index(),
            value="Simple",
        ),
        rx.tabs.content(
            async_index(),
            value="Async",
        ),
        default_value="Simple",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
