import sys
from service.bionic_phoenix_service import BionicPhoenixService
import dbus
from multiprocessing import Process

def start_service(telegram_token=None, chat_id=None):
    """
    Start BionicPhoenixService from a seperate process
    """
    # Use multiprocessing instead of threading
    # Since accessing the interface (in skills.tele)
    # seem to cause some problem if using the same pid
    p = Process(target=BionicPhoenixService, args=(telegram_token, chat_id))
    p.start()

def make_interface():
    bus = dbus.SessionBus()
    try:
        remote_object = bus.get_object("com.bionic.PhoenixService", "/Tele")
        # print(remote_object.Introspect(dbus_interface="org.freedesktop.DBus.Introspectable"))
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
