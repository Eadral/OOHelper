set -v

rm test.in

python3 ~/Develop/PyCharm/OOHelper/gen9.py

time java -jar "$1.jar" < test.in > "$1.out"
time java -jar "$2.jar" < test.in > "$2.out"

diff "$1.out" "$2.out"

while [[ "$?" == "0" ]]; do

    rm test.in

    python3 ~/Develop/PyCharm/OOHelper/gen9.py

    time java -jar "$1.jar" < test.in > "$1.out"
    time java -jar "$2.jar" < test.in > "$2.out"

    diff "$1.out" "$2.out"

done

