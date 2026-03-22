/* ═══════════════════════════════════
   NEURAL NETWORK + PARTICLES — hero bg
═══════════════════════════════════ */
(function initNeural(){
  const canvas = document.getElementById('neural-canvas');
  if(!canvas) return;
  const ctx = canvas.getContext('2d');

  let W, H, nodes = [], particles = [];
  const NODE_COUNT    = 52;
  const PARTICLE_COUNT = 110;
  const MAX_DIST      = 170;
  const PULSE_SPEED   = 0.003;

  function resize(){
    W = canvas.width  = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }
  resize();
  window.addEventListener('resize', () => { resize(); initNodes(); });

  /* ── Nodes */
  function initNodes(){
    nodes = [];
    for(let i = 0; i < NODE_COUNT; i++){
      nodes.push({
        x:    Math.random() * W,
        y:    Math.random() * H,
        vx:   (Math.random() - .5) * .18,
        vy:   (Math.random() - .5) * .18,
        r:    .8 + Math.random() * 1.6,
        // pulse phase
        phase: Math.random() * Math.PI * 2,
        // is an "agent node" (larger, brighter)
        agent: Math.random() < .18,
        opacity: .3 + Math.random() * .5,
      });
    }
  }
  initNodes();

  /* ── Particles (floating dust) */
  function makeParticle(){
    return {
      x:    Math.random() * W,
      y:    H + Math.random() * 60,
      vx:   (Math.random() - .5) * .3,
      vy:   -.12 - Math.random() * .25,
      r:    .4 + Math.random() * .9,
      life: 1,
      decay: .0012 + Math.random() * .001,
    };
  }
  for(let i = 0; i < PARTICLE_COUNT; i++){
    const p = makeParticle();
    p.y = Math.random() * H; // scatter vertically on init
    p.life = Math.random();
    particles.push(p);
  }

  /* ── Signal pulses travelling along edges */
  const signals = [];
  function spawnSignal(nodeA, nodeB){
    signals.push({ a:nodeA, b:nodeB, t:0, speed:.006 + Math.random()*.006 });
  }

  let tick = 0;

  function draw(){
    requestAnimationFrame(draw);
    tick++;

    ctx.clearRect(0, 0, W, H);

    /* ── Radial ambient glow — centre du hero */
    const grd = ctx.createRadialGradient(W*.5, H*.42, 0, W*.5, H*.42, W*.55);
    grd.addColorStop(0,   'rgba(255,255,255,.028)');
    grd.addColorStop(.55, 'rgba(255,255,255,.006)');
    grd.addColorStop(1,   'rgba(0,0,0,0)');
    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, W, H);

    /* ── Move nodes */
    nodes.forEach(n => {
      n.x += n.vx; n.y += n.vy;
      if(n.x < -20) n.x = W + 20;
      if(n.x > W+20) n.x = -20;
      if(n.y < -20) n.y = H + 20;
      if(n.y > H+20) n.y = -20;
    });

    /* ── Draw edges */
    for(let i = 0; i < nodes.length; i++){
      for(let j = i+1; j < nodes.length; j++){
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const d  = Math.sqrt(dx*dx + dy*dy);
        if(d > MAX_DIST) continue;

        const alpha = (1 - d/MAX_DIST) * .12;
        ctx.strokeStyle = `rgba(26,40,100,${alpha})`;
        ctx.lineWidth   = .5;
        ctx.beginPath();
        ctx.moveTo(nodes[i].x, nodes[i].y);
        ctx.lineTo(nodes[j].x, nodes[j].y);
        ctx.stroke();

        /* Spawn signal occasionally */
        if(tick % 90 === 0 && Math.random() < .06){
          spawnSignal(nodes[i], nodes[j]);
        }
      }
    }

    /* ── Draw signals (pulses along edges) */
    for(let s = signals.length - 1; s >= 0; s--){
      const sig = signals[s];
      sig.t += sig.speed;
      if(sig.t > 1){ signals.splice(s, 1); continue; }

      const x = sig.a.x + (sig.b.x - sig.a.x) * sig.t;
      const y = sig.a.y + (sig.b.y - sig.a.y) * sig.t;
      const glow = ctx.createRadialGradient(x, y, 0, x, y, 5);
      glow.addColorStop(0,  'rgba(26,48,180,.7)');
      glow.addColorStop(.5, 'rgba(26,48,180,.15)');
      glow.addColorStop(1,  'rgba(255,255,255,0)');
      ctx.fillStyle = glow;
      ctx.beginPath(); ctx.arc(x, y, 5, 0, Math.PI*2); ctx.fill();
    }

    /* ── Draw nodes */
    nodes.forEach(n => {
      const pulse = Math.sin(tick * PULSE_SPEED * 60 + n.phase) * .5 + .5;
      const alpha = n.opacity * (.5 + pulse * .5);
      const r     = n.r * (n.agent ? 1.8 : 1) * (1 + pulse * .3);

      if(n.agent){
        /* Agent node — glow */
        const g = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, r * 5);
        g.addColorStop(0,   `rgba(26,48,128,${alpha * .9})`);
        g.addColorStop(.4,  `rgba(26,48,128,${alpha * .2})`);
        g.addColorStop(1,   'rgba(255,255,255,0)');
        ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(n.x, n.y, r * 5, 0, Math.PI*2); ctx.fill();
      }

      ctx.fillStyle = `rgba(26,40,100,${alpha})`;
      ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI*2); ctx.fill();
    });

    /* ── Particles (dust) */
    particles.forEach((p, i) => {
      p.x += p.vx; p.y += p.vy;
      p.life -= p.decay;

      if(p.life <= 0){
        particles[i] = makeParticle();
        return;
      }

      ctx.fillStyle = `rgba(255,255,255,${p.life * .18})`;
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill();
    });
  }

  draw();
})();
