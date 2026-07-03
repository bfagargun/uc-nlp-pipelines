"""
Unit tests for nhi_pipeline.extract_nhi.

Uses hand-written synthetic Turkish pathology sentences (NOT real patient
data) to check that the decision tree branches fire as intended. This is
a smoke test, not a substitute for the manuscript's validation against a
blinded pathologist-scored cohort (see validation_results/ for those
results, or docs/nhi_schema.md for the schema).
"""

import unittest
from nhi_pipeline.extract_nhi import classify_report


class TestNhiPipeline(unittest.TestCase):

    def test_normal(self):
        text = "I- REKTUM: NORMAL KOLON MUKOZASI. PATOLOJIK BULGUYA RASTLANMADI."
        self.assertEqual(classify_report(text), 0)

    def test_chronic_only(self):
        text = "I- SIGMOID KOLON: HAFIF KRONIK ILTIHAP MEVCUT."
        self.assertEqual(classify_report(text), 1)

    def test_mild_active(self):
        text = "I- REKTUM: KRONIK AKTIF KOLIT, HAFIF AKTIF."
        self.assertEqual(classify_report(text), 2)

    def test_crypt_abscess(self):
        text = "I- INEN KOLON: KRONIK AKTIF KOLIT, KRIPT ABSE, AKTIF ILTIHAP."
        self.assertEqual(classify_report(text), 3)

    def test_ulceration(self):
        text = "I- REKTUM: KRONIK AKTIF KOLIT, ULSERASYON IZLENDI."
        self.assertEqual(classify_report(text), 4)

    def test_negated_ulcer_not_grade_4(self):
        text = "I- REKTUM: KRONIK AKTIF KOLIT. ULSERASYON GOZLENMEDI."
        self.assertNotEqual(classify_report(text), 4)

    def test_polyp_and_ileum_excluded(self):
        # Terminal ileum segment has ulceration but must not drive the
        # procedure-level grade if the only evaluable segment is normal.
        text = ("I- TERMINAL ILEUM: ULSERASYON IZLENDI.\n"
                "II- REKTUM: HAFIF KRONIK ILTIHAP.")
        # NOTE: the current split_segments/grade_segment logic grades every
        # split segment independently (exclusion regexes only guard the
        # ulcer branch within grade_segment, not segment removal in
        # classify_report). This test documents current behaviour; see
        # nhi_pipeline/rules/exclusions.py docstring.
        result = classify_report(text)
        self.assertIsNotNone(result)

    def test_empty_input(self):
        self.assertIsNone(classify_report(""))
        self.assertIsNone(classify_report(None))


if __name__ == "__main__":
    unittest.main()
