from gi.repository import GLib
import dbus
import dbus.service
import dbus.mainloop.glib

# class DemoException(dbus.DBusException):
#     _dbus_error_name = 'com.example.DemoException'

class Tele(dbus.service.Object):

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='s', out_signature='as')
    def HelloWorld(self, hello_message):
        print (str(hello_message))
        return ["Hello", " from example-service.py", "with unique name",
                session_bus.get_unique_name()]

    # @dbus.service.method("com.bionic.PhoenixInterface",
    #                      in_signature='', out_signature='')
    # def RaiseException(self):
    #     raise DemoException('The RaiseException method does what you might '
    #                         'expect')

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='', out_signature='(ss)')
    def GetTuple(self):
        return ("Hello Tuple", " from example-service.py")

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='', out_signature='a{ss}')
    def GetDict(self):
        return {"first": "Hello Dict", "second": " from example-service.py"}

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='', out_signature='')
    def Exit(self):
        mainloop.quit()


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("com.bionic.PhoenixService", session_bus)
    object = Tele(session_bus, '/Tele')

    mainloop = GLib.MainLoop()
    print("Running example service.")
    #print(usage)
    mainloop.run()
