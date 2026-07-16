"""Edit member screen — modify existing member info with change tracking."""

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
<EditMemberScreen>:
    name: "edit_member"
    avatar_file: ""
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
                text: "编辑资料"
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
                spacing: dp(16)
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
                            text: "会员头像"
                            font_size: sp(15)
                            color: HEX.TEXT_PRIMARY
                            bold: True
                            halign: "left"
                            valign: "bottom"
                            size_hint_y: 0.5
                        Label:
                            text: "点击按钮更换头像"
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
                        text: "拍照"
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
                        text: "从相册选择"
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
                Label:
                    text: "姓名 *"
                    font_size: sp(14)
                    color: HEX.TEXT_PRIMARY
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(24)
                TextInput:
                    id: input_name
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
                Label:
                    text: "手机号 *"
                    font_size: sp(14)
                    color: HEX.TEXT_PRIMARY
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(24)
                TextInput:
                    id: input_phone
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
                Label:
                    text: "性别"
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
                        text: "男"
                        font_size: sp(15)
                        on_release: root.set_gender("男")
                        canvas.before:
                            Color:
                                rgba: (0.88, 0.88, 0.88, 1)
                            RoundedRectangle:
                                radius: [dp(6)]
                                pos: self.pos
                                size: self.size
                    Button:
                        id: btn_female
                        text: "女"
                        font_size: sp(15)
                        on_release: root.set_gender("女")
                        canvas.before:
                            Color:
                                rgba: (0.88, 0.88, 0.88, 1)
                            RoundedRectangle:
                                radius: [dp(6)]
                                pos: self.pos
                                size: self.size
                Label:
                    text: "备注"
                    font_size: sp(14)
                    color: HEX.TEXT_PRIMARY
                    bold: True
                    halign: "left"
                    size_hint_y: None
                    height: dp(24)
                TextInput:
                    id: input_notes
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
                Button:
                    text: "保存修改"
                    font_size: sp(17)
                    bold: True
                    color: 1, 1, 1, 1
                    size_hint_y: None
                    height: dp(52)
                    background_normal: ""
                    background_color: HEX.PRIMARY
                    on_release: root.save_changes()
                    canvas.before:
                        Color:
                            rgba: HEX.PRIMARY
                        RoundedRectangle:
                            radius: [dp(8)]
                            pos: self.pos
                            size: self.size
                Widget:
                    size_hint_y: None
                    height: dp(32)
"""


class EditMemberScreen(Screen):
    """Edit form for an existing member with change tracking."""

    avatar_file = ""
    _member_id = ""
    _gender = ""
    _old_avatar = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)
        os.makedirs(AVATAR_DIR, exist_ok=True)

    def load_member(self, member_id):
        self._member_id = member_id
        app = App.get_running_app()
        member = app.db.get_member(member_id)
        if not member:
            self.go_back()
            return
        self._gender = member.get("gender", "")
        self._old_avatar = member.get("avatar_path", "")
        self.avatar_file = self._old_avatar
        avatar_src = self._old_avatar if (self._old_avatar and os.path.isfile(self._old_avatar)) else ""
        self.ids.avatar_preview.source = avatar_src
        self.ids.input_name.text = member.get("name", "")
        self.ids.input_phone.text = member.get("phone", "")
        self.ids.input_notes.text = member.get("notes", "")
        self._update_gender_buttons()

    def set_gender(self, gender):
        self._gender = gender
        self._update_gender_buttons()

    def _update_gender_buttons(self):
        btn_m = self.ids.btn_male
        btn_f = self.ids.btn_female
        if self._gender == "男":
            btn_m.background_color = (0.082, 0.396, 0.753, 1)
            btn_m.color = (1, 1, 1, 1)
            btn_f.background_color = (0.88, 0.88, 0.88, 1)
            btn_f.color = (0.13, 0.13, 0.13, 1)
        elif self._gender == "女":
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
        try:
            from plyer import camera
            filename = os.path.join(AVATAR_DIR, f"photo_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
            camera.take_picture(filename=filename, on_complete=lambda p: self._on_avatar_selected(p))
        except (ImportError, NotImplementedError):
            self._show_popup("提示", "当前环境不支持拍照功能，请从相册选择图片。")

    def pick_gallery(self):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self._on_gallery_selected, filters=[["Images", "*.jpg", "*.jpeg", "*.png", "*.bmp"]])
        except (ImportError, NotImplementedError):
            self._show_popup("提示", "当前环境不支持相册功能。")

    def _on_gallery_selected(self, selection):
        if selection and len(selection) > 0:
            self._on_avatar_selected(selection[0])

    def _on_avatar_selected(self, source_path):
        if not source_path or not os.path.isfile(source_path):
            return
        ext = os.path.splitext(source_path)[1] or ".jpg"
        dest = os.path.join(AVATAR_DIR, f"avatar_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}")
        shutil.copy2(source_path, dest)
        self.avatar_file = dest
        self.ids.avatar_preview.source = dest

    def save_changes(self):
        name = self.ids.input_name.text.strip()
        phone = self.ids.input_phone.text.strip()
        if not name:
            self._show_popup("提示", "请输入会员姓名。")
            return
        if not phone:
            self._show_popup("提示", "请输入手机号。")
            return
        updates = {"name": name, "phone": phone, "gender": self._gender, "notes": self.ids.input_notes.text.strip()}
        if self.avatar_file != self._old_avatar:
            updates["avatar_path"] = self.avatar_file
        app = App.get_running_app()
        changed = app.db.update_member(self._member_id, **updates)
        if changed:
            self._show_popup("成功", f"已保存 {len(changed)} 项修改。")
        else:
            self._show_popup("提示", "没有检测到任何修改。")

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
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.35), auto_dismiss=True)
        popup.open()

    def go_back(self):
        self.manager.current = "member_detail"
