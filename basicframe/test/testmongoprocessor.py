from basicframe.playground.sf import processor


def test_fetch_random_one():
    condition = {"preprocess": True, "type": "00", 'status': 'ready'}
    doc = processor.fetch_random_one(condition)
    print(doc)