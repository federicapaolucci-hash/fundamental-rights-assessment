"""Run without pytest: PYTHONPATH=src:tests:. python tests/test_action_plan_regression.py"""
import unittest
from digcon.config import default_config
from digcon.domain.models import ActionPlanItem, AssessmentState, MitigationRecord, ResidualRiskReview
from digcon.domain.action_plan import approved, fingerprint, findings, TITLES
from digcon.engine import run_engine
from digcon.reporting.json_report import dumps, assessment_of
from engine_support import build_state, CTX
import json


def approve(s, rid):
    s.action_plan[rid] = ActionPlanItem(rule_id=rid, action='Implement the specific correction',
        rationale='Addresses this finding in this use context', owner='Responsible team', due_date='2026-11-01',
        status='AWAITING_REVIEW', implementation='Procedure implemented and exercised', evidence_refs=['doc:implementation'],
        verification_method='Review representative cases', verification_result='Finding addressed in tested cases',
        verification_evidence=['doc:test'], reviewer='Reviewer', review_date='2026-10-21',
        decision='RESOLVED', decision_reason='Evidence supports closure of this specific finding')
    s.action_plan[rid].reviewed_fingerprint = fingerprint(s,rid)


class PlanTests(unittest.TestCase):
    def setUp(self): self.cfg=default_config()
    def run_state(self,s): return run_engine(self.cfg,s,CTX)
    def remediation_case(self):
        return build_state({'elements':{'QUAL-01.E1':'MET'}})
    def test_legacy_loads(self):
        s=build_state(); d=s.model_dump(mode='json');d.pop('action_plan');d.pop('residual_reviews')
        restored=AssessmentState.model_validate(d)
        self.assertEqual(restored.action_plan,{})
    def test_progress_roundtrip(self):
        s=build_state();approve(s,'LEGAL-01')
        restored=AssessmentState.model_validate(assessment_of(json.loads(dumps(s,self.run_state(s)))))
        self.assertEqual(restored.action_plan,s.action_plan)
        self.assertTrue(approved(restored,'LEGAL-01'))
    def test_effectiveness_alone_does_not_close(self):
        s=self.remediation_case()
        s.mitigations['MIT-009']=MitigationRecord(mitigation_id='MIT-009',activated=True,status='VERIFIED_EFFECTIVE',linked_rule_ids=['QUAL-01'])
        self.assertIn('QUAL-01',[f.rule_id for f in self.run_state(s).open_remediations])
    def test_specific_approval_and_invalidation(self):
        s=self.remediation_case()
        s.mitigations['MIT-009']=MitigationRecord(mitigation_id='MIT-009',activated=True,status='VERIFIED_EFFECTIVE',linked_rule_ids=['QUAL-01','LEGAL-01'])
        approve(s,'QUAL-01')
        self.assertNotIn('QUAL-01',[f.rule_id for f in self.run_state(s).open_remediations])
        self.assertFalse(approved(s,'LEGAL-01'))
        s.answers['C01'].value='Changed context'
        self.assertFalse(approved(s,'QUAL-01'))
        self.assertIn('QUAL-01',[f.rule_id for f in self.run_state(s).open_remediations])
    def test_missing_evidence_cannot_approve(self):
        s=build_state();approve(s,'LEGAL-01');s.action_plan['LEGAL-01'].verification_evidence=[]
        s.action_plan['LEGAL-01'].reviewed_fingerprint=fingerprint(s,'LEGAL-01')
        self.assertFalse(approved(s,'LEGAL-01'))
    def test_residual_review_required_and_invalidated(self):
        s=build_state({'risks':{'RISK-07':{'scale':'MEDIUM','scope':'MODERATE','reversibility':'PARTLY_REVERSIBLE','probability':'POSSIBLE',
            'residual_scale':'LOW','residual_scope':'LIMITED','residual_reversibility':'REVERSIBLE','residual_probability':'RARE'}},
            'mitigations':{'MIT-009':{'activated':True,'status':'VERIFIED_EFFECTIVE'}}})
        self.assertIsNone(self.run_state(s).risks['RISK-07'].residual)
        s.residual_reviews['RISK-07']=ResidualRiskReview(reviewer='Reviewer',review_date='2026-10-21',rationale='Reasons for all four dimensions',
            evidence_refs=['doc:residual-test'],mitigation_ids=['MIT-009'],reviewed_fingerprint=fingerprint(s,'RISK-07'))
        self.assertEqual(self.run_state(s).risks['RISK-07'].residual.value,'VERY_LOW')
        s.mitigations['MIT-009'].activated=False
        self.assertIsNone(self.run_state(s).risks['RISK-07'].residual)
    def test_stop_cannot_be_overridden(self):
        s=build_state({'elements':{'HS06.E1':'MET','HS06.E2':'MET','HS06.E3':'MET'},'human_gates':{'HS06':'COMPLETED'}})
        approve(s,'HS06')
        self.assertEqual(self.run_state(s).outcome.value,'O5')
    def test_saved_work_not_lost_when_trigger_clears(self):
        s=build_state();approve(s,'QUAL-01');r=self.run_state(s)
        self.assertIn('QUAL-01',findings(r,s.action_plan))
    def test_titles_cover_all_non_outcome_rules(self):
        self.assertFalse([r.id for r in self.cfg.rules.rules if r.family not in ['OUT','SYS'] and r.id not in TITLES])

if __name__=='__main__':unittest.main()
