import streamlit as st
from google import genai

# 1. Konfigurasi Halaman Wide
st.set_page_config(
    page_title="EduSinergi AI - Canvas",
    page_icon="⚡",
    layout="wide"
)

# 2. Styling CSS Neon Bar & Tipografi Modern
neon_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Orbitron:wght@600;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Judul Gradasi Futuristik */
.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #00c6ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 1.5px;
    margin-bottom: 4px;
}

/* Garis Neon Bar Menyala dengan Animasi Glow */
.neon-glow-bar {
    height: 4px;
    width: 100%;
    background: linear-gradient(90deg, #00f2fe, #4facfe, #0072ff, #00f2fe);
    background-size: 200% auto;
    border-radius: 4px;
    box-shadow: 0 0 10px #00f2fe, 0 0 20px #4facfe, 0 0 30px #0072ff;
    margin-top: 6px;
    margin-bottom: 25px;
    animation: neonFlow 3s linear infinite alternate;
}

@keyframes neonFlow {
    0% {
        background-position: 0% 50%;
        box-shadow: 0 0 8px #00f2fe, 0 0 16px #4facfe;
    }
    100% {
        background-position: 100% 50%;
        box-shadow: 0 0 16px #00f2fe, 0 0 28px #4facfe, 0 0 38px #0072ff;
    }
}

/* Bingkai Kotak Canvas Bercahaya Halus */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px !important;
    border: 1px solid rgba(0, 242, 254, 0.3) !important;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.12) !important;
    background-color: rgba(255, 255, 255, 0.02) !important;
}

/* Tombol Eksekusi Aksen Neon */
.stButton > button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    background: linear-gradient(90deg, #0052d4, #4364f7, #6fb1fc) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 0 12px rgba(67, 100, 247, 0.4) !important;
    transition: all 0.3s ease-in-out !important;
}

.stButton > button:hover {
    box-shadow: 0 0 22px rgba(0, 242, 254, 0.8) !important;
    transform: translateY(-1px);
}
</style>
"""

st.markdown(neon_css, unsafe_allow_html=True)

# 3. Header dengan Bilah Lampu Neon
st.markdown('<div class="hero-title">⚡ EDUSINERGI AI</div>', unsafe_allow_html=True)
st.caption("Platform Tata Kelola Sekolah, Modul Ajar, dan Administrasi Terintegrasi")
st.markdown('<div class="neon-glow-bar"></div>', unsafe_allow_html=True)

# 4. Pengaturan API Key di Sidebar
with st.sidebar:
    st.header("⚙️ Pengaturan")
    api_key = st.text_input("Masukkan Gemini API Key:", type="password")
    st.markdown("[Dapatkan API Key di Google AI Studio](https://aistudio.google.com/)")

SYSTEM_INSTRUCTION = """
Anda adalah "EduSinergi AI", asisten komprehensif tata kelola sekolah, perancangan instruksional, dan operasional tenaga kependidikan.
Tugas Anda membantu menyusun dokumen manajerial, modul ajar, catatan rapor, tata tertib, naskah dinas, dan materi presentasi sesuai peran pengguna.
Gunakan bahasa Indonesia baku, formal, dan rapi sesuai tata naskah dinas pendidikan.
Sajikan langsung format dokumen siap pakai (tabel, poin, atau naskah resmi) tanpa basa-basi pembuka.
"""

# 5. Format Tata Letak Canvas 2 Panel
col_input, col_canvas = st.columns([1, 1], gap="medium")

with col_input:
    st.markdown("### 📋 Parameter Dokumen")
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
        placeholder="Contoh: Catatan Rapor Semester 1, Modul Ajar"
    )
    details = st.text_area(
        "Detail Tambahan / Konteks:",
        placeholder="Kriteria siswa, topik materi, atau instruksi khusus...",
        height=160
    )
    btn_generate = st.button("🚀 Susun ke Canvas", use_container_width=True)

with col_canvas:
    st.markdown("### 📄 Lembar Kerja Dokumen (Canvas)")
    canvas_container = st.container(border=True)
    
    if btn_generate:
        if not api_key:
            st.error("Silakan masukkan Gemini API Key di menu samping terlebih dahulu.")
        elif not doc_type:
            st.warning("Mohon sebutkan jenis dokumen yang ingin dibuat.")
        else:
            with st.spinner("Sedang menyusun dokumen ke lembar canvas..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt_input = f"Peran: {role}\nJenis Dokumen: {doc_type}\nKonteks/Detail: {details}"
                    
                    response = client.models.generate_content(
                        model="gemini-2.5-pro",
                        contents=prompt_input,
                        config={"system_instruction": SYSTEM_INSTRUCTION}
                    )
                    
                    with canvas_container:
                        st.markdown(response.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
    else:
        with canvas_container:
            st.caption("Hasil dokumen dinas atau draf kerja akan ditampilkan langsung di lembar canvas ini.")
