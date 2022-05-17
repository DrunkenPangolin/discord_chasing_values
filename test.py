

from tempfile import tempdir


f = open("/home/sam/Coding/discord_chasing_values/inactive.csv", "r")
temp = f.readlines()
inactive = []
for name in temp:
    inactive.append(name.split()[2])


print(inactive)