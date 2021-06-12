import numpy

DIMENSIONS = (101, 101)
array = numpy.full(DIMENSIONS, 29800, dtype = numpy.float)
array2 = numpy.full(DIMENSIONS, 1, dtype = numpy.float)
array[1, 1] = 22300
array[1, -2] = 37300

while True:
    array = (array + numpy.roll(array, 1) + numpy.roll(array, -1) + numpy.roll(array, 1, axis=0) + numpy.roll(array, -1, axis=0) )/5

    array[1, 1] = 22300
    array[1, -2] = 37300

    array2[:, :] = 1
    array2[array[:, :] > 32300] = 2

    array2[array[:, :] < 27300] = 0

    print(array[1, DIMENSIONS[1]//2])
    #print(sum(sum(array)))
    input()
    #input((array2[1, :]))
    #print(array[1, 2] - array[1, 1], array[1, 8] - array[1, 7])
    #input()
