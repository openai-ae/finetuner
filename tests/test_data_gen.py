import pytest

from tests.data_generator import fashion_doc_generator, fashion_match_doc_generator


def test_doc_generator():
    for d in fashion_doc_generator():
        assert d.tags['class']
        break


@pytest.mark.parametrize('num_pos, num_neg', [(5, 7), (10, 10)])
def test_fashion_matches_generator(num_pos, num_neg):
    for d in fashion_match_doc_generator(num_pos, num_neg):
        assert len(d.matches) == num_pos + num_neg
        all_labels = [int(d.tags['trainer']['label']) for d in d.matches]
        assert all_labels.count(1) == num_pos
        assert all_labels.count(0) == num_neg
        break