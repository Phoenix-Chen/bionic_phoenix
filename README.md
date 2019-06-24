# Bionic Phoenix
***

## Requirements
***
- [Python 3](https://www.python.org/downloads/)
- [pip](https://pypi.org/project/pip/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation/) (optional)
- Make sure [D-Bus](https://www.freedesktop.org/wiki/Software/dbus/) and [GLib](https://lazka.github.io/pgi-docs/GLib-2.0/index.html) are installed

## Setup
***
- Recommend to use virtual environment. Run:
    ```
    virtualenv -p python3 [envname]
    ```
  Activate with:
    ```
    source [envname]/bin/activate

    ```
- Rename `sample_conf.json` to `conf.json`, and fill all the required info
- To install. Run:
    ```
    ./install.sh
    ```
- To setup D-Bus. Run:
    ```
    dbus-launch
    ```
  The output should look like:
    ```
    DBUS_SESSION_BUS_ADDRESS=unix:abstract=/tmp/dbus-WnoEdNDMmB,guid=[GUID]
    DBUS_SESSION_BUS_PID=[PID]
    ```
  Then run:
    ```
    export DBUS_SESSION_BUS_ADDRESS=unix:abstract=/tmp/dbus-WnoEdNDMmB,guid=[GUID]
    export DBUS_SESSION_BUS_PID=[PID]
    ```
- To run telegram bot. Run:
    ```
    ./activate
    ```

## Future Plan
***
- Make all skill into object with `base_skill` with access checking as parent class
- Add `/dict` for dictionary
