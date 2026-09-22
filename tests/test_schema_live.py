import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"rag"))
import work_memory as wm
class SchemaLiveTest(unittest.TestCase):
    def test_records_and_live(self):
        metas,paths=wm.validate_records(); live=wm.validate_live(); self.assertIn("method-opportunity-score-v1",metas); self.assertTrue((ROOT/live["last_full_checkpoint"]).is_file())
    def test_supersession(self):
        metas,paths=wm.validate_records(); status=wm.effective_statuses(metas,paths); self.assertEqual(status[paths["method-opportunity-score-v0"]],"superseded")

