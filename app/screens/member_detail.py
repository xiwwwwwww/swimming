"""Member detail screen -- view info, quick actions, and navigation hub."""
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

KV = """
#:import HEX app.theme

<MemberDetailScreen>:
    name: "member_detail"
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
                text: "< Back"
                font_size: sp(14)
                color: 1, 1, 1, 1
                size_hint_x: None
                width: dp(80)
                background_normal: ""
                background_color: 0, 0, 0, 0
                on_release: root.go_back()
            Label:
                id: title_label
                text: "Member"
                font_size: sp(20)
                color: 1, 1, 1, 1
                bold: True
                halign: "left"
                valign: "middle"
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16)
                spacing: dp(12)
                BoxLayout:
                    size_hint_y: None
                    height: dp(120)
                    Widget:
                    BoxLayout:
                        size_hint: None, None
                        size: dp(100), dp(100)
                        canvas.before:
                            Color:
                                rgba: 0.88, 0.92, 0.98, 1
                            Ellipse:
                                pos: self.pos
                                size: self.size
                        AsyncImage:
                            id: avatar_img
                            size_hint: None, None
                            size: dp(92), dp(92)
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}
                            allow_stretch: True
                            keep_ratio: True
                    Widget:
                Label:
                    id: label_id
                    text: ""
                    font_size: sp(14)
                    color: HEX.TEXT_SECONDARY
                    halign: "center"
                    size_hint_y: None
                    height: dp(28)
                BoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height if self.minimum_height > dp(60) else dp(60)
                    padding: dp(16)
                    spacing: dp(14)
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            radius: [dp(10)]
                            pos: self.pos
                            size: self.size
                    _InfoRow:
                        label_text: "Name"
                        id: info_name
                    _InfoRow:
                        label_text: "Phone"
                        id: info_phone
                    _InfoRow:
                        label_text: "Gender"
                        id: info_gender
                    _InfoRow:
                        label_text: "Type"
                        id: info_type
                    _InfoRow:
                        label_text: "Notes"
                        id: info_notes
                BoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: dp(100)
                    padding: dp(16)
                    spacing: dp(8)
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            radius: [dp(10)]
                            pos: self.pos
                            size: self.size
                    Label:
                        text: "Remaining"
                        font_size: sp(13)
                        color: HEX.TEXT_SECONDARY
                        halign: "center"
                        size_hint_y: None
                        height: dp(22)
                    BoxLayout:
                        spacing: dp(12)
                        size_hint_y: None
                        height: dp(52)
                        Button:
                            text: "-"
                            font_size: sp(22)
                            bold: True
                            background_normal: ""
                            background_color: HEX.ERROR
                            color: 1, 1, 1, 1
                            size_hint_x: 0.25
                            on_release: root.adjust_visit(-1)
                            canvas.before:
                                Color:
                                    rgba: HEX.ERROR
                                RoundedRectangle:
                                    radius: [dp(8)]
                                    pos: self.pos
                                    size: self.size
                        Label:
                            id: label_remaining
                            text: "0"
                            font_size: sp(24)
                            color: HEX.PRIMARY
                            bold: True
                            halign: "center"
                            valign: "middle"
                            size_hint_x: 0.5
                        Button:
                            text: "+"
                            font_size: sp(22)
                            bold: True
                            background_normal: ""
                            background_color: HEX.SUCCESS
                            color: 1, 1, 1, 1
                            size_hint_x: 0.25
                            on_release: root.adjust_visit(1)
                            canvas.before:
                                Color:
                                    rgba: HEX.SUCCESS
                                RoundedRectangle:
                                    radius: [dp(8)]
                                    pos: self.pos
                                    size: self.size
                BoxLayout:
                    size_hint_y: None
                    height: dp(52)
                    spacing: dp(8)
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            radius: [dp(10)]
                            pos: self.pos
                            size: self.size
                    Label:
                        text: "Switch:"
                        font_size: sp(14)
                        color: HEX.TEXT_PRIMARY
                        size_hint_x: 0.35
                        halign: "left"
                        valign: "middle"
                        padding: dp(16), 0
                    Spinner:
                        id: spinner_change_type
                        text: "Count"
                        values: ["Count", "Month", "Season", "Year", "Trial"]
                        font_size: sp(15)
                        size_hint_x: 0.45
                        background_normal: ""
                        background_color: HEX.BACKGROUND
                        color: HEX.TEXT_PRIMARY
                        on_text: root.on_type_changed(self.text)
                    Button:
                        text: "OK"
                        font_size: sp(14)
                        color: 1, 1, 1, 1
                        size_hint_x: 0.2
                        background_normal: ""
                        background_color: HEX.PRIMARY
                        on_release: root.change_type()
                        canvas.before:
                            Color:
                                rgba: HEX.PRIMARY
                            RoundedRectangle:
                                radius: [dp(6)]
                                pos: self.pos
                                size: self.size
                BoxLayout:
                    size_hint_y: None
                    height: dp(48)
                    spacing: dp(8)
                    Button:
                        text: "Edit"
                        font_size: sp(14)
                        background_normal: ""
                        background_color: HEX.ACCENT
                        color: 1, 1, 1, 1
                        on_release: root.go_edit()
                        canvas.before:
                            Color:
                                rgba: HEX.ACCENT
                            RoundedRectangle:
                                radius: [dp(6)]
                                pos: self.pos
                                size: self.size
                    Button:
                        text: "QR Code"
                        font_size: sp(14)
                        background_normal: ""
                        background_color: HEX.PRIMARY
                        color: 1, 1, 1, 1
                        on_release: root.go_qr()
                        canvas.before:
                            Color:
                                rgba: HEX.PRIMARY
                            RoundedRectangle:
                                radius: [dp(6)]
                                pos: self.pos
                                size: self.size
                    Button:
                        text: "History"
                        font_size: sp(14)
                        background_normal: ""
                        background_color: HEX.PRIMARY_DARK
                        color: 1, 1, 1, 1
                        on_release: root.go_history()
                        canvas.before:
                            Color:
                                rgba: HEX.PRIMARY_DARK
                            RoundedRectangle:
                                radius: [dp(6)]
                                pos: self.pos
                                size: self.size
                Button:
                    text: "Delete Member"
                    font_size: sp(14)
                    color: HEX.ERROR
                    size_hint_y: None
                    height: dp(44)
                    background_normal: ""
                    background_color: 1, 1, 1, 1
                    on_release: root.confirm_delete()
                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            radius: [dp(6)]
                            pos: self.pos
                            size: self.size
                Widget:
                    size_hint_y: None
                    height: dp(24)

<_InfoRow@BoxLayout>:
    label_text: ""
    value: ""
    size_hint_y: None
    height: dp(28)
    Label:
        text: root.label_text
        font_size: sp(13)
        color: HEX.TEXT_SECONDARY
        size_hint_x: 0.3
        halign: "left"
        valign: "middle"
    Label:
        text: root.value
        font_size: sp(15)
        color: HEX.TEXT_PRIMARY
        size_hint_x: 0.7
        halign: "left"
        valign: "middle"
        text_size: self.size
        shorten: True
"""

class MemberDetailScreen(Screen):
    _member_id = ""
    _original_type = ""

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
        self._original_type = member.get("member_type", "")
        self.ids.title_label.text = member.get("name", "Member")
        self.ids.label_id.text = f"ID: {member['id']}"
        avatar = member.get("avatar_path", "")
        self.ids.avatar_img.source = avatar if (avatar and os.path.isfile(avatar)) else ""
        self.ids.info_name.value = member.get("name", "")
        self.ids.info_phone.value = member.get("phone", "")
        self.ids.info_gender.value = member.get("gender", "") or ""
        self.ids.info_type.value = member.get("member_type", "")
        self.ids.info_notes.value = member.get("notes", "") or ""
        remaining = member.get("remaining", 0)
        self.ids.label_remaining.text = str(remaining)
        if remaining <= 0:
            self.ids.label_remaining.color = (0.957, 0.263, 0.212, 1)
        else:
            self.ids.label_remaining.color = (0.082, 0.396, 0.753, 1)
        self.ids.spinner_change_type.text = self._original_type

    def on_enter(self):
        if self._member_id:
            self.load_member(self._member_id)

    def adjust_visit(self, delta):
        if not self._member_id:
            return
        app = App.get_running_app()
        new_val = app.db.add_visit(self._member_id, delta)
        if new_val is not None:
            self.ids.label_remaining.text = str(new_val)
            if new_val <= 0:
                self.ids.label_remaining.color = (0.957, 0.263, 0.212, 1)
            else:
                self.ids.label_remaining.color = (0.082, 0.396, 0.753, 1)

    def on_type_changed(self, text):
        pass

    def change_type(self):
        if not self._member_id:
            return
        new_type = self.ids.spinner_change_type.text
        app = App.get_running_app()
        if app.db.change_member_type(self._member_id, new_type):
            self._original_type = new_type
            self.ids.info_type.value = new_type

    def confirm_delete(self):
        from kivy.uix.popup import Popup
        content = Builder.load_string("""
BoxLayout:
    orientation: "vertical"
    padding: dp(16)
    spacing: dp(12)
    Label:
        text: "Delete this member? This cannot be undone."
        font_size: sp(15)
        color: (0.13, 0.13, 0.13, 1)
        halign: "center"
        valign: "middle"
    BoxLayout:
        size_hint_y: None
        height: dp(44)
        spacing: dp(12)
        Button:
            text: "Cancel"
            background_color: (0.88, 0.88, 0.88, 1)
            color: (0.13, 0.13, 0.13, 1)
            on_release: popup.dismiss()
        Button:
            text: "Confirm Delete"
            background_color: (0.957, 0.263, 0.212, 1)
            color: (1, 1, 1, 1)
            on_release: root_cb()
""")
        popup = Popup(title="Confirm", content=content, size_hint=(0.8, 0.3), auto_dismiss=False)
        content.root_cb = lambda dt=None: self._do_delete(popup)
        content.popup = popup
        popup.open()

    def _do_delete(self, popup):
        app = App.get_running_app()
        app.db.delete_member(self._member_id)
        from app.qr_manager import get_qr_path
        qr_path = get_qr_path(self._member_id)
        if os.path.isfile(qr_path):
            try:
                os.remove(qr_path)
            except OSError:
                pass
        popup.dismiss()
        self._member_id = ""
        self.go_back()

    def go_edit(self):
        if not self._member_id:
            return
        screen = self.manager.get_screen("edit_member")
        screen.load_member(self._member_id)
        self.manager.current = "edit_member"

    def go_qr(self):
        if not self._member_id:
            return
        screen = self.manager.get_screen("qr_display")
        screen.load_member(self._member_id)
        self.manager.current = "qr_display"

    def go_history(self):
        if not self._member_id:
            return
        screen = self.manager.get_screen("history")
        screen.load_member(self._member_id)
        self.manager.current = "history"

    def go_back(self):
        self.manager.current = "home"