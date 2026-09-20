import streamlit as st
from google import genai

# 1. Konfigurasi Halaman Wide Dashboard Laptop
st.set_page_config(
    page_title="SekolahKita AI - Canvas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Styling CSS Neon Bar & Layout Dashboard
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Orbitron:wght@700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Format Judul Dua Warna */
.hero-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 2px;
}

.hero-icon {
    font-size: 2.2rem;
}

.title-sekolah {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.3rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: 2px;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.4);
}

.title-kita {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.3rem;
    font-weight: 800;
    color: #FF7B00;
    letter-spacing: 2px;
    text-shadow: 0 0 14px rgba(255, 123, 0, 0.7), 0 0 25px rgba(255, 123, 0, 0.4);
}

.title-ai {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.3rem;
    font-weight: 800;
    color: #00f2fe;
    letter-spacing: 2px;
    text-shadow: 0 0 14px rgba(0, 242, 254, 0.7);
}

/* Garis Neon Bar Menyala Dua Warna */
.neon-glow-bar {
    height: 4px;
    width: 100%;
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 35%, #ff7b00 70%, #ffae19 100%);
    border-radius: 4px;
    box-shadow: 0 0 12px rgba(0, 242, 254, 0.6), 0 0 22px rgba(255, 123, 0, 0.5);
    margin-top: 6px;
    margin-bottom: 25px;
}

/* Border Dinamis Sesuai Konten (Tidak Kosong/Terpotong) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px !important;
    border: 1px solid rgba(0, 242, 254, 0.35) !important;
    box-shadow: 0 0 16px rgba(0, 242, 254, 0.08) !important;
    background-color: rgba(255, 255, 255, 0.02) !important;
    padding: 18px !important;
}

/* Tombol Eksekusi Bergradasi Oranye */
.stButton > button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    background: linear-gradient(90deg, #ff7b00, #e65c00) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 0 14px rgba(255, 123, 0, 0.45) !important;
    transition: all 0.3s ease-in-out !important;
    margin-top: 10px;
}

.stButton > button:hover {
    box-shadow: 0 0 24px rgba(255, 123, 0, 0.8) !important;
    transform: translateY(-1px);
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# 3. Header Judul
st.markdown(
    """
    <div class="hero-wrapper">
        <span class="hero-icon">⚡</span>
        <span class="title-sekolah">SEKOLAH</span>
        <span class="title-kita">KITA</span>
        <span class="title-ai">AI</span>
    </div>
    """,
    unsafe_allow_html=True
)
st.caption("Platform Tata Kelola Sekolah, Modul Ajar, dan Administrasi Terintegrasi")
st.markdown('<div class="neon-glow-bar"></div>', unsafe_allow_html=True)

# 4. Panel Samping (Sidebar)
with st.sidebar:
    st.header("⚙️ Pengaturan")
    secret_key = st.secrets.get("GEMINI_API_KEY", "")
    if secret_key:
        api_key = secret_key
        st.success("✅ API Key terhubung otomatis")
    else:
        api_key = st.text_input("Masukkan Gemini API Key:", type="password")
        st.markdown("[Dapatkan API Key di Google AI Studio](https://aistudio.google.com/)")

SYSTEM_INSTRUCTION = """
Anda adalah "SekolahKita AI", asisten komprehensif tata kelola sekolah, perancangan instruksional, dan operasional tenaga kependidikan.
Tugas Anda membantu menyusun dokumen manajerial, modul ajar, catatan rapor, tata tertib, naskah dinas, dan materi presentasi sesuai peran pengguna.
Gunakan bahasa Indonesia baku, formal, dan rapi sesuai tata naskah dinas pendidikan.
Sajikan langsung format dokumen siap pakai tanpa basa-basi pembuka.
"""

if "generated_doc" not in st.session_state:
    st.session_state.generated_doc = ""

# 5. Tata Letak Dashboard Layar Laptop (Rasio 1 : 1.4)
col_input, col_canvas = st.columns([1, 1.4], gap="large")

with col_input:
    st.markdown("### 🎛️ Studio Rancangan")
    with st.container(border=True):
        role = st.selectbox(
            "Pilih Peran Anda:",
            [
                "Wali Kelas",
                "Guru Mata Pelajaran",
                "Kepala Sekolah",
                "Tim Kurikulum",
                "Tim Kesiswaan",
                "Tata Usaha (TU)"
            ]
        )
        doc_type = st.text_input(
            "Jenis Dokumen / Administrasi:",
            placeholder="Contoh: Modul Ajar, Catatan Rapor"
        )
        details = st.text_area(
            "Detail Tambahan / Konteks:",
            placeholder="Kriteria siswa, topik materi, atau instruksi tata letak visual...",
            height=180
        )
        btn_generate = st.button("🚀 Susun ke Kanvas", use_container_width=True)

with col_canvas:
    st.markdown("### 📄 Kanvas Dokumen")
    canvas_box = st.container(border=True)

# Logika Pembuatan Naskah dengan Streaming Cepat
if btn_generate:
    if not api_key:
        st.error("Silakan masukkan Gemini API Key di menu samping terlebih dahulu.")
    elif not doc_type:
        st.warning("Mohon sebutkan jenis dokumen yang ingin dibuat.")
    else:
        with st.spinner("Sedang meracik naskah ke kanvas..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt_input = f"Peran: {role}\nJenis Dokumen: {doc_type}\nKonteks/Detail: {details}"
                
                # Streaming respon agar teks langsung mengalir seketika
                response_stream = client.models.generate_content_stream(
                    model="gemini-3.6-flash",
                    contents=prompt_input,
                    config={"system_instruction": SYSTEM_INSTRUCTION}
                )
                
                full_text = ""
                with canvas_box:
                    stream_placeholder = st.empty()
                    for chunk in response_stream:
                        full_text += chunk.text
                        stream_placeholder.markdown(full_text)
                
                st.session_state.generated_doc = full_text
                st.rerun()
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# Tampilan Kanvas Setelah Selesai Dirakit
with canvas_box:
    if st.session_state.generated_doc:
        tab_view, tab_copy = st.tabs(["👁️ Tampilan Dokumen", "📋 Format Salin ke Canva"])
        
        with tab_view:
            st.markdown(st.session_state.generated_doc)
        
        with tab_copy:
            st.caption("Klik ikon salin di pojok kanan atas kotak ini untuk menempelkannya langsung ke Canva:")
            st.code(st.session_state.generated_doc, language="markdown")
    elif not btn_generate:
        st.info("Draf dokumen dinas atau rancangan administrasi akan tampil di lembar kanvas ini.")
