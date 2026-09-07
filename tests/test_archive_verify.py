"""Guards for scripts/archive_verify.py — the trim-loss checker, FINAL FORM.

Each test names the clause it protects and the receipt that clause was bought
with (Kleiber MSG-b5bbdd). The suite is two-sided throughout: the checker must
FIRE on real loss and must NOT fire on in-place rewrites, present-on-disk paths,
or content that legitimately lives in committed docs. A check that cries wolf
gets waved off, which is worse than no check.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import archive_verify as av  # noqa: E402

SCRIPT = ROOT / "scripts" / "archive_verify.py"


# ---- clause 3: fact-token extraction survives paraphrase --------------------

def test_extracts_shas_msgids_paths_urls_and_env_vars():
    text = ("merged 8bf1f4d per MSG-caf615, see scripts/deploy_publish.sh and "
            "https://example.org/x with ROIZEN_AUTO_DEPLOY=1")
    tok = av.extract_tokens(text)
    assert "8bf1f4d" in tok["sha"]
    assert "MSG-caf615" in tok["msg-id"]
    assert "scripts/deploy_publish.sh" in tok["path"]
    assert any(u.startswith("https://example.org") for u in tok["url"])
    assert "ROIZEN_AUTO_DEPLOY" in tok["env-var"]


def test_prose_emphasis_is_not_mistaken_for_an_env_var():
    """ALL_CAPS prose (PASS_WITH_FLAG) must not be reported as a lost env var."""
    assert "PASS_WITH_FLAG" not in av.extract_tokens("a PASS_WITH_FLAG verdict")["env-var"]


# ---- clause 2: corpus is live ∪ archive ∪ committed docs --------------------

def test_locate_reports_which_surface_held_the_content():
    corpus = {"CLAUDE.md": "alpha", "session_archive.md": "beta",
              "docs/DEPLOY.md": "gamma"}
    assert av.locate("beta", corpus) == "session_archive.md"
    assert av.locate("gamma", corpus) == "docs/DEPLOY.md"
    assert av.locate("delta", corpus) is None


def test_corpus_includes_committed_docs_not_just_the_two_files():
    corpus = av.build_corpus("HEAD")
    assert "CLAUDE.md" in corpus and "session_archive.md" in corpus
    assert any(k.startswith("docs/") for k in corpus), \
        "clause 2: content legitimately lives in docs/ and must not read as lost"


# ---- clause 1: versions, not endpoints -------------------------------------

def test_walks_every_version_in_the_window_not_just_the_endpoints():
    versions = av.versions_in_window("3e27645", "HEAD")
    assert versions[0] == "3e27645"
    assert len(versions) >= 3, (
        "clause 1: a line created AND replaced inside the window is in neither "
        "endpoint, so endpoint-only comparison never examines it"
    )


# ---- clause 5: long bullets narrowed to readable fragments ------------------

def test_long_bullet_is_narrowed_to_clause_fragments():
    line = ("- a very long register row about the gate; it also mentions the "
            "deploy path — and then continues at considerable length about "
            "several other operational matters entirely")
    frags = av.clause_fragments(line)
    assert 1 <= len(frags) <= 3
    assert all(len(f) < len(line) for f in frags)


# ---- clause 4 (both edges) + the live receipt -------------------------------

def test_existing_file_path_is_not_reported_lost_when_no_longer_cited():
    """A file does not contain its own path. Kleiber's token pass flagged six
    records that were all present on disk and merely uncited."""
    assert (ROOT / "scripts/deploy_publish.sh").exists()
    proc = _run("3e27645")
    assert "scripts/deploy_publish.sh" not in proc.stdout.split("FACT-TOKENS")[-1]


def _run(base: str, head: str | None = None):
    cmd = [sys.executable, str(SCRIPT), base]
    if head:
        cmd += ["--head", head]
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=120)


def test_current_tree_is_clean_on_both_passes():
    proc = _run("3e27645")
    assert proc.returncode == 0, proc.stdout
    assert "LINE COMPLEMENT: EMPTY" in proc.stdout
    assert "FACT-TOKENS: EMPTY" in proc.stdout


def test_bite_against_the_real_historical_loss():
    """Not a fixture: run over 3e27645 -> f3adad3 (the trim, before the dea3f8d
    recovery) and the checker must reproduce the real 9-line loss."""
    proc = _run("3e27645", "f3adad3")
    assert proc.returncode == 1, "checker must BLOCK on the known historical loss"
    assert "LINE COMPLEMENT: NOT EMPTY" in proc.stdout


# ---- clause 6 + 7: honesty about limits, and the inverse direction ----------

def test_output_states_what_the_tool_cannot_decide():
    proc = _run("3e27645")
    assert "CLAUSE 6" in proc.stdout and "IN" in proc.stdout
    assert "does NOT certify" in proc.stdout, \
        "an EMPTY result must not read as certifying that a paraphrase kept the substance"


def test_inverse_pass_reports_rule_shaped_archived_blocks():
    proc = _run("3e27645")
    assert "INVERSE (clause 7)" in proc.stdout
    assert "HUMAN CALL" in proc.stdout or "archived blocks carrying RULE" in proc.stdout


def test_recovered_rule_is_now_stated_live_and_enforced():
    """The clause-7 finding from this repo's own run: the /pipe4 merge-condition
    (process evidence out of the source root) had been swept into the archive
    and was in no live surface. It must now be BOTH stated and enforced."""
    live = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "loop-artifacts" in live, "rule must be stated where a fresh session reads"
    assert "loop-artifacts/" in gitignore, "and enforced where something runs"
