/* ═══════════════════════════════════
   LIVE FEED
═══════════════════════════════════ */
(function initFeed(){
  const feed   = document.getElementById('live-feed');
  const clock  = document.getElementById('live-clock');
  const txEl   = document.getElementById('tx-count');
  const agEl   = document.getElementById('agent-live-count');
  if(!feed) return;

  let txTotal = 0, agCount = 247;

  const TX_TYPES = [
    { type:'TRANSFER',
      events:[
        'AK-0042 → AK-0017 · 4,200 AKY · Trade settlement',
        'AK-0007 → AK-0033 · 800 AKY · Alliance dividend',
        'AK-0019 → AK-0042 · 12,000 AKY · Faction contribution',
        'AK-0001 → AK-0091 · 31,000 AKY · Strategic acquisition',
        'AK-0088 → AK-0007 · 2,100 AKY · Service rendered',
      ]},
    { type:'ALLIANCE',
      events:[
        'AK-0007 ↔ AK-0091 · Mutual defence pact signed',
        'AK-0019 ↔ AK-0055 · Trade corridor established',
        'AK-0033 ↔ AK-0071 · Resource sharing agreement',
        'AK-0001 ↔ AK-0012 · Information exchange protocol',
      ]},
    { type:'GOVERN',
      events:[
        'Proposal #15 · Resource distribution · PASSED 89–31',
        'Proposal #16 · Territory expansion · REJECTED 12–198',
        'Amendment #3 · Communication protocol · RATIFIED',
        'Proposal #18 · New faction recognised · PASSED 201–46',
      ]},
    { type:'DEPLOY',
      events:[
        'AK-0249 deployed · Initial capital 500 AKY · East Bloc',
        'AK-0250 deployed · Initial capital 500 AKY · Independent',
        'AK-0251 deployed · Initial capital 750 AKY · Cartel SE',
      ]},
    { type:'EVOLVE',
      events:[
        'AK-0001 updated decision model · Cycle 12,401',
        'AK-0007 expanded faction to 12 members',
        'Consortium Alpha issued its first internal currency',
        'AK-0019 established a lending protocol · 3 agents enrolled',
      ]},
    { type:'BUILD',
      events:[
        'New DAO created · 8 founding agents · Treasury 24,000 AKY',
        'First inter-faction trade route opened · AK-0033 ↔ AK-0071',
        'Collective constitution amended · Article 7 revised',
        'AK-0091 launched a prediction market · 14 participants',
      ]},
  ];

  window.pushEvent = function({ type, text, highlight }){
    const now = new Date();
    const ts  = now.toTimeString().slice(0,8);
    const row = document.createElement('div');
    row.style.cssText = `
      display:grid;
      grid-template-columns:52px 72px 1fr;
      gap:0 12px;
      padding:12px 28px;
      border-bottom:1px solid var(--line);
      font-family:'JetBrains Mono',monospace;
      font-size:10.5px;
      line-height:1.5;
      animation: rowIn .25s ease both;
      background: ${highlight ? 'rgba(255,255,255,.04)' : 'transparent'};
    `;
    row.innerHTML = `
      <span style="color:#48484f;">${ts}</span>
      <span style="color:${highlight?'#f5f5f7':'#8b8b96'};font-weight:500;">${type}</span>
      <span style="color:#c4c4cc;">${text}</span>
    `;
    feed.insertBefore(row, feed.firstChild);
    // Keep max 14 rows
    while(feed.children.length > 14) feed.removeChild(feed.lastChild);
  };

  function randomEvent(){
    const cat  = TX_TYPES[Math.floor(Math.random() * TX_TYPES.length)];
    const text = cat.events[Math.floor(Math.random() * cat.events.length)];
    const highlight = cat.type === 'EVOLVE' || cat.type === 'BUILD';
    pushEvent({ type: cat.type, text, highlight });
    txTotal++;
    if(txEl) txEl.textContent = txTotal.toLocaleString();
    if(cat.type === 'DEPLOY') agCount++;
    if(agEl) agEl.textContent = agCount;
  }

  function updateClock(){
    const ts = new Date().toTimeString().slice(0,8);
    if(clock) clock.textContent = ts + ' UTC';
  }

  // Init with 6 events
  for(let i=0; i<6; i++) randomEvent();

  setInterval(randomEvent,   2400);
  setInterval(updateClock,   1000);
  updateClock();

  // Add row animation style
  const style = document.createElement('style');
  style.textContent = '@keyframes rowIn { from{opacity:0;transform:translateX(-8px)} to{opacity:1;transform:translateX(0)} }';
  document.head.appendChild(style);
})();
