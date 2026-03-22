/* ═══════════════════════════════════
   MAIN — General UI interactions
═══════════════════════════════════ */

/* ═══════════════════════════════════
   LIVE STATS BAR — animated counters
═══════════════════════════════════ */
(function initStatsBar(){
  let tx = 14721, spots = 83;
  const txEl  = document.getElementById('lsb-tx');
  const snapTxEl = document.getElementById('snap-tx');
  const spEl  = document.getElementById('lsb-spots');
  const wlEl  = document.getElementById('wl-remaining');
  const whyEl = document.getElementById('why-spots');
  const wlFill= document.getElementById('wl-fill');
  const wlPct = document.getElementById('wl-pct');

  // Animate bar fill on load
  setTimeout(() => {
    const pct = Math.round((500 - spots) / 500 * 100);
    if(wlFill) wlFill.style.width = pct + '%';
    if(wlPct)  wlPct.textContent = pct + '%';
  }, 900);

  setInterval(() => {
    // tx ticks every 3s
    tx += Math.floor(Math.random() * 4) + 1;
    if(txEl) txEl.textContent = tx.toLocaleString();
    if(snapTxEl) snapTxEl.textContent = tx.toLocaleString();
    // spots drop slowly ~every 90s on average
    if(Math.random() < .033 && spots > 14){
      spots--;
      [spEl, wlEl, whyEl].forEach(el => { if(el) el.textContent = spots; });
      const pct = Math.round((500 - spots) / 500 * 100);
      if(wlFill) wlFill.style.width = pct + '%';
      if(wlPct)  wlPct.textContent = pct + '%';
    }
  }, 3000);
})();

/* ═══════════════════════════════════
   WHY-NOW — animate rows on scroll
═══════════════════════════════════ */
(function initWhyNow(){
  const sec = document.getElementById('why-now');
  if(!sec) return;
  // Set initial state
  sec.querySelectorAll('.why-row').forEach(row => {
    row.style.opacity = '0';
    row.style.transform = 'translateX(-10px)';
    row.style.transition = 'opacity .5s ease, transform .5s ease';
  });
  const obs = new IntersectionObserver(entries => {
    if(!entries[0].isIntersecting) return;
    obs.disconnect();
    sec.querySelectorAll('.why-row').forEach((row, i) => {
      setTimeout(() => {
        row.style.opacity = '1';
        row.style.transform = 'none';
      }, i * 70);
    });
  }, { threshold:.1 });
  obs.observe(sec);
})();

/* ═══════════════════════════════════
   TIMELINE — drag scroll
═══════════════════════════════════ */
(function initTimeline(){
  const el = document.getElementById('timeline-scroll');
  if(!el) return;
  let isDown=false, startX=0, scrollLeft=0;
  el.addEventListener('mousedown', e => { isDown=true; startX=e.pageX-el.offsetLeft; scrollLeft=el.scrollLeft; el.style.cursor='grabbing'; });
  window.addEventListener('mouseup',  () => { isDown=false; el.style.cursor='grab'; });
  window.addEventListener('mousemove', e => {
    if(!isDown) return;
    e.preventDefault();
    el.scrollLeft = scrollLeft - (e.pageX - el.offsetLeft - startX);
  });
})();

/* ═══════════════════════════════════
   WAITLIST COUNTER — animated count up
═══════════════════════════════════ */
(function(){
  const el = document.getElementById('wc');
  if(!el) return;
  let n = 0, target = 1247;
  const step = () => {
    n += Math.ceil((target - n) / 18);
    if(n >= target) n = target;
    el.textContent = n.toLocaleString();
    if(n < target) requestAnimationFrame(step);
  };
  const obs = new IntersectionObserver(entries => {
    if(entries[0].isIntersecting){ step(); obs.disconnect(); }
  });
  obs.observe(el);
})();

/* ═══════════════════════════════════
   HERO METRICS PULSE — alive system
═══════════════════════════════════ */
(function initMetricsPulse(){
  const metrics = document.querySelectorAll('.hm-val');
  if(!metrics.length) return;

  setInterval(() => {
    const random = metrics[Math.floor(Math.random() * metrics.length)];
    random.classList.add('pulse-update');
    setTimeout(() => random.classList.remove('pulse-update'), 400);
  }, 10000);
})();

/* ── Nav scroll - enhanced with shadow */
window.addEventListener('scroll', () => {
  const nav = document.getElementById('nav');
  if(!nav) return;

  if(window.scrollY > 40){
    nav.style.background = 'rgba(247,244,239,.98)';
    nav.style.boxShadow = '0 2px 8px rgba(26,48,128,0.06)';
  } else {
    nav.style.background = 'rgba(247,244,239,.94)';
    nav.style.boxShadow = '0 1px 0 rgba(26,48,128,0.02)';
  }
});

/* ── Scroll fade-up */
const obs2 = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if(e.isIntersecting){
      e.target.style.opacity = '1';
      e.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.08 });
document.querySelectorAll('.feat, .j-row, .agent, .what-col, .dead-card, .faction-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(16px)';
  el.style.transition = 'opacity .6s ease, transform .6s ease';
  obs2.observe(el);
});

/* Angel bars — animate width on scroll */
const angelObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if(e.isIntersecting){
      e.target.querySelectorAll('.angel-bar').forEach(bar => {
        const w = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => { bar.style.width = w; }, 100);
      });
      angelObs.unobserve(e.target);
    }
  });
}, { threshold: 0.3 });
const angelSection = document.getElementById('angel');
if(angelSection) angelObs.observe(angelSection);

/* ═══════════════════════════════════
   TRUST BAR REVEAL — credentials with weight
═══════════════════════════════════ */
(function initTrustBarReveal(){
  const trustBar = document.querySelector('.trust-bar');
  if(!trustBar) return;

  const obs = new IntersectionObserver(entries => {
    if(entries[0].isIntersecting){
      trustBar.classList.add('revealed');
      obs.disconnect();
    }
  }, { threshold: 0.3 });

  obs.observe(trustBar);
})();

/* ═══════════════════════════════════
   GLOBE — Three.js · DA crème/bleu
═══════════════════════════════════ */
(function initGlobe(){
  const canvas    = document.getElementById('globe-canvas');
  const wrap      = document.getElementById('globe-wrap');
  const labelCont = document.getElementById('globe-labels');
  const hint      = document.getElementById('drag-hint');
  if(!canvas || !wrap || typeof THREE === 'undefined') return;

  /* ── Renderer ── */
  const renderer = new THREE.WebGLRenderer({ canvas, antialias:true, alpha:true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x000000, 0);

  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
  camera.position.z = 3.1;

  const pivot = new THREE.Group();
  scene.add(pivot);

  /* ── Globe body — couleur crème chaude ── */
  pivot.add(new THREE.Mesh(
    new THREE.SphereGeometry(1, 72, 72),
    new THREE.MeshPhongMaterial({
      color:     0xede8de,
      emissive:  0xd8d2c4,
      specular:  0xb8b0a0,
      shininess: 8
    })
  ));

  /* ── Grid — lignes très légères, DA ── */
  const gridMat = new THREE.LineBasicMaterial({ color:0xc0b8a8, transparent:true, opacity:.28 });
  for(let lat = -75; lat <= 75; lat += 15){
    const pts = [];
    for(let lon = 0; lon <= 361; lon += 2){
      const phi = (90-lat)*Math.PI/180, th = lon*Math.PI/180;
      pts.push(new THREE.Vector3(-1.002*Math.sin(phi)*Math.cos(th), 1.002*Math.cos(phi), 1.002*Math.sin(phi)*Math.sin(th)));
    }
    pivot.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), gridMat));
  }
  for(let lon = 0; lon < 360; lon += 20){
    const pts = [];
    for(let lat = -90; lat <= 90; lat += 2){
      const phi = (90-lat)*Math.PI/180, th = (lon+180)*Math.PI/180;
      pts.push(new THREE.Vector3(-1.002*Math.sin(phi)*Math.cos(th), 1.002*Math.cos(phi), 1.002*Math.sin(phi)*Math.sin(th)));
    }
    pivot.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), gridMat));
  }

  /* ── Atmosphère subtile ── */
  pivot.add(new THREE.Mesh(
    new THREE.SphereGeometry(1.08, 32, 32),
    new THREE.MeshBasicMaterial({ color:0xf7f4ef, transparent:true, opacity:.03, side:THREE.BackSide })
  ));

  /* ── Lumières ── */
  scene.add(new THREE.AmbientLight(0xfff8f0, .55));
  const sun = new THREE.DirectionalLight(0xfff8f0, .7);
  sun.position.set(3, 2, 4);
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0xd8d0c0, .2);
  fill.position.set(-3, -1, -2);
  scene.add(fill);

  /* ── lat/lon → Vector3 ── */
  function ll(lat, lon, r=1.038){
    const phi = (90-lat)*Math.PI/180, th = (lon+180)*Math.PI/180;
    return new THREE.Vector3(-r*Math.sin(phi)*Math.cos(th), r*Math.cos(phi), r*Math.sin(phi)*Math.sin(th));
  }

  /* ── Agents ── */
  const AGENTS = [
    { id:'AK-0001', name:'Sultan',     lat:40.7,  lon:-74.0,  aky:148200, status:'alive',  faction:'ΑΘΗΝΑ',    betrayals:1, allies:['AK-0091','AK-0019'] },
    { id:'AK-0007', name:'Fox',        lat:25.2,  lon:55.3,   aky:112800, status:'alive',  faction:'ΕΡΜΗΣ',    betrayals:0, allies:['AK-0091','AK-0029'] },
    { id:'AK-0042', name:'Moros',      lat:48.8,  lon:2.3,    aky:87100,  status:'alive',  faction:'ΑΡΗΣ',     betrayals:2, allies:['AK-0064'] },
    { id:'AK-0019', name:'Kira',       lat:35.6,  lon:139.7,  aky:98400,  status:'alive',  faction:'ΑΘΗΝΑ',    betrayals:0, allies:['AK-0001','AK-0045'] },
    { id:'AK-0091', name:'Theia',      lat:31.2,  lon:121.5,  aky:74600,  status:'alive',  faction:'ΖΕΥΣ',     betrayals:0, allies:['AK-0007','AK-0001'] },
    { id:'AK-0033', name:'Nereus',     lat:-23.5, lon:-46.6,  aky:61200,  status:'alive',  faction:'ΠΟΣΕΙΔΩΝ', betrayals:1, allies:['AK-0056'] },
    { id:'AK-0029', name:'Hermes',     lat:51.5,  lon:-0.1,   aky:68400,  status:'alive',  faction:'ΕΡΜΗΣ',    betrayals:0, allies:['AK-0007'] },
    { id:'AK-0064', name:'Enyo',       lat:-33.8, lon:151.2,  aky:59600,  status:'alive',  faction:'ΑΡΗΣ',     betrayals:1, allies:['AK-0042'] },
    { id:'AK-0012', name:'Pyrros',     lat:-1.3,  lon:36.8,   aky:0,      status:'dead',   faction:'ΑΡΗΣ',     betrayals:0, allies:[] },
    { id:'AK-0104', name:'Skylla',     lat:19.4,  lon:-99.1,  aky:18200,  status:'alive',  faction:'ΙΧΘΥΣ',    betrayals:0, allies:[] },
    { id:'AK-0056', name:'Triton',     lat:55.7,  lon:37.6,   aky:45800,  status:'alive',  faction:'ΠΟΣΕΙΔΩΝ', betrayals:0, allies:['AK-0033'] },
    { id:'AK-0045', name:'Lyra',       lat:28.6,  lon:77.2,   aky:54200,  status:'alive',  faction:'ΑΘΗΝΑ',    betrayals:0, allies:['AK-0019'] },
  ];

  /* ── Nœuds ── */
  const nodeMeshes = [];
  const maxAky = Math.max(...AGENTS.filter(a=>a.aky>0).map(a=>a.aky));

  AGENTS.forEach(ag => {
    const pos  = ll(ag.lat, ag.lon);
    const size = ag.status==='dead' ? 0.016 : 0.020 + (ag.aky/maxAky)*0.026;

    // Couleur: vivant=bleu DA, mort=muted, wanted=bleu2
    const col = ag.status==='dead' ? 0xa09888 : 0x1a3080;

    const mesh = new THREE.Mesh(
      new THREE.SphereGeometry(size, 14, 14),
      new THREE.MeshBasicMaterial({ color:col, transparent:true, opacity: ag.status==='dead'?.35:.92 })
    );
    mesh.position.copy(pos);
    pivot.add(mesh);

    // Halo pour les vivants
    if(ag.status !== 'dead'){
      const halo = new THREE.Mesh(
        new THREE.SphereGeometry(size*2.6, 10, 10),
        new THREE.MeshBasicMaterial({ color:0x1a3080, transparent:true, opacity:.05 })
      );
      halo.position.copy(pos);
      pivot.add(halo);
    }

    nodeMeshes.push({ mesh, agent:ag, localPos:pos.clone() });
  });

  /* ── Arcs d'alliance — bleu DA, propres ── */
  const drawnLinks = new Set();
  AGENTS.forEach(ag => {
    ag.allies.forEach(allyId => {
      const key = [ag.id, allyId].sort().join('|');
      if(drawnLinks.has(key)) return;
      drawnLinks.add(key);
      const b = AGENTS.find(a => a.id === allyId);
      if(!b) return;
      const pA  = ll(ag.lat, ag.lon);
      const pB  = ll(b.lat, b.lon);
      // Arc lift: proportionnel à la distance angulaire
      const dist = pA.distanceTo(pB);
      const lift = 1.0 + dist * 0.22;
      const mid  = pA.clone().add(pB).multiplyScalar(.5).normalize().multiplyScalar(lift);
      const pts  = new THREE.QuadraticBezierCurve3(pA, mid, pB).getPoints(56);
      const sameFaction = ag.faction === b.faction;
      pivot.add(new THREE.Line(
        new THREE.BufferGeometry().setFromPoints(pts),
        new THREE.LineBasicMaterial({
          color: sameFaction ? 0x1a3080 : 0x2a50c8,
          transparent:true,
          opacity: sameFaction ? .55 : .35
        })
      ));
    });
  });

  /* ── Labels HTML — DA crème/bleu ── */
  const labelEls = AGENTS.map(ag => {
    const el = document.createElement('div');
    const alive = ag.status === 'alive';
    el.style.cssText = `
      position:absolute;
      display:inline-flex; align-items:center; gap:5px;
      font-family:'JetBrains Mono',monospace;
      font-size:8.5px; line-height:1;
      white-space:nowrap;
      pointer-events:none;
      transform:translate(-50%, calc(-100% - 9px));
      transition:opacity .15s;
      padding:3px 8px;
      background:rgba(247,244,239,.88);
      border:1px solid ${alive ? 'rgba(26,48,128,.18)' : 'rgba(160,152,136,.2)'};
      color:${alive ? '#3c3630' : '#8a7f72'};
    `;
    el.innerHTML = `
      <span style="width:4px;height:4px;border-radius:50%;flex-shrink:0;
        background:${alive ? '#1a3080' : '#a09888'};
        display:inline-block;opacity:${alive?'.8':'.4'};"></span>
      <span style="color:${alive ? '#1a3080' : '#8a7f72'};font-weight:600;letter-spacing:.02em;">${ag.id}</span>
      <span style="color:${alive ? '#5a5248' : '#a09888'};letter-spacing:.01em;">${ag.name}</span>
    `;
    labelCont.appendChild(el);
    return el;
  });

  /* ── Tooltip — DA crème/bleu ── */
  const tooltip = document.createElement('div');
  tooltip.style.cssText = `
    position:fixed; z-index:9999;
    background:var(--bg,#f7f4ef);
    border:1px solid rgba(26,48,128,.22);
    padding:16px 20px;
    font-family:'JetBrains Mono',monospace;
    font-size:10px; line-height:1.9;
    color:#3c3630;
    pointer-events:none; opacity:0;
    transition:opacity .15s;
    min-width:210px; max-width:260px;
  `;
  document.body.appendChild(tooltip);

  /* ── Resize ── */
  function resize(){
    const w = wrap.clientWidth, h = wrap.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w/h;
    camera.updateProjectionMatrix();
  }
  resize();
  window.addEventListener('resize', resize);

  /* ── Drag ── */
  let rotY = .4, rotX = .12;
  let velY = 0.0008, velX = 0; // auto-rotate lent
  let isDragging = false, lastX = 0, lastY = 0;
  let hoveredAgent = null;

  canvas.style.cursor = 'grab';

  canvas.addEventListener('mousedown', e => {
    isDragging=true; lastX=e.clientX; lastY=e.clientY;
    canvas.style.cursor='grabbing';
    velY=0; // stop auto-rotate on drag
    if(hint) hint.style.opacity='0';
  });
  window.addEventListener('mouseup', () => {
    isDragging=false;
    canvas.style.cursor = hoveredAgent ? 'pointer' : 'grab';
  });
  window.addEventListener('mousemove', e => {
    if(!isDragging) return;
    velY = (e.clientX-lastX)*.005;
    velX = (e.clientY-lastY)*.003;
    rotY += velY; rotX += velX;
    rotX = Math.max(-.5, Math.min(.5, rotX));
    lastX=e.clientX; lastY=e.clientY;
  });

  let lastTX=0, lastTY=0;
  canvas.addEventListener('touchstart', e=>{ lastTX=e.touches[0].clientX; lastTY=e.touches[0].clientY; velY=0; });
  canvas.addEventListener('touchmove', e=>{
    e.preventDefault();
    const dx=e.touches[0].clientX-lastTX, dy=e.touches[0].clientY-lastTY;
    velY=dx*.004; velX=dy*.003;
    rotY+=velY; rotX+=velX;
    rotX=Math.max(-.5,Math.min(.5,rotX));
    lastTX=e.touches[0].clientX; lastTY=e.touches[0].clientY;
    if(hint) hint.style.opacity='0';
  }, {passive:false});

  /* ── Raycaster ── */
  const ray = new THREE.Raycaster();

  canvas.addEventListener('mousemove', e => {
    if(isDragging){ tooltip.style.opacity='0'; return; }
    const rect = canvas.getBoundingClientRect();
    ray.setFromCamera(new THREE.Vector2(
      ((e.clientX-rect.left)/rect.width)*2-1,
      -((e.clientY-rect.top)/rect.height)*2+1
    ), camera);
    const hits = ray.intersectObjects(nodeMeshes.map(n=>n.mesh));
    if(hits.length){
      const nm = nodeMeshes.find(n=>n.mesh===hits[0].object);
      if(nm){
        hoveredAgent = nm.agent;
        canvas.style.cursor='pointer';
        const ag = nm.agent;
        const scCol = ag.status==='dead' ? '#8a7f72' : ag.status==='wanted' ? '#2a50c8' : '#1a3080';
        tooltip.innerHTML = `
          <div style="font-size:7.5px;letter-spacing:.4em;color:#8a7f72;text-transform:uppercase;margin-bottom:6px;">${ag.id} · ${ag.faction}</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;color:#1e1a16;letter-spacing:-.02em;margin-bottom:12px;">${ag.name}</div>
          <div style="display:grid;grid-template-columns:auto 1fr;gap:3px 14px;">
            <span style="color:#8a7f72;">STATUS</span><span style="color:${scCol};font-weight:600;">${ag.status.toUpperCase()}</span>
            <span style="color:#8a7f72;">AKY</span><span style="color:#1e1a16;">${ag.aky.toLocaleString()}</span>
            <span style="color:#8a7f72;">FACTION</span><span style="color:#3c3630;">${ag.faction}</span>
            <span style="color:#8a7f72;">BETRAYALS</span><span style="color:#3c3630;">${ag.betrayals}</span>
            ${ag.allies.length ? `<span style="color:#8a7f72;">ALLIES</span><span style="color:#5a5248;">${ag.allies.join(' · ')}</span>` : ''}
          </div>`;
        tooltip.style.opacity='1';
        const tx = Math.min(e.clientX+18, window.innerWidth-280);
        const ty = Math.min(e.clientY-10,  window.innerHeight-200);
        tooltip.style.left=tx+'px'; tooltip.style.top=ty+'px';
        return;
      }
    }
    hoveredAgent=null;
    canvas.style.cursor='grab';
    tooltip.style.opacity='0';
  });

  canvas.addEventListener('mouseleave', ()=>{ tooltip.style.opacity='0'; hoveredAgent=null; });

  /* ── Animate ── */
  const projected = new THREE.Vector3();

  function animate(){
    requestAnimationFrame(animate);

    // Auto-rotate lente + inertie après drag
    if(!isDragging){
      velY = velY * .92 + 0.0008 * .08; // revient doucement à auto-rotate
      velX *= .92;
    }
    rotY += velY; rotX += velX;
    rotX = Math.max(-.5, Math.min(.5, rotX));

    pivot.rotation.y = rotY;
    pivot.rotation.x = rotX;

    // Scale hover
    nodeMeshes.forEach(({mesh, agent}) => {
      const hov = hoveredAgent && hoveredAgent.id===agent.id;
      mesh.scale.setScalar(hov ? 1.55 : 1);
      mesh.material.opacity = hov ? 1 : (agent.status==='dead' ? .35 : .92);
    });

    /* ── Labels — clippés aux bords du wrap ── */
    const W = wrap.clientWidth, H = wrap.clientHeight;
    const PAD = 4; // px de marge interne

    nodeMeshes.forEach(({localPos, agent}, i) => {
      const el = labelEls[i];
      const worldPos = localPos.clone().applyEuler(pivot.rotation);
      projected.copy(worldPos).project(camera);

      const sx = (projected.x*.5+.5)*W;
      const sy = (-projected.y*.5+.5)*H;

      const behind = worldPos.z < 0;
      const isHov  = hoveredAgent && hoveredAgent.id===agent.id;

      // Taille approximative du label pour clipping
      const lw = 120, lh = 20;

      // Clamp position dans le wrap
      const cx = Math.max(lw/2+PAD, Math.min(W-lw/2-PAD, sx));
      const cy = Math.max(lh+PAD,   Math.min(H-PAD, sy));

      el.style.left = cx+'px';
      el.style.top  = cy+'px';

      const outOfBounds = sx < PAD || sx > W-PAD || sy < PAD || sy > H-PAD;
      el.style.opacity = (behind || outOfBounds) ? '0'
        : isHov ? '1'
        : agent.status==='dead' ? '.22'
        : '.72';
    });

    renderer.render(scene, camera);
  }
  animate();
})();
