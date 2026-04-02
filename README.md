# Connect Four AI
plan:
1. add proper performance testing
2. add more algorithms (e.g. negamax), algorithm selector (either UI or console input)
3. move ordering
4. trim down computation done
    a. (theory) track "touched" rows, since empty rows won't have anything worth searching
    b. trim scans to only those rows and cut down computation time
5. record-keeping (write to .txt file with game record, algorithm used and performance data)
6. make ai play against itself