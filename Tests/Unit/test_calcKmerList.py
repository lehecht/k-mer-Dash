from src.calcKmerLists import *
from src.profile import *
import pytest

testData = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]


def test_calcFrequency():
    # Test1: without peak-position
    # Preparation
    k = 5
    peak = None
    expected_result_p1 = {"AAACC": 1, "AACCC": 2, "ACCCC": 2, "CAACC": 1, "AAAAA": 3}
    expected_result_p2 = {"TTTGG": 1, "TTGGG": 2, "TGGGG": 3, "GTTGG": 1, "GGGGC": 1, "GGGCA": 1}

    # Execution
    profiles = calcFrequency(k, peak, testData)
    p1 = profiles[0]
    p2 = profiles[1]

    # Test
    assert len(p1) == 5
    assert len(p2) == 6
    assert p1 == expected_result_p1
    assert p2 == expected_result_p2

    # Test2: with peak-pos
    peak = 4
    expected_result_p1_peak = {"aaaCc": 1, "aaCcc": 2, "aCccc": 2, "caaCc": 1, "aaaAa": 1, "aaAaa": 1, 'aAaaa': 1}
    expected_result_p2_peak = {"tttGg": 1, "ttGgg": 2, "tGggg": 2, "gttGg": 1, "tggGg": 1, "ggGgc": 1, "gGgca": 1}

    # Execution
    profiles = calcFrequency(k, peak, testData)
    p1 = profiles[0]
    p2 = profiles[1]

    # Testing
    assert len(p1) == 7
    assert len(p2) == 7
    assert p1 == expected_result_p1_peak
    assert p2 == expected_result_p2_peak


@pytest.mark.xfail(raises=InputValueException)
def test_calcFrequency_peak():  # tests if InputValueException is thrown if peak > k-Mer length
    # Test1: peak-value > sequence length
    # Preparation
    k = 5
    peak = 999

    # Execution
    calcFrequency(k, peak, testData)  # raises InputValueException


@pytest.mark.xfail(raises=InputValueException)
def test_calcFrequency_k():  # tests if InputValueException is thrown if k => sequence length
    # Test1: k > sequence length
    # Preparation
    k = 7

    # Execution
    calcFrequency(k, None, testData)  # raises InputValueException


def test_createDataFrame():
    # Test1
    # Preparation
    profil1 = Profile({"AAT": 3, "TAT": 5, "GCC": 7}, "dir/file1")
    profil2 = Profile({"AAT": 8, "TCC": 2, "GAC": 11}, "dir/file2")
    selected = ["dir/file1", "dir/file2"]

    # Execution
    df = createDataFrame(profil1, profil2, selected)
    kmerList = df.index.tolist()
    freq1 = df["file1"].values.tolist()
    freq2 = df["file2"].values.tolist()

    # Testing
    assert len(kmerList) == 5
    assert kmerList == ["AAT", "TAT", "GCC", "TCC", "GAC"]
    assert freq1 == [3, 5, 7, 0, 0]
    assert freq2 == [8, 0, 0, 2, 11]

    # Test2
    profil1 = Profile({"AAA": 1, "TTT": 1}, "dir/file1")
    profil2 = Profile({"GGG": 1, "CCC": 1}, "dir/file2")

    # Execution
    df = createDataFrame(profil1, profil2, selected)
    kmerList = df.index.tolist()
    freq1 = df["file1"].values.tolist()
    freq2 = df["file2"].values.tolist()

    # Testing
    assert len(kmerList) == 4
    assert kmerList == ["AAA", "TTT", "GGG", "CCC"]
    assert freq1 == [1, 1, 0, 0]
    assert freq2 == [0, 0, 1, 1]


def test_calcTopKmer():
    # Test1: t is smaller than amount of entries
    # Preparation
    top = 3
    profil1 = Profile({"AAT": 3, "TAT": 5, "GCC": 7, "CCC": 15, "TAA": 22}, "dir/file1")
    profil2 = Profile({"AAT": 8, "TCC": 2, "GAC": 11, "CCC": 23, "GGG": 1}, "dir/file2")

    # Execution
    top_kmer_df = calcTopKmer(top, profil1, profil2)
    topKmerList = top_kmer_df.index.tolist()
    maxFreq = top_kmer_df["Frequency"].values.tolist()
    fileNameList = top_kmer_df["File"].values.tolist()

    # Testing
    assert len(topKmerList) == int(2 * top)
    assert topKmerList == ['TAA', 'CCC', 'GCC', 'CCC', 'GAC', 'AAT']
    assert maxFreq == [22, 15, 7, 23, 11, 8]
    assert fileNameList == ["file1", "file1", "file1", "file2", "file2", "file2"]

    # Test2: t is greater than amount of entries
    # Preparation
    top = None  # is set on None in processing file

    # Execution
    top_kmer_df2 = calcTopKmer(top, profil1, profil2)
    topKmerList2 = top_kmer_df2.index.tolist()
    maxFreq2 = top_kmer_df2["Frequency"].values.tolist()
    fileNameList2 = top_kmer_df2["File"].values.tolist()

    # Testing
    assert len(topKmerList2) == len(profil1.getProfile()) + len(profil2.getProfile())
    assert topKmerList2 == ['TAA', 'CCC', 'GCC', 'TAT', 'AAT', 'CCC', 'GAC', 'AAT', 'TCC', 'GGG']
    assert maxFreq2 == [22, 15, 7, 5, 3, 23, 11, 8, 2, 1]
    assert fileNameList2 == ["file1", "file1", "file1", "file1", "file1", "file2", "file2", "file2", "file2", "file2"]


def test_createPeakPosition():
    # Test1
    # Preparation
    peak = 2
    sequence = "ACCGT"

    # Execution
    newSeq = createPeakPosition(peak, sequence)

    # Testing
    assert newSeq == "aCcgt"
