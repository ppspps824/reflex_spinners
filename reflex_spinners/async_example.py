import reflex as rx
import asyncio
from functools import wraps


class CircleSpinnerOverlay(rx.Component):
    library = "react-spinner-overlay"
    tag = "CircleSpinnerOverlay"
    message: rx.Var[str] = ""
    loading: rx.Var[bool] = False


def set_loading(attr_name):
    def decorator(func):
        @wraps(func)
        @rx.background
        async def wrapper(self, *args, **kwargs):
            async with self:
                setattr(self, attr_name, True)
            yield
            try:
                await func(self, *args, **kwargs)
            finally:
                async with self:
                    setattr(self, attr_name, False)

        return wrapper

    return decorator


class AsyncState(rx.State):
    overlay_processing: bool = False
    inside_processing1: bool = False
    inside_processing2: bool = False

    @set_loading("inside_processing1")
    async def heavy_process1(self):
        await asyncio.sleep(3)

    @set_loading("inside_processing2")
    async def heavy_process2(self):
        await asyncio.sleep(7)

    @set_loading("overlay_processing")
    async def heavy_process3(self):
        await asyncio.sleep(5)


def index():
    return rx.box(
        CircleSpinnerOverlay.create(
            loading=AsyncState.overlay_processing, message="Processing..."
        ),
        rx.center(
            rx.heading("Async Spinners"),
            rx.button(
                "Inside1",
                loading=AsyncState.inside_processing1,
                on_click=AsyncState.heavy_process1,
            ),
            rx.button(
                rx.spinner(loading=AsyncState.inside_processing2),
                "Inside2",
                on_click=AsyncState.heavy_process2,
                disabled=AsyncState.inside_processing2,
            ),
            rx.button(
                "Overlay",
                on_click=AsyncState.heavy_process3,
            ),
            direction="column",
            spacing="4",
            height="100vh",
            justify="center",
        ),
    )
