word_m10_count = 0
with open('lord_of_the_ring.txt','r') as file:
    for line in file:
        for word in line.split():
           if len(word)>10:
               word_m10_count+=1

print(word_m10_count)



