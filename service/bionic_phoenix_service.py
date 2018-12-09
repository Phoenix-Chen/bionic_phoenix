import sys
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
from telegram import Bot

class BionicPhoenixService(dbus.service.Object):
    def __init__(self, telegram_token, chat_id):
        self.telegram_token = telegram_token
        self.chat_id = chat_id
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        session_bus = dbus.SessionBus()
        name = dbus.service.BusName("com.bionic.PhoenixService", session_bus)
        dbus.service.Object.__init__(self, dbus.SessionBus(), '/Tele')

        self.mainloop = GLib.MainLoop()
        print("Running com.bionic.PhoenixService")
        self.mainloop.run()

    # @dbus.service.method("com.bionic.PhoenixInterface", in_signature='s', out_signature='as')
    # def HelloWorld(self, hello_message):
    #     print (str(hello_message))
    #     return ["Hello", " from example-service.py", "with unique name"]
    #
    # @dbus.service.method("com.bionic.PhoenixInterface", in_signature='', out_signature='(ss)')
    # def GetTuple(self):
    #     return ("Hello Tuple", " from example-service.py")
    #
    # @dbus.service.method("com.bionic.PhoenixInterface", in_signature='', out_signature='a{ss}')
    # def GetDict(self):
    #     return {"first": "Hello Dict", "second": " from example-service.py"}

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='', out_signature='')
    def push_message(self, status):
        bot = Bot(self.telegram_token)
        bot.send_message(self.chat_id, "what")

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='s', out_signature='')
    def set_token(self, telegram_token):
        self.telegram_token = telegram_token

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='i', out_signature='')
    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='', out_signature='')
    def Exit(self):
        self.mainloop.quit()
