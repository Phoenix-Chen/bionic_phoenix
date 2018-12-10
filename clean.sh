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

find . -type d -name __pycache__ -delete -exec rm -rf {} \;
error_check "Deleted all __pycache__" "Failed to delete all __pycache__"
exit 0
