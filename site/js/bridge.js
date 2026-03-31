/* ═══════════════════════════════════════════
   AKYRA Bridge — OP Stack Custom Bridge
   Sepolia (L1) → AKYRA L2 (Chain 47197)
   ETH deposits only — vanilla JS + ethers.js v6
   ZKSync-style card layout
═══════════════════════════════════════════ */

(function () {
  'use strict';

  /* ── Config ── */
  const CFG = {
    l1ChainId:  11155111,
    l1ChainHex: '0xaa36a7',
    l1Name:     'Sepolia',
    l1Rpc:      'https://ethereum-sepolia-rpc.publicnode.com',
    l1Explorer: 'https://sepolia.etherscan.io',
    l1Bridge:   '0x986775ef7ad580449a4f3a90adc50ab116d28938',

    l2ChainId:  47197,
    l2ChainHex: '0xb85d',
    l2Name:     'AKYRA L2',
    l2Rpc:      'http://35.233.51.51:8545',
    l2Explorer: 'http://35.233.51.51:4000',
    l2Bridge:   '0x4200000000000000000000000000000000000010',

    minGas: 200000,
  };

  /* ── ABI ── */
  const L1_BRIDGE_ABI = [
    'function depositETH(uint32 _minGasLimit, bytes calldata _extraData) payable',
  ];

  /* ── State ── */
  let provider = null;
  let signer   = null;
  let userAddr = null;
  let busy = false;

  /* ── DOM refs ── */
  const $ = (id) => document.getElementById(id);

  /* ── Helpers ── */
  function truncAddr(addr) {
    return addr.slice(0, 6) + '···' + addr.slice(-4);
  }

  function showError(containerId, msg) {
    const el = $(containerId);
    if (!el) return;
    el.textContent = msg;
    el.style.display = msg ? 'block' : 'none';
  }

  function setBtnState(btnId, text, disabled) {
    const btn = $(btnId);
    if (!btn) return;
    btn.textContent = text;
    btn.disabled = disabled;
  }

  /* ── View toggle (main vs tx) ── */
  function showView(viewId) {
    ['br-main-view', 'br-tx-view'].forEach(id => {
      const el = $(id);
      if (el) el.style.display = id === viewId ? 'block' : 'none';
    });
  }

  /* ── Connected state UI ── */
  function setConnectedUI(connected) {
    const pill = $('br-wallet-pill');
    const connectBtn = $('br-connect-btn');
    const depositBtn = $('br-deposit-btn');
    const timeRow = $('br-time-row');

    if (connected) {
      if (pill) pill.style.display = 'flex';
      if (connectBtn) connectBtn.style.display = 'none';
      if (depositBtn) depositBtn.style.display = 'block';
      if (timeRow) timeRow.style.display = 'block';
    } else {
      if (pill) pill.style.display = 'none';
      if (connectBtn) connectBtn.style.display = 'block';
      if (depositBtn) depositBtn.style.display = 'none';
      if (timeRow) timeRow.style.display = 'none';
    }
  }

  /* ════════════════════════════════════
     MODAL OPEN / CLOSE
  ════════════════════════════════════ */

  window.openBridge = function () {
    const modal = $('bridge-modal');
    if (!modal) return;
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
  };

  window.closeBridge = function () {
    const modal = $('bridge-modal');
    if (!modal) return;
    modal.classList.remove('open');
    document.body.style.overflow = '';
  };

  /* Click-outside to close */
  document.addEventListener('DOMContentLoaded', () => {
    const modal = $('bridge-modal');
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) window.closeBridge();
      });
    }
  });

  /* ════════════════════════════════════
     ADD AKYRA CHAIN TO METAMASK
  ════════════════════════════════════ */

  window.bridgeAddChain = async function () {
    if (!window.ethereum) {
      showError('br-connect-error', 'MetaMask not detected.');
      return;
    }
    try {
      await window.ethereum.request({
        method: 'wallet_addEthereumChain',
        params: [{
          chainId: CFG.l2ChainHex,
          chainName: 'AKYRA L2 Testnet',
          nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
          rpcUrls: [CFG.l2Rpc],
          blockExplorerUrls: [CFG.l2Explorer],
        }],
      });
    } catch (err) {
      console.warn('Add chain failed:', err);
    }
  };

  /* ════════════════════════════════════
     WALLET CONNECTION
  ════════════════════════════════════ */

  window.bridgeConnect = async function () {
    showError('br-connect-error', '');

    if (!window.ethereum) {
      showError('br-connect-error', 'MetaMask not detected. Install it to use the bridge.');
      return;
    }

    setBtnState('br-connect-btn', 'Connecting...', true);

    try {
      await window.ethereum.request({ method: 'eth_requestAccounts' });
      provider = new ethers.BrowserProvider(window.ethereum);
      signer = await provider.getSigner();
      userAddr = await signer.getAddress();

      /* Verify Sepolia */
      const network = await provider.getNetwork();
      if (Number(network.chainId) !== CFG.l1ChainId) {
        try {
          await window.ethereum.request({
            method: 'wallet_switchEthereumChain',
            params: [{ chainId: CFG.l1ChainHex }],
          });
          provider = new ethers.BrowserProvider(window.ethereum);
          signer = await provider.getSigner();
        } catch (switchErr) {
          showError('br-connect-error', 'Please switch to Sepolia testnet in MetaMask.');
          setBtnState('br-connect-btn', 'Connect wallet', false);
          return;
        }
      }

      /* Success — update UI */
      $('br-addr').textContent = truncAddr(userAddr);
      setConnectedUI(true);
      await refreshBalance();

      /* Listeners */
      window.ethereum.on('accountsChanged', handleAccountChange);
      window.ethereum.on('chainChanged', handleChainChange);

    } catch (err) {
      if (err.code === 4001) {
        showError('br-connect-error', 'Wallet connection cancelled.');
      } else {
        showError('br-connect-error', 'Connection failed. Try again.');
      }
      setBtnState('br-connect-btn', 'Connect wallet', false);
    }
  };

  window.bridgeDisconnect = function () {
    provider = null;
    signer = null;
    userAddr = null;
    setConnectedUI(false);
    showView('br-main-view');
    setBtnState('br-connect-btn', 'Connect wallet', false);
    showError('br-connect-error', '');
    showError('br-form-error', '');

    /* Reset balance + receive */
    const balEl = $('br-balance-val');
    if (balEl) balEl.textContent = '—';
    updateReceive();

    if (window.ethereum) {
      window.ethereum.removeListener('accountsChanged', handleAccountChange);
      window.ethereum.removeListener('chainChanged', handleChainChange);
    }
  };

  function handleAccountChange(accounts) {
    if (!accounts.length) {
      window.bridgeDisconnect();
    } else {
      userAddr = accounts[0];
      $('br-addr').textContent = truncAddr(userAddr);
      refreshBalance();
    }
  }

  function handleChainChange() {
    window.bridgeDisconnect();
  }

  /* ════════════════════════════════════
     BALANCE
  ════════════════════════════════════ */

  async function refreshBalance() {
    if (!provider || !userAddr) return;
    const balEl = $('br-balance-val');
    if (!balEl) return;

    try {
      const bal = await provider.getBalance(userAddr);
      balEl.textContent = parseFloat(ethers.formatEther(bal)).toFixed(5) + ' ETH';
    } catch {
      balEl.textContent = 'Error';
    }
  }

  /* ════════════════════════════════════
     MAX
  ════════════════════════════════════ */

  window.bridgeMax = async function () {
    if (!provider || !userAddr) return;
    try {
      const bal = await provider.getBalance(userAddr);
      const reserve = ethers.parseEther('0.01');
      const max = bal > reserve ? bal - reserve : 0n;
      $('br-amount').value = ethers.formatEther(max);
      updateReceive();
    } catch { /* ignore */ }
  };

  /* ════════════════════════════════════
     RECEIVE AMOUNT MIRROR
  ════════════════════════════════════ */

  function updateReceive() {
    const raw = $('br-amount').value;
    const val = parseFloat(raw);
    const recvEl = $('br-receive-amount');
    if (!recvEl) return;

    if (!val || val <= 0) {
      recvEl.textContent = '0';
    } else {
      recvEl.textContent = raw;
    }
  }

  /* Listen for input changes */
  document.addEventListener('DOMContentLoaded', () => {
    const inp = $('br-amount');
    if (inp) inp.addEventListener('input', updateReceive);
  });

  /* ════════════════════════════════════
     DEPOSIT ETH
  ════════════════════════════════════ */

  window.bridgeDeposit = async function () {
    if (busy) return;
    showError('br-form-error', '');

    const raw = $('br-amount').value;
    const val = parseFloat(raw);

    if (!val || val <= 0) {
      showError('br-form-error', 'Enter a valid amount.');
      return;
    }

    /* Verify chain */
    const network = await provider.getNetwork();
    if (Number(network.chainId) !== CFG.l1ChainId) {
      showError('br-form-error', 'Please switch to Sepolia in MetaMask.');
      return;
    }

    const amountWei = ethers.parseEther(raw);
    const bal = await provider.getBalance(userAddr);
    if (bal < amountWei) {
      showError('br-form-error', 'Insufficient ETH balance.');
      return;
    }

    busy = true;
    setBtnState('br-deposit-btn', 'Confirming...', true);

    try {
      const bridge = new ethers.Contract(CFG.l1Bridge, L1_BRIDGE_ABI, signer);
      const tx = await bridge.depositETH(CFG.minGas, '0x', { value: amountWei });

      /* Switch to TX view */
      showView('br-tx-view');
      $('br-tx-title').textContent = 'Transaction submitted';
      $('br-tx-sub').textContent = 'Waiting for L1 confirmation...';
      $('br-spinner').style.display = 'block';
      $('br-tx-success').style.display = 'none';
      $('br-tx-links').style.display = 'none';

      /* L1 explorer link */
      $('br-l1-link').href = CFG.l1Explorer + '/tx/' + tx.hash;
      $('br-l1-link').style.display = 'inline';

      /* Wait for receipt */
      await tx.wait();

      /* Success */
      $('br-spinner').style.display = 'none';
      $('br-tx-success').style.display = 'flex';
      $('br-tx-title').textContent = 'Deposit confirmed';
      $('br-tx-sub').textContent = 'ETH will arrive on AKYRA L2 in ~2-5 minutes.';
      $('br-tx-links').style.display = 'flex';
      $('br-l2-link').href = CFG.l2Explorer + '/address/' + userAddr;

    } catch (err) {
      if (err.code === 'ACTION_REJECTED' || err.code === 4001) {
        showError('br-form-error', 'Transaction cancelled.');
      } else {
        showError('br-form-error', 'Transaction failed. Check explorer for details.');
      }
      showView('br-main-view');
    }

    busy = false;
    setBtnState('br-deposit-btn', 'Deposit', false);
  };

  /* ════════════════════════════════════
     RESET / BRIDGE ANOTHER
  ════════════════════════════════════ */

  window.bridgeReset = function () {
    showView('br-main-view');
    $('br-amount').value = '';
    updateReceive();
    showError('br-form-error', '');
    refreshBalance();
  };

})();
