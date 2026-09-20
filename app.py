import streamlit as st
from google import genai

# Konfigurasi Halaman (Responsif HP & Laptop)
st.set_page_config(
    page_title="EduSinergi AI",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 EduSinergi AI")
st.caption("Asisten Administrasi, Modul Ajar, dan Tata Kelola Sekolah")

# Pengaturan API Key di Panel Samping
with st.sidebar:
    st.header("Pengaturan")
    api_key = st.text_input("Masukkan Gemini API Key:", type="password")
    st.markdown("[Dapatkan API Key di Google AI Studio](https://aistudio.google.com/)")

# Pilihan Peran Pengguna
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
    placeholder="Contoh: Catatan Rapor Semester 1, Modul Ajar, Draf Surat Panggilan"
)

details = st.text_area(
    "Detail Tambahan / Konteks:",
    placeholder="Kriteria siswa, tujuan pembelajaran, topik materi, atau instruksi khusus...",
    height=120
)

SYSTEM_INSTRUCTION = """
Anda adalah "EduSinergi AI", asisten komprehensif tata kelola sekolah, perancangan instruksional, dan operasional tenaga kependidikan.
Tugas Anda membantu menyusun dokumen manajerial, modul ajar, catatan rapor, tata tertib, naskah dinas, dan materi presentasi sesuai peran pengguna.
Gunakan bahasa Indonesia baku, formal, dan rapi sesuai tata naskah dinas pendidikan.
Sajikan langsung format dokumen siap pakai (tabel, poin, atau naskah resmi) tanpa basa-basi pembuka.
"""

if st.button("🚀 Susun Dokumen", use_container_width=True):
    if not api_key:
        st.error("Silakan masukkan Gemini API Key di menu samping terlebih dahulu.")
    elif not doc_type:
        st.warning("Mohon sebutkan jenis dokumen yang ingin dibuat.")
    else:
        with st.spinner("Sedang menyusun dokumen..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt_input = f"Peran: {role}\nJenis Dokumen: {doc_type}\nKonteks/Detail: {details}"
                
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt_input,
                    config={"system_instruction": SYSTEM_INSTRUCTION}
                )
                
                st.success("Dokumen Berhasil Disusun!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
