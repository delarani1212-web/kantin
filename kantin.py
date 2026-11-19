
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# =================================
# CLASS PRODUK
# =================================

class Produk:
    def __init__(self, nama, kategori, harga, jumlah):
        self.nama = nama
        self.kategori = kategori
        self.harga = harga
        self.jumlah = jumlah

    # Method untuk mengubah data
    def ubah_produk(self, nama, kategori, harga, jumlah):
        self.nama = nama
        self.kategori = kategori
        self.harga = harga
        self.jumlah = jumlah

    # Method untuk menghitung total stok
    def total_stok(self):
        return self.jumlah


# =================================
# SESSION STATE
# =================================

if "data_produk" not in st.session_state:
    st.session_state.data_produk = [
        Produk("Nasi Goreng", "Makanan", 15000, 10),
        Produk("Es Teh", "Minuman", 5000, 20),
        Produk("Roti Bakar", "Makanan", 10000, 8),
        Produk("Air Mineral", "Minuman", 4000, 15)
    ]


# =================================
# JUDUL APLIKASI
# =================================

st.set_page_config(
    page_title="Aplikasi Kantin",
    page_icon="🍜",
    layout="wide"
)

st.title("🍜 Aplikasi Manajemen Kantin")
st.write("Sistem pengelolaan data produk kantin menggunakan Python dan Streamlit.")

st.divider()


# =================================
# MENU NAVIGASI
# =================================

with st.sidebar:
    st.title("MENU UTAMA")

    menu = option_menu(
        menu_title=None,
        options=[
            "Beranda",
            "Data Produk",
            "Tambah Produk",
            "Kelola Produk"
        ],
        icons=[
            "house",
            "table",
            "plus-circle",
            "gear"
        ],
        default_index=0
    )


# =================================
# MENU BERANDA
# =================================

if menu == "Beranda":

    st.subheader("Dashboard Kantin")
    st.write("Selamat datang di aplikasi manajemen data produk kantin.")

    total_produk = len(st.session_state.data_produk)

    total_stok = sum(
        produk.total_stok()
        for produk in st.session_state.data_produk
    )

    total_nilai = sum(
        produk.harga * produk.jumlah
        for produk in st.session_state.data_produk
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Produk", total_produk)
    col2.metric("Total Stok", total_stok)
    col3.metric("Nilai Persediaan", f"Rp {total_nilai:,}")

    st.divider()

    st.subheader("Informasi Aplikasi")
    st.write("""
    Aplikasi ini digunakan untuk membantu pengelolaan
    produk kantin, seperti makanan dan minuman.

    Pengguna dapat menambahkan produk, melihat data,
    mengubah informasi produk, serta menghapus produk.
    """)


# =================================
# MENU DATA PRODUK
# =================================

elif menu == "Data Produk":

    st.subheader("📋 Daftar Data Produk")

    if len(st.session_state.data_produk) > 0:

        data = []

        for i, produk in enumerate(st.session_state.data_produk):
            data.append({
                "No": i + 1,
                "Nama Produk": produk.nama,
                "Kategori": produk.kategori,
                "Harga": produk.harga,
                "Jumlah Stok": produk.jumlah
            })

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Belum ada data produk.")


# =================================
# MENU TAMBAH PRODUK
# =================================

elif menu == "Tambah Produk":

    st.subheader("➕ Tambah Produk Baru")

    with st.form("form_tambah_produk"):

        nama = st.text_input("Nama Produk")

        kategori = st.selectbox(
            "Kategori",
            ["Makanan", "Minuman", "Alat Tulis",
             "Elektronik", "Pakaian"]
        )

        harga = st.number_input(
            "Harga Produk (Rp)",
            min_value=0,
            step=1000
        )

        jumlah = st.number_input(
            "Jumlah Stok",
            min_value=0,
            step=1
        )

        simpan = st.form_submit_button("Simpan Produk")

        if simpan:

            if nama.strip() == "":
                st.error("Nama produk harus diisi!")

            elif harga <= 0:
                st.error("Harga produk harus lebih dari 0!")

            else:
                produk_baru = Produk(
                    nama,
                    kategori,
                    harga,
                    jumlah
                )

                st.session_state.data_produk.append(
                    produk_baru
                )

                st.success("Produk berhasil ditambahkan!")
                st.rerun()


# =================================
# MENU KELOLA PRODUK
# =================================

elif menu == "Kelola Produk":

    st.subheader("⚙️ Kelola Data Produk")

    if len(st.session_state.data_produk) > 0:

        pilihan = st.selectbox(
            "Pilih Produk",
            range(len(st.session_state.data_produk)),
            format_func=lambda i: st.session_state.data_produk[i].nama
        )

        produk = st.session_state.data_produk[pilihan]

        st.divider()

        st.write("### Ubah Data Produk")

        with st.form("form_ubah_produk"):

            nama_baru = st.text_input(
                "Nama Produk",
                value=produk.nama
            )

            kategori_baru = st.selectbox(
                "Kategori",
                ["Makanan", "Minuman", "Alat Tulis",
                 "Elektronik", "Pakaian"],
                index=[
                    "Makanan", "Minuman", "Alat Tulis",
                    "Elektronik", "Pakaian"
                ].index(produk.kategori)
            )

            harga_baru = st.number_input(
                "Harga",
                min_value=0,
                value=int(produk.harga),
                step=1000
            )

            jumlah_baru = st.number_input(
                "Jumlah Stok",
                min_value=0,
                value=int(produk.jumlah),
                step=1
            )

            ubah = st.form_submit_button("Ubah Data")

            if ubah:

                if nama_baru.strip() == "":
                    st.error("Nama produk tidak boleh kosong!")

                elif harga_baru <= 0:
                    st.error("Harga harus lebih dari 0!")

                else:
                    produk.ubah_produk(
                        nama_baru,
                        kategori_baru,
                        harga_baru,
                        jumlah_baru
                    )

                    st.success("Data produk berhasil diubah!")
                    st.rerun()

        st.divider()

        st.write("### Hapus Produk")

        st.warning(
            f"Produk yang dipilih: {produk.nama}"
        )

        if st.button("Hapus Produk", type="primary"):

            st.session_state.data_produk.pop(pilihan)

            st.success("Produk berhasil dihapus!")
            st.rerun()

    else:
        st.info("Tidak ada produk yang dapat dikelola.")
