import streamlit as st
from google import genai

# 1. Konfigurasi Halaman Dashboard Laptop
st.set_page_config(
    page_title="SEKOLAHKITA AI - Canvas",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Styling CSS Neon Bar, Tipografi Dinamis & Layout Presisi
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Syne:wght@700;800&family=Orbitron:wght@800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Judul Utama Dinamis & Modern (SEKOLAHKITA Tersambung) */
.hero-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 2px;
}

.hero-icon {
    font-size: 2.3rem;
    filter: drop-shadow(0 0 10px rgba(255, 123, 0, 0.7));
}

.title-brand {
    font-family: 'Syne', 'Orbitron', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    background: linear-gradient(135deg, #FFFFFF 0%, #F3F4F6 45%, #FF7B00 80%, #FFAE19 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 25px rgba(255, 123, 0, 0.35);
}

.title-ai {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.5rem;
    font-weight: 900;
    color: #00F2FE;
    letter-spacing: 2px;
    text-shadow: 0 0 16px rgba(0, 242, 254, 0.75), 0 0 30px rgba(0, 242, 254, 0.4);
}

/* Garis Neon Bar Menyala Dua Aksen */
.neon-glow-bar {
    height: 4px;
    width: 100%;
    background: linear-gradient(90deg, #00f2fe 0%, #4facfe 35%, #ff7b00 70%, #ffae19 100%);
    border-radius: 4px;
    box-shadow: 0 0 12px rgba(0, 242, 254, 0.6), 0 0 22px rgba(255, 123, 0, 0.5);
    margin-top: 8px;
    margin-bottom: 22px;
}

/* Penyeragaman Tinggi Kotak Kartu agar Sejajar Rata */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px !important;
    border: 1px solid rgba(0, 242, 254, 0.35) !important;
    box-shadow: 0 0 16px rgba(0, 242, 254, 0.08) !important;
    background-color: rgba(255, 255, 255, 0.02) !important;
    padding: 16px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    min-height: 290px !important;
}

/* Ukuran Gambar Seragam & Pas di Layar */
div[data-testid="stImage"] img {
    height: 145px !important;
    width: 100% !important;
    object-fit: cover !important;
    border-radius: 8px !important;
}

/* Keterangan Teks Bawah Gambar */
div[data-testid="stCaptionContainer"] {
    text-align: center !important;
    font-weight: 600 !important;
    color: #E2E8F0 !important;
    margin-top: 6px !important;
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
    margin-top: 8px;
}

.stButton > button:hover {
    box-shadow: 0 0 24px rgba(255, 123, 0, 0.8) !important;
    transform: translateY(-1px);
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# 3. Header Judul (SEKOLAHKITA Bersambung & Font Dinamis)
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

# --- KARTU FOLDER MODERN DENGAN FOTO KONTEKS SEKOLAH RASIONAL ---
st.markdown("#### 🚀 Akselerator Administrasi Sekolah")
col_k1, col_k2, col_k3, col_k4 = st.columns(4)

with col_k1:
    with st.container(border=True):
        st.image("https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=500&auto=format&fit=crop&q=80", caption="Instruksional & Modul Ajar", use_container_width=True)
        if st.button("Pilih Modul Ajar", key="btn_tpl_1", use_container_width=True):
            st.session_state.selected_role = "Guru Mata Pelajaran"
            st.session_state.selected_doc = "Modul Ajar Kurikulum Merdeka"
            st.session_state.selected_details = "Rancang modul ajar komprehensif: Identitas modul, Capaian Pembelajaran (CP), Alur Tujuan Pembelajaran (ATP), skenario diferensiasi proses, lembar kerja siswa (LKPD), dan konsep infografik Canva."
            st.rerun()

with col_k2:
    with st.container(border=True):
        st.image("https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=500&auto=format&fit=crop&q=80", caption="Asesmen & Catatan Rapor", use_container_width=True)
        if st.button("Pilih Catatan Rapor", key="btn_tpl_2", use_container_width=True):
            st.session_state.selected_role = "Wali Kelas"
            st.session_state.selected_doc = "Catatan Wali Kelas untuk Buku Rapor"
            st.session_state.selected_details = "Kompilasi narasi catatan wali kelas yang konstruktif dan memotivasi: kategori siswa berprestasi, aktif ekstrakurikuler, pembinaan disiplin belajar dan kehadiran, serta penguatan Profil Pelajar Pancasila."
            st.rerun()

with col_k3:
    with st.container(border=True):
        st.image("https://images.unsplash.com/photo-1450133064473-71024230f91b?w=500&auto=format&fit=crop&q=80", caption="Regulasi & SK Kedinasan", use_container_width=True)
        if st.button("Pilih Regulasi & SK", key="btn_tpl_3", use_container_width=True):
            st.session_state.selected_role = "Kepala Sekolah"
            st.session_state.selected_doc = "Surat Keputusan (SK) Beban Kerja & Tim Sekolah"
            st.session_state.selected_details = "Draf naskah dinas resmi SK Kepala Sekolah tentang Pembagian Tugas Mengajar Guru dan Bimbingan Konseling Tahun Ajaran Baru, lengkap dengan konsideran menimbang, mengingat, memutuskan, serta lampiran rincian jam tugas guru."
            st.rerun()

with col_k4:
    with st.container(border=True):
        st.image("https://images.unsplash.com/photo-1577896851231-70ef18881754?w=500&auto=format&fit=crop&q=80", caption="Kesiswaan & Tata Tertib", use_container_width=True)
        if st.button("Pilih Kesiswaan", key="btn_tpl_4", use_container_width=True):
            st.session_state.selected_role = "Tim Kesiswaan"
            st.session_state.selected_doc = "Program Kesiswaan & Tata Tertib Siswa"
            st.session_state.selected_details = "Buku panduan tata tertib dan matriks sistem poin penghargaan/pelanggaran siswa, program pembiasaan budaya positif, serta jadwal pelaksanaan Masa Pengenalan Lingkungan Sekolah (MPLS)."
            st.rerun()

st.write("")

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

# 5. Tata Letak Dashboard Layar Laptop (Rasio 1 : 1.4)
col_input, col_canvas = st.columns([1, 1.4], gap="large")

roles_list = [
    "Wali Kelas",
    "Guru Mata Pelajaran",
    "Kepala Sekolah",
    "Tim Kurikulum",
    "Tim Kesiswaan",
    "Tata Usaha (TU)"
]
current_role_index = roles_list.index(st.session_state.selected_role) if st.session_state.selected_role in roles_list else 0

with col_input:
    st.markdown("### 🎛️ Studio Rancangan")
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
            placeholder="Kriteria siswa, topik materi, target jam tatap muka (JTM), atau petunjuk tata letak visual Canva...",
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
