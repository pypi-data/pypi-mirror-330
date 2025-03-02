from filedata.text_algo.ac import ACAutomaton


def test_find_all():
    words = ['测试', '方案', '测试方案', '软件']
    content = '这是一个测试方案，用来测试软件是否正常运行的方案。'

    ac = ACAutomaton(words)
    result = ac.find_all(content)

    assert len(result) == 6
    for r in result:
        assert r.word in words
        assert content[r.position[0]:r.position[1]] == r.word


def test_find_all_from_start():
    words = ['测试', '方案', '测试方案', '软件']
    content = '测试方案是用来测试软件是否正常运行的方案。'

    ac = ACAutomaton(words)
    result = ac.find_all(content, from_start=True)

    assert len(result) == 2
    for r in result:
        assert r.word in words
        assert content[r.position[0]:r.position[1]] == r.word


def test_find_all2():
    words = ['软件测试方案', '测试方案', '测试', '方案', '软件测试']
    content = '这是一个软件测试方案，用来测试软件是否正常运行的方案。'

    ac = ACAutomaton(words)
    result = ac.find_all(content)

    assert len(result) == 7
    for r in result:
        assert r.word in words
        assert content[r.position[0]:r.position[1]] == r.word


def test_find_all_from_segments():
    words = ['软件测试', '软件测试方案', '软件']
    segments = ['这是', '一个', '软件测试', '方案', '，', '可以', '用来', '做', '应用软件', '测试']

    ac = ACAutomaton(words)
    result = ac.find_all_from_segments(segments)

    assert len(result) == 2
    for r in result:
        assert r.word in words
        assert ''.join(segments[r.position[0]:r.position[1]]) == r.word
