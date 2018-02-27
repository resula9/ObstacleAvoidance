
voltage = [7 0.29, 0.25, 0.32, 0.34, 0.48, 0.41, 0.45]
x_1 = 0
p_1 = 1
r = 0.1

for i in range(50):

    k = p_1 / (p_1 + r)
    x = x_1 + k * (voltage[i] - x_1)

    p = (1-k) * p_1

    print x
    print k
    print p
    print '/n'

    x_1 = x
    p_1 = p






