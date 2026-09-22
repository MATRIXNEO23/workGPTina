import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"rag")); import work_memory as wm
class RetrievalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls): wm.build(allow_dirty=True)
    def test_gold(self): wm.run_gold()
    def test_superseded_hidden_and_recoverable(self):
        target="rag/records/method/2026/09/opportunity-score-v0.md"
        self.assertNotIn(target,{x["source"] for x in wm.search("vecchia strategia ricavo potenziale",20,False)})
        self.assertIn(target,{x["source"] for x in wm.search("vecchia strategia ricavo potenziale",20,True)})

