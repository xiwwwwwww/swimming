"""Swim Pool Membership Manager - Application Entry Point."""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from app.database import Database
from app.screens.home import HomeScreen
from app.screens.add_member import AddMemberScreen
from app.screens.member_detail import MemberDetailScreen
from app.screens.edit_member import EditMemberScreen
from app.screens.scan import ScanScreen
from app.screens.qr_display import QRDisplayScreen
from app.screens.history import HistoryScreen


Window.softinput_mode = "below_target"


class SwimPoolApp(App):
    """Main application class for the Swim Pool Membership Manager."""

    title = "??????????????????"

    def build(self):
        self.db = Database()
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(AddMemberScreen(name="add_member"))
        sm.add_widget(MemberDetailScreen(name="member_detail"))
        sm.add_widget(EditMemberScreen(name="edit_member"))
        sm.add_widget(ScanScreen(name="scan"))
        sm.add_widget(QRDisplayScreen(name="qr_display"))
        sm.add_widget(HistoryScreen(name="history"))
        return sm

    def on_stop(self):
        self.db.close()


if __name__ == "__main__":
    SwimPoolApp().run()
