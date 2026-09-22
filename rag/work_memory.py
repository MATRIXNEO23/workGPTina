#!/usr/bin/env python3
"""Canonical-source verifier and disposable generational retrieval index."""
from __future__ import annotations
import argparse, fnmatch, hashlib, json, os, re, shutil, sqlite3, subprocess, sys, tempfile, uuid
from datetime import datetime, timezone
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]; RAG=ROOT/"rag"; INDEX=RAG/"index"
GEN=INDEX/".projection-generations"; POINTER=INDEX/".projection-current"
MANIFEST=RAG/"memory_manifest.json"; GOLD=RAG/"eval/WORKGPTINA_MEMORY_GOLD.json"
TOKEN=re.compile(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ_]+")
CLASSES={"PROJECT","EXPERIMENT","METHOD","ERROR","CUSTOMER_MARKET","ECONOMICS","DECISION","OPPORTUNITY","OPEN_LOOP","EVIDENCE"}
STATUSES={"current","historical","superseded","invalidated"}

def die(msg): raise SystemExit(msg)
def sha(text): return hashlib.sha256(text.encode()).hexdigest()
def rel(path): return path.resolve().relative_to(ROOT.resolve()).as_posix()
def git_dirty():
    return bool(subprocess.run(["git","status","--porcelain"],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip())
def parse_record(path):
    text=path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text[4:]: die(f"Missing YAML front matter: {rel(path)}")
    raw, body=text[4:].split("\n---\n",1); meta=yaml.safe_load(raw)
    if not isinstance(meta,dict): die(f"Invalid metadata: {rel(path)}")
    return meta,body.strip(),text
def records(): return sorted((RAG/"records").glob("**/*.md"))
def validate_records():
    required={"schema_version","id","class","title","status","event_at","recorded_at","owner","source_refs","supersedes","tags"}
    metas={}; paths={}
    for path in records():
        meta,body,_=parse_record(path); missing=required-set(meta)
        if missing: die(f"Missing {sorted(missing)}: {rel(path)}")
        if meta["schema_version"]!=1 or meta["class"] not in CLASSES or meta["status"] not in STATUSES or meta["owner"]!="workGPTina": die(f"Invalid schema enum/owner: {rel(path)}")
        if not isinstance(meta["source_refs"],list) or not meta["source_refs"]: die(f"source_refs required: {rel(path)}")
        if not isinstance(meta["supersedes"],list) or not isinstance(meta["tags"],list) or not body: die(f"Invalid lists/body: {rel(path)}")
        rid=str(meta["id"])
        if rid in metas: die(f"Duplicate id: {rid}")
        metas[rid]=meta; paths[rid]=rel(path)
    for rid,meta in metas.items():
        for old in meta["supersedes"]:
            if old not in metas: die(f"Unknown supersedes {old}: {rid}")
            if old==rid: die(f"Self supersession: {rid}")
        for source in meta["source_refs"]:
            if "://" not in source and not (ROOT/source).exists(): die(f"Missing source_ref {source}: {rid}")
    # cycle detection and effective supersession
    def visit(node,stack):
        if node in stack: die(f"Supersession cycle: {node}")
        for nxt in metas[node]["supersedes"]: visit(nxt,stack|{node})
    for rid in metas: visit(rid,set())
    return metas,paths
def validate_live():
    live=json.loads((RAG/"live/WORKGPTINA_LIVE_CONTEXT.json").read_text())
    for key in ("last_micro_checkpoint","last_full_checkpoint"):
        if not (ROOT/live[key]).is_file(): die(f"Broken live pointer: {key}={live[key]}")
    for path in (RAG/"live/micro-checkpoints").glob("**/*.json"):
        obj=json.loads(path.read_text()); needed={"schema_version","id","created_at","trigger","summary","changed","project_ids","experiment_ids","open_loop_ids","next_action","source_refs"}
        if needed-set(obj): die(f"Invalid micro-checkpoint: {rel(path)}")
    return live
def canonical_files():
    manifest=json.loads(MANIFEST.read_text()); found={}
    for pattern in manifest["canonical_patterns"]:
        for path in ROOT.glob(pattern):
            if path.is_file() and "/.projection-" not in path.as_posix(): found[rel(path)]=path
    return [found[k] for k in sorted(found)]
def effective_statuses(metas,paths):
    status={paths[r]:metas[r]["status"] for r in metas}
    for rid,meta in metas.items():
        if meta["status"]=="current":
            todo=list(meta["supersedes"]); seen=set()
            while todo:
                old=todo.pop()
                if old in seen: continue
                seen.add(old); status[paths[old]]="superseded"; todo.extend(metas[old]["supersedes"])
    return status
def chunks():
    metas,paths=validate_records(); statuses=effective_statuses(metas,paths); out=[]
    for path in canonical_files():
        text=path.read_text(encoding="utf-8"); source=rel(path); status=statuses.get(source,"current")
        title=source
        if source.startswith("rag/records/"):
            meta,body,text=parse_record(path); title=meta["title"]
        for idx,start in enumerate(range(0,max(1,len(text)),1200)):
            part=text[start:start+1400].strip()
            if part: out.append({"id":sha(f"{source}:{idx}:{part}"),"source":source,"title":title,"status":status,"text":part})
    return out
def fingerprint(): return sha("\n".join(f"{rel(p)}\0{sha(p.read_text(encoding='utf-8'))}" for p in canonical_files()))
def verify():
    manifest=json.loads(MANIFEST.read_text())
    if manifest["writable_repository"]!="MATRIXNEO23/workGPTina" or "MATRIXNEO23/scodinzolina-conntinuity" not in manifest["read_only_repositories"]: die("Repository ownership manifest invalid")
    validate_records(); validate_live()
    if "rag/index/.projection-generations/" not in (ROOT/".gitignore").read_text(): die("Derived generations are not ignored")
    conn=sqlite3.connect(":memory:")
    try: conn.execute("CREATE VIRTUAL TABLE probe USING fts5(text)")
    except sqlite3.Error as exc: die(f"SQLite FTS5 unavailable: {exc}")
    finally: conn.close()
    print(f"OK verify: {len(records())} records, {len(canonical_files())} canonical files")
def build(allow_dirty=False):
    if git_dirty() and not allow_dirty: die("Canonical build requires clean worktree")
    verify(); data=chunks(); generation=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
    GEN.mkdir(parents=True,exist_ok=True); staging=GEN/(".staging-"+generation); final=GEN/generation; staging.mkdir()
    try:
        jsonl="".join(json.dumps(x,ensure_ascii=False)+"\n" for x in data); (staging/"memory_chunks.jsonl").write_text(jsonl)
        meta={"schema_version":1,"projection_generation":generation,"source_fingerprint":fingerprint(),"chunks":len(data),"build_complete":True}
        (staging/"index_meta.json").write_text(json.dumps(meta,indent=2)+"\n")
        db=sqlite3.connect(staging/"work_memory.sqlite3")
        db.execute("CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL)"); db.execute("CREATE TABLE chunks(id TEXT PRIMARY KEY,source TEXT,title TEXT,status TEXT,text TEXT)"); db.execute("CREATE VIRTUAL TABLE chunks_fts USING fts5(id UNINDEXED,source UNINDEXED,title,status UNINDEXED,text)")
        for x in data:
            vals=(x["id"],x["source"],x["title"],x["status"],x["text"]); db.execute("INSERT INTO chunks VALUES(?,?,?,?,?)",vals); db.execute("INSERT INTO chunks_fts VALUES(?,?,?,?,?)",vals)
        for k,v in meta.items(): db.execute("INSERT INTO meta VALUES(?,?)",(k,json.dumps(v) if not isinstance(v,str) else v))
        db.commit()
        if db.execute("PRAGMA quick_check").fetchone()[0]!="ok": die("SQLite quick_check failed")
        db.close(); staging.rename(final)
        tmp=POINTER.with_suffix(".tmp"); tmp.write_text(generation+"\n"); os.replace(tmp,POINTER)
    except Exception:
        shutil.rmtree(staging,ignore_errors=True); raise
    print(f"OK build: {generation}, {len(data)} chunks")
def active():
    if not POINTER.is_file(): build(allow_dirty=True)
    name=POINTER.read_text().strip(); directory=GEN/name
    required=[directory/"memory_chunks.jsonl",directory/"index_meta.json",directory/"work_memory.sqlite3"]
    if Path(name).name!=name or not all(p.is_file() for p in required): build(allow_dirty=True); return active()
    return required
def search(query,limit=8,all_statuses=False):
    _,_,dbpath=active(); db=sqlite3.connect(dbpath); terms=TOKEN.findall(query.casefold()); rows=[]
    if terms:
        expr=" OR ".join('"'+t.replace('"','')+'"' for t in terms)
        sql="SELECT source,title,status,text,bm25(chunks_fts) FROM chunks_fts WHERE chunks_fts MATCH ?"; params=[expr]
        if not all_statuses: sql+=" AND status='current'"
        sql+=" ORDER BY bm25(chunks_fts) LIMIT ?"; params.append(limit)
        rows=db.execute(sql,params).fetchall()
    db.close(); return [{"source":r[0],"title":r[1],"status":r[2],"text":r[3],"score":r[4]} for r in rows]
def run_gold():
    failed=[]
    for case in json.loads(GOLD.read_text()):
        hits=search(case["query"],50,case.get("all_statuses",False)); sources={h["source"] for h in hits}
        if not sources.intersection(case["expected_any"]) or sources.intersection(case.get("forbidden",[])): failed.append((case["id"],sorted(sources)))
    if failed: die("Gold failures: "+json.dumps(failed,ensure_ascii=False))
    print("OK retrieval gold")
def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True); sub.add_parser("verify"); b=sub.add_parser("build"); b.add_argument("--allow-dirty-preview",action="store_true"); s=sub.add_parser("search"); s.add_argument("query"); s.add_argument("--all-statuses",action="store_true"); sub.add_parser("test-gold")
    a=p.parse_args()
    if a.cmd=="verify": verify()
    elif a.cmd=="build": build(a.allow_dirty_preview)
    elif a.cmd=="search": print(json.dumps(search(a.query,all_statuses=a.all_statuses),ensure_ascii=False,indent=2))
    else: run_gold()
if __name__=="__main__": main()
