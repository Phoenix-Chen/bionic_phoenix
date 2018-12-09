import sys
# from traceback import print_exc
import subprocess
from service.utils import make_interface

def main():
    iface = make_interface()
    iface.push_message(1)
    # bus = dbus.SessionBus()
    #
    # try:
    #     remote_object = bus.get_object("com.bionic.PhoenixService",
    #                                    "/Tele")
    #
    #     # you can either specify the dbus_interface in each call...
    #     hello_reply_list = remote_object.HelloWorld("Hello from example-client.py!",
    #         dbus_interface = "com.bionic.PhoenixInterface")
    # except dbus.DBusException:
    #     print_exc()
    #     #print usage
    #     sys.exit(1)
    #
    # print (hello_reply_list)
    #
    # # ... or create an Interface wrapper for the remote object
    # iface = dbus.Interface(remote_object, "com.bionic.PhoenixInterface")
    #
    # hello_reply_tuple = iface.GetTuple()
    #
    # print(hello_reply_tuple)
    #
    # hello_reply_dict = iface.GetDict()
    #
    # print(hello_reply_dict)

    # D-Bus exceptions are mapped to Python exceptions
    # try:
    #     iface.RaiseException()
    # except dbus.DBusException as e:
    #     print(str(e))

    # introspection is automatically supported
    #print(remote_object.Introspect(dbus_interface="org.freedesktop.DBus.Introspectable"))

    # iface.push_message(1)

    if sys.argv[1:] == ['--exit-service']:
        iface.Exit()

if __name__ == '__main__':
    main()
