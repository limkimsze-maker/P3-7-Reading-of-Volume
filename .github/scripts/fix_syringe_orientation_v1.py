from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old='''      <line x1="${x-48}" y1="${y+h/2}" x2="${x}" y2="${y+h/2}" stroke="#6b52a3" stroke-width="8" stroke-linecap="round"/>
      <rect x="${x-73}" y="${y+8}" width="25" height="50" rx="8" fill="#d9cff4" stroke="#6b52a3" stroke-width="4"/>
      <line x1="${x+w}" y1="${y+h/2}" x2="${x+w+34}" y2="${y+h/2}" stroke="#6b52a3" stroke-width="8" stroke-linecap="round"/>
      <path d="M${x+w+34} ${y+h/2-9} L${x+w+62} ${y+h/2} L${x+w+34} ${y+h/2+9} Z" fill="#d9cff4" stroke="#6b52a3" stroke-width="3"/>'''
new='''      <line x1="${x-34}" y1="${y+h/2}" x2="${x}" y2="${y+h/2}" stroke="#6b52a3" stroke-width="8" stroke-linecap="round"/>
      <path d="M${x-34} ${y+h/2-9} L${x-62} ${y+h/2} L${x-34} ${y+h/2+9} Z" fill="#d9cff4" stroke="#6b52a3" stroke-width="3"/>
      <line x1="${x+fillW}" y1="${y+h/2}" x2="${x+w+48}" y2="${y+h/2}" stroke="#6b52a3" stroke-width="6" stroke-linecap="round"/>
      <rect x="${x+w+48}" y="${y+8}" width="25" height="50" rx="8" fill="#d9cff4" stroke="#6b52a3" stroke-width="4"/>'''
if old not in s:
    raise SystemExit('Expected syringe segment not found')
s=s.replace(old,new,1)
s=s.replace('Read volume in ml • jug • dispenser • syringe','Read volume in ml • jug • measuring cylinder • syringe')
s=s.replace('Read the volume in a dispenser or measuring cylinder','Read the volume in a measuring cylinder')
p.write_text(s,encoding='utf-8')
