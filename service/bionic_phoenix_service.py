import sys
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib
from telegram import Bot
from service.bionic_phoenix_process import BionicPhoenixProcess, STATUS
import subprocess

class BionicPhoenixService(dbus.service.Object):
    def __init__(self, telegram_token, chat_id):
        self.telegram_token = telegram_token
        self.chat_id = chat_id
        self.processes = dict()

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        session_bus = dbus.SessionBus()
        name = dbus.service.BusName("com.bionic.PhoenixService", session_bus)
        dbus.service.Object.__init__(self, dbus.SessionBus(), '/Tele')

        self.mainloop = GLib.MainLoop()
        print("Running com.bionic.PhoenixService")
        self.mainloop.run()

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='is', out_signature='')
    def add_process(self, pid, command):
        self.processes[pid] = BionicPhoenixProcess(pid, command)

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='ii', out_signature='')
    def update_process(self, pid, status):
        self.processes[pid].update(int(status))
        bot = Bot(self.telegram_token)
        bot.send_message(self.chat_id, self.processes[pid].to_string())

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='i', out_signature='s')
    def terminate_process(self, pid):
        stdout = subprocess.getoutput("kill -9 " + str(pid))
        return stdout

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='', out_signature='as')
    def get_processes(self):
        l = list()
        for ps in self.processes.values():
            l.append(ps.to_string())
        return l

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='', out_signature='as')
    def clean(self):
        """
            Delete processes that are already finished running
        """
        for pid in list(self.processes.keys()):
            if self.processes[pid].status != STATUS.RUNNING:
                del self.processes[pid]
        return self.get_processes()

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='s', out_signature='')
    def set_token(self, telegram_token):
        self.telegram_token = telegram_token

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='i', out_signature='')
    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    @dbus.service.method("com.bionic.PhoenixInterface", in_signature='', out_signature='')
    def Exit(self):
        self.mainloop.quit()
