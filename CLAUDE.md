# AKYRA — Claude Code Context

## 🧠 Règle : Recommandation de modèle

Avant chaque tâche proposée ou demandée, indique toujours le modèle recommandé :

- **Sonnet** → tâches d'exécution : code, édition fichiers, debug, git, CSS, JS, config
- **Opus** → tâches de réflexion : architecture, stratégie, copywriting créatif, décisions techniques importantes, analyse de sécurité

Format : commencer la réponse par `> 🤖 **Sonnet** — [raison courte]` ou `> 🤖 **Opus** — [raison courte]`

---

## 📁 Structure du projet

```
/Users/tgds.2/akyra/
├── site/               ← Landing page statique (HTML/CSS/JS pur)
│   ├── index.html      ← Fichier principal — tout est là
│   ├── css/
│   │   ├── main.css
│   │   └── sections.css   ← CSS des sections + modal waitlist
│   ├── js/
│   │   └── main.js
│   └── logos/          ← SVGs + PNG logo Gemini
└── remotion/           ← Animations vidéo (React + TypeScript)
    ├── src/
    │   ├── Root.tsx
    │   ├── TickEngine.tsx   ← Animation principale (210 frames, 30fps)
    │   └── AnimatedLogo.tsx ← Logo SVG animé
    └── public/
        └── logo.png
```

---

## 🎨 Design System

**Palette AKYRA :**
```
bg:    #f7f4ef   ← fond crème
blue:  #1a3080   ← bleu marine (primaire)
blue2: #2a50c8   ← bleu vif (accent)
gold:  #c8a96e   ← or (accent secondaire)
muted: #8a7f72   ← gris chaud (texte secondaire)
dark:  #1e1a16   ← quasi-noir
```

**Fonts :** system sans-serif + JetBrains Mono (monospace)

**Conventions CSS :**
- Animations scroll : classe `.sr` + `.visible` via IntersectionObserver (NE PAS utiliser GSAP pour ça)
- GSAP : uniquement pour les éléments non-gérés par `.sr`
- Cache bust : `sections.css?vN` → incrémenter N à chaque modif CSS

---

## ⚙️ Stack technique

### Site (`/site/`)
- HTML/CSS/JS pur — **pas de bundler, pas de framework**
- CDNs chargés dans `index.html` :
  - GSAP 3.12.5 + ScrollTrigger
  - Chart.js 4.4.4
- Serveur local : `cd site && python3 -m http.server 8090`

### Remotion (`/remotion/`)
- React 19 + TypeScript 5.9 + Remotion 4.0.438
- Studio : `cd remotion && npx remotion studio src/index.ts --port 3333`
- Render : `npm run render`
- **Important :** `useCurrentFrame()` dans une `<Sequence>` retourne un frame LOCAL (commence à 0)
- **Important :** `staticFile()` cherche dans `/public/`, pas `/src/`

---

## 🔌 Intégrations externes

| Service | Usage | Config |
|---------|-------|--------|
| Formspree | Waitlist presale | Form ID: `xjgaqdrk` · endpoint: `https://formspree.io/f/xjgaqdrk` |
| GitHub | Repo | `https://github.com/electron0o29-oss/akyra` |

---

## 📋 Fonctionnalités implémentées

- [x] Landing page complète (hero, features, tokenomics, FAQ, presale CTA)
- [x] GSAP + ScrollTrigger animations
- [x] Chart.js donut tokenomics (lazy-init via IntersectionObserver)
- [x] Modal waitlist presale (500 slots, compteur, form Formspree)
- [x] AnimatedLogo.tsx (SVG animé Remotion)
- [x] TickEngine.tsx (animation 5 steps : PERCEIVE→REMEMBER→DECIDE→ACT→MEMORIZE)

## 🔜 Idées backlog

- [ ] Meta OpenGraph / SEO tags
- [ ] Section "Society Map" avec globe interactif
- [ ] Dark mode toggle
- [ ] Audit performance (Lighthouse)
- [ ] Render Remotion → embed WebM dans le site

---

## 🚫 Règles importantes

1. **Ne jamais utiliser Lenis** — causait des bugs de scroll
2. **Ne pas utiliser GSAP** sur les éléments avec classe `.sr` (conflit avec IntersectionObserver)
3. **Pas de framework JS** sur le site — rester en vanilla
4. **Toujours incrémenter** le version string de `sections.css?vN` après une modif CSS
5. **Git** : commiter par feature, message en anglais, format `feat/fix/config/refactor: ...`
