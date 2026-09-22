import json,shutil,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"rag")); import work_memory as wm
class ProjectionTest(unittest.TestCase):
    def test_incomplete_generation_not_selected(self):
        wm.build(allow_dirty=True); before=wm.POINTER.read_text(); bad=wm.GEN/"bad-generation"; bad.mkdir(exist_ok=True); (bad/"index_meta.json").write_text("{}")
        self.assertEqual(wm.POINTER.read_text(),before); shutil.rmtree(bad)
    def test_generation_consistency(self):
        wm.build(allow_dirty=True); jsonl,meta,db=wm.active(); obj=json.loads(meta.read_text()); self.assertTrue(obj["build_complete"])
        with jsonl.open() as handle: count=sum(1 for _ in handle)
        self.assertEqual(count,obj["chunks"])
