import streamlit as st
import pandas as pd
import re, os, time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Helpdesk AI Assistant", page_icon="🎫", layout="wide")

BASE = Path(__file__).parent
FAQ_PATH = BASE / "kb" / "faq.md"
TICKETS_PATH = BASE / "data" / "tickets.csv"

# --- helpers ---
def mask_pii(text: str) -> str:
    # NIK 16 digit, password-like
    text = re.sub(r"\b\d{16}\b", "[MASKED_NIK]", text)
    text = re.sub(r"NIK\s*[:\-]?\s*\d+", "NIK [MASKED_NIK]", text, flags=re.I)
    text = re.sub(r"password\s*[:\-]?\s*\S+", "password [MASKED]", text, flags=re.I)
    # simple name mask if needed (demo)
    return text

def load_faq():
    return FAQ_PATH.read_text(encoding="utf-8") if FAQ_PATH.exists() else ""

FAQ_TEXT = load_faq()

# mock categorizer (fallback when no API key)
def mock_categorize(text: str):
    t = text.lower()
    if any(k in t for k in ["password","lupa","sso","otp"]):
        return "Password", 0.92
    if "printer" in t:
        return "Hardware-Printer", 0.88
    if any(k in t for k in ["install","autocad","software","sccm"]):
        return "Software", 0.85
    if any(k in t for k in ["wifi","jaringan","network","switch","ap"]):
        return "Network", 0.86
    if "email" in t:
        return "Email", 0.84
    if "erp" in t:
        return "ERP", 0.83
    return "General", 0.55

def mock_draft(category: str, masked: str):
    # simple RAG: pull relevant FAQ chunk
    faq = FAQ_TEXT.lower()
    if category=="Password" and "reset password" in faq:
        return "Reset via portal SSO → Lupa Password → verifikasi NIK+OTP → buat password baru 8+ karakter. Jika gagal, buat ticket dengan NIK.", "FAQ: Reset Password"
    if category=="Hardware-Printer":
        return "Cek kabel power+jaringan, restart printer, cek antrean print. Jika lampu merah, foto error buat ticket Hardware-Printer.", "FAQ: Printer Error"
    if category=="Software":
        return "Request install via ticketing + approval atasan, IT install remote via SCCM. Jangan install sumber tidak resmi.", "FAQ: Install Software"
    if category=="Network":
        return "Coba reconnect/lupakan jaringan. Jika semua device down, lapor IT Network dengan lokasi lantai.", "FAQ: Jaringan / WiFi"
    if category=="Email":
        return "Cek spam/junk & kuota mailbox, coba webmail. Jika tetap, kirim screenshot error.", "FAQ: Email Tidak Masuk"
    if category=="ERP":
        return "Pastikan VPN aktif + role approval. Error 403 = cek VPN/role, hubungi IT dengan NIK & modul ERP.", "FAQ: Akses ERP"
    return "Terima kasih laporannya, tim IT akan cek. Mohon sertakan lokasi & screenshot jika ada.", "FAQ: General"

def call_ai_api(masked_text: str):
    # support both Gemini (GOOGLE_API_KEY / GEMINI_API_KEY) and OpenAI
    gem_key = os.getenv("GOOGLE_API_KEY", os.getenv("GEMINI_API_KEY", "")).strip()
    oai_key = os.getenv("OPENAI_API_KEY", "").strip()
    # prefer Gemini if available (gratis)
    if gem_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gem_key)
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
            model = genai.GenerativeModel(model_name)
            prompt = f"""Kamu asisten IT Helpdesk. Kategorikan ticket dan buat draft jawaban dari FAQ berikut.

FAQ:
{FAQ_TEXT[:3000]}

Ticket (sudah dimask):
{masked_text}

Jawab JSON saja tanpa markdown: {{"category": "...", "confidence": 0.0-1.0, "draft": "...", "source": "..."}}"""
            r = model.generate_content(prompt)
            import json
            txt = r.text or ""
            m = re.search(r"\{.*\}", txt, re.S)
            if m:
                j = json.loads(m.group(0))
                return j.get("category","General"), float(j.get("confidence",0.7)), j.get("draft",""), j.get("source","FAQ")
            return None
        except Exception as e:
            st.warning(f"Gemini error, fallback mock: {e}")
            return None
    if not oai_key:
        return None
    try:
        from openai import OpenAI
        # fix proxies error: old openai + env proxies
        client = OpenAI(api_key=oai_key)
        # minimal prompt, send masked only
        prompt = f"""Kamu asisten IT Helpdesk. Kategorikan ticket dan buat draft jawaban dari FAQ berikut.

FAQ:
{FAQ_TEXT[:3000]}

Ticket (sudah dimask):
{masked_text}

Jawab JSON: {{"category": "...", "confidence": 0.0-1.0, "draft": "...", "source": "..."}}"""
        r = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}], temperature=0.2, max_tokens=300)
        import json
        txt = r.choices[0].message.content
        # try parse JSON
        m = re.search(r"\{.*\}", txt, re.S)
        if m:
            j = json.loads(m.group(0))
            return j.get("category","General"), float(j.get("confidence",0.7)), j.get("draft",""), j.get("source","FAQ")
        return None
    except Exception as e:
        st.warning(f"AI API error, fallback mock: {e}")
        return None

# --- UI ---
st.title("🎫 Helpdesk AI Assistant — PoC")
st.caption("Auto-kategorisasi + Draft FAQ + Masking + Needs Review • Python + Streamlit + AI API • MagangHub Mustika/Bank Mega")

with st.sidebar:
    st.header("⚙️ Config")
    st.write(f"FAQ: `{FAQ_PATH}`")
    st.write(f"Tickets: `{TICKETS_PATH}`")
    has_gem = bool(os.getenv("GOOGLE_API_KEY", os.getenv("GEMINI_API_KEY","")).strip())
    has_oai = bool(os.getenv("OPENAI_API_KEY","").strip())
    st.metric("AI API", "ON (Gemini)" if has_gem else ("ON (OpenAI)" if has_oai else "OFF (Mock rule-based)"))
    st.info("Tanpa key tetap jalan pakai mock. Isi .env: GOOGLE_API_KEY untuk Gemini gratis atau OPENAI_API_KEY.")
    st.divider()
    st.subheader("Test Cepat")
    if TICKETS_PATH.exists():
        df = pd.read_csv(TICKETS_PATH)
        st.dataframe(df[["masked_text","category"]].head(5), use_container_width=True)
    conf_thr = st.slider("Threshold Needs Review", 0.5, 0.9, 0.70, 0.05)

col1, col2 = st.columns([1,1])
with col1:
    st.subheader("1️⃣ Input Ticket")
    ticket = st.text_area("Tulis ticket (coba paste yang sensitif, akan dimask):", height=120,
                          placeholder="Contoh: Tolong reset password NIK 3271010101010001, tidak bisa login SSO")
    masked = mask_pii(ticket) if ticket else ""
    if ticket:
        st.write("**Masked (yang dikirim ke AI):**")
        st.code(masked)
        st.caption("✅ NIK/password dimask • raw tidak ke log/AI")

    if st.button("🚀 Proses AI", type="primary", disabled=not ticket):
        with st.spinner("Memproses..."):
            time.sleep(0.4)
            ai = call_ai_api(masked) if ticket else None
            if ai:
                # ai returns tuple of 4 if openai
                if len(ai)==4:
                    cat, conf, draft, src = ai
                else:
                    cat, conf = ai[0], ai[1]
                    draft, src = mock_draft(cat, masked)
            else:
                cat, conf = mock_categorize(masked)
                draft, src = mock_draft(cat, masked)
            st.session_state["result"] = (cat, conf, draft, src, masked)

with col2:
    st.subheader("2️⃣ Hasil AI")
    if "result" in st.session_state:
        cat, conf, draft, src, masked = st.session_state["result"]
        c1, c2 = st.columns(2)
        c1.metric("Kategori", cat)
        c2.metric("Confidence", f"{conf:.2f}")
        if conf < conf_thr:
            st.error("⚠️ Needs Review → Forward ke IT manusia (confidence rendah)")
        else:
            st.success("✅ Auto-draft siap kirim")
        st.write("**Draft jawaban (dari FAQ):**")
        st.info(draft)
        st.caption(f"Sumber: {src} • kb/faq.md")
        with st.expander("Log (untuk dashboard)"):
            st.json({"masked_input": masked, "category": cat, "confidence": conf, "source": src, "needs_review": conf < conf_thr})
    else:
        st.write("Belum ada hasil. Input ticket lalu klik Proses.")

st.divider()
st.subheader("📊 Demo Batch (data/tickets.csv)")
if TICKETS_PATH.exists():
    df = pd.read_csv(TICKETS_PATH)
    results = []
    for _, row in df.iterrows():
        m = mask_pii(row["masked_text"])
        cat, conf = mock_categorize(m)
        results.append({"ticket": row["masked_text"][:40]+"...", "label": row["category"], "pred": cat, "conf": conf, "match": row["category"]==cat})
    rdf = pd.DataFrame(results)
    st.dataframe(rdf, use_container_width=True)
    acc = rdf["match"].mean()
    st.metric("Accuracy (mock)", f"{acc*100:.1f}%")
    st.caption("Ganti mock dengan AI API untuk akurasi lebih tinggi. Log ini bisa jadi dashboard IT.")
else:
    st.write("Tambah data/tickets.csv untuk demo batch.")

st.divider()
st.markdown("**Untuk Interview:** share screen ini → tunjukkan masking + kategorisasi + Needs Review. Repo: `helpdesk-ai`")
