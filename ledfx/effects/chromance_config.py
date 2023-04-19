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

led_order = [195, 194, 193, 192, 191, 190, 189, 188, 187, 186, 185, 184, 183, 182, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 531, 530, 529, 528, 527, 526, 525, 524, 523, 522, 521, 520, 519, 518, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 447, 446, 445, 444, 443, 442, 441, 440, 439, 438, 437, 436, 435, 434, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 545, 544, 543, 542, 541, 540, 539, 538, 537, 536, 535, 534, 533, 532, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 559, 558, 557, 556, 555, 554, 553, 552, 551, 550, 549, 548, 547, 546, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 209, 208, 207, 206, 205, 204, 203, 202, 201, 200, 199, 198, 197, 196, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 461, 460, 459, 458, 457, 456, 455, 454, 453, 452, 451, 450, 449, 448, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 223, 222, 221, 220, 219, 218, 217, 216, 215, 214, 213, 212, 211, 210, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 69, 68, 67, 66, 65, 64, 63, 62, 61, 60, 59, 58, 57, 56, 307, 306, 305, 304, 303, 302, 301, 300, 299, 298, 297, 296, 295, 294, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 321, 320, 319, 318, 317, 316, 315, 314, 313, 312, 311, 310, 309, 308, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 83, 82, 81, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85, 84, 335, 334, 333, 332, 331, 330, 329, 328, 327, 326, 325, 324, 323, 322, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251]