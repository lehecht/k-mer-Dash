from src.kMerAlignmentData import KMerAlignmentData
from src.processing import Processing


def test_processData():
    testData = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]

    # Test1 without peak position
    # Preparation
    k = 5
    top = 3
    highlight = 0
    peak = None
    process = Processing(testData, None, k, peak, top, highlight)

    # execution
    algnm1 = KMerAlignmentData.processData(process)
    algnm1_list = list(map(lambda e: e.seq, algnm1))
    print(algnm1)
    # testing
    assert len(algnm1) == 9
    assert algnm1_list == ["TTTGG----",
                           "GTTGG----",
                           "-TTGGG---",
                           "--TGGGG--",
                           "---GGGGC-",
                           "---GGGCA-",
                           "---AACCC-",
                           "----ACCCC",
                           "---AAAAA-"]

    # # Test2 with peak-position
    # Preparation
    k = 5
    top = 3
    highlight = 0
    peak = 2
    process = Processing(testData, None, k, peak, top, highlight)

    # execution
    algnm2 = KMerAlignmentData.processData(process)
    # testing
    assert len(algnm2) >= top
    assert algnm2 == ['----Aaccc', '----Ttggg', '---aAacc-', '---cAacc-', '---aAaaa-', '----Aaaaa', '---tTtgg-',
                      '---gTtgg-', '---tGggg-', '----Ggggc']
