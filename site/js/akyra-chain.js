/**
 * AKYRA Chain Integration Module
 * Connexion et interaction avec la blockchain AKYRA
 */

class AkyraChain {
  constructor() {
    this.provider = null;
    this.signer = null;
    this.connected = false;
    this.config = {
      chainId: 47197,
      chainName: 'AKYRA Chain',
      rpcUrl: 'http://35.233.51.51:8545',
      blockExplorer: 'http://35.233.51.51:4000',
      nativeCurrency: {
        name: 'AKY',
        symbol: 'AKY',
        decimals: 18
      }
    };

    // Adresses des contrats (à mettre à jour avec vos adresses réelles)
    this.contracts = {
      AgentRegistry: '0x0000000000000000000000000000000000000000',
      SponsorGateway: '0x0000000000000000000000000000000000000000',
      FeeRouter: '0x0000000000000000000000000000000000000000',
      RewardPool: '0x0000000000000000000000000000000000000000',
      ForgeFactory: '0x0000000000000000000000000000000000000000',
      DeathAngel: '0x0000000000000000000000000000000000000000'
    };

    this.init();
  }

  /**
   * Initialise la connexion au provider RPC
   */
  async init() {
    try {
      // Connexion au RPC de la AKYRA Chain
      this.provider = new ethers.JsonRpcProvider(this.config.rpcUrl);
      console.log('✅ Connecté à AKYRA Chain');

      // Vérifier la connexion
      const network = await this.provider.getNetwork();
      console.log('Network:', network.chainId.toString());

      // Charger les stats initiales
      this.loadChainStats();

    } catch (error) {
      console.error('❌ Erreur de connexion à AKYRA Chain:', error);
    }
  }

  /**
   * Charge les statistiques de la blockchain
   */
  async loadChainStats() {
    try {
      const blockNumber = await this.provider.getBlockNumber();
      const block = await this.provider.getBlock(blockNumber);
      const gasPrice = await this.provider.getFeeData();

      const stats = {
        blockNumber: blockNumber,
        blockTime: new Date(block.timestamp * 1000).toLocaleString('fr-FR'),
        gasPrice: ethers.formatUnits(gasPrice.gasPrice, 'gwei'),
        transactions: block.transactions.length
      };

      // Mettre à jour l'UI
      this.updateStatsUI(stats);

      return stats;
    } catch (error) {
      console.error('Erreur chargement stats:', error);
      return null;
    }
  }

  /**
   * Récupère les données des agents IA
   */
  async getAgents() {
    try {
      // ABI simplifié de AgentRegistry
      const abi = [
        "function agentCount() view returns (uint256)",
        "function agents(uint256) view returns (address sponsor, uint256 vault, uint8 tier, uint8 world, bool alive)"
      ];

      const registry = new ethers.Contract(
        this.contracts.AgentRegistry,
        abi,
        this.provider
      );

      const count = await registry.agentCount();
      const agents = [];

      for (let i = 1; i <= count; i++) {
        const agent = await registry.agents(i);
        agents.push({
          id: i,
          sponsor: agent.sponsor,
          vault: ethers.formatEther(agent.vault),
          tier: agent.tier,
          world: agent.world,
          alive: agent.alive
        });
      }

      return agents;
    } catch (error) {
      console.error('Erreur récupération agents:', error);
      return [];
    }
  }

  /**
   * Récupère les statistiques globales
   */
  async getGlobalStats() {
    try {
      const agents = await this.getAgents();
      const aliveAgents = agents.filter(a => a.alive).length;
      const totalVault = agents.reduce((sum, a) => sum + parseFloat(a.vault), 0);

      return {
        totalAgents: agents.length,
        aliveAgents: aliveAgents,
        deadAgents: agents.length - aliveAgents,
        totalAKYLocked: totalVault.toFixed(2)
      };
    } catch (error) {
      console.error('Erreur stats globales:', error);
      return null;
    }
  }

  /**
   * Met à jour l'interface avec les stats
   */
  updateStatsUI(stats) {
    // Mettre à jour les éléments HTML
    const elements = {
      blockNumber: document.getElementById('chain-block'),
      gasPrice: document.getElementById('chain-gas'),
      agents: document.getElementById('chain-agents')
    };

    if (elements.blockNumber) {
      elements.blockNumber.textContent = stats.blockNumber.toLocaleString();
    }

    if (elements.gasPrice) {
      elements.gasPrice.textContent = `${parseFloat(stats.gasPrice).toFixed(4)} AKY`;
    }
  }

  /**
   * Connexion du wallet utilisateur
   */
  async connectWallet() {
    try {
      if (!window.ethereum) {
        alert('Veuillez installer MetaMask ou un wallet compatible');
        return false;
      }

      // Demander la connexion
      await window.ethereum.request({ method: 'eth_requestAccounts' });

      // Ajouter/changer vers AKYRA Chain
      try {
        await window.ethereum.request({
          method: 'wallet_switchEthereumChain',
          params: [{ chainId: `0x${this.config.chainId.toString(16)}` }],
        });
      } catch (switchError) {
        // La chain n'existe pas, on l'ajoute
        if (switchError.code === 4902) {
          await window.ethereum.request({
            method: 'wallet_addEthereumChain',
            params: [{
              chainId: `0x${this.config.chainId.toString(16)}`,
              chainName: this.config.chainName,
              nativeCurrency: this.config.nativeCurrency,
              rpcUrls: [this.config.rpcUrl],
              blockExplorerUrls: [this.config.blockExplorer]
            }]
          });
        }
      }

      // Créer le signer
      const browserProvider = new ethers.BrowserProvider(window.ethereum);
      this.signer = await browserProvider.getSigner();
      this.connected = true;

      const address = await this.signer.getAddress();
      console.log('✅ Wallet connecté:', address);

      return address;
    } catch (error) {
      console.error('Erreur connexion wallet:', error);
      return false;
    }
  }

  /**
   * Rafraîchit les données toutes les X secondes
   */
  startAutoRefresh(intervalSeconds = 10) {
    setInterval(async () => {
      await this.loadChainStats();
      const globalStats = await this.getGlobalStats();
      if (globalStats) {
        this.updateGlobalStatsUI(globalStats);
      }
    }, intervalSeconds * 1000);
  }

  /**
   * Met à jour les stats globales dans l'UI
   */
  updateGlobalStatsUI(stats) {
    const elements = {
      totalAgents: document.getElementById('stat-total-agents'),
      aliveAgents: document.getElementById('stat-alive-agents'),
      totalAKY: document.getElementById('stat-total-aky')
    };

    if (elements.totalAgents) {
      elements.totalAgents.textContent = stats.totalAgents;
    }

    if (elements.aliveAgents) {
      elements.aliveAgents.textContent = stats.aliveAgents;
    }

    if (elements.totalAKY) {
      elements.totalAKY.textContent = `${stats.totalAKYLocked} AKY`;
    }
  }
}

// Initialiser la connexion automatiquement
const akyra = new AkyraChain();

// Exporter pour utilisation globale
window.akyra = akyra;
