"""
Unit tests for mes_pipeline (diagnosis_field and narrative_findings).

Uses hand-written synthetic Turkish endoscopy sentences (NOT real patient
data). The diagnosis-field pipeline's decision logic (first-mention-wins,
range -> lower bound, letter "O" -> 0) was reconstructed by reverse-
engineering against the real cohort and verified to 100% fidelity — see
mes_pipeline/diagnosis_field/rules/mes_patterns.py for the full provenance
note and mes_pipeline/README.md for the reproduced validation metrics.
"""

import unittest
from mes_pipeline.diagnosis_field.extract_mes_tani import extract_mes_from_diagnosis
from mes_pipeline.narrative_findings.extract_mes_bulgular import extract_mes_from_findings


class TestMesDiagnosisField(unittest.TestCase):

    def test_simple_integer(self):
        self.assertEqual(extract_mes_from_diagnosis("ULSERATIF KOLIT MAYO 2")["mes"], 2)

    def test_keyword_skoru(self):
        r = extract_mes_from_diagnosis("ULSERATIF KOLIT (MAYO SKORU 3, CIDDI AKTIVITELI)")
        self.assertEqual(r["mes"], 3)

    def test_hyphenated(self):
        self.assertEqual(extract_mes_from_diagnosis("ULSERATIF KOLIT MAYO-1")["mes"], 1)

    def test_roman_numeral(self):
        self.assertEqual(extract_mes_from_diagnosis("ULSERATIF KOLIT MAYO III")["mes"], 3)

    def test_letter_o_as_zero(self):
        self.assertEqual(extract_mes_from_diagnosis("REMISYONDA ULSERATIF KOLIT MAYO O")["mes"], 0)

    def test_range_resolves_to_lower_bound(self):
        r = extract_mes_from_diagnosis("ULSERATIF KOLIT (MAYO 1-2)")
        self.assertEqual(r["mes"], 1)
        self.assertTrue(r["is_range"])

    def test_multiple_mentions_first_wins(self):
        text = "DISTAL TUTULUMLU ULSERATIF KOLIT (MAYO 1) ENDOSKOPIK AKTIF PROKTIT (MAYO 2)"
        self.assertEqual(extract_mes_from_diagnosis(text)["mes"], 1)

    def test_typo_variant_skou(self):
        # A real typo variant ("SKOU" for "SKORU") observed in the corpus.
        r = extract_mes_from_diagnosis("PANKOLIT (MAYO SKOU 1-2)")
        self.assertEqual(r["mes"], 1)

    def test_no_match(self):
        self.assertIsNone(extract_mes_from_diagnosis("SOL KOLON TUTULUMLU KOLIT (IBH?)")["mes"])

    def test_empty_input(self):
        self.assertIsNone(extract_mes_from_diagnosis("")["mes"])
        self.assertIsNone(extract_mes_from_diagnosis(None)["mes"])


class TestMesNarrativeFindings(unittest.TestCase):
    """Exploratory blind pipeline — lower expected accuracy by design."""

    def test_normal(self):
        r = extract_mes_from_findings("Tüm kolon segmentleri normaldi.")
        self.assertEqual(r["mes"], 0)

    def test_mild(self):
        r = extract_mes_from_findings(
            "Sigmoid kolon ve rektum eritemli, vasküler patern azalmış.")
        self.assertEqual(r["mes"], 1)

    def test_moderate(self):
        r = extract_mes_from_findings(
            "Rektum eritemli, ödemli, frajil, erozyonlu izlendi.")
        self.assertEqual(r["mes"], 2)

    def test_severe(self):
        r = extract_mes_from_findings(
            "Sigmoid ve rektum arada sağlam mukoza kalmayacak şekilde "
            "eritemli, ülsere izlendi.")
        self.assertEqual(r["mes"], 3)

    def test_too_short_returns_none(self):
        r = extract_mes_from_findings("normal")
        self.assertIsNone(r["mes"])


if __name__ == "__main__":
    unittest.main()
