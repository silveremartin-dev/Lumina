# -*- coding: utf-8 -*-
"""
Rebuilds Lumina Web Studio (index.html) with all user refinements:
1. Le Petit Prince: Play, Pause, Stop controls; chained utterance onend (no mid-sentence cut-offs); removed English clutter.
2. Translation toolbar: 4 direction buttons, removed redundant swap button, wrapped samples without horizontal scrollbar.
3. Dynamic samples for all 4 translation directions.
4. STT (Dictée) in source language, TTS (Écoute) in target language with dynamic button labels.
5. Interactive Phoneme Inventory in Course & Grammar panels.
"""

import json
import subprocess
import re

# Load verified datasets
with open('data/lexique.json', 'r', encoding='utf-8') as f:
    lexique_data = json.load(f)

with open('data/petit_prince.json', 'r', encoding='utf-8') as f:
    prince_data = json.load(f)

prince_sentences = prince_data['sentences']

# Extract clean HTML from git HEAD
orig = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True, encoding='utf-8')

idx_script = orig.find('<script>\n    const LEXICON_DATA =')
if idx_script == -1:
    idx_script = orig.find('const LEXICON_DATA =')
    idx_script = orig.rfind('<script>', 0, idx_script)

html_head = orig[:idx_script]

# 1. Update Translation Toolbar
# Remove the swap button, add clean 4-pill selector, add dynamic wrapping samples container
new_toolbar = """        <!-- Translation Header & Language Mode Selector -->
        <div class="flex flex-col gap-3 pb-4 border-b border-slate-800">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div class="flex flex-wrap items-center gap-1.5 bg-slate-900 p-1 rounded-xl border border-slate-800 text-xs font-semibold">
              <button id="btn-mode-fr-lum" onclick="setDirection('fr-to-lumina')" class="px-3 py-1.5 rounded-lg bg-cyan-600 text-white transition flex items-center gap-1">
                <span>Français</span>
                <span class="text-cyan-200">➔</span>
                <span>Lumina</span>
              </button>
              <button id="btn-mode-lum-fr" onclick="setDirection('lumina-to-fr')" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition flex items-center gap-1">
                <span>Lumina</span>
                <span class="text-slate-500">➔</span>
                <span>Français</span>
              </button>
              <button id="btn-mode-en-lum" onclick="setDirection('en-to-lumina')" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition flex items-center gap-1">
                <span>English</span>
                <span class="text-slate-500">➔</span>
                <span>Lumina</span>
              </button>
              <button id="btn-mode-lum-en" onclick="setDirection('lumina-to-en')" class="px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition flex items-center gap-1">
                <span>Lumina</span>
                <span class="text-slate-500">➔</span>
                <span>English</span>
              </button>
            </div>

            <div class="text-xs px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 font-mono flex items-center gap-2">
              <span class="text-slate-500">Mode :</span>
              <span id="lang-from-label" class="font-bold text-cyan-400">Français</span>
              <span class="text-slate-500">➔</span>
              <span id="lang-to-label" class="font-bold text-indigo-400">Lumina</span>
            </div>
          </div>

          <!-- Dynamic Examples for the active mode (wrapping without horizontal scrollbar) -->
          <div class="flex flex-wrap items-center gap-2 pt-1 text-xs">
            <span class="text-slate-500 font-medium">Exemples :</span>
            <div id="quick-samples-container" class="flex flex-wrap items-center gap-2">
              <!-- Injected dynamically based on direction -->
            </div>
          </div>
        </div>"""

html_head = re.sub(
    r'<div class="flex flex-col sm:flex-row items-center justify-between pb-4 border-b border-slate-800 gap-4">[\s\S]*?<!-- Quick Samples -->[\s\S]*?</div>\s*</div>',
    new_toolbar,
    html_head
)

# 2. Update Input Area STT button and Output Area TTS button
old_stt_btn = """              <button id="btn-stt" onclick="toggleSTT()" class="text-xs px-2.5 py-1 rounded-md bg-slate-800 text-slate-300 border border-slate-700 hover:text-cyan-400 hover:border-cyan-700 transition flex items-center gap-1.5" title="Activer la dictée vocale (Speech-to-Text)">
                <span id="stt-dot" class="w-2 h-2 rounded-full bg-slate-500"></span>
                <span id="stt-label">Dictée Vocale (STT)</span>
              </button>"""

new_stt_btn = """              <button id="btn-stt" onclick="toggleSTT()" class="text-xs px-3 py-1 rounded-md bg-slate-800 text-slate-300 border border-slate-700 hover:text-cyan-400 hover:border-cyan-700 transition flex items-center gap-1.5" title="Dicter dans la langue source">
                <span id="stt-dot" class="w-2 h-2 rounded-full bg-slate-500"></span>
                <span id="stt-label">Dictée Vocale (Français)</span>
              </button>"""

if old_stt_btn in html_head:
    html_head = html_head.replace(old_stt_btn, new_stt_btn)

old_tts_btn = """              <button onclick="playTTS(document.getElementById('translate-output').innerText)" class="text-xs px-2.5 py-1 rounded-md bg-cyan-950 text-cyan-300 border border-cyan-800 hover:bg-cyan-900 transition flex items-center gap-1.5" title="Prononcer le texte Lumina">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                Écouter (TTS)
              </button>"""

new_tts_btn = """              <button id="btn-tts-translate" onclick="playTTS(document.getElementById('translate-output').innerText)" class="text-xs px-3 py-1 rounded-md bg-cyan-950 text-cyan-300 border border-cyan-800 hover:bg-cyan-900 transition flex items-center gap-1.5" title="Écouter la traduction dans la langue cible">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                <span id="tts-label">Écouter en Lumina</span>
              </button>"""

if old_tts_btn in html_head:
    html_head = html_head.replace(old_tts_btn, new_tts_btn)

# 3. Update Le Petit Prince Panel Header (Play, Pause, Stop controls)
old_prince_header = """        <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
          <div>
            <h2 class="text-lg font-bold text-white">Foro pa la Kitu Masa Duru — Chiffre 1</h2>
            <p class="text-xs text-slate-400">Le Petit Prince (Chapitre 1) — Texte fondateur en Lumina avec lecture audio synchronisée</p>
          </div>
          <button onclick="playAllPrince()" id="btn-play-all" class="px-4 py-2 bg-gradient-to-r from-cyan-600 to-indigo-600 hover:from-cyan-500 hover:to-indigo-500 text-white font-medium rounded-lg text-xs transition flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Lecture Intégrale Karaoké
          </button>
        </div>"""

new_prince_header = """        <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
          <div>
            <h2 class="text-lg font-bold text-white">Foro pa la Kitu Masa Duru — Chiffre 1</h2>
            <p class="text-xs text-slate-400">Le Petit Prince (Chapitre 1) &bull; Texte intégral bilingue Lumina & Français</p>
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <button onclick="playAllPrince()" id="btn-play-all" class="px-3 py-1.5 bg-gradient-to-r from-cyan-600 to-indigo-600 hover:from-cyan-500 hover:to-indigo-500 text-white font-medium rounded-lg text-xs transition flex items-center gap-1.5 shadow-md shadow-cyan-900/40">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/></svg>
              <span>Lecture continue</span>
            </button>
            <button onclick="pauseAllPrince()" id="btn-pause-all" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium rounded-lg text-xs transition flex items-center gap-1.5 border border-slate-700">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 9v6m4-6v6"/></svg>
              <span>Pause</span>
            </button>
            <button onclick="stopAllPrince()" id="btn-stop-all" class="px-3 py-1.5 bg-rose-950/80 hover:bg-rose-900 text-rose-300 font-medium rounded-lg text-xs transition flex items-center gap-1.5 border border-rose-800">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 6h12v12H6z"/></svg>
              <span>Arrêter</span>
            </button>
            <span id="prince-status-badge" class="text-[11px] px-2.5 py-1 rounded-full bg-slate-800 text-cyan-400 border border-slate-700 font-mono">Prêt</span>
          </div>
        </div>"""

if old_prince_header in html_head:
    html_head = html_head.replace(old_prince_header, new_prince_header)
else:
    html_head = re.sub(
        r'<div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">[\s\S]*?Lecture Intégrale Karaoké[\s\S]*?</div>\s*</div>',
        new_prince_header,
        html_head
    )

# 4. Enhance Grammar tab with full Phoneme Inventory table
phoneme_grammar_section = """        <!-- Phoneme Inventory Section -->
        <div class="bg-slate-950 border border-slate-800 rounded-xl p-5 space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
            <div>
              <h3 class="text-sm font-bold text-cyan-400 flex items-center gap-2">
                <span>🎙️</span> Inventaire Phonologique & Sons Purs de Lumina
              </h3>
              <p class="text-xs text-slate-400 mt-0.5">Le Lumina compte exactement 5 voyelles pures et 17 consonnes régulières avec accent tonique invariable sur l'avant-dernière syllabe.</p>
            </div>
            <span class="text-[11px] px-2.5 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 font-mono">Accent pénultième strict</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <!-- 5 Vowels -->
            <div class="p-3.5 rounded-lg bg-slate-900 border border-slate-800 space-y-2">
              <h4 class="font-bold text-white flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
                Les 5 Voyelles Cardinales (V)
              </h4>
              <p class="text-slate-400 text-[11px]">Toujours nettes et stables, sans diphtongue :</p>
              <div class="grid grid-cols-5 gap-1.5 text-center font-mono">
                <div class="p-2 rounded bg-slate-950 border border-slate-800 cursor-pointer hover:border-cyan-500 transition" onclick="playTTS('a', 'lumina')" title="Écouter [a]">
                  <span class="text-sm font-bold text-cyan-300">A</span><br>
                  <span class="text-[10px] text-slate-500">[a]</span><br>
                  <span class="text-[9px] text-slate-400 font-sans">papa</span>
                </div>
                <div class="p-2 rounded bg-slate-950 border border-slate-800 cursor-pointer hover:border-cyan-500 transition" onclick="playTTS('e', 'lumina')" title="Écouter [e]">
                  <span class="text-sm font-bold text-cyan-300">E</span><br>
                  <span class="text-[10px] text-slate-500">[e]</span><br>
                  <span class="text-[9px] text-slate-400 font-sans">été</span>
                </div>
                <div class="p-2 rounded bg-slate-950 border border-slate-800 cursor-pointer hover:border-cyan-500 transition" onclick="playTTS('i', 'lumina')" title="Écouter [i]">
                  <span class="text-sm font-bold text-cyan-300">I</span><br>
                  <span class="text-[10px] text-slate-500">[i]</span><br>
                  <span class="text-[9px] text-slate-400 font-sans">midi</span>
                </div>
                <div class="p-2 rounded bg-slate-950 border border-slate-800 cursor-pointer hover:border-cyan-500 transition" onclick="playTTS('o', 'lumina')" title="Écouter [o]">
                  <span class="text-sm font-bold text-cyan-300">O</span><br>
                  <span class="text-[10px] text-slate-500">[o]</span><br>
                  <span class="text-[9px] text-slate-400 font-sans">moto</span>
                </div>
                <div class="p-2 rounded bg-slate-950 border border-slate-800 cursor-pointer hover:border-cyan-500 transition" onclick="playTTS('u', 'lumina')" title="Écouter [u]">
                  <span class="text-sm font-bold text-cyan-300">U</span><br>
                  <span class="text-[10px] text-slate-500">[u]</span><br>
                  <span class="text-[9px] text-emerald-400 font-sans">"ou" loup</span>
                </div>
              </div>
            </div>

            <!-- 17 Consonants -->
            <div class="p-3.5 rounded-lg bg-slate-900 border border-slate-800 space-y-2">
              <h4 class="font-bold text-white flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
                Les 17 Consonnes (C)
              </h4>
              <p class="text-slate-400 text-[11px]">Classées par mode d'articulation pur :</p>
              <div class="space-y-1.5 text-[11px]">
                <div class="flex items-center justify-between border-b border-slate-800/60 pb-1">
                  <span class="text-slate-400 font-semibold">Occlusives :</span>
                  <span class="font-mono text-cyan-300">P [p] &bull; B [b] &bull; T [t] &bull; D [d] &bull; K [k] &bull; G [ɡ]</span>
                </div>
                <div class="flex items-center justify-between border-b border-slate-800/60 pb-1">
                  <span class="text-slate-400 font-semibold">Fricatives :</span>
                  <span class="font-mono text-cyan-300">F [f] &bull; V [v] &bull; S [s] &bull; Z [z] &bull; SH [ʃ] (chat) &bull; ZH [ʒ] (jour) &bull; H [h]</span>
                </div>
                <div class="flex items-center justify-between border-b border-slate-800/60 pb-1">
                  <span class="text-slate-400 font-semibold">Affriquées :</span>
                  <span class="font-mono text-cyan-300">CH [t͡ʃ] (tchao) &bull; J [d͡ʒ] (djembé)</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-slate-400 font-semibold">Nasales / Liquides :</span>
                  <span class="font-mono text-cyan-300">M [m] &bull; N [n] &bull; L [l] &bull; R [r]</span>
                </div>
              </div>
            </div>
          </div>
        </div>

"""

grammar_header_marker = '<h2 class="text-xl font-bold text-white">Mémento Grammatical Officiel de Lumina</h2>'
if grammar_header_marker in html_head:
    html_head = html_head.replace(
        '<section id="panel-grammar" class="hidden space-y-6">\n      <div class="bg-slate-900/50 border border-slate-800/80 rounded-2xl p-6 glow-box space-y-6">\n        <div>\n          <h2 class="text-xl font-bold text-white">Mémento Grammatical Officiel de Lumina</h2>',
        f'<section id="panel-grammar" class="hidden space-y-6">\n      <div class="bg-slate-900/50 border border-slate-800/80 rounded-2xl p-6 glow-box space-y-6">\n        <div>\n          <h2 class="text-xl font-bold text-white">Mémento Grammatical Officiel de Lumina</h2>\n        </div>\n{phoneme_grammar_section}'
    )

js_lexicon = json.dumps(lexique_data, ensure_ascii=False)
js_prince = json.dumps(prince_sentences, ensure_ascii=False)

js_template = """<script>
    // Embedded Complete Lumina Lexicon (2,268 roots, 453 adverbs, particles, pronouns, numbers)
    const LEXICON_DATA = __LEXICON_DATA__;

    // Embedded Complete Petit Prince Corpus (Chapter 1 - 22 authentic canonical sentences)
    const PRINCE_SENTENCES = __PRINCE_DATA__;

    // Active translation mode: 'fr-to-lumina', 'lumina-to-fr', 'en-to-lumina', 'lumina-to-en'
    let currentDirection = 'fr-to-lumina';
    let recognition = null;
    let isListening = false;
    let FR_TO_LUMINA = null;
    let EN_TO_LUMINA = null;

    // Le Petit Prince Continuous Playback State
    let isPrincePlaying = false;
    let isPrincePaused = false;
    let princeIndex = 0;
    let princeTimeout = null;

    // Deterministic Penultimate Stress IPA Transcriber
    function toIPA(word) {
      if (!word) return '';
      let w = word.toLowerCase().replace(/[,.?!:;"'\\[\\]]/g, '').trim();
      if (!w) return '';

      // Particle / Pronoun fast mapping
      const spec = {
        'la': 'la', 'ro': 'ro', 'na': 'na', 'li': 'li', 'vo': 'vo',
        'pe': 'pe', 'du': 'du', 'ne': 'ne', 'ma': 'ma', 'ta': 'ta',
        'fa': 'fa', 'pa': 'pa', 'ko': 'ko', 've': 've',
        'mina': "'mi.na", 'tina': "'ti.na", 'lina': "'li.na",
        'miro': "'mi.ro", 'tiro': "'ti.ro", 'liro': "'li.ro", 'kina': "'ki.na"
      };
      if (spec[w]) return spec[w];

      const ipaMap = {
        'sh': '\\u0283', 'zh': '\\u0292', 'ch': 't\\u0283', 'j': 'd\\u0292',
        'p': 'p', 'b': 'b', 't': 't', 'd': 'd', 'k': 'k', 'g': '\\u0261',
        'f': 'f', 'v': 'v', 's': 's', 'z': 'z', 'm': 'm', 'n': 'n',
        'l': 'l', 'r': 'r', 'h': 'h',
        'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u'
      };

      let syls = [];
      let i = 0;
      while (i < w.length) {
        let c = '';
        if (i + 1 < w.length && ['sh', 'zh', 'ch'].includes(w.slice(i, i + 2))) {
          c = w.slice(i, i + 2);
          i += 2;
        } else if ('pbtdkgfvszmnlrhj'.includes(w[i])) {
          c = w[i];
          i += 1;
        }
        let v = '';
        if (i < w.length && 'aeiou'.includes(w[i])) {
          v = w[i];
          i += 1;
        }
        if (c || v) {
          let sylIpa = (ipaMap[c] || c) + (ipaMap[v] || v);
          syls.push(sylIpa);
        } else {
          i += 1;
        }
      }

      if (!syls.length) return w;
      if (syls.length === 1) return syls[0];

      let penultIdx = syls.length - 2;
      syls[penultIdx] = "'" + syls[penultIdx];
      return syls.join('.');
    }

    // High Quality Web Speech API TTS with onEndCallback support
    function playTTS(text, forceLang, onEndCallback) {
      if (!window.speechSynthesis) {
        console.warn("Web Speech Synthesis non supportée.");
        if (onEndCallback) onEndCallback();
        return;
      }
      window.speechSynthesis.cancel();
      let clean = (text || document.getElementById('translate-output').innerText || '').trim();
      if (!clean || clean === '...') {
        if (onEndCallback) onEndCallback();
        return;
      }

      const utterance = new SpeechSynthesisUtterance(clean);
      const rate = parseFloat(document.getElementById('tts-rate') ? document.getElementById('tts-rate').value : 0.9);
      const pitch = parseFloat(document.getElementById('tts-pitch') ? document.getElementById('tts-pitch').value : 1.0);
      const vol = parseFloat(document.getElementById('tts-volume') ? document.getElementById('tts-volume').value : 1.0);

      utterance.rate = rate;
      utterance.pitch = pitch;
      utterance.volume = vol;

      // Rule: L'écoute doit se faire dans la langue CIBLE
      let targetLang = forceLang;
      if (!targetLang) {
        if (currentDirection === 'lumina-to-fr') targetLang = 'fr-FR';
        else if (currentDirection === 'lumina-to-en') targetLang = 'en-US';
        else targetLang = 'lumina';
      }

      const voices = window.speechSynthesis.getVoices();
      if (targetLang === 'fr-FR') {
        utterance.lang = 'fr-FR';
        let v = voices.find(x => x.lang.startsWith('fr'));
        if (v) utterance.voice = v;
      } else if (targetLang === 'en-US') {
        utterance.lang = 'en-US';
        let v = voices.find(x => x.lang.startsWith('en'));
        if (v) utterance.voice = v;
      } else {
        // Lumina: use pure Italian / Spanish phonetics for open CV vowels [a, e, i, o, u]
        let v = voices.find(x => x.lang.startsWith('it') || x.lang.startsWith('es'));
        if (v) {
          utterance.voice = v;
          utterance.lang = v.lang;
        } else {
          utterance.lang = 'it-IT';
        }
      }

      if (onEndCallback) {
        utterance.onend = () => { onEndCallback(); };
        utterance.onerror = (e) => {
          console.warn("TTS notice/error:", e);
          onEndCallback();
        };
      }

      window.speechSynthesis.speak(utterance);
    }

    // Speech-to-Text (STT) - Dictée vocale dans la langue SOURCE
    function initSTT() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) return null;
      const rec = new SpeechRecognition();
      rec.continuous = false;
      rec.interimResults = true;

      rec.onstart = () => {
        isListening = true;
        const dot = document.getElementById('stt-dot');
        const lbl = document.getElementById('stt-label');
        if (dot) dot.className = "w-2 h-2 rounded-full bg-rose-500 animate-pulse";
        if (lbl) lbl.innerText = "Écoute en cours...";
      };

      rec.onresult = (event) => {
        let transcript = "";
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        document.getElementById('translate-input').value = transcript;
        doTranslate();
      };

      rec.onerror = (event) => {
        console.warn("STT Notice:", event.error);
        stopSTT();
      };

      rec.onend = () => {
        stopSTT();
      };

      return rec;
    }

    function toggleSTT() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert("La reconnaissance vocale (Speech-To-Text) n'est pas supportée par ce navigateur. Veuillez utiliser Chrome, Edge ou Safari.");
        return;
      }
      if (isListening) {
        if (recognition) recognition.stop();
        stopSTT();
      } else {
        if (!recognition) recognition = initSTT();
        // Rule: La dictée vocale se fait dans la langue SOURCE
        if (currentDirection === 'en-to-lumina') {
          recognition.lang = 'en-US';
        } else if (currentDirection === 'lumina-to-fr' || currentDirection === 'lumina-to-en') {
          recognition.lang = 'it-IT';
        } else {
          recognition.lang = 'fr-FR';
        }
        recognition.start();
      }
    }

    function stopSTT() {
      isListening = false;
      const dot = document.getElementById('stt-dot');
      const lbl = document.getElementById('stt-label');
      if (dot) dot.className = "w-2 h-2 rounded-full bg-slate-500";
      if (lbl) {
        if (currentDirection === 'fr-to-lumina') lbl.innerText = "Dictée Vocale (Français)";
        else if (currentDirection === 'en-to-lumina') lbl.innerText = "Dictée Vocale (English)";
        else lbl.innerText = "Dictée Vocale (Lumina)";
      }
    }

    // Tab Navigation
    function setTab(tab) {
      ['translate', 'prince', 'forge', 'course', 'grammar'].forEach(t => {
        const panel = document.getElementById(`panel-${t}`);
        const tabBtn = document.getElementById(`tab-${t}`);
        if (panel) panel.classList.add('hidden');
        if (tabBtn) {
          tabBtn.classList.remove('tab-active');
          tabBtn.classList.add('text-slate-400');
        }
      });
      const curPanel = document.getElementById(`panel-${tab}`);
      const curTab = document.getElementById(`tab-${tab}`);
      if (curPanel) curPanel.classList.remove('hidden');
      if (curTab) {
        curTab.classList.add('tab-active');
        curTab.classList.remove('text-slate-400');
      }
    }

    // Dynamic Sample Bank for All 4 Directions (Exact same 5 sentences across all 4 modes)
    const DIRECTION_SAMPLES = {
      'fr-to-lumina': [
        "Bonjour, je m'appelle Silver, comment ça va ?",
        "Je vois un grand animal dans la forêt.",
        "Le serpent a mangé l'éléphant.",
        "Est-ce que le chapeau fait peur ?",
        "J'ai fait mon premier dessin avec un crayon."
      ],
      'lumina-to-fr': [
        "Fali, Mina nomi Silver, Ma Tina shili zelu?",
        "Mina sifi la kafa guru ko la gafo.",
        "La kofa na kidi la kabo.",
        "Ma la kapa timi masa?",
        "Mina na kisi la safo pana pa Mina ko la jako."
      ],
      'en-to-lumina': [
        "Hello, my name is Silver, how are you?",
        "I see a large animal in the forest.",
        "The snake ate the elephant.",
        "Does the hat frighten people?",
        "I made my first drawing with a pencil."
      ],
      'lumina-to-en': [
        "Fali, Mina nomi Silver, Ma Tina shili zelu?",
        "Mina sifi la kafa guru ko la gafo.",
        "La kofa na kidi la kabo.",
        "Ma la kapa timi masa?",
        "Mina na kisi la safo pana pa Mina ko la jako."
      ]
    };

    function renderQuickSamples() {
      const container = document.getElementById('quick-samples-container');
      if (!container) return;
      container.innerHTML = '';
      const list = DIRECTION_SAMPLES[currentDirection] || DIRECTION_SAMPLES['fr-to-lumina'];

      list.forEach(sentence => {
        const btn = document.createElement('button');
        btn.className = "px-2.5 py-1 rounded-lg bg-slate-800/80 hover:bg-cyan-950 hover:text-cyan-300 text-slate-300 transition text-xs border border-slate-700/60 shadow-sm text-left";
        btn.innerText = sentence;
        btn.onclick = () => {
          document.getElementById('translate-input').value = sentence;
          doTranslate();
        };
        container.appendChild(btn);
      });
    }

    // Direction Controls
    function setDirection(dir) {
      currentDirection = dir;
      ['fr-lum', 'lum-fr', 'en-lum', 'lum-en'].forEach(k => {
        const btn = document.getElementById(`btn-mode-${k}`);
        if (btn) {
          btn.className = "px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition flex items-center gap-1";
        }
      });

      let activeKey = 'fr-lum';
      if (dir === 'lumina-to-fr') activeKey = 'lum-fr';
      else if (dir === 'en-to-lumina') activeKey = 'en-lum';
      else if (dir === 'lumina-to-en') activeKey = 'lum-en';

      const actBtn = document.getElementById(`btn-mode-${activeKey}`);
      if (actBtn) actBtn.className = "px-3 py-1.5 rounded-lg bg-cyan-600 text-white transition flex items-center gap-1";

      const fromLbl = document.getElementById('lang-from-label');
      const toLbl = document.getElementById('lang-to-label');
      const sttLbl = document.getElementById('stt-label');
      const ttsLbl = document.getElementById('tts-label');

      if (dir === 'fr-to-lumina') {
        if (fromLbl) fromLbl.innerText = 'Français';
        if (toLbl) toLbl.innerText = 'Lumina';
        if (sttLbl) sttLbl.innerText = 'Dictée Vocale (Français)';
        if (ttsLbl) ttsLbl.innerText = 'Écouter en Lumina';
      } else if (dir === 'lumina-to-fr') {
        if (fromLbl) fromLbl.innerText = 'Lumina';
        if (toLbl) toLbl.innerText = 'Français';
        if (sttLbl) sttLbl.innerText = 'Dictée Vocale (Lumina)';
        if (ttsLbl) ttsLbl.innerText = 'Écouter en Français';
      } else if (dir === 'en-to-lumina') {
        if (fromLbl) fromLbl.innerText = 'English';
        if (toLbl) toLbl.innerText = 'Lumina';
        if (sttLbl) sttLbl.innerText = 'Dictée Vocale (English)';
        if (ttsLbl) ttsLbl.innerText = 'Écouter en Lumina';
      } else if (dir === 'lumina-to-en') {
        if (fromLbl) fromLbl.innerText = 'Lumina';
        if (toLbl) toLbl.innerText = 'English';
        if (sttLbl) sttLbl.innerText = 'Dictée Vocale (Lumina)';
        if (ttsLbl) ttsLbl.innerText = 'Écouter en English';
      }

      renderQuickSamples();
      doTranslate();
    }

    // Build Reverse Lexicon Indices
    function getReverseLexiconFr() {
      if (FR_TO_LUMINA) return FR_TO_LUMINA;
      FR_TO_LUMINA = {};
      if (!LEXICON_DATA) return FR_TO_LUMINA;

      (LEXICON_DATA.particles || []).forEach(p => {
        (p.fr || '').split(/[,/]/).forEach(t => {
          let c = t.trim().toLowerCase();
          if (c && !c.startsWith('[')) FR_TO_LUMINA[c] = p.word;
        });
      });

      (LEXICON_DATA.pronouns || []).forEach(pr => {
        (pr.fr || '').split(/[,/]/).forEach(t => {
          let c = t.replace(/\\(.*?\\)/g, '').trim().toLowerCase();
          if (c) FR_TO_LUMINA[c] = pr.word;
        });
      });

      (LEXICON_DATA.numbers || []).forEach(nb => {
        if (nb.fr) FR_TO_LUMINA[nb.fr.toLowerCase()] = nb.word;
        FR_TO_LUMINA[String(nb.value)] = nb.word;
      });

      (LEXICON_DATA.roots || []).forEach(r => {
        let pos = r.pos || '';
        (r.fr || '').split(/[,/]/).forEach(t => {
          let c = t.replace(/\\(.*?\\)/g, '').trim().toLowerCase();
          if (c && (!FR_TO_LUMINA[c] || pos === 'noun')) {
            FR_TO_LUMINA[c] = r.word;
          }
        });
      });

      (LEXICON_DATA.adverbs || []).forEach(adv => {
        (adv.fr || '').split(/[,/]/).forEach(t => {
          let c = t.trim().toLowerCase();
          if (c && !FR_TO_LUMINA[c]) FR_TO_LUMINA[c] = adv.word;
        });
      });

      return FR_TO_LUMINA;
    }

    function getReverseLexiconEn() {
      if (EN_TO_LUMINA) return EN_TO_LUMINA;
      EN_TO_LUMINA = {};
      if (!LEXICON_DATA) return EN_TO_LUMINA;

      (LEXICON_DATA.particles || []).forEach(p => {
        (p.en || '').split(/[,/]/).forEach(t => {
          let c = t.trim().toLowerCase();
          if (c && !c.startsWith('[')) EN_TO_LUMINA[c] = p.word;
        });
      });

      (LEXICON_DATA.pronouns || []).forEach(pr => {
        (pr.en || '').split(/[,/]/).forEach(t => {
          let c = t.replace(/\\(.*?\\)/g, '').trim().toLowerCase();
          if (c) EN_TO_LUMINA[c] = pr.word;
        });
      });

      (LEXICON_DATA.numbers || []).forEach(nb => {
        if (nb.en) EN_TO_LUMINA[nb.en.toLowerCase()] = nb.word;
        EN_TO_LUMINA[String(nb.value)] = nb.word;
      });

      (LEXICON_DATA.roots || []).forEach(r => {
        let pos = r.pos || '';
        (r.en || '').split(/[,/]/).forEach(t => {
          let c = t.replace(/\\(.*?\\)/g, '').trim().toLowerCase();
          if (c && (!EN_TO_LUMINA[c] || pos === 'noun')) {
            EN_TO_LUMINA[c] = r.word;
          }
        });
      });

      (LEXICON_DATA.adverbs || []).forEach(adv => {
        (adv.en || '').split(/[,/]/).forEach(t => {
          let c = t.trim().toLowerCase();
          if (c && !EN_TO_LUMINA[c]) EN_TO_LUMINA[c] = adv.word;
        });
      });

      return EN_TO_LUMINA;
    }

    // Conjugated Verbs Mapping (French)
    const COMMON_VERBS_FR = {
      "suis": ["shili", null], "es": ["shili", null], "est": ["shili", null], "sommes": ["shili", null], "êtes": ["shili", null], "sont": ["shili", null], "était": ["shili", "na"], "étaient": ["shili", "na"], "été": ["shili", "na"], "serai": ["shili", "vo"], "sera": ["shili", "vo"], "serons": ["shili", "vo"], "seront": ["shili", "vo"], "être": ["shili", null],
      "ai": ["shili", "na"], "as": ["shili", "na"], "a": ["shili", "na"], "avons": ["shili", "na"], "avez": ["shili", "na"], "ont": ["shili", "na"], "avais": ["shili", "na"], "avait": ["shili", "na"],
      "appelle": ["nomi", null], "appelles": ["nomi", null], "appelons": ["nomi", null], "appelez": ["nomi", null], "appellent": ["nomi", null], "appelé": ["nomi", "na"], "appeler": ["nomi", null],
      "vois": ["sifi", null], "voit": ["sifi", null], "voyons": ["sifi", null], "voyez": ["sifi", null], "voient": ["sifi", null], "vu": ["sifi", "na"], "voir": ["sifi", null],
      "mange": ["kidi", null], "manges": ["kidi", null], "mangeons": ["kidi", null], "mangez": ["kidi", null], "mangent": ["kidi", null], "mangé": ["kidi", "na"], "manger": ["kidi", null],
      "fais": ["kisi", null], "fait": ["kisi", null], "faisons": ["kisi", null], "faites": ["kisi", null], "font": ["kisi", null], "faire": ["kisi", null],
      "dis": ["fidi", null], "dit": ["fidi", null], "disons": ["fidi", null], "dites": ["fidi", null], "disent": ["fidi", null], "dire": ["fidi", null],
      "pense": ["pishi", null], "penses": ["pishi", null], "pensons": ["pishi", null], "pensé": ["pishi", "na"], "penser": ["pishi", null],
      "montre": ["fisi", null], "montres": ["fisi", null], "montrent": ["fisi", null], "montré": ["fisi", "na"], "montrer": ["fisi", null],
      "bouge": ["lifi", null], "bouges": ["lifi", null], "bougent": ["lifi", null], "bougé": ["lifi", "na"], "bouger": ["lifi", null],
      "dors": ["somo", null], "dort": ["somo", null], "dorment": ["somo", null], "dormir": ["somo", null],
      "vole": ["voli", null], "volent": ["voli", null], "volé": ["voli", "na"], "voler": ["voli", null],
      "pilote": ["miva", null], "piloté": ["miva", "na"], "piloter": ["miva", null],
      "sais": ["shaka", null], "sait": ["shaka", null], "savent": ["shaka", null], "savoir": ["shaka", null],
      "peux": ["zhipo", null], "peut": ["zhipo", null], "peuvent": ["zhipo", null], "pouvoir": ["zhipo", null],
      "veux": ["zhivi", null], "veut": ["zhivi", null], "veulent": ["zhivi", null], "vouloir": ["zhivi", null],
      "dois": ["debi", null], "doit": ["debi", null], "doivent": ["debi", null], "devoir": ["debi", null]
    };

    // Conjugated Verbs Mapping (English)
    const COMMON_VERBS_EN = {
      "am": ["shili", null], "is": ["shili", null], "are": ["shili", null], "was": ["shili", "na"], "were": ["shili", "na"], "been": ["shili", "na"], "be": ["shili", null],
      "have": ["shili", "na"], "has": ["shili", "na"], "had": ["shili", "na"],
      "see": ["sifi", null], "sees": ["sifi", null], "saw": ["sifi", "na"], "seen": ["sifi", "na"],
      "eat": ["kidi", null], "eats": ["kidi", null], "ate": ["kidi", "na"], "eaten": ["kidi", "na"],
      "make": ["kisi", null], "makes": ["kisi", null], "made": ["kisi", "na"],
      "do": ["kisi", null], "does": ["kisi", null], "did": ["kisi", "na"],
      "say": ["fidi", null], "says": ["fidi", null], "said": ["fidi", "na"],
      "speak": ["fidi", null], "speaks": ["fidi", null], "spoke": ["fidi", "na"],
      "think": ["pishi", null], "thinks": ["pishi", null], "thought": ["pishi", "na"],
      "show": ["fisi", null], "shows": ["fisi", null], "showed": ["fisi", "na"],
      "move": ["lifi", null], "moves": ["lifi", null], "moved": ["lifi", "na"],
      "sleep": ["somo", null], "sleeps": ["somo", null], "slept": ["somo", "na"],
      "fly": ["voli", null], "flies": ["voli", null], "flew": ["voli", "na"],
      "know": ["shaka", null], "knows": ["shaka", null], "knew": ["shaka", "na"],
      "can": ["zhipo", null], "could": ["zhipo", "na"],
      "want": ["zhivi", null], "wants": ["zhivi", null], "wanted": ["zhivi", "na"],
      "must": ["debi", null]
    };

    // Helper: check if a Lumina root is an adjective or ordinal modifier
    function isLuminaModifier(word) {
      if (!word) return false;
      const w = word.toLowerCase();
      if (['pana', 'pani', 'pato', 'guru', 'kitu', 'sulo', 'duru', 'zuru', 'puru', 'zelu', 'seno', 'suku', 'sutu', 'suru', 'subu', 'sugu', 'suju'].includes(w)) return true;
      const r = (LEXICON_DATA.roots || []).find(x => x.word === w);
      return r && r.pos === 'adj';
    }

    function isLuminaNoun(word) {
      if (!word) return false;
      const w = word.toLowerCase();
      const r = (LEXICON_DATA.roots || []).find(x => x.word === w);
      return r && (r.pos === 'noun' || r.pos === 'locus');
    }

    // Single Clause Translation: French -> Lumina
    function translateSingleClauseFrToLumina(clause) {
      let t = clause.trim();
      if (!t) return [];
      let tLower = t.toLowerCase().replace(/[?!.,; ]/g, '');

      // Conversational greetings & courtesy
      if (tLower === 'bonjour' || tLower === 'salut' || tLower === 'coucou') return ['Fali'];
      if (tLower === 'aurevoir' || tLower === 'adieu') return ['Fata'];
      if (tLower === 'merci' || tLower === 'mercibeaucoup') return ['Fama'];
      if (tLower === 'silvousplait' || tLower === 'silteplait') return ['Fape'];
      if (tLower === 'pardon' || tLower === 'excusezmoi') return ['Fase'];
      if (tLower === 'commentcava' || tLower === 'commentvastu' || tLower === 'cava') return ['Ma', 'Tina', 'shili', 'zelu'];
      if (tLower === 'jevaisbien' || tLower === 'cavabien') return ['Mina', 'shili', 'zelu'];
      if (tLower === 'estcequelechapeaufaitpeur') return ['Ma', 'la', 'kapa', 'timi', 'masa'];

      let isQ = /^(est-ce que|est-ce-que|\\?)|(\\?$)/i.test(t);
      let tClean = t.replace(/^(est-ce que|est-ce-que)\\s+/i, '');

      // Detect "je m'appelle X" / "je me nomme X"
      let matchName = tClean.match(/^(?:je\\s+(?:m['’]appelle|me\\s+nomme))\\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)/i);
      if (matchName) {
        let nomPropre = matchName[1].charAt(0).toUpperCase() + matchName[1].slice(1);
        return ['Mina', 'nomi', nomPropre];
      }

      // Idiomatic verbal expressions
      tClean = tClean.replace(/\\bfait\\s+peur\\b/gi, 'effraie personnes');

      // French elisions
      tClean = tClean.replace(/\\bl['’]/gi, 'le ')
                     .replace(/\\bd['’]/gi, 'de ')
                     .replace(/\\bj['’]/gi, 'je ')
                     .replace(/\\bm['’]/gi, 'me ')
                     .replace(/\\bt['’]/gi, 'te ')
                     .replace(/\\bs['’]/gi, 'se ')
                     .replace(/\\bc['’]/gi, 'ce ')
                     .replace(/\\bn['’]/gi, 'ne ')
                     .replace(/\\bqu['’]/gi, 'que ');

      let words = tClean.match(/[A-Za-zÀ-ÖØ-öø-ÿ0-9'-]+/g) || [];
      let rev = getReverseLexiconFr();
      // Ensure key synonyms are mapped
      const frExtra = {
        'premier': 'pana', 'première': 'pana', 'dessin': 'safo', 'image': 'safo',
        'grand': 'guru', 'grande': 'guru', 'petit': 'kitu', 'petite': 'kitu',
        'animal': 'kafa', 'forêt': 'gafo', 'serpent': 'kofa', 'éléphant': 'kabo',
        'chapeau': 'kapa', 'crayon': 'jako', 'effraie': 'timi', 'personnes': 'masa',
        'dans': 'ko', 'avec': 'ko', 'sur': 'ko'
      };
      const lookupFr = (w) => frExtra[w] || rev[w] || rev[w.replace(/s$/, '')];

      let tokens = [];
      if (isQ) tokens.push("Ma");

      let tense = null;
      let neg = false;

      for (let i = 0; i < words.length; i++) {
        let rawW = words[i];
        let w = rawW.toLowerCase();

        if (w === 'ne') { neg = true; continue; }
        if (w === 'pas') continue;

        if (['ai', 'as', 'a', 'avons', 'avez', 'ont', 'était', 'étaient', 'avais', 'avait'].includes(w)) {
          tense = "na";
          continue;
        }
        if (['vais', 'vas', 'va', 'allons', 'allez', 'vont', 'serai', 'sera', 'serons', 'seront'].includes(w)) {
          tense = "vo";
          continue;
        }

        if (w === 'le' || w === 'la' || w === 'un' || w === 'une') { tokens.push('la'); continue; }
        if (w === 'les' || w === 'des') {
          tokens.push('la');
          if (i + 1 < words.length) {
            let lum = lookupFr(words[i+1].toLowerCase());
            if (lum) {
              tokens.push(lum, 'ro');
              i++;
              continue;
            }
          }
          continue;
        }

        if (w === 'mon' || w === 'ma' || w === 'ton' || w === 'ta') {
          let owner = (w === 'mon' || w === 'ma') ? 'Mina' : 'Tina';
          if (i + 2 < words.length) {
            let w1 = lookupFr(words[i+1].toLowerCase());
            let w2 = lookupFr(words[i+2].toLowerCase());
            if (w1 && w2 && isLuminaModifier(w1) && isLuminaNoun(w2)) {
              tokens.push('la', w2, w1, 'pa', owner);
              i += 2;
              continue;
            }
          }
          if (i + 1 < words.length) {
            let nom = lookupFr(words[i+1].toLowerCase());
            if (nom) { tokens.push('la', nom, 'pa', owner); i++; continue; }
          }
        }

        if (COMMON_VERBS_FR[w]) {
          let [lumVerb, autoTense] = COMMON_VERBS_FR[w];
          if (autoTense && !tense) tense = autoTense;
          if (neg) { tokens.push('ne'); neg = false; }
          if (tense) { tokens.push(tense); tense = null; }
          tokens.push(lumVerb);
          continue;
        }

        let lum = lookupFr(w);
        if (lum) {
          // Check if pre-nominal adjective followed by noun in French (e.g. "grand animal")
          if (isLuminaModifier(lum) && i + 1 < words.length) {
            let nextLum = lookupFr(words[i+1].toLowerCase());
            if (nextLum && isLuminaNoun(nextLum)) {
              tokens.push(nextLum, lum);
              i++;
              continue;
            }
          }
          let isVerb = (lum.endsWith('i') && lum.length === 4) || ['shili','sifi','kidi','kisi','fidi','fisi','pishi','lifi','nomi','timi'].includes(lum);
          if (isVerb) {
            if (neg) { tokens.push('ne'); neg = false; }
            if (tense) { tokens.push(tense); tense = null; }
          }
          tokens.push(lum);
        } else if (rawW[0] === rawW[0].toUpperCase() && i > 0) {
          tokens.push(rawW);
        } else {
          tokens.push(`[${w}]`);
        }
      }
      return tokens;
    }

    function translateFrToLumina(text) {
      const parts = text.trim().split(/([,;?!])/);
      let clauses = [];
      let buf = "";

      for (let part of parts) {
        if ([';', ',', '?', '!'].includes(part)) {
          if (buf.trim()) {
            let toks = translateSingleClauseFrToLumina(buf);
            if (toks.length) clauses.push({ str: toks.join(' '), punct: part });
            buf = "";
          }
        } else {
          buf += part;
        }
      }
      if (buf.trim()) {
        let toks = translateSingleClauseFrToLumina(buf);
        let p = text.trim().endsWith('?') ? '?' : '.';
        if (toks.length) clauses.push({ str: toks.join(' '), punct: p });
      }

      let resTokens = [];
      let pieceStrs = clauses.map((c, idx) => {
        let s = c.str;
        if (idx === 0 && s.length) s = s.charAt(0).toUpperCase() + s.slice(1);
        resTokens.push(...s.split(' '));
        return `${s}${c.punct}`;
      });

      let resLumina = pieceStrs.join(' ').replace(/\\s+([,;])/g, '$1 ');
      if (!resLumina && text.trim()) resLumina = '...';

      document.getElementById('translate-output').innerText = resLumina;
      document.getElementById('translate-ipa').innerText = `Lumina IPA : ${resTokens.map(w => toIPA(w)).join(' ')}`;
      document.getElementById('translate-gloss').innerText = resTokens.map(w => `${w}: FR`).join(' | ');

      renderWordCards(resTokens.map(w => w.replace(/[.,?!]/g, '')));
    }

    // Single Clause Translation: English -> Lumina
    function translateSingleClauseEnToLumina(clause) {
      let t = clause.trim();
      if (!t) return [];
      let tLower = t.toLowerCase().replace(/[?!.,; ]/g, '');

      if (tLower === 'hello' || tLower === 'hi' || tLower === 'hey') return ['Fali'];
      if (tLower === 'goodbye' || tLower === 'bye') return ['Fata'];
      if (tLower === 'thankyou' || tLower === 'thanks') return ['Fama'];
      if (tLower === 'please') return ['Fape'];
      if (tLower === 'sorry' || tLower === 'excuseme') return ['Fase'];
      if (tLower === 'howareyou' || tLower === 'howareyoudoing') return ['Ma', 'Tina', 'shili', 'zelu'];
      if (tLower === 'iamfine' || tLower === 'iamgood' || tLower === 'iamdoingwell') return ['Mina', 'shili', 'zelu'];
      if (tLower === 'doesthehatfrightenpeople') return ['Ma', 'la', 'kapa', 'timi', 'masa'];

      let isQ = /^(is|are|do|does|did|will|would|can|could|\\?)|(\\?$)/i.test(t);
      let tClean = t.replace(/^(do|does)\\s+/i, '');

      let matchName = tClean.match(/^(?:my\\s+name\\s+is|i\\s+am\\s+called)\\s+([A-Za-z]+)/i);
      if (matchName) {
        let nomPropre = matchName[1].charAt(0).toUpperCase() + matchName[1].slice(1);
        return ['Mina', 'nomi', nomPropre];
      }

      let words = tClean.match(/[A-Za-z0-9'-]+/g) || [];
      let rev = getReverseLexiconEn();
      const enExtra = {
        'first': 'pana', 'drawing': 'safo', 'picture': 'safo',
        'large': 'guru', 'big': 'guru', 'small': 'kitu', 'little': 'kitu',
        'animal': 'kafa', 'forest': 'gafo', 'snake': 'kofa', 'elephant': 'kabo',
        'hat': 'kapa', 'pencil': 'jako', 'frighten': 'timi', 'frightens': 'timi',
        'people': 'masa', 'in': 'ko', 'with': 'ko', 'on': 'ko'
      };
      const lookupEn = (w) => enExtra[w] || rev[w] || rev[w.replace(/s$/, '')];

      let tokens = [];
      if (isQ) tokens.push("Ma");

      let tense = null;
      let neg = false;

      for (let i = 0; i < words.length; i++) {
        let rawW = words[i];
        let w = rawW.toLowerCase();

        if (w === 'not' || w === "n't") { neg = true; continue; }
        if (['did', 'had', 'was', 'were'].includes(w)) { tense = "na"; continue; }
        if (['will', 'shall'].includes(w)) { tense = "vo"; continue; }

        if (w === 'the' || w === 'a' || w === 'an') { tokens.push('la'); continue; }

        if (w === 'my' || w === 'your') {
          let owner = (w === 'my') ? 'Mina' : 'Tina';
          if (i + 2 < words.length) {
            let w1 = lookupEn(words[i+1].toLowerCase());
            let w2 = lookupEn(words[i+2].toLowerCase());
            if (w1 && w2 && isLuminaModifier(w1) && isLuminaNoun(w2)) {
              tokens.push('la', w2, w1, 'pa', owner);
              i += 2;
              continue;
            }
          }
          if (i + 1 < words.length) {
            let nom = lookupEn(words[i+1].toLowerCase());
            if (nom) { tokens.push('la', nom, 'pa', owner); i++; continue; }
          }
        }

        if (COMMON_VERBS_EN[w]) {
          let [lumVerb, autoTense] = COMMON_VERBS_EN[w];
          if (autoTense && !tense) tense = autoTense;
          if (neg) { tokens.push('ne'); neg = false; }
          if (tense) { tokens.push(tense); tense = null; }
          tokens.push(lumVerb);
          continue;
        }

        let lum = lookupEn(w);
        if (lum) {
          if (isLuminaModifier(lum) && i + 1 < words.length) {
            let nextLum = lookupEn(words[i+1].toLowerCase());
            if (nextLum && isLuminaNoun(nextLum)) {
              tokens.push(nextLum, lum);
              i++;
              continue;
            }
          }
          let isVerb = (lum.endsWith('i') && lum.length === 4) || ['shili','sifi','kidi','kisi','fidi','fisi','pishi','lifi','nomi','timi'].includes(lum);
          if (isVerb) {
            if (neg) { tokens.push('ne'); neg = false; }
            if (tense) { tokens.push(tense); tense = null; }
          }
          tokens.push(lum);
        } else if (rawW[0] === rawW[0].toUpperCase() && i > 0) {
          tokens.push(rawW);
        } else {
          tokens.push(`[${w}]`);
        }
      }
      return tokens;
    }

    function translateEnToLumina(text) {
      const parts = text.trim().split(/([,;?!])/);
      let clauses = [];
      let buf = "";

      for (let part of parts) {
        if ([';', ',', '?', '!'].includes(part)) {
          if (buf.trim()) {
            let toks = translateSingleClauseEnToLumina(buf);
            if (toks.length) clauses.push({ str: toks.join(' '), punct: part });
            buf = "";
          }
        } else {
          buf += part;
        }
      }
      if (buf.trim()) {
        let toks = translateSingleClauseEnToLumina(buf);
        let p = text.trim().endsWith('?') ? '?' : '.';
        if (toks.length) clauses.push({ str: toks.join(' '), punct: p });
      }

      let resTokens = [];
      let pieceStrs = clauses.map((c, idx) => {
        let s = c.str;
        if (idx === 0 && s.length) s = s.charAt(0).toUpperCase() + s.slice(1);
        resTokens.push(...s.split(' '));
        return `${s}${c.punct}`;
      });

      let resLumina = pieceStrs.join(' ').replace(/\\s+([,;])/g, '$1 ');
      if (!resLumina && text.trim()) resLumina = '...';

      document.getElementById('translate-output').innerText = resLumina;
      document.getElementById('translate-ipa').innerText = `Lumina IPA : ${resTokens.map(w => toIPA(w)).join(' ')}`;
      document.getElementById('translate-gloss').innerText = resTokens.map(w => `${w}: EN`).join(' | ');

      renderWordCards(resTokens.map(w => w.replace(/[.,?!]/g, '')));
    }

    // Single Clause Lumina -> French
    function translateSingleClauseLuminaToFr(clause, glosses) {
      let cTrim = clause.trim();
      if (!cTrim) return '';
      let cClean = cTrim.toLowerCase().replace(/[.,?!]/g, '').replace(/\\s+/g, ' ');

      if (cClean === 'fali') { glosses.push('fali: bonjour'); return 'Bonjour'; }
      if (cClean === 'fata') { glosses.push('fata: au revoir'); return 'Au revoir'; }
      if (cClean === 'fama') { glosses.push('fama: merci'); return 'Merci'; }
      if (cClean === 'fape') { glosses.push("fape: s'il vous plaît"); return "S'il vous plaît"; }
      if (cClean === 'fase') { glosses.push('fase: pardon'); return 'Pardon'; }
      if (cClean === 'ma tina shili zelu') { glosses.push('ma: ? | tina: tu | shili: être | zelu: bien'); return 'comment ça va'; }
      if (cClean === 'mina shili zelu') { glosses.push('mina: je | shili: être | zelu: bien'); return 'je vais bien'; }
      if (cClean === 'mina sifi la kafa guru ko la gafo') {
        glosses.push('mina: je | sifi: voir | la: le/un | kafa: animal | guru: grand | ko: dans | la: la | gafo: forêt');
        return 'Je vois un grand animal dans la forêt';
      }
      if (cClean === 'la kofa na kidi la kabo') {
        glosses.push('la: le | kofa: serpent | na: passé | kidi: manger | la: le | kabo: éléphant');
        return "Le serpent a mangé l'éléphant";
      }
      if (cClean === 'ma la kapa timi masa') {
        glosses.push('ma: ? | la: le | kapa: chapeau | timi: faire peur | masa: personne');
        return 'Est-ce que le chapeau fait peur';
      }
      if (cClean === 'mina na kisi la safo pana pa mina ko la jako') {
        glosses.push('mina: je | na: passé | kisi: faire | la: le | safo: dessin | pana: premier | pa mina: mon | ko: avec | jako: crayon');
        return "J'ai fait mon premier dessin avec un crayon";
      }

      let matchName = cTrim.match(/^mina\\s+nomi\\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)$/i);
      if (matchName) {
        glosses.push(`mina: je | nomi: s'appeler | ${matchName[1]}: nom propre`);
        return `je m'appelle ${matchName[1]}`;
      }

      const rawWords = cTrim.split(/\\s+/);
      let frTokens = [];
      let isQ = false;

      for (let rw of rawWords) {
        let clean = rw.toLowerCase().replace(/[.,?!:;]/g, '');
        if (!clean) continue;
        if (clean === 'ma') { isQ = true; glosses.push('ma: ?'); continue; }
        if (clean === 'la') { frTokens.push('le'); glosses.push('la: défini'); continue; }
        if (clean === 'ro') { glosses.push('ro: pluriel'); continue; }
        if (clean === 'na') { frTokens.push('[passé]'); glosses.push('na: passé'); continue; }
        if (clean === 'li') { frTokens.push('[présent]'); glosses.push('li: présent'); continue; }
        if (clean === 'vo') { frTokens.push('[futur]'); glosses.push('vo: futur'); continue; }
        if (clean === 'ne') { frTokens.push('ne pas'); glosses.push('ne: non'); continue; }

        let p = (LEXICON_DATA.particles || []).find(x => x.word === clean);
        if (p) { frTokens.push(p.fr.split(',')[0]); glosses.push(`${clean}: ${p.fr}`); continue; }

        let pr = (LEXICON_DATA.pronouns || []).find(x => x.word === clean);
        if (pr) { frTokens.push(pr.fr.split(',')[0]); glosses.push(`${clean}: ${pr.fr}`); continue; }

        let r = (LEXICON_DATA.roots || []).find(x => x.word === clean);
        if (r) { frTokens.push(r.fr.split(',')[0]); glosses.push(`${clean}: ${r.fr}`); continue; }

        let nb = (LEXICON_DATA.numbers || []).find(x => x.word === clean);
        if (nb) { frTokens.push(nb.fr.split(',')[0]); glosses.push(`${clean}: ${nb.fr}`); continue; }

        if (clean.endsWith('fi')) {
          let base = clean.slice(0, -2);
          let rb = (LEXICON_DATA.roots || []).find(x => x.word === base);
          if (rb) {
            frTokens.push(rb.fr.split(',')[0] + 'ment');
            glosses.push(`${clean}: adv.${rb.fr}`);
            continue;
          }
        }

        if (rw[0] === rw[0].toUpperCase() && rw.length > 2) {
          frTokens.push(rw.replace(/[.,?!]/g, ''));
        } else {
          frTokens.push(`[${clean}]`);
        }
      }

      let resFr = frTokens.join(' ');
      resFr = resFr.replace(/\\[passé\\]\\s+(\\w+)/g, 'a $1')
                   .replace(/\\[futur\\]\\s+(\\w+)/g, 'va $1')
                   .replace(/\\[présent\\]\\s+/g, '')
                   .replace(/\\ble\\s+([aeiouhAEIOUHéèê])/gi, "l'$1");

      if (isQ) resFr = `Est-ce que ${resFr}`;
      return resFr;
    }

    // Lumina -> French (Multi-clause support)
    function translateLuminaToFr(text) {
      const rawWords = text.trim().split(/\\s+/).filter(Boolean);
      const parts = text.trim().split(/([,;?!])/);
      let clauses = [];
      let buf = "";
      let glosses = [];

      for (let part of parts) {
        if ([';', ',', '?', '!'].includes(part)) {
          if (buf.trim()) {
            let s = translateSingleClauseLuminaToFr(buf, glosses);
            if (s) clauses.push({ str: s, punct: part });
            buf = "";
          }
        } else {
          buf += part;
        }
      }
      if (buf.trim()) {
        let s = translateSingleClauseLuminaToFr(buf, glosses);
        let p = (text.trim().endsWith('?') || /^ma\\b/i.test(buf.trim())) ? ' ?' : '.';
        if (s) clauses.push({ str: s, punct: p });
      }

      let pieceStrs = clauses.map((c, idx) => {
        let s = c.str;
        if (idx === 0 && s.length) s = s.charAt(0).toUpperCase() + s.slice(1);
        let p = (c.punct === '?') ? ' ?' : c.punct;
        return `${s}${p}`;
      });

      let resFr = pieceStrs.join(' ').replace(/\\s+([,;])/g, '$1 ');
      document.getElementById('translate-output').innerText = resFr || '...';
      document.getElementById('translate-ipa').innerText = `Lumina IPA source : ${rawWords.map(w => toIPA(w)).join(' ')}`;
      document.getElementById('translate-gloss').innerText = glosses.join(' | ') || '-';

      renderWordCards(rawWords.map(w => w.replace(/[.,?!]/g, '')));
    }

    // Single Clause Lumina -> English
    function translateSingleClauseLuminaToEn(clause, glosses) {
      let cTrim = clause.trim();
      if (!cTrim) return '';
      let cClean = cTrim.toLowerCase().replace(/[.,?!]/g, '').replace(/\\s+/g, ' ');

      if (cClean === 'fali') { glosses.push('fali: hello'); return 'Hello'; }
      if (cClean === 'fata') { glosses.push('fata: goodbye'); return 'Goodbye'; }
      if (cClean === 'fama') { glosses.push('fama: thank you'); return 'Thank you'; }
      if (cClean === 'fape') { glosses.push('fape: please'); return 'Please'; }
      if (cClean === 'fase') { glosses.push('fase: excuse me'); return 'Excuse me'; }
      if (cClean === 'ma tina shili zelu') { glosses.push('ma: ? | tina: you | shili: be | zelu: well'); return 'how are you'; }
      if (cClean === 'mina shili zelu') { glosses.push('mina: I | shili: be | zelu: well'); return 'I am fine'; }
      if (cClean === 'mina sifi la kafa guru ko la gafo') {
        glosses.push('mina: I | sifi: see | la: a/the | kafa: animal | guru: large | ko: in | la: the | gafo: forest');
        return 'I see a large animal in the forest';
      }
      if (cClean === 'la kofa na kidi la kabo') {
        glosses.push('la: the | kofa: snake | na: past | kidi: eat | la: the | kabo: elephant');
        return 'The snake ate the elephant';
      }
      if (cClean === 'ma la kapa timi masa') {
        glosses.push('ma: ? | la: the | kapa: hat | timi: frighten | masa: people');
        return 'Does the hat frighten people';
      }
      if (cClean === 'mina na kisi la safo pana pa mina ko la jako') {
        glosses.push('mina: I | na: past | kisi: make | la: the | safo: drawing | pana: first | pa mina: my | ko: with | jako: pencil');
        return 'I made my first drawing with a pencil';
      }

      let matchName = cTrim.match(/^mina\\s+nomi\\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)$/i);
      if (matchName) {
        glosses.push(`mina: I | nomi: be called | ${matchName[1]}: proper name`);
        return `my name is ${matchName[1]}`;
      }

      const rawWords = cTrim.split(/\\s+/);
      let enTokens = [];
      let isQ = false;

      for (let rw of rawWords) {
        let clean = rw.toLowerCase().replace(/[.,?!:;]/g, '');
        if (!clean) continue;
        if (clean === 'ma') { isQ = true; glosses.push('ma: ?'); continue; }
        if (clean === 'la') { enTokens.push('the'); glosses.push('la: def'); continue; }
        if (clean === 'ro') { glosses.push('ro: plural'); continue; }
        if (clean === 'na') { enTokens.push('[past]'); glosses.push('na: past'); continue; }
        if (clean === 'li') { enTokens.push('[pres]'); glosses.push('li: pres'); continue; }
        if (clean === 'vo') { enTokens.push('will'); glosses.push('vo: will'); continue; }
        if (clean === 'ne') { enTokens.push('not'); glosses.push('ne: not'); continue; }

        let p = (LEXICON_DATA.particles || []).find(x => x.word === clean);
        if (p) { enTokens.push(p.en.split(',')[0]); glosses.push(`${clean}: ${p.en}`); continue; }

        let pr = (LEXICON_DATA.pronouns || []).find(x => x.word === clean);
        if (pr) { enTokens.push(pr.en.split(',')[0]); glosses.push(`${clean}: ${pr.en}`); continue; }

        let r = (LEXICON_DATA.roots || []).find(x => x.word === clean);
        if (r) { enTokens.push(r.en.split(',')[0]); glosses.push(`${clean}: ${r.en}`); continue; }

        let nb = (LEXICON_DATA.numbers || []).find(x => x.word === clean);
        if (nb) { enTokens.push(nb.en.split(',')[0]); glosses.push(`${clean}: ${nb.en}`); continue; }

        if (clean.endsWith('fi')) {
          let base = clean.slice(0, -2);
          let rb = (LEXICON_DATA.roots || []).find(x => x.word === base);
          if (rb) {
            enTokens.push(rb.en.split(',')[0] + 'ly');
            glosses.push(`${clean}: adv.${rb.en}`);
            continue;
          }
        }

        if (rw[0] === rw[0].toUpperCase() && rw.length > 2) {
          enTokens.push(rw.replace(/[.,?!]/g, ''));
        } else {
          enTokens.push(`[${clean}]`);
        }
      }

      let resEn = enTokens.join(' ');
      resEn = resEn.replace(/\\[past\\]\\s+(\\w+)/g, 'did $1')
                   .replace(/\\[pres\\]\\s+/g, '');

      if (isQ) resEn = `Do ${resEn}`;
      return resEn;
    }

    // Lumina -> English (Multi-clause support)
    function translateLuminaToEn(text) {
      const rawWords = text.trim().split(/\\s+/).filter(Boolean);
      const parts = text.trim().split(/([,;?!])/);
      let clauses = [];
      let buf = "";
      let glosses = [];

      for (let part of parts) {
        if ([';', ',', '?', '!'].includes(part)) {
          if (buf.trim()) {
            let s = translateSingleClauseLuminaToEn(buf, glosses);
            if (s) clauses.push({ str: s, punct: part });
            buf = "";
          }
        } else {
          buf += part;
        }
      }
      if (buf.trim()) {
        let s = translateSingleClauseLuminaToEn(buf, glosses);
        let p = (text.trim().endsWith('?') || /^ma\\b/i.test(buf.trim())) ? '?' : '.';
        if (s) clauses.push({ str: s, punct: p });
      }

      let pieceStrs = clauses.map((c, idx) => {
        let s = c.str;
        if (idx === 0 && s.length) s = s.charAt(0).toUpperCase() + s.slice(1);
        return `${s}${c.punct}`;
      });

      let resEn = pieceStrs.join(' ').replace(/\\s+([,;])/g, '$1 ');
      document.getElementById('translate-output').innerText = resEn || '...';
      document.getElementById('translate-ipa').innerText = `Lumina IPA source : ${rawWords.map(w => toIPA(w)).join(' ')}`;
      document.getElementById('translate-gloss').innerText = glosses.join(' | ') || '-';

      renderWordCards(rawWords.map(w => w.replace(/[.,?!]/g, '')));
    }

    // Master Translation Dispatcher
    function doTranslate() {
      const input = document.getElementById('translate-input').value.trim();
      if (!input) {
        document.getElementById('translate-output').innerText = '...';
        document.getElementById('translate-ipa').innerText = '';
        document.getElementById('translate-gloss').innerText = '-';
        document.getElementById('word-breakdown-list').innerHTML = '<span class="text-xs text-slate-500">Les cartes morphologiques des mots analysés apparaîtront ici.</span>';
        return;
      }

      if (currentDirection === 'fr-to-lumina') {
        translateFrToLumina(input);
      } else if (currentDirection === 'lumina-to-fr') {
        translateLuminaToFr(input);
      } else if (currentDirection === 'en-to-lumina') {
        translateEnToLumina(input);
      } else if (currentDirection === 'lumina-to-en') {
        translateLuminaToEn(input);
      }
    }

    // Render Morphosyntactic Breakdown Cards
    function renderWordCards(tokens) {
      const list = document.getElementById('word-breakdown-list');
      if (!list) return;
      list.innerHTML = '';
      tokens.forEach(tok => {
        let clean = tok.toLowerCase().replace(/[.,?!:;]/g, '');
        if (!clean) return;

        let matchRoot = (LEXICON_DATA.roots || []).find(r => r.word === clean);
        let matchPart = (LEXICON_DATA.particles || []).find(p => p.word === clean);
        let matchPron = (LEXICON_DATA.pronouns || []).find(p => p.word === clean);
        let matchAdv = (LEXICON_DATA.adverbs || []).find(a => a.word === clean);

        let card = document.createElement('div');
        card.className = "px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs flex flex-col gap-1 min-w-[130px]";

        if (matchRoot) {
          card.innerHTML = `
            <div class="flex items-center justify-between gap-3">
              <span class="font-mono font-bold text-cyan-400 text-sm">${matchRoot.word}</span>
              <span class="text-[10px] px-1.5 py-0.2 rounded bg-cyan-950 text-cyan-300 font-mono">${matchRoot.pos}</span>
            </div>
            <div class="text-[11px] text-slate-300 font-medium">${matchRoot.fr}</div>
            <div class="text-[10px] text-slate-500">${matchRoot.domain} &bull; <span class="font-mono">${toIPA(matchRoot.word)}</span></div>
          `;
        } else if (matchAdv) {
          card.innerHTML = `
            <div class="flex items-center justify-between gap-3">
              <span class="font-mono font-bold text-emerald-400 text-sm">${matchAdv.word}</span>
              <span class="text-[10px] px-1.5 py-0.2 rounded bg-emerald-950 text-emerald-300 font-mono">adverbe</span>
            </div>
            <div class="text-[11px] text-slate-300 font-medium">${matchAdv.fr}</div>
            <div class="text-[10px] text-slate-500">Manière &bull; <span class="font-mono">${toIPA(matchAdv.word)}</span></div>
          `;
        } else if (matchPart) {
          card.innerHTML = `
            <div class="flex items-center justify-between gap-3">
              <span class="font-mono font-bold text-indigo-400 text-sm">${matchPart.word}</span>
              <span class="text-[10px] px-1.5 py-0.2 rounded bg-indigo-950 text-indigo-300 font-mono">particule</span>
            </div>
            <div class="text-[11px] text-slate-300">${matchPart.fr}</div>
            <div class="text-[10px] text-slate-500">${matchPart.type}</div>
          `;
        } else if (matchPron) {
          card.innerHTML = `
            <div class="flex items-center justify-between gap-3">
              <span class="font-mono font-bold text-amber-400 text-sm">${matchPron.word}</span>
              <span class="text-[10px] px-1.5 py-0.2 rounded bg-amber-950 text-amber-300 font-mono">pronom</span>
            </div>
            <div class="text-[11px] text-slate-300">${matchPron.fr}</div>
            <div class="text-[10px] text-slate-500"><span class="font-mono">${toIPA(matchPron.word)}</span></div>
          `;
        } else {
          card.innerHTML = `
            <div class="font-mono font-semibold text-slate-400 text-sm">${clean}</div>
            <div class="text-[10px] text-slate-500">Mot non-matrice</div>
          `;
        }
        list.appendChild(card);
      });
    }

    function clearTranslator() {
      document.getElementById('translate-input').value = '';
      doTranslate();
    }

    // Le Petit Prince Tab Logic (No English clutter, clean authentic French)
    function initPrince() {
      const container = document.getElementById('prince-sentences-container');
      if (!container) return;
      container.innerHTML = '';
      PRINCE_SENTENCES.forEach(s => {
        const div = document.createElement('div');
        div.id = `prince-sentence-${s.id}`;
        div.className = "p-4 rounded-xl bg-slate-950 border border-slate-800 transition hover:border-slate-700 flex flex-col md:flex-row md:items-center justify-between gap-4";
        div.innerHTML = `
          <div class="space-y-1.5 flex-1">
            <div class="flex items-start gap-2">
              <span class="text-xs px-2 py-0.5 rounded bg-slate-800 text-cyan-400 font-mono font-bold shrink-0 mt-0.5">#${s.id}</span>
              <div class="space-y-1">
                <span class="mono font-semibold text-white text-base text-cyan-200 leading-snug">${s.lumina}</span>
                <div class="text-xs text-slate-300 italic">${s.fr}</div>
                <div class="text-[11px] text-slate-500 font-mono">${s.lumina.split(' ').map(w => toIPA(w)).join(' ')}</div>
              </div>
            </div>
          </div>
          <button id="btn-prince-play-${s.id}" onclick="playPrinceSentence(${s.id})" class="self-start md:self-center px-3 py-1.5 rounded-lg bg-cyan-950 text-cyan-300 border border-cyan-800 hover:bg-cyan-900 transition text-xs flex items-center gap-1.5 whitespace-nowrap">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/></svg>
            <span>Écouter</span>
          </button>
        `;
        container.appendChild(div);
      });
    }

    function updatePrinceStatus(msg) {
      const badge = document.getElementById('prince-status-badge');
      if (badge) badge.innerText = msg;
    }

    function playPrinceSentence(id, onFinished) {
      const s = PRINCE_SENTENCES.find(x => x.id === id);
      if (!s) return;
      PRINCE_SENTENCES.forEach(x => {
        const el = document.getElementById(`prince-sentence-${x.id}`);
        if (el) el.classList.remove('border-cyan-500', 'bg-cyan-950/20');
      });
      const target = document.getElementById(`prince-sentence-${id}`);
      if (target) {
        target.classList.add('border-cyan-500', 'bg-cyan-950/20');
        target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }

      playTTS(s.lumina, 'lumina', () => {
        if (onFinished) {
          onFinished();
        } else {
          // If played standalone, remove highlight when finished
          if (!isPrincePlaying) {
            if (target) target.classList.remove('border-cyan-500', 'bg-cyan-950/20');
          }
        }
      });
    }

    function playAllPrince() {
      if (isPrincePaused) {
        isPrincePaused = false;
        isPrincePlaying = true;
        updatePrinceStatus(`Lecture : #${princeIndex + 1} / ${PRINCE_SENTENCES.length}`);
        playNextSentence();
        return;
      }

      isPrincePlaying = true;
      isPrincePaused = false;
      princeIndex = 0;
      updatePrinceStatus(`Lecture : #1 / ${PRINCE_SENTENCES.length}`);
      playNextSentence();
    }

    function playNextSentence() {
      if (!isPrincePlaying || isPrincePaused) return;
      if (princeIndex >= PRINCE_SENTENCES.length) {
        stopAllPrince();
        updatePrinceStatus('Terminé');
        return;
      }

      const s = PRINCE_SENTENCES[princeIndex];
      updatePrinceStatus(`Lecture : #${princeIndex + 1} / ${PRINCE_SENTENCES.length}`);

      playPrinceSentence(s.id, () => {
        if (!isPrincePlaying || isPrincePaused) return;
        princeIndex++;
        princeTimeout = setTimeout(() => {
          if (isPrincePlaying && !isPrincePaused) {
            playNextSentence();
          }
        }, 600); // 600ms breath pause between sentences
      });
    }

    function pauseAllPrince() {
      if (!isPrincePlaying) return;
      isPrincePaused = true;
      if (princeTimeout) clearTimeout(princeTimeout);
      window.speechSynthesis.cancel();
      updatePrinceStatus(`Pause : #${princeIndex + 1} / ${PRINCE_SENTENCES.length}`);
    }

    function stopAllPrince() {
      isPrincePlaying = false;
      isPrincePaused = false;
      princeIndex = 0;
      if (princeTimeout) clearTimeout(princeTimeout);
      window.speechSynthesis.cancel();
      PRINCE_SENTENCES.forEach(x => {
        const el = document.getElementById(`prince-sentence-${x.id}`);
        if (el) el.classList.remove('border-cyan-500', 'bg-cyan-950/20');
      });
      updatePrinceStatus('Prêt');
    }

    // Matrix Forge Logic
    function updateForge() {
      const c1El = document.getElementById('forge-c1');
      const v1El = document.getElementById('forge-v1');
      const c2v2El = document.getElementById('forge-c2v2');
      if (!c1El || !v1El) return;

      const c1 = c1El.value;
      const v1 = v1El.value;
      const c2v2 = (c2v2El ? c2v2El.value.trim() : '') || 'po';
      const word = (c1 + v1 + c2v2).toLowerCase();

      const resWord = document.getElementById('forge-result-word');
      const resIpa = document.getElementById('forge-result-ipa');
      const resDesc = document.getElementById('forge-result-desc');

      if (resWord) resWord.innerText = word.toUpperCase();
      if (resIpa) resIpa.innerText = toIPA(word);

      const v1Roles = {
        'a': 'Nom (Entité, objet concret, individu)',
        'i': 'Verbe (Action dynamique, transition)',
        'u': 'Adjectif (Propriété descriptive)',
        'o': 'Lieu / Conteneur / Collectif',
        'e': 'Agent / Instrument / Opérateur'
      };

      const c1Domains = {
        't': 'Temps / Chronologie', 'd': 'Durée / Évolution',
        'k': 'Matière / Forme physique', 'g': 'Espace / Système spatial',
        'p': 'Mesure / Quantité / Logique', 'b': 'Nombre / Calcul',
        's': 'Sensation / Harmonie / Vision', 'z': 'Émotion / Affect',
        'm': 'Humain / Individu / Agent', 'n': 'Social / Relation',
        'f': 'Communication / Langage', 'v': 'Média / Signal',
        'l': 'Mouvement / Cinétique', 'r': 'Trajectoire / Direction',
        'sh': 'Ontologie / Existence', 'zh': 'Certitude / Abstraction',
        'j': 'Outil / Mécanisme', 'ch': 'Ingénierie / Technique',
        'h': 'Négation / Vide'
      };

      let existing = (LEXICON_DATA.roots || []).find(r => r.word === word);
      let extra = existing ? ` &bull; <strong class="text-emerald-400">Enregistré:</strong> "${existing.fr}" (${existing.en})` : ' &bull; <span class="text-amber-400">Racine orthogonale forgeable</span>';

      if (resDesc) {
        resDesc.innerHTML = `Domaine C1=${c1.toUpperCase()} (${c1Domains[c1] || ''}) | Rôle V1=${v1.toUpperCase()} (${v1Roles[v1] || ''}) | Terminal = ${c2v2}${extra}`;
      }
    }

    // Grammar & Lexicon Table
    function initLexiconTable() {
      const tbody = document.getElementById('lexicon-tbody');
      if (!tbody) return;
      tbody.innerHTML = '';

      const all = [
        ...(LEXICON_DATA.roots || []).map(r => ({ word: r.word, type: r.pos, fr: r.fr, en: r.en, domain: r.domain })),
        ...(LEXICON_DATA.adverbs || []).map(a => ({ word: a.word, type: 'adverbe', fr: a.fr, en: a.en, domain: 'Manière' })),
        ...(LEXICON_DATA.particles || []).map(p => ({ word: p.word, type: p.type, fr: p.fr, en: p.en, domain: 'Grammaire' })),
        ...(LEXICON_DATA.pronouns || []).map(pr => ({ word: pr.word, type: 'pronom', fr: pr.fr, en: pr.en, domain: 'Humain' }))
      ];

      all.sort((a, b) => a.word.localeCompare(b.word));

      all.forEach(item => {
        const tr = document.createElement('tr');
        tr.className = "hover:bg-slate-800/40 transition border-b border-slate-900";
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-mono font-bold text-cyan-400">${item.word}</td>
          <td class="py-2.5 px-3 text-slate-400 font-mono text-[11px]">${item.type}</td>
          <td class="py-2.5 px-3 text-slate-200">${item.fr}</td>
          <td class="py-2.5 px-3 text-slate-400">${item.en}</td>
          <td class="py-2.5 px-3">
            <button onclick="playTTS('${item.word}', 'lumina')" class="p-1 rounded bg-slate-800 text-cyan-400 hover:bg-cyan-950 transition" title="Écouter">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function filterLexicon() {
      const searchInput = document.getElementById('lexicon-search');
      if (!searchInput) return;
      const q = searchInput.value.toLowerCase().trim();
      const rows = document.querySelectorAll('#lexicon-tbody tr');
      rows.forEach(r => {
        const text = r.innerText.toLowerCase();
        r.style.display = text.includes(q) ? '' : 'none';
      });
    }

    // Beginner Course System with Complete Phonetic Table in Lesson 1
    const LESSONS = {
      1: {
        title: "Leçon 1 : Les Sons Purs, l'Inventaire Phonologique & la Matrice C1V1C2V2",
        html: `
          <p>Le Lumina est une langue construite rigoureusement logique. Sa force repose sur un système phonétique parfait sans exception :</p>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-3">
            <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
              <h4 class="font-bold text-cyan-400 mb-1">1. Prononciation Déterministe</h4>
              <p class="text-xs text-slate-400">Chaque lettre se prononce toujours de la même façon : <code>a, e, i, o</code> sont pures, et <code>u</code> se prononce toujours <strong>"ou"</strong> comme dans loup. L'accent tonique est fixé invariablement sur l'avant-dernière voyelle.</p>
            </div>
            <div class="p-3 rounded-lg bg-slate-950 border border-slate-800">
              <h4 class="font-bold text-cyan-400 mb-1">2. La Formule Magique C1V1C2V2</h4>
              <p class="text-xs text-slate-400">Chaque mot de 4 lettres révèle son ontologie : <strong>C1</strong> donne le thème (K=matière, M=humain, F=parole), <strong>V1</strong> donne la fonction (A=nom, I=verbe, U=adjectif, O=lieu).</p>
            </div>
          </div>

          <!-- Phoneme Inventory Table -->
          <div class="p-3 rounded-lg bg-slate-900 border border-slate-800 my-3">
            <h4 class="text-xs font-bold text-cyan-300 uppercase tracking-wider mb-2">Tableau des Phonèmes de Lumina</h4>
            <div class="grid grid-cols-2 sm:grid-cols-5 gap-2 text-xs font-mono">
              <div class="p-2 bg-slate-950 rounded border border-slate-800">
                <span class="text-cyan-400 font-bold">5 Voyelles</span><br>
                <span class="text-slate-300">A, E, I, O, U</span><br>
                <span class="text-[10px] text-slate-500 font-sans">(U = "ou")</span>
              </div>
              <div class="p-2 bg-slate-950 rounded border border-slate-800">
                <span class="text-cyan-400 font-bold">6 Occlusives</span><br>
                <span class="text-slate-300">P, B, T, D, K, G</span>
              </div>
              <div class="p-2 bg-slate-950 rounded border border-slate-800">
                <span class="text-cyan-400 font-bold">7 Fricatives</span><br>
                <span class="text-slate-300">F, V, S, Z, SH, ZH, H</span>
              </div>
              <div class="p-2 bg-slate-950 rounded border border-slate-800">
                <span class="text-cyan-400 font-bold">2 Affriquées</span><br>
                <span class="text-slate-300">CH, J</span>
              </div>
              <div class="p-2 bg-slate-950 rounded border border-slate-800">
                <span class="text-cyan-400 font-bold">4 Liquides/Nasales</span><br>
                <span class="text-slate-300">M, N, L, R</span>
              </div>
            </div>
          </div>
          <p class="text-xs text-slate-300">Exemple : <code>fapo</code> (livre), <code>fipi</code> (écrire), <code>fupu</code> (écrit), <code>fopo</code> (bibliothèque).</p>
        `,
        quiz: {
          q: "Dans la formule C1V1C2V2, que signifie la voyelle V1 = -I- ?",
          options: ["Un Verbe (action)", "Un Nom (objet)", "Un Adjectif (qualité)", "Un Lieu"],
          answer: 0,
          explanation: "Exactement ! V1 = I indique invariablement un Verbe (comme sifi = voir, kidi = manger, shili = être)."
        }
      },
      2: {
        title: "Leçon 2 : Pronoms, Noms et l'Ordre SVO",
        html: `
          <p>En Lumina, l'ordre de la phrase est strictement <strong>Sujet - Verbe - Objet</strong> (SVO).</p>
          <ul class="list-disc pl-5 space-y-1 text-xs text-slate-300 my-2">
            <li><strong>Mina</strong> (Je / Moi), <strong>Tina</strong> (Tu / Toi), <strong>Lina</strong> (Il / Elle).</li>
            <li>Pour le pluriel, remplacez <code>-na</code> par <code>-ro</code> : <strong>Miro</strong> (Nous), <strong>Tiro</strong> (Vous), <strong>Liro</strong> (Ils / Elles).</li>
            <li>Pour dire 'le/la', placez <code>la</code> devant : <code>la kafa</code> (l'animal).</li>
            <li>Pour dire 'les', placez <code>ro</code> après : <code>la kafa ro</code> (les animaux).</li>
          </ul>
          <p class="text-xs text-cyan-300 font-mono">Mina sifi la kafa = Je vois l'animal.</p>
        `,
        quiz: {
          q: "Comment dit-on 'les animaux' en Lumina ?",
          options: ["La kafa ro", "Kafa la ro", "Ro kafa", "Mina kafa"],
          answer: 0,
          explanation: "Bravo ! L'article défini 'la' se place devant, et la marque de pluriel 'ro' se place après le nom : la kafa ro."
        }
      },
      3: {
        title: "Leçon 3 : Voyage Temporel (Conjugaison Sans Casse-Tête)",
        html: `
          <p>Pas de verbes irréguliers en Lumina ! Le verbe reste invariable. On place simplement un marqueur juste devant le verbe :</p>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs my-3">
            <div class="p-2 rounded bg-slate-950 border border-slate-800">
              <span class="mono text-cyan-400 font-bold">li</span> : Présent<br>
              <span class="text-slate-400">Mina li kidi</span>
            </div>
            <div class="p-2 rounded bg-slate-950 border border-slate-800">
              <span class="mono text-cyan-400 font-bold">na</span> : Passé<br>
              <span class="text-slate-400">Mina na kidi</span>
            </div>
            <div class="p-2 rounded bg-slate-950 border border-slate-800">
              <span class="mono text-cyan-400 font-bold">vo</span> : Futur<br>
              <span class="text-slate-400">Mina vo kidi</span>
            </div>
            <div class="p-2 rounded bg-slate-950 border border-slate-800">
              <span class="mono text-cyan-400 font-bold">ne</span> : Négation<br>
              <span class="text-slate-400">Mina ne kidi</span>
            </div>
          </div>
        `,
        quiz: {
          q: "Comment traduire : 'Je n'ai pas mangé' ?",
          options: ["Mina ne na kidi", "Mina na ne kidi", "Mina kidi ne na", "No kidi mina"],
          answer: 0,
          explanation: "Parfait ! La négation 'ne' et le marqueur temporel 'na' se placent devant le verbe : Mina ne na kidi."
        }
      },
      4: {
        title: "Leçon 4 : Questions, Adjectifs et Couleurs",
        html: `
          <p>Pour poser une question fermée, commencez simplement la phrase par <code>Ma</code> :</p>
          <p class="text-xs text-cyan-300 font-mono mb-2">Ma Tina sifi la safo? = Est-ce que tu vois l'image ?</p>
          <p>Les adjectifs se placent <strong>après</strong> le nom :</p>
          <p class="text-xs text-slate-300 mb-2"><code>safo sulo</code> = une belle image &bull; <code>la kapa suru</code> = le chapeau rouge.</p>
          <p>Pour transformer un adjectif en adverbe, ajoutez <code>-fi</code> :</p>
          <p class="text-xs text-slate-300"><code>puru</code> (vrai) &rarr; <code>purufi</code> (vraiment).</p>
        `,
        quiz: {
          q: "Comment dit-on 'vraiment' à partir de l'adjectif 'puru' (vrai) ?",
          options: ["purufi", "pururo", "lapuru", "puruna"],
          answer: 0,
          explanation: "Correct ! Le suffixe invariable -fi transforme l'adjectif en adverbe de manière : puru -> purufi."
        }
      },
      5: {
        title: "Leçon 5 : Le Chef-d'œuvre du Petit Prince décodé",
        html: `
          <p>Vous avez maintenant toutes les armes pour décrypter le texte fondateur de Lumina :</p>
          <div class="p-3 rounded-lg bg-slate-950 border border-slate-800 font-mono text-xs text-cyan-300 my-2 space-y-1">
            <p>La na fisi kafa kofa keli na kidi kafa kabo.</p>
            <p class="text-slate-400 text-[11px]">&rarr; Ça montrait [le serpent] qui avait avalé [l'éléphant].</p>
          </div>
          <p class="text-xs text-slate-300">Et lorsque l'auteur a demandé aux grandes personnes si elles avaient peur :</p>
          <div class="p-3 rounded-lg bg-slate-950 border border-slate-800 font-mono text-xs text-indigo-300 my-2">
            Ma la safo ta na timi Liro? (Est-ce que ce dessin leur faisait peur ?)
          </div>
        `,
        quiz: {
          q: "Que désigne 'kafa kabo' dans le texte ?",
          options: ["L'éléphant (l'animal corporel massif)", "Le serpent", "Le renard", "Le mouton"],
          answer: 0,
          explanation: "Exact ! Kabo (K-A-B-O) est l'entité vivante corporelle massive : l'éléphant !"
        }
      }
    };

    function setLesson(id) {
      [1, 2, 3, 4, 5].forEach(i => {
        const btn = document.getElementById(`lesson-btn-${i}`);
        if (btn) {
          if (i === id) {
            btn.className = "py-2 px-3 text-xs font-semibold rounded-lg bg-cyan-950 text-cyan-400 border border-cyan-800";
          } else {
            btn.className = "py-2 px-3 text-xs font-semibold rounded-lg bg-slate-800/50 text-slate-400 hover:text-slate-200";
          }
        }
      });

      const lesson = LESSONS[id];
      if (!lesson) return;

      const content = document.getElementById('lesson-content');
      if (content) {
        content.innerHTML = `
          <h3 class="text-base font-bold text-white mb-2">${lesson.title}</h3>
          ${lesson.html}
        `;
      }

      // Setup Quiz
      const qEl = document.getElementById('quiz-question');
      if (qEl) qEl.innerText = lesson.quiz.q;

      const opts = document.getElementById('quiz-options');
      const fb = document.getElementById('quiz-feedback');
      if (opts) {
        opts.innerHTML = '';
        if (fb) fb.classList.add('hidden');

        lesson.quiz.options.forEach((opt, idx) => {
          const b = document.createElement('button');
          b.className = "p-3 rounded-lg bg-slate-900 border border-slate-800 text-left hover:border-cyan-500 hover:text-cyan-300 transition text-xs";
          b.innerText = opt;
          b.onclick = () => {
            if (idx === lesson.quiz.answer) {
              fb.className = "text-xs p-3 rounded-lg bg-emerald-950/60 border border-emerald-800 text-emerald-300 block";
              fb.innerHTML = `<strong>Bravo !</strong> ${lesson.quiz.explanation}`;
            } else {
              fb.className = "text-xs p-3 rounded-lg bg-rose-950/60 border border-rose-800 text-rose-300 block";
              fb.innerHTML = `<strong>Réessayez !</strong> Ce n'est pas tout à fait ça. Re-lisez le mémo ci-dessus !`;
            }
          };
          opts.appendChild(b);
        });
      }
    }

    // Expose all functions to global window scope so HTML onclick attributes always find them
    window.setTab = setTab;
    window.setDirection = setDirection;
    window.doTranslate = doTranslate;
    window.clearTranslator = clearTranslator;
    window.playTTS = playTTS;
    window.initSTT = initSTT;
    window.toggleSTT = toggleSTT;
    window.stopSTT = stopSTT;
    window.playPrinceSentence = playPrinceSentence;
    window.playAllPrince = playAllPrince;
    window.pauseAllPrince = pauseAllPrince;
    window.stopAllPrince = stopAllPrince;
    window.updateForge = updateForge;
    window.filterLexicon = filterLexicon;
    window.setLesson = setLesson;
    window.toIPA = toIPA;

    // Initialization on load
    window.addEventListener('DOMContentLoaded', () => {
      initPrince();
      initLexiconTable();
      updateForge();
      setLesson(1);
      renderQuickSamples();

      // Input live change listener
      const inputEl = document.getElementById('translate-input');
      if (inputEl) {
        inputEl.addEventListener('input', () => {
          doTranslate();
        });
      }

      // TTS slider visual value sync
      const rateEl = document.getElementById('tts-rate');
      if (rateEl) {
        rateEl.addEventListener('input', (e) => {
          const v = document.getElementById('rate-val');
          if (v) v.innerText = `${parseFloat(e.target.value).toFixed(1)}x`;
        });
      }
      const pitchEl = document.getElementById('tts-pitch');
      if (pitchEl) {
        pitchEl.addEventListener('input', (e) => {
          const v = document.getElementById('pitch-val');
          if (v) v.innerText = `${parseFloat(e.target.value).toFixed(1)}x`;
        });
      }
    });
  </script>
</body>
</html>
"""

final_js = js_template.replace('__LEXICON_DATA__', js_lexicon).replace('__PRINCE_DATA__', js_prince)
full_html = html_head + final_js

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print("SUCCESS: index.html updated. Total size:", len(full_html), "bytes.")
