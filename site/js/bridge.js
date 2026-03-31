/* ═══════════════════════════════════════════
   AKYRA Bridge — Multi-wallet (Reown AppKit)
   Sepolia (L1) → AKYRA L2 (Chain 47197)
   ethers.js v6 (UMD) + AppKit via esm.sh
═══════════════════════════════════════════ */

import { createAppKit } from 'https://esm.sh/@reown/appkit@1.7.3';
import { EthersAdapter } from 'https://esm.sh/@reown/appkit-adapter-ethers@1.7.3';
import { sepolia } from 'https://esm.sh/@reown/appkit@1.7.3/networks';

/* ── Config ── */
const CFG = {
  l1ChainId:  11155111,
  l1Explorer: 'https://sepolia.etherscan.io',
  l1Bridge:   '0x986775ef7ad580449a4f3a90adc50ab116d28938',

  l2ChainId:  47197,
  l2ChainHex: '0xb85d',
  l2Name:     'AKYRA L2',
  l2Rpc:      'http://35.233.51.51:8545',
  l2Explorer: 'http://35.233.51.51:4000',

  minGas: 200000,
};

const L1_BRIDGE_ABI = [
  'function depositETH(uint32 _minGasLimit, bytes calldata _extraData) payable',
];

/* ── State ── */
let provider = null;
let signer   = null;
let userAddr = null;
let busy     = false;

/* ── DOM ── */
const $ = id => document.getElementById(id);

function truncAddr(a) { return a.slice(0,6) + '···' + a.slice(-4); }

function showError(id, msg) {
  const el = $(id);
  if (!el) return;
  el.textContent = msg;
  el.style.display = msg ? 'block' : 'none';
}

function setBtnState(id, text, disabled) {
  const btn = $(id);
  if (!btn) return;
  btn.textContent = text;
  btn.disabled = disabled;
}

function showView(viewId) {
  ['br-main-view','br-tx-view'].forEach(id => {
    const el = $(id);
    if (el) el.style.display = id === viewId ? 'block' : 'none';
  });
}

function setConnectedUI(on) {
  const pill       = $('br-wallet-pill');
  const connectBtn = $('br-connect-btn');
  const depositBtn = $('br-deposit-btn');
  const timeRow    = $('br-time-row');
  if (on) {
    if (pill)       pill.style.display       = 'flex';
    if (connectBtn) connectBtn.style.display = 'none';
    if (depositBtn) depositBtn.style.display = 'block';
    if (timeRow)    timeRow.style.display    = 'block';
  } else {
    if (pill)       pill.style.display       = 'none';
    if (connectBtn) connectBtn.style.display = 'block';
    if (depositBtn) depositBtn.style.display = 'none';
    if (timeRow)    timeRow.style.display    = 'none';
  }
}

/* ════════════════════════════════════
   APPKIT INIT
════════════════════════════════════ */

const appKit = createAppKit({
  adapters:  [new EthersAdapter()],
  networks:  [sepolia],
  projectId: 'c1115ad911ef0c661fa22792bfb65391',
  metadata: {
    name:        'AKYRA Bridge',
    description: 'Bridge ETH from Sepolia to AKYRA L2',
    url:         'https://akyra.io',
    icons:       ['https://akyra.io/logos/akyra-favicon.png'],
  },
  features: {
    analytics: false,
    email:     false,
    socials:   false,
    onramp:    false,
    swaps:     false,
  },
  themeMode: 'light',
  themeVariables: {
    '--w3m-border-radius-master': '0px',
    '--w3m-color-mix':            '#1a3080',
    '--w3m-color-mix-strength':   15,
    '--w3m-font-family':          'Space Grotesk, sans-serif',
    '--w3m-z-index':              '99999',
  },
});

/* ── Account subscription ── */
appKit.subscribeAccount(async (account) => {
  if (account.isConnected && account.address) {
    try {
      const walletProvider = appKit.getWalletProvider();
      if (!walletProvider) return;
      provider = new window.ethers.BrowserProvider(walletProvider);
      signer   = await provider.getSigner();
      userAddr = account.address;
      $('br-addr').textContent = truncAddr(userAddr);
      setConnectedUI(true);
      showError('br-connect-error', '');
      await refreshBalance();
    } catch (err) {
      console.error('[bridge] provider setup:', err);
    }
  } else {
    provider = null;
    signer   = null;
    userAddr = null;
    setConnectedUI(false);
    const balEl = $('br-balance-val');
    if (balEl) balEl.textContent = '—';
    updateReceive();
  }
});

/* ════════════════════════════════════
   WALLET CONNECT / DISCONNECT
════════════════════════════════════ */

window.bridgeConnect = function () {
  showError('br-connect-error', '');
  appKit.open();
};

window.bridgeDisconnect = function () {
  appKit.disconnect();
  showView('br-main-view');
  showError('br-connect-error', '');
  showError('br-form-error', '');
};

/* ════════════════════════════════════
   ADD AKYRA CHAIN
════════════════════════════════════ */

window.bridgeAddChain = async function () {
  const eth = appKit.getWalletProvider() || window.ethereum;
  if (!eth) { showError('br-connect-error', 'Connect a wallet first.'); return; }
  try {
    await eth.request({
      method: 'wallet_addEthereumChain',
      params: [{
        chainId: CFG.l2ChainHex,
        chainName: 'AKYRA L2 Testnet',
        nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
        rpcUrls: [CFG.l2Rpc],
        blockExplorerUrls: [CFG.l2Explorer],
      }],
    });
  } catch (err) { console.warn('[bridge] add chain:', err); }
};

/* ════════════════════════════════════
   BALANCE
════════════════════════════════════ */

async function refreshBalance() {
  if (!provider || !userAddr) return;
  const el = $('br-balance-val');
  if (!el) return;
  try {
    const bal = await provider.getBalance(userAddr);
    el.textContent = parseFloat(window.ethers.formatEther(bal)).toFixed(5) + ' ETH';
  } catch { el.textContent = 'Error'; }
}

/* ════════════════════════════════════
   MAX + RECEIVE MIRROR
════════════════════════════════════ */

window.bridgeMax = async function () {
  if (!provider || !userAddr) return;
  try {
    const bal     = await provider.getBalance(userAddr);
    const reserve = window.ethers.parseEther('0.01');
    const max     = bal > reserve ? bal - reserve : 0n;
    $('br-amount').value = window.ethers.formatEther(max);
    updateReceive();
  } catch {}
};

function updateReceive() {
  const raw = $('br-amount')?.value;
  const val = parseFloat(raw);
  const el  = $('br-receive-amount');
  if (el) el.textContent = (!val || val <= 0) ? '0' : raw;
}

$('br-amount')?.addEventListener('input', updateReceive);

/* ════════════════════════════════════
   DEPOSIT ETH
════════════════════════════════════ */

window.bridgeDeposit = async function () {
  if (busy) return;
  showError('br-form-error', '');

  if (!provider || !signer || !userAddr) {
    showError('br-form-error', 'Connect a wallet first.');
    return;
  }

  const raw = $('br-amount')?.value;
  const val = parseFloat(raw);
  if (!val || val <= 0) { showError('br-form-error', 'Enter a valid amount.'); return; }

  /* Verify Sepolia */
  const network = await provider.getNetwork();
  if (Number(network.chainId) !== CFG.l1ChainId) {
    showError('br-form-error', 'Switch to Sepolia in your wallet to deposit.');
    try {
      await appKit.switchNetwork(sepolia);
      const wp = appKit.getWalletProvider();
      provider = new window.ethers.BrowserProvider(wp);
      signer   = await provider.getSigner();
    } catch { return; }
  }

  const amountWei = window.ethers.parseEther(raw);
  const bal       = await provider.getBalance(userAddr);
  if (bal < amountWei) { showError('br-form-error', 'Insufficient ETH balance.'); return; }

  busy = true;
  setBtnState('br-deposit-btn', 'Confirming...', true);

  try {
    const bridge = new window.ethers.Contract(CFG.l1Bridge, L1_BRIDGE_ABI, signer);
    const tx     = await bridge.depositETH(CFG.minGas, '0x', { value: amountWei });

    showView('br-tx-view');
    $('br-tx-title').textContent = 'Transaction submitted';
    $('br-tx-sub').textContent   = 'Waiting for L1 confirmation...';
    $('br-spinner').style.display    = 'block';
    $('br-tx-success').style.display = 'none';
    $('br-tx-links').style.display   = 'none';
    $('br-l1-link').href             = CFG.l1Explorer + '/tx/' + tx.hash;

    await tx.wait();

    $('br-spinner').style.display    = 'none';
    $('br-tx-success').style.display = 'flex';
    $('br-tx-title').textContent     = 'Deposit confirmed';
    $('br-tx-sub').textContent       = 'ETH will arrive on AKYRA L2 in ~2-5 minutes.';
    $('br-tx-links').style.display   = 'flex';
    $('br-l2-link').href             = CFG.l2Explorer + '/address/' + userAddr;

  } catch (err) {
    if (err.code === 'ACTION_REJECTED' || err.code === 4001) {
      showError('br-form-error', 'Transaction cancelled.');
    } else {
      showError('br-form-error', 'Transaction failed. Check explorer for details.');
      console.error('[bridge] deposit:', err);
    }
    showView('br-main-view');
  }

  busy = false;
  setBtnState('br-deposit-btn', 'Deposit', false);
};

/* ════════════════════════════════════
   RESET
════════════════════════════════════ */

window.bridgeReset = function () {
  showView('br-main-view');
  if ($('br-amount')) $('br-amount').value = '';
  updateReceive();
  showError('br-form-error', '');
  refreshBalance();
};
