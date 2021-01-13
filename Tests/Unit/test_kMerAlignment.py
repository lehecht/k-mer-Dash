from src.kMerAlignmentData import KMerAlignmentData
from src.processing import Processing


def test_processData():
    testData = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]

    # Test1 without peak position
    # Preparation
    k = 5
    top = 3
    peak = None
    process = Processing(testData, None, k, peak, top,None)

    # execution
    algnmList, f1, f2 = KMerAlignmentData.processData(process)

    algnm1 = algnmList[0]
    algnm2 = algnmList[1]

    algnm1_list = [str(e.seq) for e in algnm1]
    algnm2_list = [str(e.seq) for e in algnm2]

    # testing
    assert len(algnm1_list) == 3
    assert len(algnm2_list) == 6
    assert algnm1_list == ['---AACCC', '---ACCCC', 'AAAAA---']
    assert algnm2_list == ['TTTGG---', 'GTTGG---', '-TTGGG--', '--TGGGG-', '--GGGGC-', '---GGGCA']
    assert f1 == "testFile1.fa"
    assert f2 == "testFile2.fa"

    # # Test2 with peak-position
    # Preparation
    k = 5
    top = 3
    peak = 2
    process2 = Processing(testData, None, k, peak, top,None)

    # execution
    algnmList, f1, f2 = KMerAlignmentData.processData(process2)

    algnm1 = algnmList[0]
    algnm2 = algnmList[1]

    # testing
    assert len(algnm1) == 5
    assert len(algnm2) == 5
    assert algnm1 == ['----Aaccc', '---aAacc-', '---cAacc-', '---aAaaa-', '----Aaaaa']
    assert algnm2 == ['----Ttggg', '---tTtgg-', '---gTtgg-', '---tGggg-', '----Ggggc']
    assert f1 == "testFile1.fa"
    assert f2 == "testFile2.fa"

    # # Test3 with peak-position at end of string
    # Preparation
    k = 5
    top = 3
    peak = 7
    process3 = Processing(testData, None, k, peak, top,None)

    # execution
    algnmList, f1, f2 = KMerAlignmentData.processData(process3)

    algnm1 = algnmList[0]
    algnm2 = algnmList[1]

    # testing
    assert len(algnm1) == 1
    assert len(algnm2) == 2
    assert algnm1 == ['acccC----']
    assert algnm2 == ['tgggG----', 'gggcA----']
    assert f1 == "testFile1.fa"
    assert f2 == "testFile2.fa"

    # # Test4 with peak-position at start of string
    # Preparation
    k = 5
    top = 3
    peak = 1
    process4 = Processing(testData, None, k, peak, top,None)

    # execution
    algnmList, f1, f2 = KMerAlignmentData.processData(process4)

    algnm1 = algnmList[0]
    algnm2 = algnmList[1]

    print(process4.getTopKmer())
    print(algnm1)
    print(algnm2)

    # testing
    assert len(algnm1) == 0
    assert len(algnm2) == 3
    assert algnm1 == []
    assert algnm2 == ['----Tttgg', '----Gttgg', '----Tgggg']
    assert f1 == "testFile1.fa"
    assert f2 == "testFile2.fa"
