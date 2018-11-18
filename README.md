# Bionic Phoenix
***

## Requirements
***
- [Python 3](https://www.python.org/downloads/)
- [pip](https://pypi.org/project/pip/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation/) (optional)

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
- To run telegram bot. Run:
    ```
    ./activate
    ```

## Future Plan
***
- Make all skill into object with `base_skill` with access checking as parent class
- Add `/dict` for dictionary
- Add `/lyrics` for lyrics using Genius API
