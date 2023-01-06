right = ["        *", "        *", "        *" , "        *", "        *", "        *", "        *"]

left = ["*        ", "*        ", "*        ",  "*        ", "*        ", "*        ", "*        "]

horizontal = [""]

line = "* * * * * * * * * * * * * * * * * * * * * *"

centre = ["            ", "            ", "            ", "            ", "            ", "            ", "            ",  "            "]

oh = ["            ", "    ****    ", "  *      *  ", "  *      *  ", "  *      *  ", "    ****    ", "            "]

ex = ["            ", "  *       * ", "    *   *   ", "      *     ", "    *   *   ", "  *       * ", "            "]

# ex = ["          ", " *      * ", "   *   *  ", "   *   *  ", " *      * ", "          "]
# oh = ["          ", "   ****   ", "  *    *  ", "  *    *  ", "   ****   ", "          "]


vertical = ["*", "*", "*", "*", "*","*", "*", "*"]
print(len(vertical))
# for line in oh:
#   print(line)


top_positions = [centre, vertical, centre, vertical, centre]

# test = list(zip(centre, vertical, oh, vertical, centre))


test_2 = list(zip(*top_positions))
top_positions[2] = oh
top_positions[4] = ex
top_positions[0] = oh
test_3 = list(zip(*top_positions))

for each in test_2:
  print(each[0], each[1], each[2], each[3], each[4])
print(line)
for each in test_3:
  print(each[0], each[1], each[2], each[3], each[4])
print(line)
for each in test_2:
  print(each[0], each[1], each[2], each[3], each[4])
# exit()


# for each in test:
#   print(each[0], each[1], each[2], each[3], each[4])

# print(line)
# test = list(zip(right, oh, left))
# for each in test:
#   print(each[0], each[1], each[2])
