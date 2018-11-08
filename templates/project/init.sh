DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
sed -i "s/__PROJECT_NAME__/$1/g" "$DIR/CMakeLists.txt"
