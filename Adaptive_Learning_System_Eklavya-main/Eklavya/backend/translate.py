"""Translate any English text into the 22 scheduled Indian languages (AI4Bharat IndicTrans2, runs locally).
Optional install:  pip install torch transformers sentencepiece IndicTransToolkit
Without it the server still runs; /api/translate answers 503 and the app simply stays in English.
Results are cached in translations.db, so each sentence is translated once for all students."""
import os
import sqlite3
import threading

from config import BASE_DIR

DB = os.path.join(BASE_DIR, "translations.db")
LOCK = threading.Lock()
CKPT = "ai4bharat/indictrans2-en-indic-dist-200M"
FLORES = {"as": "asm_Beng", "bn": "ben_Beng", "brx": "brx_Deva", "doi": "doi_Deva", "gu": "guj_Gujr", "hi": "hin_Deva",
          "kn": "kan_Knda", "ks": "kas_Arab", "kok": "gom_Deva", "mai": "mai_Deva", "ml": "mal_Mlym", "mni": "mni_Mtei",
          "mr": "mar_Deva", "ne": "npi_Deva", "or": "ory_Orya", "pa": "pan_Guru", "sa": "san_Deva", "sat": "sat_Olck",
          "sd": "snd_Arab", "ta": "tam_Taml", "te": "tel_Telu", "ur": "urd_Arab"}
_m = {}


class Unavailable(Exception):
    pass


def _engine(texts, tgt):
    if not _m:   # model loads on first use only
        try:
            import torch
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
            from IndicTransToolkit.processor import IndicProcessor
        except ImportError as e:
            raise Unavailable("Translation engine not installed: " + str(e))
        _m["tok"] = AutoTokenizer.from_pretrained(CKPT, trust_remote_code=True)
        _m["model"] = AutoModelForSeq2SeqLM.from_pretrained(CKPT, trust_remote_code=True).eval()
        _m["ip"], _m["torch"] = IndicProcessor(inference=True), torch
    ip, tok = _m["ip"], _m["tok"]
    batch = ip.preprocess_batch(texts, src_lang="eng_Latn", tgt_lang=tgt)
    inputs = tok(batch, truncation=True, padding="longest", return_tensors="pt")
    with _m["torch"].no_grad():
        out = _m["model"].generate(**inputs, num_beams=4, max_length=256)
    return ip.postprocess_batch(tok.batch_decode(out, skip_special_tokens=True), lang=tgt)


def translate_texts(target, texts):
    """Returns a list of translations in the same order as texts. Raises ValueError / Unavailable."""
    if target not in FLORES:
        raise ValueError("Unsupported language")
    if not isinstance(texts, list) or len(texts) > 50 or any(not isinstance(t, str) or len(t) > 1000 for t in texts):
        raise ValueError("Send up to 50 strings of at most 1000 characters")
    with LOCK:
        c = sqlite3.connect(DB)
        try:
            c.execute("CREATE TABLE IF NOT EXISTS tx(lang TEXT, src TEXT, out TEXT, PRIMARY KEY(lang, src))")
            have = {}
            if texts:
                q = ",".join("?" * len(texts))
                have = dict(c.execute(f"SELECT src,out FROM tx WHERE lang=? AND src IN ({q})", [target, *texts]))
            todo = [t for t in dict.fromkeys(texts) if t not in have]
            if todo:
                for s, o in zip(todo, _engine(todo, FLORES[target])):
                    have[s] = o
                    c.execute("INSERT OR REPLACE INTO tx VALUES(?,?,?)", (target, s, o))
                c.commit()
        finally:
            c.close()
    return [have.get(t, "") for t in texts]
