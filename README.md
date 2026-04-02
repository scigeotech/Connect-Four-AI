# Connect Four AI
plan:
1. add proper performance testing
2. add more algorithms (e.g. negamax) algorithm selector
3. trim down computation done
    a. (theory) track "touched" rows, since empty rows won't have anything worth searching
    b. trim scans to only those rows and cut down computation time
4. record-keeping (write to .txt file with game record, algorithm used and performance data)
5. make ai play against itself