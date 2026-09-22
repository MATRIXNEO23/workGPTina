import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"rag"))
from repo_guard import assert_write_target

class GuardTest(unittest.TestCase):
    def test_allowed(self): self.assertEqual(assert_write_target("https://github.com/MATRIXNEO23/workGPTina.git"),"MATRIXNEO23/workGPTina")
    def test_gptina_blocked_before_mutation(self):
        called=False
        def mutation():
            nonlocal called; called=True
        with self.assertRaises(PermissionError):
            assert_write_target("MATRIXNEO23/scodinzolina-conntinuity"); mutation()
        self.assertFalse(called)
    def test_every_other_repo_blocked(self):
        for target in ("owner/other","","MATRIXNEO23/workGPTina-evil"):
            with self.assertRaises(PermissionError): assert_write_target(target)

