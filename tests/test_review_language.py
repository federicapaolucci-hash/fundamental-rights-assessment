"""Guard colour polarity independently of the internal MET/NOT_MET codes."""
import unittest

from digcon.config import default_config
from digcon.ui.review_language import FACTS, PROBLEMS, element_label, element_question


class ReviewLanguageTests(unittest.TestCase):
    def test_all_workbook_elements_have_an_explicit_display_classification(self):
        elements = {e.id for r in default_config().rules.rules for e in r.encoding.elements}
        self.assertEqual(elements, set(PROBLEMS) | set(FACTS))
        self.assertFalse(set(PROBLEMS) & set(FACTS))

    def test_absent_legal_basis_is_red_not_green(self):
        self.assertTrue(element_label('HS02.E1', 'MET').startswith('🔴'))
        self.assertTrue(element_label('HS02.E1', 'NOT_MET').startswith('🟢'))

    def test_essential_oversight_and_vulnerability_are_not_failures(self):
        for eid in ('HS05.E1', 'HS06.E1', 'HS09.E1', 'PROP-10.E1'):
            self.assertTrue(element_label(eid, 'MET').startswith('🔵'))
            self.assertTrue(element_label(eid, 'NOT_MET').startswith('⚪'))

    def test_unknown_and_unanswered_never_mean_no(self):
        for eid in set(PROBLEMS) | set(FACTS):
            self.assertTrue(element_label(eid, 'UNCERTAIN').startswith('🟡'))
            self.assertTrue(element_label(eid, None).startswith('⚪'))

    def test_new_condition_is_neutral_until_explicitly_classified(self):
        self.assertTrue(element_label('FUTURE.E1', 'MET').startswith('🔵'))
        self.assertEqual(element_question('FUTURE.E1', 'Original text'), 'Original text')


if __name__ == '__main__':
    unittest.main()
