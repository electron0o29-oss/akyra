/* ═══════════════════════════════════════════
   AKYRA Bridge — Reown AppKit multi-wallet
   Override des fonctions fallback si AppKit charge
═══════════════════════════════════════════ */

import { createAppKit } from 'https://esm.sh/@reown/appkit@1.7.3';
import { EthersAdapter } from 'https://esm.sh/@reown/appkit-adapter-ethers@1.7.3';
import { sepolia } from 'https://esm.sh/@reown/appkit@1.7.3/networks';

const CFG = {
  l1ChainId:  11155111,
  l1Explorer: 'https://sepolia.etherscan.io',
  l1Bridge:   '0x986775ef7ad580449a4f3a90adc50ab116d28938',
  l2Explorer: 'http://35.233.51.51:4000',
  minGas:     200000,
};

const L1_BRIDGE_ABI = [
  'function depositETH(uint32 _minGasLimit, bytes calldata _extraData) payable',
];

const $ = id => document.getElementById(id);

function showError(id, msg) {
  const el = $(id);
  if (!el) return;
  el.textContent = msg;
  el.style.display = msg ? 'block' : 'none';
}

function setConnectedUI(on) {
  const pill = $('br-wallet-pill'), cb = $('br-connect-btn'), db = $('br-deposit-btn'), tr = $('br-time-row');
  if (on) {
    if (pill) pill.style.display = 'flex';
    if (cb)   cb.style.display   = 'none';
    if (db)   db.style.display   = 'block';
    if (tr)   tr.style.display   = 'block';
  } else {
    if (pill) pill.style.display = 'none';
    if (cb)   cb.style.display   = 'block';
    if (db)   db.style.display   = 'none';
    if (tr)   tr.style.display   = 'none';
  }
}

/* ── Init AppKit ── */
let appKit;
try {
  appKit = createAppKit({
    adapters:  [new EthersAdapter()],
    networks:  [sepolia],
    projectId: 'c1115ad911ef0c661fa22792bfb65391',
    metadata: {
      name: 'AKYRA Bridge', description: 'Bridge ETH Sepolia → AKYRA L2',
      url: 'https://akyra.io', icons: ['https://akyra.io/logos/akyra-favicon.png'],
    },
    features: { analytics: false, email: false, socials: false, onramp: false, swaps: false },
    themeMode: 'light',
    themeVariables: {
      '--w3m-border-radius-master': '0px',
      '--w3m-color-mix': '#1a3080',
      '--w3m-color-mix-strength': 15,
      '--w3m-font-family': 'Space Grotesk, sans-serif',
      '--w3m-z-index': '99999',
    },
  });
} catch(e) {
  console.warn('[bridge] AppKit init failed, using MetaMask fallback:', e);
  appKit = null;
}

/* ── Subscription compte ── */
if (appKit) {
  appKit.subscribeAccount(async (account) => {
    if (account.isConnected && account.address) {
      try {
        const wp = appKit.getWalletProvider();
        if (!wp) return;
        window._brProvider = new window.ethers.BrowserProvider(wp);
        window._brSigner   = await window._brProvider.getSigner();
        window._brAddr     = account.address;
        $('br-addr').textContent = window._brAddr.slice(0,6)+'···'+window._brAddr.slice(-4);
        setConnectedUI(true);
        showError('br-connect-error', '');
        const bal = await window._brProvider.getBalance(window._brAddr);
        const balEl = $('br-balance-val');
        if (balEl) balEl.textContent = parseFloat(window.ethers.formatEther(bal)).toFixed(5)+' ETH';
      } catch(e) { console.error('[bridge] provider setup:', e); }
    } else {
      window._brProvider = null; window._brSigner = null; window._brAddr = null;
      setConnectedUI(false);
      const balEl = $('br-balance-val');
      if (balEl) balEl.textContent = '—';
      const r = $('br-receive-amount');
      if (r) r.textContent = '0';
    }
  });

  /* Override bridgeConnect avec AppKit */
  window.bridgeConnect = function() {
    showError('br-connect-error', '');
    appKit.open();
  };

  window.bridgeDisconnect = function() {
    appKit.disconnect();
    setConnectedUI(false);
    document.getElementById('br-main-view').style.display = 'block';
    document.getElementById('br-tx-view').style.display   = 'none';
    showError('br-connect-error',''); showError('br-form-error','');
  };
}

/* ════════════════════════════════════
   DEPOSIT (commun fallback + AppKit)
════════════════════════════════════ */

let busy = false;

window.bridgeDeposit = async function() {
  if (busy) return;
  showError('br-form-error', '');

  if (!window._brProvider || !window._brSigner || !window._brAddr) {
    showError('br-form-error', 'Connecte un wallet d\'abord.');
    return;
  }

  const raw = $('br-amount')?.value;
  const val = parseFloat(raw);
  if (!val || val <= 0) { showError('br-form-error', 'Entre un montant valide.'); return; }

  const network = await window._brProvider.getNetwork();
  if (Number(network.chainId) !== CFG.l1ChainId) {
    showError('br-form-error', 'Switch sur Sepolia pour déposer.');
    try {
      if (appKit) await appKit.switchNetwork(sepolia);
      else await window.ethereum.request({ method:'wallet_switchEthereumChain', params:[{chainId:'0xaa36a7'}] });
      window._brProvider = new window.ethers.BrowserProvider(appKit ? appKit.getWalletProvider() : window.ethereum);
      window._brSigner   = await window._brProvider.getSigner();
    } catch { return; }
  }

  const amountWei = window.ethers.parseEther(raw);
  const bal       = await window._brProvider.getBalance(window._brAddr);
  if (bal < amountWei) { showError('br-form-error', 'Balance ETH insuffisante.'); return; }

  busy = true;
  const db = $('br-deposit-btn');
  if (db) { db.textContent = 'Confirmation…'; db.disabled = true; }

  try {
    const bridge = new window.ethers.Contract(CFG.l1Bridge, L1_BRIDGE_ABI, window._brSigner);
    const tx     = await bridge.depositETH(CFG.minGas, '0x', { value: amountWei });

    $('br-main-view').style.display = 'none';
    $('br-tx-view').style.display   = 'block';
    $('br-tx-title').textContent    = 'Transaction envoyée';
    $('br-tx-sub').textContent      = 'Attente confirmation L1…';
    $('br-spinner').style.display   = 'block';
    $('br-tx-success').style.display= 'none';
    $('br-tx-links').style.display  = 'none';
    $('br-l1-link').href            = CFG.l1Explorer + '/tx/' + tx.hash;

    await tx.wait();

    $('br-spinner').style.display   = 'none';
    $('br-tx-success').style.display= 'flex';
    $('br-tx-title').textContent    = 'Dépôt confirmé ✓';
    $('br-tx-sub').textContent      = 'L\'ETH arrive sur AKYRA L2 dans ~2-5 minutes.';
    $('br-tx-links').style.display  = 'flex';
    $('br-l2-link').href            = CFG.l2Explorer + '/address/' + window._brAddr;

  } catch(err) {
    showError('br-form-error', err.code === 'ACTION_REJECTED' || err.code === 4001 ? 'Transaction annulée.' : 'Transaction échouée.');
    $('br-main-view').style.display = 'block';
    $('br-tx-view').style.display   = 'none';
  }

  busy = false;
  if (db) { db.textContent = 'Deposit'; db.disabled = false; }
};
