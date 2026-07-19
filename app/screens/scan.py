"""QR code scanner screen with camera preview for real-time QR detection."""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup


KV = """
#:import HEX app.theme
<ScanScreen>:
    name: "scan"
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            id: camera_container
            size_hint_y: 0.7
            canvas.before:
                Color:
                    rgba: 0, 0, 0, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
        BoxLayout:
            size_hint_y: 0.3
            orientation: "vertical"
            padding: dp(16)
            spacing: dp(12)
            canvas.before:
                Color:
                    rgba: HEX.BACKGROUND
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                id: scan_status
                text: "??????????????????????????????"
                font_size: sp(16)
                color: HEX.TEXT_PRIMARY
                halign: "center"
                valign: "middle"
                size_hint_y: 0.35
            BoxLayout:
                size_hint_y: 0.3
                spacing: dp(12)
                Widget:
                    size_hint_x: 0.2
                Button:
                    text: "??????"
                    font_size: sp(15)
                    background_normal: ""
                    background_color: HEX.TEXT_SECONDARY
                    color: 1, 1, 1, 1
                    size_hint_x: 0.3
                    on_release: root.go_back()
                    canvas.before:
                        Color:
                            rgba: HEX.TEXT_SECONDARY
                        RoundedRectangle:
                            radius: [dp(8)]
                            pos: self.pos
                            size: self.size
                Button:
                    text: "????????????ID"
                    font_size: sp(15)
                    background_normal: ""
                    background_color: HEX.PRIMARY
                    color: 1, 1, 1, 1
                    size_hint_x: 0.3
                    on_release: root.manual_input()
                    canvas.before:
                        Color:
                            rgba: HEX.PRIMARY
                        RoundedRectangle:
                            radius: [dp(8)]
                            pos: self.pos
                            size: self.size
                Widget:
                    size_hint_x: 0.2
            Label:
                text: ""
                size_hint_y: 0.35
"""


class ScanScreen(Screen):
    """Camera-based QR code scanner with manual ID fallback."""

    _camera = None
    _scanning = False
    _scan_event = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)

    def on_enter(self):
        self._start_camera()

    def on_leave(self):
        self._stop_camera()

    def _start_camera(self):
        try:
            from kivy.uix.camera import Camera
            self._camera = Camera(resolution=(640, 480), play=True)
            self.ids.camera_container.add_widget(self._camera)
            self._scanning = True
            self._scan_event = Clock.schedule_interval(self._analyze_frame, 0.5)
        except Exception:
            self.ids.scan_status.text = "????????????????????????????????????????????????"

    def _stop_camera(self):
        self._scanning = False
        if self._scan_event:
            Clock.unschedule(self._scan_event)
            self._scan_event = None
        if self._camera:
            self._camera.play = False
            self.ids.camera_container.clear_widgets()
            self._camera = None

    def _analyze_frame(self, dt):
        if not self._scanning or not self._camera:
            return
        texture = self._camera.texture
        if not texture or not texture.pixels:
            return
        try:
            from PIL import Image
            from pyzbar.pyzbar import decode as zb_decode
            size = texture.size
            pixels = texture.pixels
            fmt = texture.colorfmt or "rgba"
            mode_map = {"rgba": "RGBA", "rgb": "RGB", "bgra": "RGBA", "bgr": "RGB"}
            mode = mode_map.get(fmt.lower(), "RGBA")
            w, h = int(size[0]), int(size[1])
            if w <= 0 or h <= 0:
                return
            img = Image.frombytes(mode, (w, h), pixels)
            if mode == "RGBA":
                img = img.convert("L")
            results = zb_decode(img)
            if results:
                from app.qr_manager import decode_member_qr
                for r in results:
                    data = r.data.decode("utf-8", errors="replace")
                    member_id = decode_member_qr(data)
                    if member_id:
                        self._on_qr_found(member_id)
                        return
        except ImportError:
            self._stop_camera()
            self.ids.scan_status.text = "?????????????????????????????????????????????"
        except Exception:
            pass

    def _on_qr_found(self, member_id):
        self._scanning = False
        app = App.get_running_app()
        member = app.db.get_member(member_id)
        if member:
            screen = self.manager.get_screen("member_detail")
            screen.load_member(member_id)
            self.manager.current = "member_detail"
        else:
            self.ids.scan_status.text = f"???????????????: {member_id}"
            Clock.schedule_once(lambda dt: self._restart_scan(), 2)

    def _restart_scan(self):
        self._scanning = True
        self.ids.scan_status.text = "??????????????????????????????"

    def manual_input(self):
        from kivy.uix.textinput import TextInput
        content = Builder.load_string("""
BoxLayout:
    orientation: "vertical"
    padding: dp(16)
    spacing: dp(12)
    Label:
        text: "???????????????ID????????????"
        font_size: sp(14)
        color: (0.13, 0.13, 0.13, 1)
        halign: "center"
        valign: "middle"
    TextInput:
        id: manual_id_input
        hint_text: "??? SP000001 ????????????"
        font_size: sp(16)
        multiline: False
        size_hint_y: None
        height: dp(44)
    BoxLayout:
        size_hint_y: None
        height: dp(44)
        spacing: dp(12)
        Button:
            text: "??????"
            on_release: popup.dismiss()
        Button:
            text: "??????"
            on_release: root_callback(manual_id_input.text)
""")
        popup = Popup(
            title="????????????",
            content=content,
            size_hint=(0.85, 0.35),
            auto_dismiss=False,
        )

        def do_search(text):
            text = text.strip()
            if not text:
                return
            app = App.get_running_app()
            member = app.db.get_member(text)
            if not member:
                results = app.db.get_all_members(text)
                if results:
                    member = results[0]
            if member:
                popup.dismiss()
                screen = self.manager.get_screen("member_detail")
                screen.load_member(member["id"])
                self.manager.current = "member_detail"
            else:
                self.ids.scan_status.text = "????????????????????????"

        content.root_callback = do_search
        content.popup = popup
        popup.open()

    def go_back(self):
        self._stop_camera()
        self.manager.current = "home"
