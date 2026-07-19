"""Home screen ??? member list with search and quick actions."""

import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
AVATAR_DIR = os.path.join(DATA_DIR, "avatars")


KV = """
#:import HEX app.theme

<MemberCard@BoxLayout>:
    member_id: ""
    name: ""
    member_type: ""
    remaining: 0
    avatar_path: ""
    size_hint_y: None
    height: dp(72)
    padding: dp(8)
    spacing: dp(12)
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            radius: [dp(8)]
            pos: self.pos
            size: self.size
    BoxLayout:
        size_hint: None, None
        size: dp(56), dp(56)
        canvas.before:
            Color:
                rgba: 0.88, 0.92, 0.98, 1
            Ellipse:
                pos: self.pos
                size: self.size
        AsyncImage:
            source: root.avatar_path if root.avatar_path and root.avatar_path.strip() else ""
            size_hint: None, None
            size: dp(48), dp(48)
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            allow_stretch: True
            keep_ratio: True
    BoxLayout:
        orientation: "vertical"
        size_hint_x: 0.55
        Label:
            text: root.name
            font_size: sp(16)
            color: HEX.TEXT_PRIMARY
            bold: True
            halign: "left"
            valign: "middle"
            text_size: self.size
            shorten: True
        Label:
            text: root.member_type + "  ??  ID: " + root.member_id
            font_size: sp(12)
            color: HEX.TEXT_SECONDARY
            halign: "left"
            valign: "middle"
            text_size: self.size
    BoxLayout:
        size_hint_x: 0.25
        orientation: "vertical"
        Label:
            text: str(root.remaining) + "???"
            font_size: sp(18)
            color: HEX.PRIMARY if root.remaining > 0 else HEX.ERROR
            bold: True
            halign: "right"
            valign: "middle"
        Label:
            text: "??????"
            font_size: sp(11)
            color: HEX.TEXT_SECONDARY
            halign: "right"
            valign: "middle"
    Label:
        text: ">"
        font_size: sp(18)
        color: HEX.TEXT_SECONDARY
        size_hint_x: None
        width: dp(24)
        halign: "center"
        valign: "middle"


<HomeScreen>:
    name: "home"
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
            Label:
                text: "??????????????????"
                font_size: sp(20)
                color: 1, 1, 1, 1
                bold: True
                halign: "left"
                valign: "middle"
                size_hint_x: 0.8
            Button:
                text: "??????"
                font_size: sp(14)
                color: 1, 1, 1, 1
                size_hint_x: 0.2
                size_hint_y: None
                height: dp(40)
                background_normal: ""
                background_color: HEX.PRIMARY_DARK
                on_release: root.go_scan()
                canvas.before:
                    Color:
                        rgba: HEX.PRIMARY_DARK
                    RoundedRectangle:
                        radius: [dp(20)]
                        pos: self.pos
                        size: self.size

        # Search bar
        BoxLayout:
            size_hint_y: None
            height: dp(52)
            padding: dp(12), dp(6)
            TextInput:
                id: search_input
                hint_text: "?????????????????????????????????ID"
                font_size: sp(15)
                multiline: False
                background_normal: ""
                background_color: 1, 1, 1, 1
                foreground_color: HEX.TEXT_PRIMARY
                cursor_color: HEX.PRIMARY
                padding: dp(12), dp(10)
                on_text: root.on_search(self.text)
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    RoundedRectangle:
                        radius: [dp(22)]
                        pos: self.pos
                        size: self.size

        # Separator
        BoxLayout:
            size_hint_y: None
            height: dp(1)
            canvas.before:
                Color:
                    rgba: 0.9, 0.9, 0.9, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

        # Member list
        ScrollView:
            id: scroll_view
            do_scroll_x: False
            BoxLayout:
                id: member_list
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(12), dp(8)
                spacing: dp(8)

        # Empty state (hidden by default)
        BoxLayout:
            id: empty_state
            orientation: "vertical"
            size_hint_y: 0.6
            opacity: 0
            disabled: True
            Label:
                text: "????????????"
                font_size: sp(18)
                color: HEX.TEXT_SECONDARY
                halign: "center"
                valign: "bottom"
                size_hint_y: 0.6
            Label:
                text: "??????????????? + ?????????????????????"
                font_size: sp(14)
                color: HEX.TEXT_SECONDARY
                halign: "center"
                valign: "top"
                size_hint_y: 0.4

    # FAB
    FloatLayout:
        Button:
            text: "+"
            font_size: sp(28)
            color: 1, 1, 1, 1
            size_hint: None, None
            size: dp(56), dp(56)
            pos_hint: {"right": 0.92, "y": 0.05}
            background_normal: ""
            background_color: HEX.PRIMARY
            on_release: root.go_add()
            canvas.before:
                Color:
                    rgba: HEX.PRIMARY
                Ellipse:
                    pos: self.pos
                    size: self.size
"""


class HomeScreen(Screen):
    """Main screen showing the member list with search functionality."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)

    def on_enter(self):
        """Refresh the member list every time this screen is shown."""
        self.refresh_list()

    def refresh_list(self, search=""):
        """Rebuild the member list from the database."""
        app = App.get_running_app()
        members = app.db.get_all_members(search)

        container = self.ids.member_list
        container.clear_widgets()
        empty = self.ids.empty_state

        if not members:
            empty.opacity = 1
            empty.disabled = False
            return

        empty.opacity = 0
        empty.disabled = True

        for m in members:
            avatar = m.get("avatar_path", "")
            if avatar and not os.path.isfile(avatar):
                avatar = ""
            card_layout = Builder.load_string("""
<MemberCard>:
""")
            # Build card manually since dynamic class loading is tricky
            from kivy.factory import Factory
            card = Factory.MemberCard()
            card.member_id = m["id"]
            card.name = m["name"]
            card.member_type = m["member_type"]
            card.remaining = m["remaining"]
            card.avatar_path = avatar
            card.bind(on_touch_down=self._make_card_tap(m["id"]))
            container.add_widget(card)

    def _make_card_tap(self, member_id):
        """Return a callback that navigates to the member detail screen."""
        def on_tap(instance, touch):
            if instance.collide_point(*touch.pos):
                self.go_detail(member_id)
                return True
            return False
        return on_tap

    def on_search(self, text):
        """Filter the member list as the user types."""
        self.refresh_list(text.strip())

    def go_detail(self, member_id):
        """Navigate to member detail screen."""
        screen = self.manager.get_screen("member_detail")
        screen.load_member(member_id)
        self.manager.current = "member_detail"

    def go_add(self):
        self.manager.current = "add_member"

    def go_scan(self):
        self.manager.current = "scan"
