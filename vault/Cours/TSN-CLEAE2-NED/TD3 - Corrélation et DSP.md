---
tags: [TSN, TD, autocorrélation, DSP, matlab]
---
# TD3 — Corrélation et densité spectrale de puissance
Retour : [[00 - Sommaire TSN]] · Cours : [[11 - Estimation de l'autocorrélation]], [[12 - Estimation de la densité spectrale de puissance]]

> [!info] Statut de la correction
> Aucune correction officielle n'a été distribuée pour ce TD : les réponses ci-dessous sont une **proposition** construite à partir du cours. Le bruit $\sigma$ n'étant pas fixé par l'énoncé, on prend $\sigma = 0{,}5$.

## 1 Rappels
- Autocorrélation d'un signal stationnaire d'ordre 2 : $R_X(t_1,t_2) = \mathbb{E}[X(t_1)X^*(t_2)]$
- Estimateur (numérique) : $\hat R_x[n] = \frac1N\sum_{k=n}^{N-1}x[k]\,x^*[k-n]$, $n = 0,\dots,N-1$ (version **biaisée**)
- DSP : $S_x(f) = \mathcal{F}(R_x)(f)$
- Périodogramme : $\hat S_x[k] = \frac1N|\text{DFT}(x)[k]|^2$

## 2 Introduction
On veut estimer l'autocorrélation et la DSP de
$$x(t) = A_1\cos(2\pi f_1t) + A_2\cos(2\pi f_2t)$$
mesuré avec un bruit additif du système de réception :
$$y(t) = x(t) + b(t), \qquad b(t)\sim\mathcal{N}(0,\sigma^2) \text{ stationnaire d'ordre 2}$$
On compare le cas idéal (sans bruit) et le cas mesuré (avec bruit).

**Paramètres** : durée 2 s, $F_e = 200$ Hz, $f_1 = 10$ Hz, $f_2 = 25$ Hz, $A_1 = 1$, $A_2 = 0{,}7$.

> [!tip] Ce qu'on doit trouver (théorie)
> - $R_x(\tau) = \frac{A_1^2}{2}\cos(2\pi f_1\tau) + \frac{A_2^2}{2}\cos(2\pi f_2\tau)$ → $R_x(0) = 0{,}745$
> - $R_b[n] = \sigma^2\delta[n]$ → pic de hauteur $\sigma^2 = 0{,}25$ en 0 seulement
> - $R_y = R_x + R_b$
> - $S_y$ : raies en $\pm10$ et $\pm25$ Hz posées sur un plancher plat à $\sigma^2$ (soit $10\log_{10}(0{,}25) \approx -6$ dB avec la normalisation $|X|^2/N$).

### 2.1–2.4 Génération du signal

> [!question] 2.1 Générer le vecteur temps · 2.2 Générer $x[n]$ · 2.3 Générer $y[n]$ · 2.4 Tracer $x$, $b$ et $y$

> [!success]- Correction
> ```matlab
> %% Paramètres
> Fe = 200;          % Fréquence d'échantillonnage (Hz)
> Te = 1/Fe;         % Période d'échantillonnage (s)
> T  = 2;            % Durée d'observation (s)
> t  = 0:Te:T-Te;    % Temps (s)
> N  = length(t);    % Nombre de points (400)
>
> %% Signal idéal
> f1 = 10; f2 = 25;  % Fréquences (Hz)
> A1 = 1;  A2 = 0.7; % Amplitudes
> x  = A1*cos(2*pi*f1*t) + A2*cos(2*pi*f2*t);
>
> %% Signal observé
> sigma = 0.5;
> b = sigma*randn(1,N);   % Bruit blanc gaussien N(0, sigma^2)
> y = x + b;
>
> %% Tracés
> figure;
> subplot(3,1,1); plot(t,x); title('x (idéal)');  ylabel('Amplitude');
> subplot(3,1,2); plot(t,b); title('b (bruit)');  ylabel('Amplitude');
> subplot(3,1,3); plot(t,y); title('y = x + b');  ylabel('Amplitude'); xlabel('Temps (s)');
> ```

## 3 Estimation de la fonction d'autocorrélation

> [!question] 3.1 Tracer les estimateurs **non biaisés** de l'autocorrélation de $x$, $b$ et $y$ avec `xcorr`. Axe des retards en secondes.

> [!success]- Correction
> ```matlab
> [Rx, lags] = xcorr(x, 'unbiased');
> Rb = xcorr(b, 'unbiased');
> Ry = xcorr(y, 'unbiased');
> tau = lags*Te;                         % retards en secondes (de -2 à 2 s)
>
> figure;
> subplot(3,1,1); plot(tau,Rx); title('R_x non biaisé');
> subplot(3,1,2); plot(tau,Rb); title('R_b non biaisé');
> subplot(3,1,3); plot(tau,Ry); title('R_y non biaisé'); xlabel('\tau (s)');
> ```
> **Observations** :
> - $R_x$ : somme de deux cosinus (10 et 25 Hz) d'amplitude constante, $R_x(0)\approx0{,}745$ = puissance de $x$.
> - $R_b$ : un pic ≈ $\sigma^2$ en $\tau = 0$, fluctuations ailleurs → bruit **blanc** (décorrélé).
> - $R_y \approx R_x + R_b$ : le bruit n'ajoute qu'un pic en 0 ; la structure périodique de $x$ reste lisible.
> - Aux **bords** ($|\tau|\to2$ s), l'estimateur non biaisé divise par $N-|n|$ très petit → **forte variance**, courbes erratiques.
> - Pour comparaison : `xcorr(y,'biased')` donne des courbes atténuées en triangle, mais bien moins bruitées aux bords.

> [!question] 3.2 Relancer plusieurs fois pour comparer les réalisations.

> [!success]- Correction
> ```matlab
> figure; hold on;
> for r = 1:5
>     yr = x + sigma*randn(1,N);
>     plot(tau, xcorr(yr,'unbiased'));
> end
> hold off; xlabel('\tau (s)'); title('R_y : 5 réalisations');
> ```
> Les réalisations **se superposent près de $\tau=0$** (beaucoup de termes moyennés) et **divergent aux grands retards** (peu de termes) : c'est la variance de l'estimateur qui croît avec $|n|$. $R_x$ lui ne change pas (signal déterministe).

## 4 Estimation de la densité spectrale de puissance
Les spectres sont affichés **en dB**.

> [!question] 4.1 Estimer la DSP à partir de la fonction d'autocorrélation (corrélogramme).

> [!success]- Correction
> ```matlab
> L  = length(Ry);                       % 2N-1 retards
> fL = ((0:L-1) - floor(L/2))*Fe/L;      % axe fréquentiel centré (Hz)
>
> % ifftshift place le retard 0 en première position avant la DFT
> Sy_corr_nb = fftshift(real(fft(ifftshift(Ry))));                 % à partir du non biaisé
> Sy_corr_b  = fftshift(real(fft(ifftshift(xcorr(y,'biased')))));  % à partir du biaisé
>
> figure;
> plot(fL, 10*log10(abs(Sy_corr_nb))); hold on;
> plot(fL, 10*log10(abs(Sy_corr_b)));  hold off;
> legend('corrélogramme (R non biaisé)','corrélogramme (R biaisé)');
> xlabel('Fréquence (Hz)'); ylabel('DSP (dB)');
> ```
> - Pics à ±10 et ±25 Hz, plancher de bruit vers $10\log_{10}\sigma^2\approx-6$ dB.
> - Avec $\hat R$ non biaisé, la DSP estimée peut être **négative** (d'où le `abs` pour passer en dB) et elle est plus bruitée : les retards extrêmes mal estimés pèsent autant que les autres.

> [!question] 4.2 Estimer la DSP par périodogramme.

> [!success]- Correction
> ```matlab
> fN = ((0:N-1) - floor(N/2))*Fe/N;
> Sy_per = abs(fftshift(fft(y))).^2/N;
> figure; plot(fN, 10*log10(Sy_per));
> xlabel('Fréquence (Hz)'); ylabel('DSP (dB)'); title('Périodogramme');
> ```
> Pics de hauteur $\approx \frac{A^2}{4}N$ (en puissance par case) : $10\log_{10}(0{,}25\times400)=20$ dB pour $f_1$, ≈17 dB pour $f_2$. Le plancher de bruit fluctue fortement (±5–10 dB) : estimateur **non consistant**.

> [!question] 4.3 Comparer les deux estimateurs sur une figure.

> [!success]- Correction
> ```matlab
> figure;
> plot(fL, 10*log10(abs(Sy_corr_b))); hold on;
> plot(fN, 10*log10(Sy_per), '--');    hold off;
> legend('Corrélogramme (R biaisé)','Périodogramme');
> ```
> Le **corrélogramme biaisé et le périodogramme coïncident** (Wiener–Khinchin discret) : le premier est simplement évalué sur $2N-1$ fréquences au lieu de $N$ — il est égal à `abs(fft(y,2*N-1)).^2/N`. Le corrélogramme non biaisé, lui, s'en écarte (plus de variance, valeurs négatives possibles).

> [!question] 4.4 Quel est l'intérêt de la méthode de Welch par rapport au périodogramme ?

> [!success]- Correction
> Le périodogramme est **non consistant** : sa variance ne diminue pas quand $N$ augmente. Welch découpe le signal en segments **qui se chevauchent**, **fenêtrés**, et **moyenne** leurs périodogrammes :
> - **variance réduite** (d'un facteur ≈ nombre de segments) → spectre lisse, plancher de bruit bien estimé ;
> - **fuite spectrale réduite** grâce à la fenêtre ;
> - **prix à payer** : résolution dégradée ($\approx F_e/M$ au lieu de $F_e/N$), car chaque segment est plus court.

> [!question] 4.5 Utiliser Welch (`pwelch`) et comparer avec le périodogramme.

> [!success]- Correction
> ```matlab
> M = 64;                 % taille des segments
> w = hann(M);            % fenêtre
> noverlap = M/2;         % chevauchement 50 %
> nfft = 256;             % points de DFT par segment (zéro-padding)
> [Pw, fw] = pwelch(y, w, noverlap, nfft, Fe, 'centered');
>
> figure;
> plot(fN, 10*log10(Sy_per/Fe)); hold on;     % /Fe : périodogramme en unités²/Hz comme pwelch
> plot(fw, 10*log10(Pw), 'LineWidth', 1.5); hold off;
> legend('Périodogramme','Welch'); xlabel('Fréquence (Hz)'); ylabel('DSP (dB/Hz)');
> ```
> - Welch : plancher de bruit **lisse** et proche de $10\log_{10}(\sigma^2/F_e)\approx-29$ dB/Hz ; pics plus **larges** (résolution ≈ $F_e/M \approx 3$ Hz, voire $2\times$ avec Hann).
> - Périodogramme : pics fins mais plancher très fluctuant.
>
> ⚠️ L'énoncé écrit « `pwelsh` » : la fonction MATLAB s'appelle **`pwelch`** (méthode de *Welch*). L'option `'centered'` donne un spectre bilatéral centré, comparable à `fftshift`.

> [!question] 4.6 Appliquer un fenêtrage différent.

> [!success]- Correction
> ```matlab
> wins  = {rectwin(M), hann(M), hamming(M), blackman(M)};
> names = {'Rectangulaire','Hann','Hamming','Blackman'};
> figure; hold on;
> for i = 1:4
>     [P, fw] = pwelch(y, wins{i}, M/2, nfft, Fe, 'centered');
>     plot(fw, 10*log10(P));
> end
> hold off; legend(names); xlabel('Fréquence (Hz)'); ylabel('dB/Hz');
> ```
> Rectangulaire : pics les plus étroits mais lobes secondaires (−13 dB) qui « bavent » ; Blackman : pics les plus larges, lobes secondaires invisibles. Cf. tableau de [[08 - Résolution spectrale et fenêtrage#Comparaison des fenêtres usuelles]]. Pour mieux voir l'effet, baisser $\sigma$ (ex. 0,01) : sinon les lobes secondaires sont noyés dans le bruit.

> [!question] 4.7 Faire varier la taille de la fenêtre et comparer.

> [!success]- Correction
> ```matlab
> figure; hold on;
> for M = [16 32 64 128 256]
>     [P, fw] = pwelch(y, hann(M), M/2, max(256,M), Fe, 'centered');
>     plot(fw, 10*log10(P), 'DisplayName', sprintf('M = %d', M));
> end
> hold off; legend show;
> ```
> **$M$ petit** : beaucoup de segments → variance faible (spectre lisse) mais **pics larges** (mauvaise résolution ; à $M=16$, $F_e/M = 12{,}5$ Hz et le lobe principal de Hann fait $4F_e/M = 50$ Hz de large : les raies à 10 et 25 Hz se confondent).
> **$M$ grand** : pics fins mais spectre bruité ; $M = N$ → on retrouve un périodogramme fenêtré.
> ⟹ **compromis résolution / variance**.

## 5 Comparaison

> [!question] 5.1 Modifier la variance du bruit et observer l'autocorrélation et la DSP.

> [!success]- Correction
> Tester $\sigma \in \{0;\ 0{,}1;\ 0{,}5;\ 1;\ 3\}$ :
> - **Autocorrélation** : seul le pic en $\tau = 0$ augmente ($R_y(0) = 0{,}745 + \sigma^2$), les oscillations restent, mais les fluctuations autour s'amplifient.
> - **DSP** : le **plancher** monte en $10\log_{10}\sigma^2$ (+6 dB quand $\sigma$ double) ; les raies restent à la même hauteur mais **émergent de moins en moins** (baisse du SNR). Pour $\sigma$ grand, la raie à 25 Hz (plus faible) disparaît la première dans le périodogramme ; Welch permet de la retrouver plus longtemps.

> [!question] 5.2 Définir un autre signal, éventuellement aléatoire, et observer son autocorrélation et sa DSP.

> [!success]- Correction (exemple : bruit coloré AR(1))
> ```matlab
> a = 0.9;
> z = filter(1, [1 -a], randn(1,N));     % z[n] = a z[n-1] + e[n]
> [Rz, lz] = xcorr(z,'biased');
> [Pz, fz] = pwelch(z, hann(64), 32, 256, Fe, 'centered');
> Hth = 1./abs(1 - a*exp(-2i*pi*fz/Fe)).^2 / Fe;   % DSP théorique (unités²/Hz)
> figure; subplot(2,1,1); plot(lz*Te, Rz); xlabel('\tau (s)');
> subplot(2,1,2); plot(fz, 10*log10(Pz), fz, 10*log10(Hth), '--'); legend('Welch','théorie');
> ```
> Théorie : $R_z[n] = \dfrac{a^{|n|}}{1-a^2}$ (décroissance exponentielle : le signal « se souvient » de son passé) et $S_z(f) = \dfrac{1}{|1-a\,e^{-2i\pi f/F_e}|^2}$ : DSP **passe-bas** (bruit « rose/rouge »), illustration de $S_y = |H|^2S_x$ ([[13 - Filtrage linéaire]]).
> Autres idées : sinusoïde à phase aléatoire $\cos(2\pi f_0t + \phi[n])$ (étalement de la raie), chirp (`chirp`), signal carré (harmoniques impaires).

> [!question] 5.3 Mettre en évidence la limite de résolution du spectre avec un remplissage par zéros.

> [!success]- Correction
> Rapprocher les deux fréquences en dessous de la résolution $1/T = 0{,}5$ Hz :
> ```matlab
> x2 = cos(2*pi*10*t) + 0.7*cos(2*pi*10.3*t);   % écart 0,3 Hz < 1/T
> for Mzp = [1 4 16]
>     Np = Mzp*N;
>     X2 = abs(fftshift(fft(x2, Np))).^2/N;
>     fp = ((0:Np-1) - floor(Np/2))*Fe/Np;
>     figure; plot(fp, 10*log10(X2)); xlim([5 15]);
>     title(sprintf('Zero-padding x%d', Mzp));
> end
> ```
> Même avec un zéro-padding ×16 (courbe très lisse), **un seul pic** apparaît : le zéro-padding **interpole** le spectre mais **n'améliore pas la résolution**. Avec un écart de 1 Hz (ex. 10 et 11 Hz), ou avec $T = 4$ s, les deux pics se séparent.

> [!question] 5.4 Modifier $F_e$ et la durée de mesure, observer leur influence.

> [!success]- Correction
> - **$F_e$** (à $T$ fixé) :
>   - $F_e = 200 \to 100$ Hz : rien ne change qualitativement (axe restreint à ±50 Hz) ;
>   - $F_e = 50$ Hz : 25 Hz est à la fréquence de Nyquist (cas limite) ;
>   - $F_e = 40$ Hz : **repliement**, la raie à 25 Hz apparaît à $40-25 = 15$ Hz ;
>   - le plancher de bruit en dB/Hz ($\sigma^2/F_e$) baisse quand $F_e$ augmente (même puissance étalée sur une bande plus large).
> - **$T$** (à $F_e$ fixé) :
>   - $T$ petit (0,2 s) → $N=40$, pics larges (résolution $1/T = 5$ Hz), autocorrélation courte ;
>   - $T$ grand (10 s) → pics fins ; la **variance du périodogramme ne diminue pas** pour autant (non-consistance), alors que Welch en profite (plus de segments).
