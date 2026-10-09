"""KPI panels using measured scenario outcomes only; no external assets."""
from collections import Counter
from html import escape

STATUSES = ('Passed', 'Failed', 'Error', 'Skipped', 'Not run')
COLORS = {'Passed':'#87c948', 'Failed':'#f04438', 'Error':'#ffc400', 'Skipped':'#8854bd', 'Not run':'#8794a5'}


def panels(rows):
    groups = sorted({r['group'] for r in rows})
    counts = Counter(r['status'] for r in rows)
    table_rows, bars, durations = [], [], []
    for group in groups:
        subset = [r for r in rows if r['group'] == group]
        c = Counter(r['status'] for r in subset)
        table_rows.append('<tr><th scope="row">'+escape(group)+'</th>'+''.join(f'<td>{c[s]}</td>' for s in STATUSES)+f'<td>{len(subset)}</td></tr>')
        segments = ''.join(f'<span style="width:{100*c[s]/len(subset):.4f}%;background:{COLORS[s]}" title="{s}: {c[s]}">{c[s]}</span>' for s in STATUSES if c[s])
        label = ', '.join(f'{s}: {c[s]}' for s in STATUSES)
        bars.append(f'<div class="barrow"><span>{escape(group)}</span><div class="stack" role="img" aria-label="{escape(group)} — {label}">{segments}</div><small>{len(subset)} tests</small></div>')
        measured = [r['duration'] for r in subset if r['status'] not in ('Skipped', 'Not run')]
        average = f'{sum(measured)/len(measured):.2f}s' if measured else '—'
        longest = f'{max(measured):.2f}s' if measured else '—'
        durations.append(f'<tr><th scope="row">{escape(group)}</th><td>{len(measured)}</td><td>{average}</td><td>{longest}</td></tr>')
    table_rows.append('<tr class="total"><th scope="row">Total</th>'+''.join(f'<td>{counts[s]}</td>' for s in STATUSES)+f'<td>{len(rows)}</td></tr>')
    legend = ''.join(f'<span><i style="background:{COLORS[s]}"></i>{s}</span>' for s in STATUSES)
    headings = ''.join(f'<th scope="col" style="border-top:4px solid {COLORS[s]}">{s}</th>' for s in STATUSES)
    slowest = sorted((r for r in rows if r['status'] not in ('Skipped','Not run')), key=lambda r:r['duration'], reverse=True)[:6]
    maximum = max((r['duration'] for r in slowest), default=0) or 1
    timings = ''.join(f'<div class="timing"><span title="{escape(r["title"], quote=True)}">{escape(r["case"])} · {escape(r["title"])}</span><div><b style="width:{100*r["duration"]/maximum:.4f}%"></b></div><strong>{r["duration"]:.2f}s</strong></div>' for r in slowest)
    empty = '<p class="muted">No executed scenarios in this run.</p>'
    reviewed = counts['Passed'] + counts['Failed'] + counts['Error']
    rate = f'{100*counts["Passed"]/reviewed:.1f}%' if reviewed else '—'
    return f'''<section class="kpi-grid" aria-label="Run KPI dashboard">
<div class="panel wide"><h2>Test outcomes by function</h2><div class="split"><div class="table-scroll"><table><thead><tr><th scope="col">Function</th>{headings}<th scope="col">Total</th></tr></thead><tbody>{''.join(table_rows)}</tbody></table></div><div class="distribution"><div class="scale"><span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span></div>{''.join(bars) or '<p>No selected scenarios.</p>'}<div class="legend">{legend}</div></div></div></div>
<div class="panel"><h2>Scenario execution time</h2><div class="panelbody">{timings or empty}<p class="caption">Longest six scenarios · seconds, including setup and cleanup.</p></div></div>
<div class="panel"><h2>Run completion and review</h2><div class="panelbody"><div class="completion"><strong>{rate}</strong><div>Pass share of attempted scenarios<small>{counts['Passed']} passed / {reviewed} attempted, including errors</small></div></div><dl><div><dt>Checks needing investigation</dt><dd>{counts['Failed']+counts['Error']}</dd></div><div><dt>Skipped or not run</dt><dd>{counts['Skipped']+counts['Not run']}</dd></div><div><dt>Confirmed website defects</dt><dd>Not assessed</dd></div></dl><p class="caption">A failed check is not automatically a website defect.</p></div></div>
<div class="panel"><h2>Average execution time by function</h2><div class="panelbody table-scroll"><table><thead><tr><th>Function</th><th>Attempted</th><th>Average</th><th>Longest</th></tr></thead><tbody>{''.join(durations)}</tbody></table><p class="caption">Skipped and not-run scenarios excluded. Includes setup and cleanup.</p></div></div>
<div class="panel"><h2>How to read this dashboard</h2><div class="panelbody guide"><p><b>Passed:</b> the automated assertions succeeded.</p><p><b>Failed:</b> inspect the expected result and evidence below.</p><p><b>Error:</b> setup or cleanup failed; check the environment.</p><p><b>Skipped / not run:</b> no pass is claimed.</p><p class="caption">Current run only. Weekly trends, severity and resolution times require a separate defect history.</p></div></div></section>'''


CSS = '''
:root{background:#fff;color:#282d33;font-family:Arial,Helvetica,sans-serif}body{border-top:5px solid #7530ae}main{max-width:1440px;padding:26px 30px}header{margin-bottom:14px}h1{font-size:34px;letter-spacing:-.8px}.eyebrow{color:#7530ae}.metrics{gap:0;border:1px solid #d9dce1;margin:18px 0}.metric{border:0;border-right:1px solid #d9dce1;border-radius:0;padding:10px 18px}.metric:last-child{border-right:0}.metric strong{font-size:28px}.kpi-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:14px 0 24px}.panel{border:1px solid #d6d8dc;padding:7px;min-width:0}.panel.wide{grid-column:1/-1}.panel>h2{font-size:16px;background:#f0f0f0;padding:7px 9px;margin:0;font-weight:700}.split{display:grid;grid-template-columns:1fr 1.25fr;gap:20px;padding:16px 5px 10px}.table-scroll{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:12px}th,td{padding:7px 8px;border:1px solid #dedede;text-align:center;white-space:nowrap}th:first-child{text-align:left}thead{background:#f3f4f5}tbody tr:nth-child(even){background:#f4f4f4}.total{font-weight:bold;border-bottom:2px solid #009ffa}.barrow{display:grid;grid-template-columns:85px 1fr 45px;gap:7px;align-items:center;font-size:11px;margin:8px 0}.stack{display:flex;height:25px;background:#f0f0f0;overflow:hidden}.stack>span{display:flex;align-items:center;justify-content:center;font-size:11px;color:#111;font-weight:bold;overflow:hidden}.stack>span[style*="#8854bd"]{color:white}.scale{display:flex;justify-content:space-between;margin:0 50px 6px 92px;color:#666;font-size:10px}.legend{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;font-size:11px;margin-top:12px}.legend i{display:inline-block;width:8px;height:8px;margin-right:4px}.panelbody{padding:12px 8px 5px}.caption{font-size:11px;color:#687078;margin:12px 0 2px}.timing{display:grid;grid-template-columns:45% 1fr 55px;gap:8px;align-items:center;margin:9px 0;font-size:11px}.timing>span{white-space:nowrap;text-overflow:ellipsis;overflow:hidden}.timing>div{background:#ecf7ff;height:13px}.timing b{display:block;height:13px;background:#009fff}.timing strong{text-align:right;font-weight:400}.completion{display:flex;align-items:center;gap:20px}.completion>strong{font-size:40px;color:#009fff}.completion>div{font-size:13px}.completion small{display:block;color:#687078;font-size:11px}dl{margin:10px 0}dl>div{display:flex;justify-content:space-between;border-top:1px solid #eee;padding:5px 0;font-size:12px}dd{margin:0;font-weight:bold}.guide p{font-size:12px;margin:0 0 7px}.notice{font-size:12px;border-radius:0;background:#f6f3fa;border-left-color:#7530ae;padding:10px 14px;margin:0 0 18px}article{border-radius:0;padding:18px;margin:8px 0}.toolbar{padding:12px;background:#f2f2f2;gap:10px}.toolbar input,.toolbar select,.toolbar button{border-radius:2px;padding:8px}.columns{gap:20px;font-size:13px}.rowhead h2{font-size:17px}.badge{border-radius:2px}.panel{break-inside:avoid}@media(max-width:850px){.split{grid-template-columns:1fr}.kpi-grid{grid-template-columns:1fr}.panel.wide{grid-column:auto}main{padding:20px 12px}h1{font-size:26px}.metrics{grid-template-columns:repeat(5,1fr)}.metric{padding:8px}.metric span{font-size:10px}.metric strong{font-size:23px}}@media print{body{border:0}.kpi-grid{grid-template-columns:1fr 1fr}.split{grid-template-columns:1fr 1fr}h1{font-size:25px}.panel>h2{font-size:13px}*{print-color-adjust:exact;-webkit-print-color-adjust:exact}}
'''
