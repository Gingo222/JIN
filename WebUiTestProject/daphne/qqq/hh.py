a = [2,1, 3, 8, 5, 4]


def new_sort(li):
    for i in range(0, len(li)):
        for j in range(i, len(li)-1):
            if li[i] > li[j+1]:
                li[i], li[j+1] = li[j+1], li[i]
    return li


print new_sort(a)