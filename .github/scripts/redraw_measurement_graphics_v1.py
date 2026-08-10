from pathlib import Path
import re

p = Path("index.html")
s = p.read_text(encoding="utf-8")

s = s.replace(
    'badge:"Dispenser",\n    question:"What is the volume of chilli oil in the dispenser?",',
    'badge:"Cylinder",\n    question:"What is the volume of blue sports drink in the measuring cylinder?",'
)
s = s.replace(
    'explain:`The dispenser reads ${formatNum(value)} ml.`',
    'explain:`The measuring cylinder reads ${formatNum(value)} ml.`'
)
s = s.replace(
    'question:"What is the volume of medicine syrup in the syringe?",',
    'question:"What is the volume of coloured water in the syringe?",'
)

beakers = r'''function beakerPairSVG(v1,v2){
  function oneCup(x,v,label){
    const max=1000, top=34, bottom=190, right=118;
    const fillH=(v/max)*(bottom-top);
    const y=bottom-fillH;
    let ticks="";
    for(let m=50;m<=1000;m+=50){
      const ty=bottom-(m/max)*(bottom-top);
      const major=m%100===0;
      ticks+=`<line x1="${right-(major?24:14)}" y1="${ty}" x2="${right}" y2="${ty}" stroke="${major?'#173b5e':'#68859d'}" stroke-width="${major?2.4:1.4}"/>`;
      if(major) ticks+=`<text x="${right+7}" y="${ty+4}" font-size="12" font-weight="900" fill="#173b5e">${m}</text>`;
    }
    return `<g transform="translate(${x},10)">
      <path d="M24 22 H112 L104 190 Q103 204 88 204 H42 Q27 204 26 190 Z" fill="#f8fdff" stroke="#176ca5" stroke-width="4" stroke-linejoin="round"/>
      <path d="M34 28 H100" stroke="#176ca5" stroke-width="7" stroke-linecap="round"/>
      <path d="M28 ${y} H102 L98 190 Q97 196 88 196 H43 Q34 196 33 190 Z" fill="#ffbf4a" opacity=".82"/>
      <line x1="31" y1="${y}" x2="101" y2="${y}" stroke="#e68a12" stroke-width="3"/>
      ${ticks}
      <rect x="30" y="210" width="84" height="22" rx="11" fill="#e9f6ff"/>
      <text x="72" y="225" text-anchor="middle" font-size="13" font-weight="900" fill="#0b5a90">${label}</text>
      <text x="72" y="50" text-anchor="middle" font-size="10" font-weight="900" fill="#176ca5">ml</text>
    </g>`;
  }
  return `<svg class="measureSvg" viewBox="0 0 680 250" aria-label="two original measuring cups and a sports jug">
    <defs><linearGradient id="sfJug" x1="0" x2="1"><stop offset="0" stop-color="#e9f8ff"/><stop offset="1" stop-color="#cfefff"/></linearGradient></defs>
    <g transform="translate(18,28)">
      <path d="M48 30 H180 L166 176 Q164 198 142 202 H70 Q48 198 46 176 Z" fill="url(#sfJug)" stroke="#176ca5" stroke-width="5"/>
      <path d="M54 112 H172 L166 176 Q164 190 142 194 H70 Q54 191 52 176 Z" fill="#ffbf4a" opacity=".72"/>
      <path d="M176 47 Q224 52 221 103 Q219 153 171 158" fill="none" stroke="#176ca5" stroke-width="12" stroke-linecap="round"/>
      <path d="M180 47 L208 34" stroke="#176ca5" stroke-width="8" stroke-linecap="round"/>
      <rect x="67" y="45" width="77" height="24" rx="12" fill="#176ca5"/>
      <text x="106" y="62" text-anchor="middle" font-size="12" font-weight="900" fill="#fff">SPORTS MIX</text>
    </g>
    <g transform="translate(258,105)"><path d="M0 9 H47 V0 L88 18 L47 36 V27 H0 Z" fill="#31a67a"/></g>
    ${oneCup(365,v1,'Cup A')}
    ${oneCup(515,v2,'Cup B')}
  </svg>`;
}

'''
s, n = re.subn(
    r'function beakerPairSVG\(v1,v2\)\{.*?\n\}\n\nfunction cylinderSVG',
    beakers + 'function cylinderSVG', s, count=1, flags=re.S
)
if n != 1:
    raise SystemExit("Could not replace beakerPairSVG")

cylinder = r'''function cylinderSVG(value,mode){
  const max=60;
  const x=226, y0=22, w=126, h=182;
  const fillH=(value/max)*h, fillY=y0+h-fillH;
  const step=Number(mode)||10;
  let ticks="";
  const tickStep=step===1?1:step===5?5:10;
  for(let m=0;m<=60;m+=tickStep){
    const y=y0+h-(m/max)*h;
    const major=m%10===0;
    const mid=m%5===0;
    const len=major?42:mid?28:16;
    ticks+=`<line x1="${x+w}" y1="${y}" x2="${x+w+len}" y2="${y}" stroke="${major?'#173b5e':'#6d8497'}" stroke-width="${major?3.2:1.5}"/>`;
    if(major && m<60) ticks+=`<text x="${x+w+50}" y="${y+6}" font-size="20" font-weight="900" fill="#173b5e">${m}</text>`;
  }
  return `<svg class="measureSvg" viewBox="0 0 640 240" aria-label="original Sports Lab measuring cylinder">
    <g>
      <rect x="188" y="9" width="230" height="28" rx="14" fill="#176ca5"/>
      <text x="303" y="28" text-anchor="middle" font-size="14" font-weight="900" fill="#fff">SPORTS LAB • 60 ml</text>
      <path d="M${x} ${y0} H${x+w} L${x+w-8} ${y0+h} H${x+8} Z" fill="#f8fdff" stroke="#176ca5" stroke-width="4"/>
      <path d="M${x+8} ${fillY} H${x+w-8} L${x+w-14} ${y0+h-4} H${x+14} Z" fill="#62c6e8" opacity=".88"/>
      <line x1="${x+8}" y1="${fillY}" x2="${x+w-8}" y2="${fillY}" stroke="#1689bd" stroke-width="3"/>
      ${ticks}
      <path d="M${x+22} ${y0+h+4} H${x+w-22} L${x+w+5} ${y0+h+22} H${x-5} Z" fill="#dcefff" stroke="#176ca5" stroke-width="4"/>
      <text x="${x+w/2}" y="232" text-anchor="middle" font-size="18" font-weight="900" fill="#0b5a90">ml</text>
    </g>
  </svg>`;
}

'''
s, n = re.subn(
    r'function cylinderSVG\(value,mode\)\{.*?\n\}\n\nfunction syringeSVG',
    cylinder + 'function syringeSVG', s, count=1, flags=re.S
)
if n != 1:
    raise SystemExit("Could not replace cylinderSVG")

syringe = r'''function syringeSVG(value,mode,showHelper){
  const max=10;
  const x=160, y=112, w=330, h=66;
  const fillW=(value/max)*w;
  let ticks="";
  for(let m=0;m<=10;m++){
    const tx=x+(m/max)*w;
    ticks+=`<line x1="${tx}" y1="${y}" x2="${tx}" y2="${y+(m%5===0?25:17)}" stroke="#273f57" stroke-width="${m%5===0?3:2}"/>`;
    if(m<10) ticks+=`<text x="${tx+5}" y="${y+40}" font-size="15" font-weight="900" fill="#273f57">${m}</text>`;
  }
  const helper=showHelper?`<g><rect x="155" y="28" width="340" height="48" rx="24" fill="#f1ebff" stroke="#bcaee8" stroke-width="3"/><text x="325" y="48" text-anchor="middle" font-size="14" font-weight="900" fill="#523f89">Needleless 10 ml syringe</text><text x="325" y="67" text-anchor="middle" font-size="13" font-weight="900" fill="#523f89">Each numbered interval is 1 ml.</text></g>`:'';
  return `<svg class="measureSvg" viewBox="0 0 640 240" aria-label="original needleless 10 ml syringe">
    ${helper}
    <g>
      <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="22" fill="#f8fdff" stroke="#6b52a3" stroke-width="5"/>
      <rect x="${x+4}" y="${y+5}" width="${Math.max(0,fillW-6)}" height="${h-10}" rx="16" fill="#65d1c2" opacity=".9"/>
      <line x1="${x+fillW}" y1="${y-9}" x2="${x+fillW}" y2="${y+h+9}" stroke="#4d397d" stroke-width="6"/>
      ${ticks}
      <line x1="${x-48}" y1="${y+h/2}" x2="${x}" y2="${y+h/2}" stroke="#6b52a3" stroke-width="8" stroke-linecap="round"/>
      <rect x="${x-73}" y="${y+8}" width="25" height="50" rx="8" fill="#d9cff4" stroke="#6b52a3" stroke-width="4"/>
      <line x1="${x+w}" y1="${y+h/2}" x2="${x+w+34}" y2="${y+h/2}" stroke="#6b52a3" stroke-width="8" stroke-linecap="round"/>
      <path d="M${x+w+34} ${y+h/2-9} L${x+w+62} ${y+h/2} L${x+w+34} ${y+h/2+9} Z" fill="#d9cff4" stroke="#6b52a3" stroke-width="3"/>
      <rect x="${x+118}" y="${y+h+18}" width="96" height="24" rx="12" fill="#6b52a3"/>
      <text x="${x+166}" y="${y+h+35}" text-anchor="middle" font-size="12" font-weight="900" fill="#fff">SPORTS LAB</text>
      <text x="${x+w+72}" y="${y+h/2+6}" font-size="16" font-weight="900" fill="#0b5a90">ml</text>
    </g>
  </svg>`;
}

'''
s, n = re.subn(
    r'function syringeSVG\(value,mode,showHelper\)\{.*?\n\}\n\nfunction renderMeasureScene',
    syringe + 'function renderMeasureScene', s, count=1, flags=re.S
)
if n != 1:
    raise SystemExit("Could not replace syringeSVG")

p.write_text(s, encoding="utf-8")
