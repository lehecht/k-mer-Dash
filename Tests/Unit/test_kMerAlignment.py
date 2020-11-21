from src.kMerAlignmentData import KMerAlignmentData
from src.processing import Processing
import re


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

    # testing
    assert len(algnm1) == 2 * top

    # # Test2 with peak-position
    # Preparation
    k = 5
    top = 3
    highlight = 0
    peak = 2
    pattern = '[A-Z]+[a-z]+$'
    process = Processing(testData, None, k, peak, top, highlight)

    # execution
    algnm2 = KMerAlignmentData.processData(process)

    # testing
    assert len(algnm2) == 4
    for kmer in algnm2:
        assert re.search(pattern, kmer) is not None  # checks if there are only kmere containg the peak position
