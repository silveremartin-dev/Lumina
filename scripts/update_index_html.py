"""Update index.html with the new rich multi-thousand words lexicon,
22 authentic Petit Prince sentences, and enhanced bidirectional translation.
"""

import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def main():
    index_path = ROOT_DIR / "index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Load lexique.json
    lexique_path = ROOT_DIR / "data" / "lexique.json"
    with open(lexique_path, "r", encoding="utf-8") as f:
        lex_data = json.load(f)

    # 2. Load petit_prince.json
    prince_path = ROOT_DIR / "data" / "petit_prince.json"
    with open(prince_path, "r", encoding="utf-8") as f:
        prince_data = json.load(f)

    # 3. Replace PRINCE_SENTENCES in index.html
    s_prince = html.find("const PRINCE_SENTENCES =")
    e_prince = html.find("];", s_prince) + 2
    if s_prince != -1 and e_prince != -1:
        prince_sentences_js = "const PRINCE_SENTENCES = " + json.dumps(prince_data["sentences"], ensure_ascii=False, indent=2) + ";"
        html = html[:s_prince] + prince_sentences_js + html[e_prince:]
        print("Updated PRINCE_SENTENCES in index.html.")

    # 4. Replace LEXICON_DATA in index.html
    s_lex = html.find("const LEXICON_DATA =")
    e_lex = html.find("};", s_lex) + 2
    if s_lex != -1 and e_lex != -1:
        lex_js = "const LEXICON_DATA = " + json.dumps(lex_data, ensure_ascii=False, indent=2) + ";"
        html = html[:s_lex] + lex_js + html[e_lex:]
        print("Updated LEXICON_DATA in index.html.")

    # 5. Replace translateFrToLumina and translateLuminaToFr
    s_fr = html.find("function translateFrToLumina")
    e_lum = html.find("function renderWordCards")

    new_translators_js = """let FR_TO_LUMINA = null;

    function getReverseLexicon() {
      if (FR_TO_LUMINA) return FR_TO_LUMINA;
      FR_TO_LUMINA = {};
      if (!LEXICON_DATA) return FR_TO_LUMINA;

      (LEXICON_DATA.particles || []).forEach(p => {
        p.fr.split(/[,/]/).forEach(t => {
          let c = t.trim().toLowerCase();
          if (c && !c.startsWith('[')) FR_TO_LUMINA[c] = p.word;
        });
      });
      (LEXICON_DATA.pronouns || []).forEach(pr => {
        pr.fr.split(/[,/]/).forEach(t => {
          let c = t.replace(/\\(.*?\\)/g, '').trim().toLowerCase();
          if (c) FR_TO_LUMINA[c] = pr.word;
        });
      });
      (LEXICON_DATA.numbers || []).forEach(nb => {
        FR_TO_LUMINA[nb.fr.toLowerCase()] = nb.word;
        FR_TO_LUMINA[String(nb.value)] = nb.word;
      });
      (LEXICON_DATA.roots || []).forEach(r => {
        let pos = r.pos || '';
        r.fr.split(/[,/]/).forEach(t => {
          let c = t.replace(/\\(.*?\\)/g, '').trim().toLowerCase();
          if (c && (!FR_TO_LUMINA[c] || pos === 'noun')) {
            FR_TO_LUMINA[c] = r.word;
          }
        });
      });
      (LEXICON_DATA.adverbs || []).forEach(adv => {
        adv.fr.split(/[,/]/).forEach(t => {
          let c = t.trim().toLowerCase();
          if (c && !FR_TO_LUMINA[c]) FR_TO_LUMINA[c] = adv.word;
        });
      });
      return FR_TO_LUMINA;
    }

    const COMMON_VERBS_JS = {
      "suis": ["shili", null], "es": ["shili", null], "est": ["shili", null], "sommes": ["shili", null], "êtes": ["shili", null], "sont": ["shili", null], "était": ["shili", "na"], "étaient": ["shili", "na"], "été": ["shili", "na"], "serai": ["shili", "vo"], "sera": ["shili", "vo"], "être": ["shili", null],
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

    function translateSingleClauseFrToLumina(clause) {
      let t = clause.trim();
      if (!t) return [];
      let tLower = t.toLowerCase().replace(/[?!.,; ]/g, '');
      if (tLower === 'bonjour' || tLower === 'salut' || tLower === 'coucou') return ['Fali'];
      if (tLower === 'aurevoir' || tLower === 'adieu') return ['Fata'];
      if (tLower === 'merci' || tLower === 'mercibeaucoup') return ['Fama'];
      if (tLower === 'silvousplait' || tLower === 'silteplait') return ['Fape'];
      if (tLower === 'pardon' || tLower === 'excusezmoi') return ['Fase'];
      if (tLower === 'commentcava' || tLower === 'commentvastu' || tLower === 'cava') return ['Ma', 'Tina', 'shili', 'zelu'];
      if (tLower === 'jevaisbien' || tLower === 'cavabien') return ['Mina', 'shili', 'zelu'];

      let isQ = /^(est-ce que|\?)|(\?$)/i.test(t);
      let tClean = t.replace(/^(est-ce que|est-ce-que)\\s+/i, '');

      // Détection "je m'appelle X"
      let matchName = tClean.match(/^(?:je\\s+(?:m['’]appelle|me\\s+nomme))\\s+([A-Za-zÀ-ÖØ-öø-ÿ]+)/i);
      if (matchName) {
        let nomPropre = matchName[1].charAt(0).toUpperCase() + matchName[1].slice(1);
        return ['Mina', 'nomi', nomPropre];
      }

      // Élisions
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
      let rev = getReverseLexicon();
      let tokens = [];
      if (isQ) tokens.push("Ma");

      let tense = null;
      let neg = false;

      for (let i = 0; i < words.length; i++) {
        let rawW = words[i];
        let w = rawW.toLowerCase();

        if (w === 'ne') { neg = true; continue; }
        if (w === 'pas') continue;

        if (['ai', 'as', 'a', 'avons', 'avez', 'ont', 'était', 'étaient', 'avais'].includes(w)) {
          tense = "na";
          continue;
        }
        if (['vais', 'vas', 'va', 'allons', 'allez', 'vont', 'serai', 'sera'].includes(w)) {
          tense = "vo";
          continue;
        }

        if (w === 'le' || w === 'la') { tokens.push('la'); continue; }
        if (w === 'les' || w === 'des') {
          tokens.push('la');
          if (i + 1 < words.length) {
            let nextWord = words[i+1].toLowerCase().replace(/s$/, '');
            let lum = rev[words[i+1].toLowerCase()] || rev[nextWord];
            if (lum) {
              tokens.push(lum, 'ro');
              i++;
              continue;
            }
          }
          continue;
        }
        if (w === 'un' || w === 'une') continue;

        if (w === 'mon' || w === 'ma') {
          if (i + 1 < words.length) {
            let nom = rev[words[i+1].toLowerCase()];
            if (nom) { tokens.push('la', nom, 'pa', 'Mina'); i++; continue; }
          }
        }
        if (w === 'ton' || w === 'ta') {
          if (i + 1 < words.length) {
            let nom = rev[words[i+1].toLowerCase()];
            if (nom) { tokens.push('la', nom, 'pa', 'Tina'); i++; continue; }
          }
        }

        if (COMMON_VERBS_JS[w]) {
          let [lumVerb, autoTense] = COMMON_VERBS_JS[w];
          if (autoTense && !tense) tense = autoTense;
          if (neg) { tokens.push('ne'); neg = false; }
          if (tense) { tokens.push(tense); tense = null; }
          tokens.push(lumVerb);
          continue;
        }

        let base = w.replace(/s$/, '');
        let lum = rev[w] || rev[base];
        if (lum) {
          let isVerb = (lum.endsWith('i') && lum.length === 4) || ['shili','sifi','kidi','kisi','fidi','fisi','pishi','lifi','nomi'].includes(lum);
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

      let resLumina = pieceStrs.join(' ').replace(/\\s+([,;])\\s*/g, '$1 ');
      if (!resLumina && text.trim()) resLumina = '...';

      document.getElementById('translate-output').innerText = resLumina;
      document.getElementById('translate-ipa').innerText = `Lumina IPA : ${resTokens.map(w => toIPA(w)).join(' ')}`;
      document.getElementById('translate-gloss').innerText = resTokens.map(w => `${w}: FR`).join(' | ');

      renderWordCards(resTokens.map(w => w.replace(/[.,?!]/g, '')));
    }

    function translateLuminaToFr(text) {
      const rawWords = text.trim().split(/\\s+/);
      let frTokens = [];
      let glosses = [];
      let isQ = false;

      rawWords.forEach(rw => {
        let clean = rw.toLowerCase().replace(/[.,?!:;]/g, '');
        if (clean === 'ma') { isQ = true; glosses.push('ma: [question]'); return; }
        if (clean === 'la') { frTokens.push('le/la'); glosses.push('la: défini'); return; }
        if (clean === 'ro') { glosses.push('ro: pluriel'); return; }
        if (clean === 'na') { frTokens.push('[passé]'); glosses.push('na: passé'); return; }
        if (clean === 'li') { frTokens.push('[présent]'); glosses.push('li: présent'); return; }
        if (clean === 'vo') { frTokens.push('[futur]'); glosses.push('vo: futur'); return; }
        if (clean === 'ne') { frTokens.push('ne pas'); glosses.push('ne: non'); return; }

        if (rw[0] === rw[0].toUpperCase() && !LEXICON_DATA.roots.find(x => x.word === clean)) {
          frTokens.push(rw.replace(/[.,?!:;]/g, ''));
          glosses.push(`${rw}: [Nom propre]`);
          return;
        }

        let p = (LEXICON_DATA.particles || []).find(x => x.word === clean);
        if (p) { frTokens.push(p.fr.split(',')[0]); glosses.push(`${clean}: ${p.fr}`); return; }

        let pr = (LEXICON_DATA.pronouns || []).find(x => x.word === clean);
        if (pr) { frTokens.push(pr.fr.split(',')[0]); glosses.push(`${clean}: ${pr.fr}`); return; }

        let r = (LEXICON_DATA.roots || []).find(x => x.word === clean);
        if (r) {
          let meaning = r.fr.split(',')[0].replace(/\\(.*?\\)/g, '').trim();
          if (clean === 'nomi') meaning = "s'appeler";
          if (clean === 'fali') meaning = "bonjour";
          frTokens.push(meaning);
          glosses.push(`${clean}: ${r.fr}`);
          return;
        }

        let adv = (LEXICON_DATA.adverbs || []).find(x => x.word === clean);
        if (adv) {
          frTokens.push(adv.fr.split(',')[0]);
          glosses.push(`${clean}: ${adv.fr}`);
          return;
        }

        frTokens.push(`[${clean}]`);
      });

      let resFr = frTokens.join(' ');
      resFr = resFr.replace(/\\bMina\\s+s'appeler\\s+(\\w+)/gi, "Je m'appelle $1")
                   .replace(/\\bTina\\s+s'appeler\\s+(\\w+)/gi, "Tu t'appelles $1")
                   .replace(/\\bLina\\s+s'appeler\\s+(\\w+)/gi, "Il s'appelle $1")
                   .replace(/\\bJe\\s+s'appeler\\s+(\\w+)/gi, "Je m'appelle $1")
                   .replace(/\\bTu\\s+être\\s+heureux\\b/gi, "tu vas bien")
                   .replace(/\\bJe\\s+être\\s+heureux\\b/gi, "je vais bien")
                   .replace(/Je\\s+\\[passé\\]\\s+voir/gi, "J'ai vu")
                   .replace(/Je\\s+\\[passé\\]\\s+manger/gi, "J'ai mangé")
                   .replace(/Je\\s+\\[passé\\]\\s+faire/gi, "J'ai fait")
                   .replace(/\\[passé\\]\\s+(\\w+)/g, 'a $1')
                   .replace(/\\[futur\\]\\s+(\\w+)/g, 'va $1')
                   .replace(/\\[présent\\]\\s+/g, '')
                   .replace(/\\ble\\/la\\s+([aeiouh][\\w-]+)/gi, "l'$1")
                   .replace(/\\ble\\/la\\b/g, 'le');

      if (isQ && !resFr.endsWith('?')) {
        if (!resFr.toLowerCase().startsWith('est-ce que')) {
          resFr = `Est-ce que ${resFr.charAt(0).toLowerCase()}${resFr.slice(1)}`;
        }
        resFr += ' ?';
      } else if (resFr && !resFr.endsWith('.')) {
        resFr = resFr.charAt(0).toUpperCase() + resFr.slice(1) + '.';
      }

      document.getElementById('translate-output').innerText = resFr;
      document.getElementById('translate-ipa').innerText = `Lumina IPA source : ${rawWords.map(w => toIPA(w)).join(' ')}`;
      document.getElementById('translate-gloss').innerText = glosses.join(' | ');

      renderWordCards(rawWords.map(w => w.replace(/[.,?!]/g, '')));
    }
    """

    if s_fr != -1 and e_lum != -1:
        html = html[:s_fr] + new_translators_js + html[e_lum:]
        print("Updated translateFrToLumina and translateLuminaToFr in index.html.")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved {index_path}.")

if __name__ == "__main__":
    main()
