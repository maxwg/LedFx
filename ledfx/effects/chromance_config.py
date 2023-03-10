def headof(S):
    return (S - 1) * 14

def tailof(S):
    return headof(S) + 13

# Beam 0 is at 12:00 and advance clockwise
# -1 means nothing connected on that side
nodeConnections = [
    [-1, -1, 1, -1, 0, -1],
    [-1, -1, 3, -1, 2, -1],
    [-1, -1, 5, -1, 4, -1],
    [-1, 0, 6, 12, -1, -1],
    [-1, 2, 8, 14, 7, 1],
    [-1, 4, 10, 16, 9, 3],
    [-1, -1, -1, 18, 11, 5],
    [-1, 7, -1, 13, -1, 6],
    [-1, 9, -1, 15, -1, 8],
    [-1, 11, -1, 17, -1, 10],
    [12, -1, 19, -1, -1, -1],
    [14, -1, 21, -1, 20, -1],
    [16, -1, 23, -1, 22, -1],
    [18, -1, -1, -1, 24, -1],
    [13, 20, 25, 29, -1, -1],
    [15, 22, 27, 31, 26, 21],
    [17, 24, -1, 33, 28, 23],
    [-1, 26, -1, 30, -1, 25],
    [-1, 28, -1, 32, -1, 27],
    [29, -1, 34, -1, -1, -1],
    [31, -1, 36, -1, 35, -1],
    [33, -1, -1, -1, 37, -1],
    [30, 35, 38, -1, -1, 34],
    [32, 37, -1, -1, 39, 36],
    [-1, 39, -1, -1, -1, 38]
]
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
#     [-1, -1, -1, -1, -1, -1],
# ]

# First member: Node closer to ceiling
# Second: Node closer to floor
segmentConnections = [
    [0, 3],
    [0, 4],
    [1, 4],
    [1, 5],
    [2, 5],
    [2, 6],
    [3, 7],
    [4, 7],
    [4, 8],
    [5, 8],
    [5, 9],
    [6, 9],
    [3, 10],
    [7, 14],
    [4, 11],
    [8, 15],
    [5, 12],
    [9, 16],
    [6, 13],
    [10, 14],
    [11, 14],
    [11, 15],
    [12, 15],
    [12, 16],
    [13, 16],
    [14, 17],
    [15, 17],
    [15, 18],
    [16, 18],
    [14, 19],
    [17, 22],
    [15, 20],
    [18, 23],
    [16, 21],
    [19, 22],
    [20, 22],
    [20, 23],
    [21, 23],
    [22, 24],
    [23, 24]
]

# ledAssignments = [
# [2, headof(3), tailof(3)],
# [2, tailof(2), headof(2)],
# [1, headof(10), tailof(10)],
# [1, tailof(9), headof(9)],
# [1, headof(4), tailof(4)],
# [1, tailof(3), headof(3)],
# [2, tailof(6), headof(6)],
# [3, tailof(11), headof(11)],
# [1, headof(11), tailof(11)],
# [1, tailof(8), headof(8)],
# [1, headof(12), tailof(12)],
# [0, tailof(11), headof(11)],
# [2, headof(4), tailof(4)],
# [3, tailof(10), headof(10)],
# [2, tailof(1), headof(1)],
# [1, tailof(7), headof(7)],
# [1, headof(5), tailof(5)],
# [0, tailof(10), headof(10)],
# [1, tailof(2), headof(2)],
# [2, headof(5), tailof(5)],
# [3, tailof(4), headof(4)],
# [3, headof(5), tailof(5)],
# [0, headof(5), tailof(5)],
# [0, tailof(4), headof(4)],
# [1, tailof(1), headof(1)],
# [3, tailof(9), headof(9)],
# [0, headof(6), tailof(6)],
# [1, tailof(6), headof(6)],
# [0, tailof(9), headof(9)],
# [3, tailof(3), headof(3)],
# [3, tailof(8), headof(8)],
# [3, headof(6), tailof(6)],
# [0, tailof(8), headof(8)],
# [0, tailof(3), headof(3)],
# [3, tailof(2), headof(2)],
# [3, headof(7), tailof(7)],
# [0, headof(7), tailof(7)],
# [0, tailof(2), headof(2)],
# [3, tailof(1), headof(1)],
# [0, tailof(1), headof(1)]
# ]
# print(len([x for x in ledAssignments if x[0] == 0]))
# print(len([x for x in ledAssignments if x[0] == 1]))
# print(len([x for x in ledAssignments if x[0] == 2]))
# print(len([x for x in ledAssignments if x[0] == 3]))
#
# ledAssignments2 = []
# offsets = [17, 28, 11, 0]
# for l in ledAssignments:
#     offset = offsets[l[0]] * 14
#     ledAssignments2.append([l[1] + offset, l[2] + offset])
# #
# print(ledAssignments2)
ledAssignments = [[182, 195], [181, 168], [518, 531], [517, 504], [434, 447], [433, 420], [237, 224], [153, 140], [532, 545], [503, 490], [546, 559], [391, 378], [196, 209], [139, 126], [167, 154], [489, 476], [448, 461], [377, 364], [419, 406], [210, 223], [55, 42], [56, 69], [294, 307], [293, 280], [405, 392], [125, 112], [308, 321], [475, 462], [363, 350], [41, 28], [111, 98], [70, 83], [349, 336], [279, 266], [27, 14], [84, 97], [322, 335], [265, 252], [13, 0], [251, 238]]

numberOfBorderNodes = 10
borderNodes = [0, 1, 2, 3, 6, 10, 13, 19, 21, 24]

numberOfCubeNodes = 8
cubeNodes = [7, 8, 9, 11, 12, 17, 18]

starburstNode = 15