with open('lord_of_the_ring.txt') as f:
    word_count = 0
    word_dict = {}
    for line in f:
        for word in line.split():
            word_count +=1
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
i= 0
for word in word_dict:
    print(word_dict[word])
    i +=1
    if i == 5:
        break