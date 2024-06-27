import reflex as rx
import time


class CircleSpinnerOverlay(rx.Component):
    library = "react-spinner-overlay"
    tag = "CircleSpinnerOverlay"
    message: rx.Var[str] = ""
    loading: rx.Var[bool] = False


class State(rx.State):
    overlay_process: bool = False
    inside_process1: bool = False
    inside_process2: bool = False

    def heavy_process1(self):
        self.inside_process1 = True
        yield
        time.sleep(3)
        self.inside_process1 = False

    def heavy_process2(self):
        self.inside_process2 = True
        yield
        time.sleep(3)
        self.inside_process2 = False

    def heavy_process3(self):
        self.overlay_process = True
        yield
        time.sleep(3)
        self.overlay_process = False


def SpinnerButton(text, on_click, loading=False, disabled=False):
    return rx.button(
        text,
        rx.spinner(loading=loading),
        on_click=on_click,
        disabled=disabled,
    )


def index():
    return rx.box(
        CircleSpinnerOverlay.create(
            loading=State.overlay_process, message="Processing..."
        ),
        rx.center(
            rx.heading("Simple Spinners"),
            rx.button(
                "Inside1",
                loading=State.inside_process1,
                on_click=State.heavy_process1,
            ),
            rx.button(
                rx.spinner(loading=State.inside_process2),
                "Inside2",
                on_click=State.heavy_process2,
                disabled=State.inside_process2,
            ),
            rx.button(
                "Overlay",
                on_click=State.heavy_process3,
            ),
            direction="column",
            spacing="4",
            height="100vh",
            justify="center",
        ),
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index)
