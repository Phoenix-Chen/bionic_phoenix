import sys
import threading
from service.bionic_phoenix_service import BionicPhoenixService
import dbus

def start_service(telegram_token=None, chat_id=None):
    thread = threading.Thread(target=BionicPhoenixService, args=(telegram_token, chat_id))
    thread.setDaemon(True)
    thread.start()

def make_interface():
    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("com.bionic.PhoenixService", "/Tele")
        print(remote_object.Introspect(dbus_interface="org.freedesktop.DBus.Introspectable"))
        iface = dbus.Interface(remote_object, "com.bionic.PhoenixInterface")
        return iface
    except dbus.DBusException as dbe:
        print(dbe)
        sys.exit(1)

def set_service(telegram_token, chat_id):
    """
        Set Telegram token and chat_id for BionicPhoenixService
    """
    iface = make_interface()
    iface.set_token(telegram_token)
    iface.set_chat_id(chat_id)
