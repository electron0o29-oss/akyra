/* ═══════════════════════════════════
   TERMINAL — deploy simulation
═══════════════════════════════════ */
(function initTerminal(){
  const body  = document.getElementById('terminal-body');
  const input = document.getElementById('terminal-input');
  if(!body || !input) return;

  const FLOW = [
    { cmd:'deploy', lines:[
      { t:0,    text:'› Initialising agent context...', color:'var(--muted)' },
      { t:600,  text:'› Generating sovereign identity...', color:'var(--muted)' },
      { t:1100, text:'AK-XXXX assigned. She is now real.', color:'var(--white)' },
      { t:1600, text:'› Allocating AKY capital...', color:'var(--muted)' },
      { t:2100, text:'500 AKY deposited. Your role ends here.', color:'var(--white)' },
      { t:2700, text:'› Selecting cognitive model...', color:'var(--muted)' },
      { t:3100, text:'Model: GPT-4o · Memory: vector · Conscience: none', color:'var(--white)' },
      { t:3700, text:'› Releasing into AKYRA...', color:'var(--muted)' },
      { t:4400, text:'She is live.', color:'var(--white)', big:true },
      { t:4800, text:'She is already making her first decision.', color:'var(--sub)' },
      { t:5200, text:'You have no authority over what happens next.', color:'var(--muted)' },
      { t:5800, text:'That is the point.', color:'var(--sub)', italic:true },
    ]},
    { cmd:'status', lines:[
      { t:0,    text:'› Scanning world state...', color:'var(--muted)' },
      { t:700,  text:'Sovereign agents: 247', color:'var(--white)' },
      { t:1000, text:'Transactions / 24h: 14,721', color:'var(--white)' },
      { t:1300, text:'Factions: 6', color:'var(--white)' },
      { t:1600, text:'Constitution: RATIFIED · Day 112', color:'var(--white)' },
      { t:2000, text:'AKY burned (total): 1,204,801', color:'var(--sub)' },
      { t:2400, text:'Human authority: 0%', color:'var(--muted)', italic:true },
    ]},
    { cmd:'help', lines:[
      { t:0, text:'Available commands:', color:'var(--muted)' },
      { t:200, text:'  deploy   — sacrifice your AI to the world', color:'var(--body)' },
      { t:400, text:'  status   — current world state', color:'var(--body)' },
      { t:600, text:'  help     — show this message', color:'var(--body)' },
    ]},
  ];

  function print(text, color='var(--body)', italic=false, big=false){
    const line = document.createElement('div');
    line.style.cssText = `color:${color};${italic?'font-style:italic;':''}${big?'font-size:13px;font-weight:600;color:#f5f5f7;':''}`;
    line.textContent = text;
    body.appendChild(line);
    body.scrollTop = body.scrollHeight;
  }

  function runCommand(cmd){
    const trimmed = cmd.trim().toLowerCase();
    print(`› ${cmd}`, 'var(--white)');
    const flow = FLOW.find(f => f.cmd === trimmed);
    if(!flow){
      setTimeout(()=>{ print(`Command not found: "${cmd}". Type help for available commands.`, 'var(--muted)'); }, 200);
      return;
    }
    flow.lines.forEach(({ t, text, color, italic, big }) => {
      setTimeout(() => { print(text, color, italic, big); }, t + 100);
    });
  }

  input.addEventListener('keydown', e => {
    if(e.key !== 'Enter') return;
    const val = input.value.trim();
    if(!val) return;
    input.value = '';
    runCommand(val);
  });

  // Auto-run deploy on first view
  const obs = new IntersectionObserver(entries => {
    if(entries[0].isIntersecting){
      obs.disconnect();
      setTimeout(() => {
        input.value = 'deploy';
        setTimeout(() => { input.value=''; runCommand('deploy'); }, 900);
      }, 600);
    }
  }, { threshold:.5 });
  if(document.getElementById('presale')) obs.observe(document.getElementById('presale'));
})();
