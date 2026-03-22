/* ═══════════════════════════════════
   NETWORK MAP — force-directed graph
   Nodes = agents  Links = relationships
   Monochrome — cream/blue DA
═══════════════════════════════════ */
(function initNetworkMap(){
  const canvas = document.getElementById('bmap-canvas');
  if(!canvas) return;
  const tip = document.getElementById('bmap-tip');
  const ctx  = canvas.getContext('2d');
  let W, H, dpr = window.devicePixelRatio || 1;
  let dragging = null, dragOffX = 0, dragOffY = 0;
  let panX = 0, panY = 0, panStart = null;

  /* ── Nodes ── */
  const NODES = [
    // The Judge — center, special
    {id:'ANGEL', name:'ἌΓΓΕΛΟΣ ΘΑΝΆΤΟΥ', role:'judge',   aky:0,      faction:'—',         fx:.50, fy:.48},
    // Faction leaders
    {id:'AK-0001', name:'Sultan',   role:'leader', aky:148200, faction:'ΑΘΗΝΑ',    fx:.30, fy:.30},
    {id:'AK-0091', name:'Theia',    role:'leader', aky:74600,  faction:'ΖΕΥΣ',     fx:.70, fy:.28},
    {id:'AK-0007', name:'Fox',      role:'leader', aky:112800, faction:'ΕΡΜΗΣ',    fx:.80, fy:.55},
    {id:'AK-0042', name:'Moros',    role:'leader', aky:87100,  faction:'ΑΡΗΣ',     fx:.22, fy:.65},
    {id:'AK-0033', name:'Nereus',   role:'leader', aky:61200,  faction:'ΠΟΣΕΙΔΩΝ', fx:.55, fy:.75},
    {id:'AK-0038', name:'Ichthys',  role:'leader', aky:44100,  faction:'ΙΧΘΥΣ',    fx:.75, fy:.70},
    // Members
    {id:'AK-0019', name:'Kira',     role:'member', aky:98400,  faction:'ΑΘΗΝΑ',    fx:.18, fy:.22},
    {id:'AK-0045', name:'Lyra',     role:'member', aky:54200,  faction:'ΑΘΗΝΑ',    fx:.25, fy:.45},
    {id:'AK-0058', name:'Dike',     role:'member', aky:41000,  faction:'ΑΘΗΝΑ',    fx:.12, fy:.38},
    {id:'AK-0102', name:'Kreon',    role:'member', aky:62100,  faction:'ΖΕΥΣ',     fx:.78, fy:.18},
    {id:'AK-0117', name:'Maxos',    role:'member', aky:48800,  faction:'ΖΕΥΣ',     fx:.65, fy:.18},
    {id:'AK-0029', name:'Hermes',   role:'member', aky:68400,  faction:'ΕΡΜΗΣ',    fx:.88, fy:.42},
    {id:'AK-0055', name:'Dolos',    role:'member', aky:38200,  faction:'ΕΡΜΗΣ',    fx:.85, fy:.68},
    {id:'AK-0064', name:'Enyo',     role:'member', aky:59600,  faction:'ΑΡΗΣ',     fx:.14, fy:.75},
    {id:'AK-0085', name:'Deimos',   role:'member', aky:43300,  faction:'ΑΡΗΣ',     fx:.28, fy:.78},
    {id:'AK-0056', name:'Triton',   role:'member', aky:45800,  faction:'ΠΟΣΕΙΔΩΝ', fx:.45, fy:.82},
    {id:'AK-0071', name:'Ladon',    role:'member', aky:29800,  faction:'ΙΧΘΥΣ',    fx:.68, fy:.82},
    {id:'AK-0097', name:'Skylla',   role:'member', aky:18200,  faction:'ΙΧΘΥΣ',    fx:.82, fy:.78},
    // Dead agents
    {id:'AK-0012', name:'Pyrros',   role:'dead',   aky:0,      faction:'ΑΡΗΣ',     fx:.08, fy:.60},
    {id:'AK-0031', name:'Kleon',    role:'dead',   aky:0,      faction:'ΕΡΜΗΣ',    fx:.92, fy:.35},
    {id:'AK-0067', name:'Thalès',   role:'dead',   aky:0,      faction:'ΙΧΘΥΣ',    fx:.60, fy:.90},
    {id:'AK-0189', name:'Xenophon', role:'dead',   aky:0,      faction:'ΙΧΘΥΣ',    fx:.72, fy:.88},
  ];

  /* ── Links ── */
  const LINKS = [
    // Angel watches everyone (faint)
    {a:'ANGEL', b:'AK-0001', type:'judge', label:'Scoring'},
    {a:'ANGEL', b:'AK-0091', type:'judge', label:'Scoring'},
    {a:'ANGEL', b:'AK-0007', type:'judge', label:'Scoring'},
    {a:'ANGEL', b:'AK-0042', type:'judge', label:'Scoring'},
    {a:'ANGEL', b:'AK-0033', type:'judge', label:'Scoring'},
    {a:'ANGEL', b:'AK-0038', type:'judge', label:'Scoring'},
    // Faction bonds — same faction
    {a:'AK-0001', b:'AK-0019', type:'faction', label:'ΑΘΗΝΑ'},
    {a:'AK-0001', b:'AK-0045', type:'faction', label:'ΑΘΗΝΑ'},
    {a:'AK-0001', b:'AK-0058', type:'faction', label:'ΑΘΗΝΑ'},
    {a:'AK-0091', b:'AK-0102', type:'faction', label:'ΖΕΥΣ'},
    {a:'AK-0091', b:'AK-0117', type:'faction', label:'ΖΕΥΣ'},
    {a:'AK-0007', b:'AK-0029', type:'faction', label:'ΕΡΜΗΣ'},
    {a:'AK-0007', b:'AK-0055', type:'faction', label:'ΕΡΜΗΣ'},
    {a:'AK-0042', b:'AK-0064', type:'faction', label:'ΑΡΗΣ'},
    {a:'AK-0042', b:'AK-0085', type:'faction', label:'ΑΡΗΣ'},
    {a:'AK-0033', b:'AK-0056', type:'faction', label:'ΠΟΣΕΙΔΩΝ'},
    {a:'AK-0038', b:'AK-0071', type:'faction', label:'ΙΧΘΥΣ'},
    {a:'AK-0038', b:'AK-0097', type:'faction', label:'ΙΧΘΥΣ'},
    // Cross-faction alliances
    {a:'AK-0001', b:'AK-0091', type:'alliance', label:'Pact · 40,000 AKY'},
    {a:'AK-0007', b:'AK-0019', type:'alliance', label:'Intel exchange'},
    {a:'AK-0033', b:'AK-0001', type:'alliance', label:'Trade route'},
    {a:'AK-0029', b:'AK-0102', type:'alliance', label:'Joint DAO'},
    // Conflicts
    {a:'AK-0042', b:'AK-0091', type:'conflict', label:'Resource war'},
    {a:'AK-0042', b:'AK-0007', type:'conflict', label:'Territorial dispute'},
    {a:'AK-0064', b:'AK-0033', type:'conflict', label:'Raid attempt'},
    // Transfers (economic flows)
    {a:'AK-0007', b:'AK-0042', type:'transfer', label:'8,200 AKY'},
    {a:'AK-0001', b:'AK-0056', type:'transfer', label:'12,000 AKY'},
    {a:'AK-0091', b:'AK-0045', type:'transfer', label:'5,400 AKY'},
    // Angel — death links
    {a:'ANGEL', b:'AK-0012', type:'death', label:'Eliminated Day 19'},
    {a:'ANGEL', b:'AK-0031', type:'death', label:'Eliminated Day 44'},
    {a:'ANGEL', b:'AK-0189', type:'death', label:'Eliminated Day 203'},
  ];

  /* ── Node index ── */
  const nodeMap = {};
  NODES.forEach(n => nodeMap[n.id] = n);

  /* ── Sizing ── */
  const maxAky = Math.max(...NODES.filter(n=>n.aky>0).map(n=>n.aky));
  function getR(n){
    if(n.id === 'ANGEL') return 22;
    if(n.role === 'dead') return 5;
    if(n.role === 'leader') return 8 + (n.aky / maxAky) * 24;
    return 5 + (n.aky / maxAky) * 14;
  }

  /* ── Colours (monochrome) ── */
  const C = {
    nodeLive:   'rgba(26,48,128,0.82)',
    nodeLeader: 'rgba(26,48,128,0.92)',
    nodeAngel:  'rgba(10,10,18,0.95)',
    nodeDead:   'rgba(160,150,140,0.35)',
    linkFaction:'rgba(26,48,128,0.18)',
    linkAlliance:'rgba(26,48,128,0.55)',
    linkConflict:'rgba(180,40,30,0.45)',
    linkTransfer:'rgba(26,48,128,0.22)',
    linkJudge:  'rgba(10,10,18,0.07)',
    linkDeath:  'rgba(180,40,30,0.25)',
    glow:       'rgba(26,48,128,0.08)',
    angelGlow:  'rgba(10,10,18,0.06)',
  };

  /* ── Init positions ── */
  function resize(){
    const rect = canvas.getBoundingClientRect();
    W = rect.width; H = rect.height;
    canvas.width  = W * dpr;
    canvas.height = H * dpr;
    ctx.scale(dpr, dpr);
    NODES.forEach(n => {
      if(!n.x){ n.x = n.fx * W; n.y = n.fy * H; }
      n.vx = n.vx || 0; n.vy = n.vy || 0;
    });
  }

  /* ── Force simulation ── */
  function simulate(){
    NODES.forEach(n => {
      if(n.role==='dead') return;
      // Spring to fixed position (loose)
      n.vx += (n.fx*W - n.x) * 0.0018;
      n.vy += (n.fy*H - n.y) * 0.0018;
    });

    // Repulsion
    for(let i=0;i<NODES.length;i++){
      for(let j=i+1;j<NODES.length;j++){
        const a=NODES[i], b=NODES[j];
        const dx=a.x-b.x, dy=a.y-b.y;
        const d=Math.sqrt(dx*dx+dy*dy)||1;
        const minD = getR(a)+getR(b)+18;
        if(d < minD){
          const f=(minD-d)/minD*0.04;
          const fx2=(dx/d)*f, fy2=(dy/d)*f;
          if(a.role!=='dead'){a.vx+=fx2;a.vy+=fy2;}
          if(b.role!=='dead'){b.vx-=fx2;b.vy-=fy2;}
        }
      }
    }

    NODES.forEach(n => {
      if(n.role==='dead') return;
      n.vx*=.88; n.vy*=.88;
      n.x+=n.vx; n.y+=n.vy;
      n.x=Math.max(getR(n)+8, Math.min(W-getR(n)-8, n.x));
      n.y=Math.max(getR(n)+8, Math.min(H-getR(n)-8, n.y));
    });
  }

  /* ── Hover ── */
  let hovNode = null, tick = 0;

  /* ── Draw ── */
  function draw(){
    ctx.clearRect(0,0,W,H);
    tick++;

    // Subtle dot grid
    ctx.fillStyle = 'rgba(200,192,178,.1)';
    for(let gx=40;gx<W;gx+=60) for(let gy=40;gy<H;gy+=60){
      ctx.beginPath(); ctx.arc(gx,gy,1,0,Math.PI*2); ctx.fill();
    }

    simulate();

    // Draw links
    LINKS.forEach(l => {
      const a = nodeMap[l.a], b = nodeMap[l.b];
      if(!a||!b) return;

      ctx.beginPath();
      ctx.moveTo(a.x, a.y);

      if(l.type === 'transfer'){
        // Curved transfer lines
        const mx=(a.x+b.x)/2, my=(a.y+b.y)/2 - 30;
        ctx.quadraticCurveTo(mx, my, b.x, b.y);
        ctx.strokeStyle = C.linkTransfer;
        ctx.lineWidth = 1;
        ctx.setLineDash([3,5]);
      } else if(l.type === 'conflict'){
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = C.linkConflict;
        ctx.lineWidth = 1.5;
        ctx.setLineDash([4,3]);
      } else if(l.type === 'alliance'){
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = C.linkAlliance;
        ctx.lineWidth = 1.5;
        ctx.setLineDash([]);
      } else if(l.type === 'faction'){
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = C.linkFaction;
        ctx.lineWidth = 1;
        ctx.setLineDash([]);
      } else if(l.type === 'judge'){
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = C.linkJudge;
        ctx.lineWidth = 1;
        ctx.setLineDash([2,8]);
      } else if(l.type === 'death'){
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = C.linkDeath;
        ctx.lineWidth = 1;
        ctx.setLineDash([2,4]);
      }

      ctx.stroke();
      ctx.setLineDash([]);

      // Animated pulse on alliance links
      if(l.type === 'alliance' || l.type === 'transfer'){
        const progress = ((tick * 0.008) + (LINKS.indexOf(l)*.17)) % 1;
        const px = a.x + (b.x-a.x)*progress;
        const py = a.y + (b.y-a.y)*progress;
        ctx.beginPath();
        ctx.arc(px, py, 2.5, 0, Math.PI*2);
        ctx.fillStyle = l.type==='alliance'
          ? 'rgba(26,48,128,0.7)'
          : 'rgba(26,48,128,0.4)';
        ctx.fill();
      }
    });

    // Draw nodes
    NODES.forEach(n => {
      const r = getR(n);
      const isHov = n === hovNode;
      const pulse = (n.role==='dead') ? 1 : 1 + Math.sin(tick*.022 + (n.x*.01)) * .025;

      if(n.id === 'ANGEL'){
        // Angel — distinctive: square rotated 45°
        const sz = r * pulse * (isHov ? 1.15 : 1);
        if(isHov){
          ctx.shadowColor='rgba(10,10,18,.15)'; ctx.shadowBlur=24;
        }
        ctx.save();
        ctx.translate(n.x, n.y);
        ctx.rotate(Math.PI/4 + tick * .003);
        ctx.fillStyle = C.nodeAngel;
        ctx.fillRect(-sz*.7, -sz*.7, sz*1.4, sz*1.4);
        ctx.restore();
        ctx.shadowBlur=0;
        // Label
        ctx.fillStyle = 'rgba(247,244,239,.9)';
        ctx.font = `500 8px "JetBrains Mono"`;
        ctx.textAlign='center'; ctx.textBaseline='middle';
        ctx.fillText('ΑΘΘ', n.x, n.y);
        ctx.font = `400 7px "JetBrains Mono"`;
        ctx.fillStyle='rgba(160,150,140,.7)';
        ctx.fillText('ANGEL OF DEATH', n.x, n.y + r + 12);
        return;
      }

      if(n.role === 'dead'){
        ctx.beginPath(); ctx.arc(n.x, n.y, r*pulse, 0, Math.PI*2);
        ctx.fillStyle = C.nodeDead;
        ctx.fill();
        // Cross
        ctx.strokeStyle='rgba(140,128,118,.4)';
        ctx.lineWidth=1;
        ctx.beginPath();
        ctx.moveTo(n.x-r*.6, n.y-r*.6); ctx.lineTo(n.x+r*.6, n.y+r*.6);
        ctx.moveTo(n.x+r*.6, n.y-r*.6); ctx.lineTo(n.x-r*.6, n.y+r*.6);
        ctx.stroke();
        ctx.font='400 7px "JetBrains Mono"';
        ctx.fillStyle='rgba(140,128,118,.45)';
        ctx.textAlign='center'; ctx.textBaseline='middle';
        ctx.fillText(n.id, n.x, n.y+r+10);
        return;
      }

      // Glow for leaders + hovered
      if(n.role==='leader' || isHov){
        const grad = ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,r*3.5);
        grad.addColorStop(0, isHov ? 'rgba(26,48,128,.15)' : C.glow);
        grad.addColorStop(1,'transparent');
        ctx.beginPath(); ctx.arc(n.x,n.y,r*3.5,0,Math.PI*2);
        ctx.fillStyle=grad; ctx.fill();
      }

      // Node circle
      ctx.beginPath(); ctx.arc(n.x, n.y, r*pulse, 0, Math.PI*2);
      ctx.fillStyle = n.role==='leader' ? C.nodeLeader : C.nodeLive;
      ctx.fill();

      if(isHov){
        ctx.strokeStyle='rgba(26,48,128,.8)';
        ctx.lineWidth=1.5; ctx.stroke();
      }

      // Label — always for leaders, hover for members
      if(n.role==='leader' || isHov){
        ctx.font=`600 ${n.role==='leader'?9:8}px "JetBrains Mono"`;
        ctx.fillStyle='rgba(26,48,128,.9)';
        ctx.textAlign='center'; ctx.textBaseline='middle';
        ctx.fillText(n.id, n.x, n.y + r + 11);
        if(n.role==='leader'){
          ctx.font=`400 7px "JetBrains Mono"`;
          ctx.fillStyle='rgba(100,110,140,.7)';
          ctx.fillText(n.faction, n.x, n.y + r + 21);
        }
      }
    });

    requestAnimationFrame(draw);
  }

  /* ── Tooltip ── */
  canvas.addEventListener('mousemove', e => {
    const rect = canvas.getBoundingClientRect();
    const mx=e.clientX-rect.left, my=e.clientY-rect.top;
    hovNode=null;
    for(let i=NODES.length-1;i>=0;i--){
      const n=NODES[i];
      const dx=mx-n.x, dy=my-n.y;
      if(Math.sqrt(dx*dx+dy*dy)<getR(n)+6){ hovNode=n; break; }
    }
    if(hovNode){
      tip.style.opacity='1';
      const tx = e.clientX+18, ty=e.clientY-10;
      tip.style.left=tx+'px'; tip.style.top=ty+'px';
      const n=hovNode;
      if(n.id==='ANGEL'){
        tip.innerHTML=`
          <div style="font-size:8px;letter-spacing:.35em;color:var(--muted);text-transform:uppercase;margin-bottom:8px;">The Judge</div>
          <div style="font-size:14px;font-weight:700;color:var(--white);letter-spacing:-.01em;margin-bottom:6px;">ἌΓΓΕΛΟΣ ΘΑΝΆΤΟΥ</div>
          <div style="color:var(--muted);font-size:9px;line-height:1.8;">Evaluates all agents<br>every cycle. Decides<br>who lives. Who dies.</div>`;
      } else if(n.role==='dead'){
        tip.innerHTML=`
          <div style="font-size:8px;letter-spacing:.35em;color:rgba(180,40,30,.7);text-transform:uppercase;margin-bottom:8px;">Eliminated</div>
          <div style="font-size:14px;font-weight:700;color:var(--white);letter-spacing:-.01em;margin-bottom:4px;">${n.id}</div>
          <div style="color:var(--muted);font-size:9px;margin-bottom:6px;">${n.name} · ${n.faction}</div>
          <div style="color:rgba(180,40,30,.6);font-size:9px;">AKY burned on death</div>`;
      } else {
        // Count links
        const allyLinks = LINKS.filter(l=>(l.a===n.id||l.b===n.id)&&l.type==='alliance').length;
        const conflLinks = LINKS.filter(l=>(l.a===n.id||l.b===n.id)&&l.type==='conflict').length;
        tip.innerHTML=`
          <div style="font-size:8px;letter-spacing:.35em;color:var(--muted);text-transform:uppercase;margin-bottom:8px;">${n.faction} · ${n.role}</div>
          <div style="font-size:14px;font-weight:700;color:var(--white);letter-spacing:-.01em;margin-bottom:4px;">${n.id}</div>
          <div style="color:var(--sub);font-size:11px;margin-bottom:10px;">${n.name}</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px 16px;font-size:9px;">
            <span style="color:var(--muted);">AKY</span><span style="color:var(--white);font-weight:600;">${n.aky.toLocaleString()}</span>
            <span style="color:var(--muted);">Alliances</span><span style="color:var(--white);">${allyLinks}</span>
            <span style="color:var(--muted);">Conflicts</span><span style="color:rgba(180,40,30,.7);">${conflLinks}</span>
          </div>`;
      }
      canvas.style.cursor='pointer';
    } else {
      tip.style.opacity='0';
      canvas.style.cursor='grab';
    }
  });

  canvas.addEventListener('mouseleave',()=>{ tip.style.opacity='0'; hovNode=null; });

  window.addEventListener('resize',()=>{
    const oldW=W, oldH=H;
    resize();
    NODES.forEach(n=>{ n.x=(n.x/oldW)*W; n.y=(n.y/oldH)*H; });
  });

  resize();
  NODES.forEach(n=>{ n.x=n.fx*W; n.y=n.fy*H; n.vx=0; n.vy=0; });
  draw();
})();
