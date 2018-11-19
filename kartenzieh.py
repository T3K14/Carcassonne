j = True
inp = (input("hier\n")).split(" ")
while j:
    if int(inp[0]) in (range(10)):
        l = len(inp)


        #für jedes element in inputliste wird position festgestellt, wenn len=6 dann entspricht inp[0] der nummer und so
        #  weiter
        #aber ohne if len ==... nr = inp[0], ...
        #davor länge festlegen und falls länge länger als abcdmlschild, dann differenz abklären und dann ist labcdm
        # gleich dem i ten element    #auch nicht die ideallösung

        #nr,a,b,c,d,m,schild = except valuerror, dann differenz und = inp[i]

        liste = [inp[pos] for pos in inp ]
        print(liste)
        #nr,a,b,c,d,m,schild =


        #info = [a,b,c,d,m,schild]
