"""Modification history screen showing a timeline of all changes for a member."""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label


KV = """
#:import HEX app.theme
<HistoryScreen>:
    name: "history"
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
        ScrollView:
            id: scroll_view
            do_scroll_x: False
            BoxLayout:
                id: log_list
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(16), dp(12)
                spacing: dp(10)
"""


class HistoryScreen(Screen):
    """Timeline view of modification history for a member."""

    _member_id = ""
    FIELD_LABELS = {
        "name": "??????",
        "phone": "?????????",
        "gender": "??????",
        "member_type": "????????????",
        "remaining": "????????????",
        "notes": "??????",
        "avatar_path": "??????",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)

    def load_member(self, member_id):
        self._member_id = member_id
        self._refresh_logs()

    def on_enter(self):
        if self._member_id:
            self._refresh_logs()

    def _refresh_logs(self):
        container = self.ids.log_list
        container.clear_widgets()
        if not self._member_id:
            return
        app = App.get_running_app()
        logs = app.db.get_modification_log(self._member_id)
        if not logs:
            no_log = Builder.load_string("""
BoxLayout:
    orientation: "vertical"
    size_hint_y: None
    height: dp(120)
    Label:
        text: "??????????????????"
        font_size: sp(16)
        color: HEX.TEXT_SECONDARY
        halign: "center"
        valign: "middle"
""")
            container.add_widget(no_log)
            return
        for log_entry in logs:
            field_cn = self.FIELD_LABELS.get(log_entry["field_name"], log_entry["field_name"])
            old_val = log_entry.get("old_value", "") or "(???)"
            new_val = log_entry.get("new_value", "") or "(???)"
            timestamp = log_entry.get("timestamp", "")
            # Build entry card
            card = Builder.load_string("""
BoxLayout:
    orientation: "vertical"
    size_hint_y: None
    height: self.minimum_height
    padding: dp(14)
    spacing: dp(4)
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            radius: [dp(8)]
            pos: self.pos
            size: self.size
    Label:
        text: root.timestamp
        font_size: sp(12)
        color: HEX.TEXT_SECONDARY
        halign: "left"
        valign: "middle"
        size_hint_y: None
        height: dp(20)
    Label:
        text: root.summary
        font_size: sp(15)
        color: HEX.TEXT_PRIMARY
        halign: "left"
        valign: "middle"
        size_hint_y: None
        height: dp(24)
        text_size: self.size
""")
            card.timestamp = timestamp
            card.summary = f"{field_cn}: {old_val} -> {new_val}"
            container.add_widget(card)

    def go_back(self):
        self.manager.current = "member_detail"
