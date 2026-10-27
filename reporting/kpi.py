"""KPI panels using measured scenario outcomes only; no external assets."""
from collections import Counter
from html import escape

STATUSES = ('Passed', 'Failed', 'Error', 'Skipped', 'Not run')
COLORS = {'Passed':'#268563', 'Failed':'#c74b60', 'Error':'#b87820', 'Skipped':'#8564b0', 'Not run':'#8794a5'}


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
<div class="panel"><h2>How to read this dashboard</h2><div class="panelbody guide"><p><b>Passed:</b> the automated assertions succeeded.</p><p><b>Failed:</b> open the scenario and compare its expected result with the evidence.</p><p><b>Error:</b> setup or cleanup failed; check the environment.</p><p><b>Skipped / not run:</b> no pass is claimed.</p><p class="caption">Current run only. Weekly trends, severity and resolution times require a separate defect history.</p></div></div></section>'''
