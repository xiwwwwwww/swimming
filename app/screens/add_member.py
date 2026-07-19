"""Add member screen ??? form for creating a new member record."""

import os
import shutil
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
AVATAR_DIR = os.path.join(DATA_DIR, "avatars")


KV = """
#:import HEX app.theme

<AddMemberScreen>:
    name: "add_member"
    avatar_file: ""
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: HEX.BACKGROUND
            Rectangle:
                pos: self.pos
                size: self.size

        # Top bar
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
                text: "< ??????"
                font_size: sp(14)
                color: 1, 1, 1, 1
                size_hint_x: None
                width: dp(80)
                background_normal: ""
                background_color: 0, 0, 0, 0
                on_release: root.go_back()
            Label:
                text: "????????????"
                font_size: sp(20)
                color: 1, 1, 1, 1
                bold: True
                halign: "left"
                valign: "middle"

        # Form
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16)
                spacing: dp(16)

                # Avatar section
                BoxLayout:
                    size_hint_y: None
                    height: dp(100)
                    spacing: dp(16)
                    BoxLayout:
                        size_hint: None, None
                        size: dp(80), dp(80)
                        canvas.before:
                            Color:
                                rgba: 0.88, 0.92, 0.98, 1
                            Ellipse:
                                pos: self.pos
                                size: self.size
                        AsyncImage:
                            id: avatar_preview
                            size_hint: None, None
                            size: dp(72), dp(72)
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}
                            allow_stretch: True
                            keep_ratio: True
                    BoxLayout:
                        orientation: "vertical"
                        spacing: dp(4)
                        Label:
                            text: "????????????"
                            font_size: sp(15)
                            color: HEX.TEXT_PRIMARY
                            bold: True
                            halign: "left"
                            valign: "bottom"
                            size_hint_y: 0.5
                        Label:
                            text: "????????????????????????????????????????????????"
                            font_size: sp(12)
                            color: HEX.TEXT_SECONDARY
                            halign: "left"
                            valign: "top"
                            size_hint_y: 0.5

                BoxLayout:
                    size_hint_y: None
                    height: dp(44)
                    spacing: dp(8)
                    Button:
                        text: "??????"
                        font_size: sp(14)
                        background_normal: ""
                        background_color: HEX.PRIMARY_LIGHT
                        color: 1, 1, 1, 1
                        on_release: root.take_photo()
                        canvas.before:
                            Color:
                                rgba: HEX.PRIMARY_LIGHT
                            RoundedRectangle:
                                radius: [dp(6)]
                                pos: self.pos
                                size: self.size
                    Button:
                        text: "???????????????"
                        font_size: sp(14)
                        background_normal: ""
                        background_color: HEX.ACCENT
                        color: 1, 1, 1, 1
                        on_release: root.pick_gallery()
                        canvas.before:
                            Color:
                                rgba: HEX.ACCENT
                            RoundedRectangle:
                                radius: [dp(6)]
                                pos: self.pos
                                size: self.size

                # Name
                Label:
                    text: "?????? *"
                    font_size: sp(14)
                    color: HEX.TEXT_PRIMARY
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(24)
                TextInput:
                    id: input_name
                    hint_text: "?????????????????????"
                    font_size: sp(16)
                    multiline: False
                    size_hint_y: None
                    height: dp(48)
                    background_normal: ""
                    background_color: 1, 1, 1, 1
                    foreground_color: HEX.TEXT_PRIMARY
                    cursor_color: HEX.PRIMARY
                    padding: dp(12), dp(10)
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            radius: [dp(8)]
                            pos: self.pos
                            size: self.size

                # Phone
                Label:
                    text: "????????? *"
                    font_size: sp(14)
                    color: HEX.TEXT_PRIMARY
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(24)
                TextInput:
                    id: input_phone
                    hint_text: "??????????????????"
                    font_size: sp(16)
                    multiline: False
                    input_filter: "int"
                    size_hint_y: None
                    height: dp(48)
                    background_normal: ""
                    background_color: 1, 1, 1, 1
                    foreground_color: HEX.TEXT_PRIMARY
                    cursor_color: HEX.PRIMARY
                    padding: dp(12), dp(10)
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            radius: [dp(8)]
                            pos: self.pos
                            size: self.size

                # Gender
                Label:
                    text: "??????"
                    font_size: sp(14)
                    color: HEX.TEXT_PRIMARY
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(24)
                BoxLayout:
                    size_hint_y: None
                    height: dp(44)
                    spacing: dp(8)
                    Button:
                        id: btn_male
                        text: "???"
                        font_size: sp(15)
                        background_normal: ""
                        background_color: HEX.PRIMARY
                        color: 1, 1, 1, 1
                        on_release: root.set_gender("???")
                        canvas.before:
                            Color:
                                rgba: HEX.PRIMARY
                            RoundedRectangle:
                                radius: [dp(6)]
                                pos: self.pos
                                size: self.size
                    Button:
                        id: btn_female
                        text: "???"
                        font_size: sp(15)
                        background_normal: ""
                        background_color: HEX.BACKGROUND
                        color: HEX.TEXT_PRIMARY
                        on_release: root.set_gender("???")
                        canvas.before:
                            Color:
                                rgba: 0.88, 0.88, 0.88, 1
                            RoundedRectangle:
                                radius: [dp(6)]
                                pos: self.pos
                                size: self.size

                # Member type
                Label:
                    text: "????????????"
                    font_size: sp(14)
                    color: HEX.TEXT_PRIMARY
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(24)
                Spinner:
                    id: spinner_type
                    text: "??????"
                    values: ["??????", "??????", "??????", "??????", "?????????"]
                    font_size: sp(16)
                    size_hint_y: None
                    height: dp(48)
                    background_normal: ""
                    background_color: 1, 1, 1, 1
                    color: HEX.TEXT_PRIMARY
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            radius: [dp(8)]
                            pos: self.pos
                            size: self.size

                # Initial visits
                Label:
                    text: "????????????"
                    font_size: sp(14)
                    color: HEX.TEXT_PRIMARY
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(24)
                TextInput:
                    id: input_remaining
                    text: "0"
                    hint_text: "???????????????????????????"
                    font_size: sp(16)
                    multiline: False
                    input_filter: "int"
                    size_hint_y: None
                    height: dp(48)
                    background_normal: ""
                    background_color: 1, 1, 1, 1
                    foreground_color: HEX.TEXT_PRIMARY
                    cursor_color: HEX.PRIMARY
                    padding: dp(12), dp(10)
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            radius: [dp(8)]
                            pos: self.pos
                            size: self.size

                # Notes
                Label:
                    text: "??????"
                    font_size: sp(14)
                    color: HEX.TEXT_PRIMARY
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(24)
                TextInput:
                    id: input_notes
                    hint_text: "??????????????????"
                    font_size: sp(15)
                    size_hint_y: None
                    height: dp(88)
                    background_normal: ""
                    background_color: 1, 1, 1, 1
                    foreground_color: HEX.TEXT_PRIMARY
                    cursor_color: HEX.PRIMARY
                    padding: dp(12), dp(10)
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            radius: [dp(8)]
                            pos: self.pos
                            size: self.size

                # Save button
                Button:
                    text: "??????????????????"
                    font_size: sp(17)
                    bold: True
                    color: 1, 1, 1, 1
                    size_hint_y: None
                    height: dp(52)
                    background_normal: ""
                    background_color: HEX.PRIMARY
                    on_release: root.save_member()
                    canvas.before:
                        Color:
                            rgba: HEX.PRIMARY
                        RoundedRectangle:
                            radius: [dp(8)]
                            pos: self.pos
                            size: self.size

                # Bottom spacer
                Widget:
                    size_hint_y: None
                    height: dp(32)
"""


class AddMemberScreen(Screen):
    """Form screen for adding a new member."""

    avatar_file = ""
    _gender = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)
        os.makedirs(AVATAR_DIR, exist_ok=True)

    def on_enter(self):
        """Reset form when entering this screen."""
        self.avatar_file = ""
        self._gender = ""
        self.ids.avatar_preview.source = ""
        self.ids.input_name.text = ""
        self.ids.input_phone.text = ""
        self.ids.input_remaining.text = "0"
        self.ids.input_notes.text = ""
        self.ids.spinner_type.text = "??????"
        self._update_gender_buttons()

    def set_gender(self, gender):
        self._gender = gender
        self._update_gender_buttons()

    def _update_gender_buttons(self):
        btn_m = self.ids.btn_male
        btn_f = self.ids.btn_female
        if self._gender == "???":
            btn_m.background_color = (0.082, 0.396, 0.753, 1)
            btn_m.color = (1, 1, 1, 1)
            btn_f.background_color = (0.88, 0.88, 0.88, 1)
            btn_f.color = (0.13, 0.13, 0.13, 1)
        elif self._gender == "???":
            btn_f.background_color = (0.082, 0.396, 0.753, 1)
            btn_f.color = (1, 1, 1, 1)
            btn_m.background_color = (0.88, 0.88, 0.88, 1)
            btn_m.color = (0.13, 0.13, 0.13, 1)
        else:
            btn_m.background_color = (0.88, 0.88, 0.88, 1)
            btn_m.color = (0.13, 0.13, 0.13, 1)
            btn_f.background_color = (0.88, 0.88, 0.88, 1)
            btn_f.color = (0.13, 0.13, 0.13, 1)

    def take_photo(self):
        """Take a photo using the device camera."""
        try:
            from plyer import camera
            filename = os.path.join(AVATAR_DIR, f"photo_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
            camera.take_picture(
                filename=filename,
                on_complete=lambda path: self._on_avatar_selected(path),
            )
        except (ImportError, NotImplementedError):
            self._show_popup("??????", "???????????????????????????????????????????????????????????????")

    def pick_gallery(self):
        """Pick an image from the device gallery."""
        try:
            from plyer import filechooser
            filechooser.open_file(
                on_selection=self._on_gallery_selected,
                filters=[["Images", "*.jpg", "*.jpeg", "*.png", "*.bmp"]],
            )
        except (ImportError, NotImplementedError):
            self._show_popup("??????", "????????????????????????????????????")

    def _on_gallery_selected(self, selection):
        if selection and len(selection) > 0:
            self._on_avatar_selected(selection[0])

    def _on_avatar_selected(self, source_path):
        if not source_path or not os.path.isfile(source_path):
            return
        # Copy to local avatar directory
        ext = os.path.splitext(source_path)[1] or ".jpg"
        dest = os.path.join(AVATAR_DIR, f"avatar_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}")
        shutil.copy2(source_path, dest)
        self.avatar_file = dest
        self.ids.avatar_preview.source = dest

    def save_member(self):
        """Validate and save the member record."""
        name = self.ids.input_name.text.strip()
        phone = self.ids.input_phone.text.strip()

        if not name:
            self._show_popup("??????", "????????????????????????")
            return
        if not phone:
            self._show_popup("??????", "?????????????????????")
            return
        if len(phone) < 7:
            self._show_popup("??????", "????????????????????????????????????7???????????????")
            return

        member_type = self.ids.spinner_type.text
        remaining_text = self.ids.input_remaining.text.strip()
        remaining = int(remaining_text) if remaining_text else 0
        notes = self.ids.input_notes.text.strip()

        app = App.get_running_app()
        mid = app.db.add_member(
            name=name,
            phone=phone,
            gender=self._gender,
            member_type=member_type,
            remaining=remaining,
            notes=notes,
            avatar_path=self.avatar_file,
        )

        # Generate QR code for this member
        from app.qr_manager import generate_qr_image
        generate_qr_image(mid, save=True)

        self._show_popup("??????", f"?????? {name} ???????????????\n??????ID: {mid}")

    def _show_popup(self, title, message):
        content = Builder.load_string("""
BoxLayout:
    orientation: "vertical"
    padding: dp(16)
    spacing: dp(12)
    Label:
        text: root_msg
        font_size: sp(15)
        color: (0.13, 0.13, 0.13, 1)
        halign: "center"
        valign: "middle"
        text_size: self.size
""")
        content.root_msg = message
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.35),
            auto_dismiss=True,
        )
        popup.open()

    def go_back(self):
        self.manager.current = "home"
