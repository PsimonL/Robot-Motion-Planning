# no_episodes = 30
#
#
# def help():
#     x = int(input("Podaj"))
#     if x == 1:
#         return True
#     if x == 0:
#         return False
#
#
# for episode in range(no_episodes):
#     print(f"EPISODE{episode}")
#     episode_flag = True
#     print(f"STATUS OF EPISODE_FLAG = {episode_flag}")
#
#     while episode_flag:
#
#         check = help()
#         if check:
#             print("EPISODE_FLAG TURNED TO FALSE")
#             episode_flag = False
#         if not check:
#             print("Sorry!")
#             break


import math
import time


def length():
    return math.dist([242, 322], [235, 786])


start_time = time.time()
for x in range(30_000):
    print(x)
    length()
end_time = time.time()
print("DONE")
print(f"Total time = {end_time - start_time}")
