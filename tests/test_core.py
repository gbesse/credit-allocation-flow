import unittest
from credit_allocation_flow import run

def line(id,cents=100,currency='EUR'):return dict(id=id,remaining_cents=cents,currency=currency,vat_code='s')
def credit(id,keys,cents=100,currency='EUR'):return dict(id=id,amount_cents=cents,currency=currency,vat_code='s',eligible_lines=keys)
class DomainTests(unittest.TestCase):
 def test_residual_reassignment_avoids_greedy_failure(self):
  r=run({'invoice_lines':[line('a'),line('b')],'credits':[credit('flex',['a','b']),credit('only_a',['a'])]});self.assertTrue(r['fully_allocated']);self.assertIn({'credit':'only_a','line':'a','cents':100},r['allocations'])
 def test_capacity_never_exceeded(self):
  r=run({'invoice_lines':[line('a',50)],'credits':[credit('c',['a'])]});self.assertEqual(r['allocated_cents'],50);self.assertEqual(r['unallocated'][0]['cents'],50)
 def test_currency_mismatch_not_allocated(self):
  r=run({'invoice_lines':[line('a',currency='USD')],'credits':[credit('c',['a'])]});self.assertEqual(r['allocated_cents'],0);self.assertEqual(len(r['rejected_eligibility_edges']),1)
 def test_duplicate_ids_rejected(self):
  with self.assertRaises(ValueError):run({'invoice_lines':[line('a'),line('a')],'credits':[]})
 def test_vat_mismatch(self):
  c=credit('c',['a']);c['vat_code']='reduced';self.assertFalse(run({'invoice_lines':[line('a')],'credits':[c]})['fully_allocated'])
