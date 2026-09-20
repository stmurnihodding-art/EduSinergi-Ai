import streamlit as st
from google import genai

# 1. Konfigurasi Halaman Dashboard Laptop
st.set_page_config(
    page_title="SEKOLAHKITA AI - Canvas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Styling CSS Neon Bar & Layout 3 Kolom Simetris
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Syne:wght@700;800&family=Orbitron:wght@800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Judul Utama Dinamis SEKOLAHKITA AI */
.hero-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0px;
}

.hero-icon {
    font-size: 2.1rem;
    filter: drop-shadow(0 0 10px rgba(255, 123, 0, 0.7));
}

.title-brand {
    font-family: 'Syne', 'Orbitron', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    background: linear-gradient(135deg, #FFFFFF 0%, #F3F4F6 45%, #FF7B00 80%, #FFAE19 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 25px rgba(255, 123, 0, 0.35);
}

.title-ai {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.2rem;
    font-weight: 900;
    color: #00F2FE;
    letter-spacing: 2px;
    text-shadow: 0 0 16px rgba(0, 242, 254, 0.75);
}

/* Neon Glow Bar */
.neon-glow-bar {
    height: 3px;
    width: 100%;
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 35%, #ff7b00 70%, #ffae19 100%);
    border-radius: 4px;
    box-shadow: 0 0 10px rgba(0, 242, 254, 0.6), 0 0 18px rgba(255, 123, 0, 0.5);
    margin-top: 4px;
    margin-bottom: 14px;
}

/* Kotak Border Dinamis & Serasi */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px !important;
    border: 1px solid rgba(0, 242, 254, 0.35) !important;
    box-shadow: 0 0 16px rgba(0, 242, 254, 0.08) !important;
    background-color: rgba(255, 255, 255, 0.02) !important;
    padding: 10px 12px !important;
}

/* Ukuran Gambar Kartu Samping Vertikal */
div[data-testid="stImage"] img {
    height: 85px !important;
    width: 100% !important;
    object-fit: cover !important;
    border-radius: 6px !important;
}

div[data-testid="stCaptionContainer"] {
    text-align: center !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
    font-size: 0.78rem !important;
    margin-top: 3px !important;
}

/* Tombol Kartu Vertikal Samping */
.side-btn > button {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(0, 242, 254, 0.4) !important;
    color: #E2E8F0 !important;
    transition: all 0.2s ease-in-out !important;
    margin-top: 4px !important;
    padding: 4px 8px !important;
}

.side-btn > button:hover {
    background: linear-gradient(90deg, #ff7b00, #e65c00) !important;
    color: white !important;
    border-color: #ff7b00 !important;
    box-shadow: 0 0 12px rgba(255, 123, 0, 0.6) !important;
}

/* Tombol Eksekusi Utama di Studio Tengah */
.main-btn > button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    background: linear-gradient(90deg, #ff7b00, #e65c00) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 0 14px rgba(255, 123, 0, 0.45) !important;
    transition: all 0.3s ease-in-out !important;
    margin-top: 6px;
}

.main-btn > button:hover {
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
        <span class="title-brand">SEKOLAHKITA</span>
        <span class="title-ai">AI</span>
    </div>
    """,
    unsafe_allow_html=True
)
st.caption("Platform Tata Kelola Sekolah, Modul Ajar, dan Administrasi Terintegrasi")
st.markdown('<div class="neon-glow-bar"></div>', unsafe_allow_html=True)

# Inisialisasi State Formulir
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "Guru Mata Pelajaran"
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = ""
if "selected_details" not in st.session_state:
    st.session_state.selected_details = ""
if "generated_doc" not in st.session_state:
    st.session_state.generated_doc = ""

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
Anda adalah "SEKOLAHKITA AI", asisten komprehensif tata kelola sekolah, perancangan beban mengajar guru (JTM), perancangan kurikulum instruksional, dan operasional tenaga kependidikan.
Tugas Anda membantu menyusun matriks pembagian jam mengajar guru, dokumen manajerial, modul ajar, catatan rapor, tata tertib, naskah dinas SK resmi, dan materi presentasi visual siap pakai untuk Canva.
Gunakan bahasa Indonesia baku, formal, dan rapi sesuai tata naskah dinas pendidikan.
Sajikan langsung format dokumen atau matriks tabel siap pakai tanpa basa-basi pembuka.
"""

# 5. Tata Letak 3 Kolom: 2 Kartu Kiri - Studio Tengah - 2 Kartu Kanan (Rasio 1 : 1.8 : 1)
col_left, col_center, col_right = st.columns([1, 1.8, 1], gap="medium")

# --- SISI KIRI: 2 KARTU TERSUSUN VERTIKAL KE BAWAH ---
with col_left:
    st.markdown("##### 📁 Akselerator Kiri")
    
    # Kartu 1: Modul Ajar
    with st.container(border=True):
        st.image("https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=400&q=80", caption="Instruksional & Modul", use_container_width=True)
        st.markdown('<div class="side-btn">', unsafe_allow_html=True)
        if st.button("Pilih Modul Ajar", key="btn_tpl_1", use_container_width=True):
            st.session_state.selected_role = "Guru Mata Pelajaran"
            st.session_state.selected_doc = "Modul Ajar Kurikulum Merdeka"
            st.session_state.selected_details = "Rancang modul ajar komprehensif: Identitas modul, Capaian Pembelajaran (CP), Alur Tujuan Pembelajaran (ATP), skenario diferensiasi proses, lembar kerja siswa (LKPD), dan konsep infografik Canva."
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Kartu 2: Catatan Rapor
    with st.container(border=True):
        st.image("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&q=80", caption="Asesmen & Rapor", use_container_width=True)
        st.markdown('<div class="side-btn">', unsafe_allow_html=True)
        if st.button("Pilih Catatan Rapor", key="btn_tpl_2", use_container_width=True):
            st.session_state.selected_role = "Wali Kelas"
            st.session_state.selected_doc = "Catatan Wali Kelas untuk Buku Rapor"
            st.session_state.selected_details = "Kompilasi narasi catatan wali kelas yang konstruktif dan memotivasi: kategori siswa berprestasi, aktif ekstrakurikuler, pembinaan disiplin belajar dan kehadiran, serta penguatan Profil Pelajar Pancasila."
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- SISI TENGAH: STUDIO RANCANGAN SEIMBANG & SELARAS ---
roles_list = [
    "Guru Mata Pelajaran",
    "Wali Kelas",
    "Kepala Sekolah",
    "Tim Kurikulum",
    "Tim Kesiswaan",
    "Tata Usaha (TU)"
]
current_role_index = roles_list.index(st.session_state.selected_role) if st.session_state.selected_role in roles_list else 0

with col_center:
    st.markdown("##### 🎛️ Studio Rancangan")
    with st.container(border=True):
        role = st.selectbox(
            "Pilih Peran Anda:",
            roles_list,
            index=current_role_index
        )
        doc_type = st.text_input(
            "Jenis Dokumen / Administrasi:",
            value=st.session_state.selected_doc,
            placeholder="Contoh: Modul Ajar, Catatan Rapor, SK Pembagian Tugas"
        )
        details = st.text_area(
            "Detail Tambahan / Konteks:",
            value=st.session_state.selected_details,
            placeholder="Kriteria siswa, topik materi, target jam tatap muka (JTM), atau petunjuk tata letak Canva...",
            height=130
        )
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        btn_generate = st.button("🚀 Susun ke Kanvas", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- SISI KANAN: 2 KARTU TERSUSUN VERTIKAL KE BAWAH ---
with col_right:
    st.markdown("##### 📁 Akselerator Kanan")
    
    # Kartu 3: Regulasi & SK
    with st.container(border=True):
        st.image("https://images.unsplash.com/photo-1450133064473-71024230f91b?w=400&q=80", caption="Regulasi & SK Dinas", use_container_width=True)
        st.markdown('<div class="side-btn">', unsafe_allow_html=True)
        if st.button("Pilih Regulasi & SK", key="btn_tpl_3", use_container_width=True):
            st.session_state.selected_role = "Kepala Sekolah"
            st.session_state.selected_doc = "Surat Keputusan (SK) Beban Kerja & Tim Sekolah"
            st.session_state.selected_details = "Draf naskah dinas resmi SK Kepala Sekolah tentang Pembagian Tugas Mengajar Guru dan Bimbingan Konseling Tahun Ajaran Baru, lengkap dengan konsideran menimbang, mengingat, memutuskan, serta lampiran rincian jam tugas guru."
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Kartu 4: Kesiswaan & Tata Tertib
    with st.container(border=True):
        st.image("https://images.unsplash.com/photo-1577896851231-70ef18881754?w=400&q=80", caption="Kesiswaan & Disiplin", use_container_width=True)
        st.markdown('<div class="side-btn">', unsafe_allow_html=True)
        if st.button("Pilih Kesiswaan", key="btn_tpl_4", use_container_width=True):
            st.session_state.selected_role = "Tim Kesiswaan"
            st.session_state.selected_doc = "Program Kesiswaan & Tata Tertib Siswa"
            st.session_state.selected_details = "Buku panduan tata tertib dan matriks sistem poin penghargaan/pelanggaran siswa, program pembiasaan budaya positif, serta jadwal pelaksanaan Masa Pengenalan Lingkungan Sekolah (MPLS)."
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- BAGIAN BAWAH: KANVAS DOKUMEN MEMBENTANG PENUH ---
st.write("")
st.markdown("#### 📄 Kanvas Dokumen")
canvas_box = st.container(border=True)

# Logika Streaming Generasi
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

# Tampilan Hasil di Kanvas
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
