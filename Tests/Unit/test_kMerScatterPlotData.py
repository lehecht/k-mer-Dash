from src.kMerScatterPlotData import KMerScatterPlotData as sctPlt


def test_processData():
    # Test1
    # Preparation
    test_data = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]
    k = 5
    top = 3
    peak = None
    process = sctPlt(test_data, test_data, k, peak, top, None,False)

    # Execution
    results = sctPlt.processData(process)
    df = results[0]
    labels = results[1]
    file_name1 = results[2][0]
    file_name2 = results[2][1]

    res_kmer_list = ["AAACC", "AACCC", "ACCCC", "CAACC", "AAAAA", "TTTGG", "TTGGG", "TGGGG", "GTTGG", "GGGGC", "GGGCA"]
    res_x_axis = [1, 2, 2, 1, 3, 0, 0, 0, 0, 0, 0]
    res_y_axis = [0, 0, 0, 0, 0, 1, 2, 3, 1, 1, 1]
    x_a_res_dict = dict(zip(res_kmer_list, res_x_axis))
    y_a_res_dict = dict(zip(res_kmer_list, res_y_axis))

    top_kmer = process.getTopKmer()
    top_kmer_list = top_kmer.index.tolist()

    # Testing

    # checks if frequencies are are equal
    for label in labels:
        assert x_a_res_dict[label] == df.loc[label, ['testFile1.fa']].tolist()[0]
        assert y_a_res_dict[label] == df.loc[label, ['testFile2.fa']].tolist()[0]

    assert set(labels) == {"AAACC", "AACCC", "ACCCC", "CAACC", "AAAAA", "TTTGG", "TTGGG", "TGGGG", "GTTGG", "GGGGC",
                           "GGGCA"}
    assert file_name1 == "testFile1.fa"
    assert file_name2 == "testFile2.fa"

    for i in range(0, len(df.index)):
        kmer = df.index.tolist()[i]
        if kmer in top_kmer_list:
            assert df['highlight'][i] == "TOP {}-mer".format(k)
        else:
            assert df['highlight'][i] == "{}-mer".format(k)

    # Test2: with peak position
    # Preparation
    test_data = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]
    k = 5
    top = 3
    peak = 2
    process2 = sctPlt(test_data, test_data, k, peak, top, None, False)

    # Execution
    results2 = sctPlt.processData(process2)
    df2 = results2[0]
    labels = results2[1]
    file_name1 = results2[2][0]
    file_name2 = results2[2][1]

    top_kmer2 = process2.getTopKmer()
    top_kmer_list2 = top_kmer2.index.tolist()

    res_kmer_list = ['aAacc', 'Aaccc', 'acccc', 'cAacc', 'aAaaa', 'Aaaaa', 'aaaaa', 'tTtgg', 'Ttggg', 'tgggg', 'gTtgg',
                     'tGggg', 'Ggggc', 'gggca']
    res_x_axis = [1, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    res_y_axis = [0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 1, 1, 1]
    x_a_res_dict = dict(zip(res_kmer_list, res_x_axis))
    y_a_res_dict = dict(zip(res_kmer_list, res_y_axis))

    # Testing

    # checks if frequencies are are equal
    for label in labels:
        assert x_a_res_dict[label] == df2.loc[label, ['testFile1.fa']].tolist()[0]
        assert y_a_res_dict[label] == df2.loc[label, ['testFile2.fa']].tolist()[0]

    assert set(labels) == {'aAacc', 'Aaccc', 'acccc', 'cAacc', 'aAaaa', 'Aaaaa', 'aaaaa', 'tTtgg', 'Ttggg', 'tgggg',
                           'gTtgg',
                           'tGggg', 'Ggggc', 'gggca'}

    assert file_name1 == "testFile1.fa"
    assert file_name2 == "testFile2.fa"

    for i in range(0, len(df2.index)):
        kmer = df2.index.tolist()[i]
        if kmer in top_kmer_list2:
            assert df2['highlight'][i] == "TOP {}-mer".format(k)
        else:
            assert df2['highlight'][i] == "{}-mer".format(k)
