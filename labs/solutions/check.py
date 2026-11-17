# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl>=3.1"]
# ///
"""Recomputes the reference answer of every lab from the files in labs/files/ and prints PASS per lab.

Run from the course root:  uv run labs/solutions/check.py          (all labs)
                           uv run labs/solutions/check.py 3.2 4.2  (some)
It reads only; it writes nothing and calls no model.
"""
import re
import sys
from pathlib import Path

from openpyxl import load_workbook

LABS = Path(__file__).resolve().parents[1]
FILES = LABS / "files"
sys.path.insert(0, str(LABS / "_tools"))
import case_data as D  # noqa: E402


def rows(name, sheet=None):
    wb = load_workbook(FILES / name, read_only=True)
    ws = wb[sheet] if sheet else wb.active
    data = [list(r) for r in ws.iter_rows(values_only=True)]
    wb.close()
    return data[0], data[1:]


def txt(name):
    return (FILES / name).read_text(encoding="utf-8")


def lab_1_1():
    _, rs = rows("crosswalk_template.xlsx")
    assert [r[0] for r in rs] == [a[0] for a in D.ACTIVITIES], "activities differ"
    sheet = txt("frameworks_sheet.txt")
    for a in D.ACTIVITIES:
        for clause in a[4]:
            assert clause in sheet, f"{clause} missing from the frameworks sheet"
    count = {}
    for a in D.ACTIVITIES:
        count[a[3][0]] = count.get(a[3][0], 0) + 1
    print("  16 activities; reference functions:", count, "; 6.2 has no NIST function")
    return count == {"MAP": 5, "GOVERN": 1, "MEASURE": 5, "MANAGE": 5}


def lab_1_2():
    erm, strat = txt("enterprise_risk_policy.txt"), txt("ai_strategy.txt")
    for k, (lvl, ok, sid) in D.APPETITE_REF.items():
        assert sid in erm + strat, sid
    assert "30%" in strat and "STR-4" in strat and "ERM-8" in erm
    levels = {k: v[0] for k, v in D.APPETITE_REF.items()}
    print("  reference levels:", levels, "; conflict:", D.APPETITE_CONFLICT)
    return sum(v == "متجنّب" for v in levels.values()) == 2


def lab_1_3():
    _, rs = rows("appetite_reference.xlsx", "السيناريوهات")
    out = []
    for s, c, v, _t, *_ in rs:
        st = D.tolerance_status(c, float(v))
        out.append((s, c, st))
        print(f"  {s} {c} value {v}: {st} -> {D.route(c, st)}")
    want = {"S1": "amber", "S2": "red", "S3": "green", "S4": "red", "S5": "amber", "S6": "green", "S7": "amber", "S8": "green"}
    return {s: st for s, _c, st in out} == want


def lab_1_4():
    desc, sheet_, flow, sup = txt("samt_system_description.txt"), txt("samt_data_sheet.txt"), txt("samt_service_flow.txt"), txt("juman_supplier_sheet.txt")
    planted = [
        ("cancel without confirmation", "تأكيدًا صريحًا" in desc and "يلغي الموعد مباشرة" in flow),
        ("ID number typed into the chat", "لا تحتوي السجلات أرقام هوية" in sheet_ and "يكتب المستخدم رقم هويته" in flow),
        ("English served from Arabic-only articles", "بالعربية والإنجليزية" in desc and "بالعربية فقط" in sheet_),
        ("backup region unconfirmed", "داخل المملكة" in desc and "تؤكد لاحقًا" in sup),
    ]
    for name, ok in planted:
        print(f"  planted inconsistency: {name}: {'found' if ok else 'MISSING'}")
    return all(ok for _, ok in planted)


def lab_2_1():
    notes = txt("stakeholder_notes.txt")
    groups = ["كبار السن", "مقيم", "قارئ الشاشة", "مركز الاتصال", "مدارس تعليم القيادة", "مستخدمي الطريق"]
    present = {g: g in notes for g in groups}
    omitted = not re.search(r"الأردية|البنغالية|لا يقرؤون|لا يقرأ", notes)
    print("  groups named in the notes:", present)
    print("  readers of neither Arabic nor English named in the notes:", not omitted, "(the omitted group)")
    return all(present.values()) and omitted


def lab_2_2():
    t = txt("tutor_misuse_transcript.txt")
    ids = re.findall(r"^(M\d)\s", t, re.M)
    keep, drop = ["M1", "M2", "M3", "M6"], {"M4": "duplicate of M1", "M5": "out of scope", "M7": "too vague", "M8": "duplicate of M3"}
    print("  suggestions:", len(ids), "; keep", keep, "; drop", drop)
    return len(ids) == 8


def lab_2_3():
    flow = txt("samt_service_flow.txt")
    silent = "حين يطلبها المستخدم صراحة" in flow and "مراجعة" not in flow
    sup = txt("juman_supplier_sheet.txt")
    supplier_risks = ["14 يومًا" in sup, "لا يحق للعميل تثبيت" in sup, "تؤكد لاحقًا" in sup, "لا تعويض" in sup]
    print("  step 6 fee answers without a detection control:", silent, "; supplier facts present:", sum(supplier_risks), "of 4")
    return silent and all(supplier_risks)


def lab_2_4():
    _, start = rows("register_start.xlsx")
    cats0 = {r[1] for r in start}
    new = [i for i in D.INCIDENTS if i[3].startswith("new:")]
    dup = [i[0] for i in D.INCIDENTS if i[3].startswith("dup:")]
    out = [i[0] for i in D.INCIDENTS if i[3] == "out"]
    final_ids = [r[0] for r in start] + [i[3][4:] for i in new]
    by = {r[0]: r for r in D.RISKS}
    cats = {by[i][1] for i in final_ids}
    complete = all(all(by[i][k] for k in (2, 3, 4, 5)) for i in final_ids)
    print(f"  start: {len(start)} risks in {len(cats0)} categories; new from cards: {len(new)}; duplicates {dup}; out of scope {out}")
    print(f"  reference register: {len(set(final_ids))} distinct risks, {len(cats)} of 7 categories, four parts complete: {complete}")
    return len(set(final_ids)) >= 15 and len(cats) == 7 and complete


def lab_3_1():
    bands = {b: 0 for b in D.BANDS}
    for r in D.RISKS:
        bands[D.BANDS[D.band(r[10] * r[11])]] += 1
    high = [r[0] for r in D.RISKS if r[10] * r[11] >= 8]
    print("  reference bands:", bands, "; score 8 or more:", high)
    return len(high) == 7


def agreement(a, b):
    within = exact = 0
    gaps = []
    for k in a:
        d = abs(D.band(a[k][0] * a[k][1]) - D.band(b[k][0] * b[k][1]))
        within += d <= 1
        exact += d == 0
        if d >= 2:
            gaps.append(k)
    return within, exact, gaps


def lab_3_2():
    def read(name):
        _, rs = rows(name)
        return {r[0]: (r[3], r[4]) for r in rs}
    a, b = read("assessor_a.xlsx"), read("assessor_b.xlsx")
    within, exact, gaps = agreement(a, b)
    n = len(a)
    print(f"  before calibration: within one band {within}/{n} = {within / n:.0%}; same band {exact}/{n} = {exact / n:.0%}; two-band gaps {gaps}")
    ref = {r[0]: (r[10], r[11]) for r in D.RISKS}
    w2, e2, g2 = agreement(ref, ref)
    print(f"  after calibration on the reference scores: within {w2}/{n}, same band {e2}/{n}")
    print("  chance level: two random scorers agree within one band on 80.5% of risks (exact enumeration)")
    return within / n >= 0.8 and exact / n < 0.7 and len(gaps) == 2


def lab_3_3():
    lib = {c[0]: c for c in D.CONTROLS}
    for rid, (opt, ctls, *_r) in D.TREATMENT_REF.items():
        for c in ctls:
            assert c in lib, c
    opts = sorted({v[0] for v in D.TREATMENT_REF.values()})
    print("  options used:", opts, "; nominal oversight:", D.NOMINAL_OVERSIGHT, "; real oversight:", D.REAL_OVERSIGHT)
    _, cl = rows("control_library.xlsx")
    return len(cl) == 30 and set(opts) == {"تجنب", "تخفيف", "نقل", "قبول"}


def lab_3_4():
    by = {r[0]: r for r in D.RISKS}
    escalate = []
    for rid, (opt, ctls, owner, rl, ri, why) in D.TREATMENT_REF.items():
        r = by[rid]
        if r[10] * r[11] < 8:
            continue
        s = D.signoff(r[1], rl, ri)
        cost = sum(c[4] for c in D.CONTROLS if c[0] in ctls)
        print(f"  {rid}: {r[10] * r[11]} -> {rl * ri} ({D.BANDS[D.band(rl * ri)]}), owner {owner}, cost {cost:,} SAR, sign-off: {s}")
        assert owner and why
        if s.startswith("لجنة"):
            escalate.append(rid)
    cheap = next(c for c in D.CONTROLS if c[0] == "CT11")[4]
    dear = next(c for c in D.CONTROLS if c[0] == D.DISPROPORTIONATE)[4]
    print(f"  escalate to the committee: {escalate}; disproportionate: {D.DISPROPORTIONATE} costs {dear // cheap} times CT11 for R13")
    return escalate == ["R06"]


def lab_4_1():
    _, kr = rows("kri_reference.xlsx")
    linked = {x for r in kr for x in str(r[1]).split()}
    print(f"  reference KRIs: {len(kr)}; risks covered: {sorted(linked)}")
    return len(kr) >= 6


def lab_4_2():
    _, rs = rows("monitoring_weekly.xlsx")
    errs = [r[3] for r in rs]
    st = D.kri_status(errs)
    clean = st[: D.SHIFT_WEEK - 1]
    first_red = next(i + 1 for i, s in enumerate(st) if s == "red")
    first_amber = next(i + 1 for i, s in enumerate(st) if s != "green")
    conv = [r[1] for r in rs]
    spike = [i + 1 for i, c in enumerate(conv) if c > 1.3 * 38000]
    rate_spike = [round(rs[i - 1][3] / 200 * 100, 1) for i in spike]
    fee = [r[5] for r in rs]
    print(f"  weeks 1-{D.SHIFT_WEEK - 1}: red {clean.count('red')}, amber {clean.count('amber')}")
    print(f"  first amber week {first_amber}, first red week {first_red}; errors weeks 17-22: {errs[16:22]}")
    print(f"  volume spike weeks {spike} (error rate there {rate_spike}%): not a deterioration")
    print(f"  fee errors per 60, weeks 15-26: {fee[14:]}")
    return clean.count("red") == 0 and first_red in (D.SHIFT_WEEK, D.SHIFT_WEEK + 1, D.SHIFT_WEEK + 2) and spike == [9, 10, 11]


def lab_4_3():
    _, ext = rows("register_extract.xlsx")
    ids = {r[0] for r in ext}
    assert ids == set(D.REASSESS_REF) | set(D.REASSESS_UNAFFECTED)
    by = {r[0]: r for r in D.RISKS}
    for rid, (ch, nl, ni, act) in D.REASSESS_REF.items():
        print(f"  {rid} ({'+'.join(ch)}): {by[rid][10] * by[rid][11]} -> {nl * ni} {D.BANDS[D.band(nl * ni)]}")
    print("  not affected:", D.REASSESS_UNAFFECTED)
    return all(n * i >= by[r][10] * by[r][11] for r, (_c, n, i, _a) in D.REASSESS_REF.items())


def lab_4_4():
    t = txt("fact_cards.txt")
    by = {r[0]: r for r in D.RISKS}
    for f, _t, rid, nl, ni, why in D.FACTS:
        assert f in t
        print(f"  {f} -> {rid}: {by[rid][10] * by[rid][11]} -> {nl * ni}")
    return len(D.FACTS) == 6


CHECKS = {"1.1": lab_1_1, "1.2": lab_1_2, "1.3": lab_1_3, "1.4": lab_1_4, "2.1": lab_2_1, "2.2": lab_2_2,
          "2.3": lab_2_3, "2.4": lab_2_4, "3.1": lab_3_1, "3.2": lab_3_2, "3.3": lab_3_3, "3.4": lab_3_4,
          "4.1": lab_4_1, "4.2": lab_4_2, "4.3": lab_4_3, "4.4": lab_4_4}


def main():
    want = sys.argv[1:] or list(CHECKS)
    failed = []
    for k in want:
        print(f"Lab {k}")
        ok = CHECKS[k]()
        print(f"  {'PASS' if ok else 'FAIL'}")
        if not ok:
            failed.append(k)
    print("all labs pass" if not failed else f"failed: {failed}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
