"""QR code display screen showing member QR for printing or sharing."""

import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


KV = """
#:import HEX app.theme
<QRDisplayScreen>:
    name: "qr_display"
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: HEX.BACKGROUND
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: dp(56)
            padding: dp(16), dp(8)
            spacing: dp(8)
            canvas.before:
                Color:
                    rgba: HEX.PRIMARY
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: "< 返回"
                font_size: sp(14)
                color: 1, 1, 1, 1
                size_hint_x: None
                width: dp(80)
                background_normal: ""
                background_color: 0, 0, 0, 0
                on_release: root.go_back()
            Label:
                text: "会员二维码"
                font_size: sp(20)
                color: 1, 1, 1, 1
                bold: True
                halign: "left"
                valign: "middle"
        BoxLayout:
            orientation: "vertical"
            padding: dp(24)
            spacing: dp(16)
            Widget:
                size_hint_y: 0.1
            BoxLayout:
                size_hint_y: None
                height: dp(280)
                Widget:
                    size_hint_x: 0.1
                BoxLayout:
                    size_hint_x: 0.8
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            radius: [dp(12)]
                            pos: self.pos
                            size: self.size
                    AsyncImage:
                        id: qr_image
                        size_hint: None, None
                        size: dp(240), dp(240)
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        allow_stretch: True
                        keep_ratio: True
                Widget:
                    size_hint_x: 0.1
            Label:
                id: label_name
                text: ""
                font_size: sp(18)
                color: HEX.TEXT_PRIMARY
                bold: True
                halign: "center"
                size_hint_y: None
                height: dp(30)
            Label:
                id: label_id
                text: ""
                font_size: sp(14)
                color: HEX.TEXT_SECONDARY
                halign: "center"
                size_hint_y: None
                height: dp(24)
            Label:
                text: "请让工作人员扫描此二维码"
                font_size: sp(13)
                color: HEX.TEXT_SECONDARY
                halign: "center"
                size_hint_y: None
                height: dp(24)
            Widget:
"""


class QRDisplayScreen(Screen):
    """Displays a member's QR code image."""

    _member_id = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)

    def load_member(self, member_id):
        self._member_id = member_id
        app = App.get_running_app()
        member = app.db.get_member(member_id)
        if not member:
            self.go_back()
            return
        self.ids.label_name.text = member.get("name", "")
        self.ids.label_id.text = f"ID: {member_id}"
        from app.qr_manager import get_qr_path, generate_qr_image
        qr_path = get_qr_path(member_id)
        if not os.path.isfile(qr_path):
            qr_path = generate_qr_image(member_id, save=True)
        self.ids.qr_image.source = qr_path
        self.ids.qr_image.reload()

    def go_back(self):
        self.manager.current = "member_detail"
