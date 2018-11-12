RED='\033[0;31m'
LIGHTGREEN='\033[1;32m'
NC='\033[0m'

error_check() {
    if [ $? -eq 0 ]; then
        echo -e "${LIGHTGREEN}$1${NC}"
    else
        echo -e "${RED}$2${NC}"
        exit 1
    fi
}

pip install -r requirements.txt
error_check "Python packages installed" "Failed to install python packages"
exit 0
