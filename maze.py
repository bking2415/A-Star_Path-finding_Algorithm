# Simple creating a maze example

cols = 5
rows = 5

listClicks = [[0, 0], [1, 1], [2, 3], [4, 4]]


def maze(list):
    # Create maze to maneuver
    output = [[0 for y in range(cols)] for x in range(rows)]
    # print(output)
    # Transverse the output
    for i in list:
        output[i[1]][i[0]] = 1
    return output


print(maze(listClicks))
