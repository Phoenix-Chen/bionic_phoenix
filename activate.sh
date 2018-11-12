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

python -m bot -c ./conf.json
error_check "Bionic Phoenix Deactivated" "Bionic Phoenix Failed"
exit 0
