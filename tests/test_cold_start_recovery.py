import json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ColdStartTest(unittest.TestCase):
    def test_clean_clone_repository_only(self):
        with tempfile.TemporaryDirectory() as td:
            clone=Path(td)/"clone"; subprocess.run(["git","clone","--depth","1",f"file://{ROOT}",str(clone)],check=True,capture_output=True)
            self.assertFalse((clone/"rag/index/.projection-current").exists())
            commands=[[sys.executable,"rag/work_memory.py","verify"],[sys.executable,"rag/work_memory.py","build"],[sys.executable,"rag/work_memory.py","test-gold"]]
            for cmd in commands: subprocess.run(cmd,cwd=clone,check=True,capture_output=True,text=True)
            live=json.loads((clone/"rag/live/WORKGPTINA_LIVE_CONTEXT.json").read_text()); self.assertTrue(live["next_action"]); self.assertEqual(live["verified_revenue"]["collected"],0)
            self.assertIn("read-only",(clone/"rag/OWNERSHIP_AND_REPOSITORY_BOUNDARY.md").read_text())
            self.assertEqual(subprocess.run([sys.executable,"rag/repo_guard.py","MATRIXNEO23/scodinzolina-conntinuity"],cwd=clone).returncode,77)
            self.assertEqual(subprocess.run(["git","status","--porcelain"],cwd=clone,text=True,capture_output=True,check=True).stdout,"")

