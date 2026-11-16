from models.pengguna import Pelanggan, Admin, PetugasMaskapai, PetugasPembayaran
from models.penerbangan import Pesawat, Rute, Penerbangan
from models.pemesanan import Pemesanan
from models.pembayaran import PembayaranTransfer, PembayaranEWallet, Laporan

def inisialisasi_data():
    # Data Akun Default untuk Simulasi 4 Aktor
    daftar_pengguna = [
        Pelanggan("USR-01", "budi", "123", "Budi Santoso", "budi@email.com"),
        Admin("ADM-01", "admin", "123", "Siti Rahma (Admin)", "admin@airline.com"),
        PetugasMaskapai("MSK-01", "maskapai", "123", "Andi Wijaya (Maskapai)", "ops@airline.com"),
        PetugasPembayaran("BYR-01", "kasir", "123", "Rina Kusuma (Finance)", "finance@airline.com"),
    ]

    # Data Penerbangan Awal
    p1 = Penerbangan(
        "GA-101",
        Pesawat("PK-GIA", "Boeing 737-800", 6),
        Rute("RT-01", "Jakarta (CGK)", "Denpasar (DPS)"),
        "2026-12-01 08:00",
        1200000,
    )
    p2 = Penerbangan(
        "JT-205",
        Pesawat("PK-LNI", "Airbus A320", 6),
        Rute("RT-02", "Surabaya (SUB)", "Makassar (UPG)"),
        "2026-12-02 13:30",
        950000,
    )
    return daftar_pengguna, [p1, p2], [], []


def tampilkan_penerbangan(daftar_penerbangan):
    print("\n--- DAFTAR JADWAL PENERBANGAN ---")
    if not daftar_penerbangan:
        print("Belum ada jadwal penerbangan.")
        return
    for p in daftar_penerbangan:
        sisa = len(p.cek_ketersediaan_kursi())
        print(
            f"[{p.kode_penerbangan}] {p.rute.asal} -> {p.rute.tujuan} | "
            f"Jadwal: {p.jadwal} | Pesawat: {p.pesawat.jenis} | "
            f"Harga Ekonomi: Rp{p.harga:,.0f} (Bisnis 1.5x) | Kursi Tersedia: {sisa}/{len(p.daftar_kursi)}"
        )


def menu_pelanggan(user: Pelanggan, daftar_penerbangan, daftar_pemesanan, daftar_pembayaran):
    while True:
        print(f"\n=== MENU PELANGGAN ({user.nama}) ===")
        print("1. Cari Penerbangan & Cek Kursi")
        print("2. Pesan Tiket")
        print("3. Bayar Tiket")
        print("4. Lihat Riwayat Pemesanan & Unduh E-Tiket")
        print("5. Batalkan Pemesanan")
        print("6. Kelola Profil")
        print("0. Switch Session / Logout")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            tampilkan_penerbangan(daftar_penerbangan)
            kode = input("Masukkan kode penerbangan untuk detail kursi (Enter untuk batal): ").strip()
            if kode:
                target = next((p for p in daftar_penerbangan if p.kode_penerbangan.upper() == kode.upper()), None)
                if target:
                    kursi_str = ", ".join(f"{k.nomor_kursi}({k.kelas}-{k.status_kursi})" for k in target.daftar_kursi)
                    print(f"Detail Kursi {target.kode_penerbangan}: {kursi_str}")
                else:
                    print("[!] Penerbangan tidak ditemukan.")

        elif pilih == "2":
            tampilkan_penerbangan(daftar_penerbangan)
            kode = input("Masukkan kode penerbangan yang dipilih: ").strip()
            target = next((p for p in daftar_penerbangan if p.kode_penerbangan.upper() == kode.upper()), None)
            if not target:
                print("[!] Penerbangan tidak ditemukan.")
                continue

            tersedia = target.cek_ketersediaan_kursi()
            if not tersedia:
                print("[!] Maaf, seluruh kursi pada penerbangan ini sudah penuh.")
                continue

            print("Kursi Tersedia:", ", ".join(f"{k.nomor_kursi} [{k.kelas}]" for k in tersedia))
            pilihan_kursi = input("Masukkan nomor kursi (pisahkan koma jika >1, misal: B1,E1): ").upper().split(",")
            kursi_dipilih = []
            for no in [x.strip() for x in pilihan_kursi if x.strip()]:
                obj_kursi = next((k for k in tersedia if k.nomor_kursi == no), None)
                if obj_kursi and obj_kursi.pesan_kursi():
                    kursi_dipilih.append(obj_kursi)
                else:
                    print(f"[!] Kursi '{no}' tidak valid atau sudah terisi.")

            if kursi_dipilih:
                no_pms = f"ORD-{len(daftar_pemesanan) + 1:03d}"
                pms = Pemesanan(no_pms, user, target, kursi_dipilih)
                daftar_pemesanan.append(pms)
                user.riwayat_pemesanan.append(pms)
                print(f"[✓] Pemesanan berhasil dibuat! Nomor Order: {no_pms} | Total Tagihan: Rp{pms.hitung_total_bayar():,.0f}")

        elif pilih == "3":
            belum_bayar = [p for p in user.riwayat_pemesanan if p.status_pemesanan == "MENUNGGU PEMBAYARAN"]
            if not belum_bayar:
                print("[!] Tidak ada tagihan pemesanan yang menunggu pembayaran.")
                continue
            for p in belum_bayar:
                print(f"- {p.nomor_pemesanan} | {p.penerbangan.kode_penerbangan} | Total: Rp{p.hitung_total_bayar():,.0f}")

            no_pms = input("Masukkan Nomor Pemesanan yang akan dibayar: ").strip().upper()
            pms = next((p for p in belum_bayar if p.nomor_pemesanan == no_pms), None)
            if not pms:
                print("[!] Nomor pemesanan tidak ditemukan.")
                continue

            print("Pilih Metode Pembayaran: [1] Transfer Bank  [2] E-Wallet")
            metode = input("Pilihan (1/2): ").strip()
            id_byr = f"PAY-{len(daftar_pembayaran) + 1:03d}"
            if metode == "1":
                rek = input("Masukkan Nomor Rekening Tujuan (misal: BCA 12345678): ").strip() or "BCA 8800112233"
                byr = PembayaranTransfer(id_byr, pms, pms.hitung_total_bayar(), rek)
            else:
                prov = input("Masukkan Nama E-Wallet (GoPay/OVO/DANA): ").strip() or "GoPay"
                byr = PembayaranEWallet(id_byr, pms, pms.hitung_total_bayar(), prov)

            daftar_pembayaran.append(byr)
            pms.ubah_status("MENUNGGU VERIFIKASI")
            print(f"[✓] Pembayaran tercatat ({id_byr}): {byr.proses_pembayaran()}")
            print("    Silakan Switch Session ke 'Petugas Pembayaran' untuk memverifikasi pembayaran ini.")

        elif pilih == "4":
            print(f"\n--- RIWAYAT PEMESANAN ({user.nama}) ---")
            if not user.riwayat_pemesanan:
                print("Belum ada riwayat pemesanan.")
                continue
            for p in user.riwayat_pemesanan:
                print(f"\nOrder: {p.nomor_pemesanan} | Rute: {p.penerbangan.rute.asal} -> {p.penerbangan.rute.tujuan}")
                print(f"Tanggal Pesan: {p.tanggal_pesan} | Total: Rp{p.hitung_total_bayar():,.0f} | Status: {p.status_pemesanan}")
                if p.status_pemesanan == "LUNAS":
                    print("  === E-TIKET RESMI DITERBITKAN ===")
                    for t in p.daftar_tiket:
                        print(f"  * {t.id_tiket} | Kursi: {t.kursi.nomor_kursi} ({t.kursi.kelas}) | Harga: Rp{t.hitung_harga():,.0f}")
                if p.status_pemesanan == "DIBATALKAN":
                    print(f"  [STATUS] Pemesanan dibatalkan (Estimasi Refund 70% jika sudah lunas: Rp{p.hitung_refund():,.0f})")

        elif pilih == "5":
            aktif = [p for p in user.riwayat_pemesanan if p.status_pemesanan in ("MENUNGGU PEMBAYARAN", "MENUNGGU VERIFIKASI", "LUNAS")]
            if not aktif:
                print("[!] Tidak ada pemesanan aktif yang bisa dibatalkan.")
                continue
            for p in aktif:
                print(f"- {p.nomor_pemesanan} ({p.penerbangan.kode_penerbangan}) | Status: {p.status_pemesanan}")
            no_pms = input("Masukkan Nomor Pemesanan yang dibatalkan: ").strip().upper()
            pms = next((p for p in aktif if p.nomor_pemesanan == no_pms), None)
            if pms:
                pms.batalkan_pemesanan()
            else:
                print("[!] Pemesanan tidak ditemukan.")

        elif pilih == "6":
            nama_baru = input(f"Nama baru (Enter tetap '{user.nama}'): ")
            email_baru = input(f"Email baru (Enter tetap '{user.email}'): ")
            user.kelola_profil(nama_baru, email_baru)

        elif pilih == "0":
            break


def menu_admin(user: Admin, daftar_pengguna, daftar_pemesanan , daftar_pembayaran):
    while True:
        print(f"\n=== MENU ADMIN ({user.nama}) ===")
        print("1. Kelola status Akun Pengguna (Aktifkan / Nonaktifkan).")
        print("2. Lihat Laporan Penjualan.")
        print("3. Konfirmasi Pembatalan Pesanan Tiket.")
        print("0. Switch Session / Logout")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            print("\n--- DAFTAR AKUN PENGGUNA ---")
            for u in daftar_pengguna:
                st = "AKTIF" if u.status_aktif else "NONAKTIF"
                print(f"- [{u.id_pengguna}] {u.username} | {u.nama} ({type(u).__name__}) | Status: {st}")
            uname = input("Masukkan username yang akan diubah statusnya: ").strip()
            target = next((u for u in daftar_pengguna if u.username == uname), None)
            if target:
                aksi = input("Pilih status: [1] Aktifkan  [2] Nonaktifkan: ").strip()
                user.ubah_status_akun(target, aksi == "1")
            else:
                print("[!] Username tidak ditemukan.")

        elif pilih == "2":
            laporan = Laporan("Periode Berjalan 2026")
            jml, omzet = laporan.rekap_penjualan(daftar_pembayaran)
            print(f"\n--- REKAP LAPORAN PENJUALAN ({laporan.periode}) ---")
            print(f"Total Transaksi Terverifikasi : {jml} transaksi")
            print(f"Total Pendapatan Masuk        : Rp{omzet:,.0f}")
        
        elif pilih == "3":
            pengajuan = [
                p for u in daftar_pengguna if isinstance(u, Pelanggan)
                for p in u.riwayat_pemesanan if p.status_pemesanan == "MENGAJUKAN PEMBATALAN"
            ]
            if not pengajuan:
                print("[i] Tidak ada pengajuan pembatalan tiket saat ini.")
                continue

            print("\n--- DAFTAR PENGAJUAN PEMBATALAN TIKET ---")
            for p in pengajuan:
                print(f"- [{p.nomor_pemesanan}] Pelanggan: {p.pelanggan.nama} | Penerbangan: {p.penerbangan.kode_penerbangan} | Total: Rp{p.hitung_total_bayar():,.0f}")

            no_pms = input("\nMasukkan Nomor Pemesanan (atau Enter / 0 untuk batal): ").strip().upper()
            if not no_pms or no_pms == "0":
                continue

            target = next((p for p in pengajuan if p.nomor_pemesanan == no_pms), None)
            if not target:
                print("[!] Nomor pemesanan tidak ditemukan.")
                continue

            keputusan = input("Keputusan: [1] Setujui Pembatalan  [2] Tolak  [0] Batal: ").strip()
            if keputusan == "1":
                user.konfirmasi_pembatalan(target, daftar_pembayaran, True)
            elif keputusan == "2":
                user.konfirmasi_pembatalan(target, daftar_pembayaran, False)
        
        elif pilih == "0":
            break


def menu_maskapai(user: PetugasMaskapai, daftar_penerbangan):
    while True:
        print(f"\n=== MENU PETUGAS MASKAPAI ({user.nama}) ===")
        print("1. Lihat Semua Jadwal Penerbangan")
        print("2. Tambah Data Penerbangan Baru")
        print("3. Ubah Harga Dasar Penerbangan")
        print("4. Hapus Penerbangan")
        print("0. Switch Session / Logout")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            tampilkan_penerbangan(daftar_penerbangan)

        elif pilih == "2":
            kode = input("Kode Penerbangan (misal: ID-701): ").strip().upper()
            kd_pswt = input("Kode Pesawat (misal: PK-BTK): ").strip().upper()
            jns_pswt = input("Jenis Pesawat (misal: Airbus A320): ").strip()
            asal = input("Kota Asal (misal: Jakarta (CGK)): ").strip()
            tujuan = input("Kota Tujuan (misal: Medan (KNO)): ").strip()
            jadwal = input("Jadwal Keberangkatan (YYYY-MM-DD HH:MM): ").strip()
            harga = float(input("Harga Dasar Ekonomi (Rp): "))

            p_baru = Penerbangan(
                kode,
                Pesawat(kd_pswt, jns_pswt, 6),
                Rute(f"RT-{len(daftar_penerbangan) + 1:02d}", asal, tujuan),
                jadwal,
                harga,
            )
            user.tambah_penerbangan(daftar_penerbangan, p_baru)

        elif pilih == "3":
            tampilkan_penerbangan(daftar_penerbangan)
            kode = input("Masukkan kode penerbangan: ").strip().upper()
            target = next((p for p in daftar_penerbangan if p.kode_penerbangan == kode), None)
            if target:
                harga_baru = float(input("Masukkan harga baru (Rp): "))
                target.harga = harga_baru
                print(f"[✓] Harga penerbangan {kode} diperbarui menjadi Rp{target.harga:,.0f}.")
            else:
                print("[!] Kode penerbangan tidak ditemukan.")

        elif pilih == "4":
            kode = input("Masukkan kode penerbangan yang dihapus: ").strip()
            user.hapus_penerbangan(daftar_penerbangan, kode)

        elif pilih == "0":
            break


def menu_pembayaran(user: PetugasPembayaran, daftar_pembayaran):
    while True:
        print(f"\n=== MENU PETUGAS PEMBAYARAN ({user.nama}) ===")
        print("1. Verifikasi Pembayaran Masuk")
        print("2. Memantau Semua Transaksi & Rekap Laporan")
        print("0. Switch Session / Logout")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            pending = [b for b in daftar_pembayaran if b.status_pembayaran == "MENUNGGU VERIFIKASI"]
            if not pending:
                print("[!] Tidak ada pembayaran yang menunggu verifikasi.")
                continue
            for b in pending:
                print(f"- [{b.id_pembayaran}] Order: {b.pemesanan.nomor_pemesanan} | {b.proses_pembayaran()}")
            id_byr = input("Masukkan ID Pembayaran yang akan diverifikasi: ").strip().upper()
            target = next((b for b in pending if b.id_pembayaran == id_byr), None)
            if target:
                user.verifikasi_transaksi(target, target.pemesanan)
            else:
                print("[!] ID Pembayaran tidak ditemukan.")

        elif pilih == "2":
            print("\n--- DAFTAR SELURUH TRANSAKSI PEMBAYARAN ---")
            if not daftar_pembayaran:
                print("Belum ada transaksi pembayaran.")
            for b in daftar_pembayaran:
                print(f"- [{b.id_pembayaran}] Order {b.pemesanan.nomor_pemesanan} | {b.proses_pembayaran()}")

            laporan = Laporan("Periode Berjalan 2026")
            jml, omzet = laporan.rekap_penjualan(daftar_pembayaran)
            print(f"\nRekap Valid: {jml} Transaksi | Total Pendapatan: Rp{omzet:,.0f}")

        elif pilih == "0":
            break


def main():
    daftar_pengguna, daftar_penerbangan, daftar_pemesanan, daftar_pembayaran = inisialisasi_data()

    while True:
        print("\n=======================================================")
        print("   SISTEM MANAJEMEN PENJUALAN TIKET PESAWAT (OOP)      ")
        print("=======================================================")
        print("Akun Demo Tersedia (Password semua: 123):")
        print("  - Pelanggan          : budi")
        print("  - Admin              : admin")
        print("  - Petugas Maskapai   : maskapai")
        print("  - Petugas Pembayaran : kasir")
        print("-------------------------------------------------------")
        print("1. Login / Switch Session")
        print("2. Registrasi Akun Pelanggan Baru")
        print("0. Keluar Program")
        aksi = input("Pilihan: ").strip()

        if aksi == "1":
            uname = input("Username: ").strip()
            pwd = input("Password: ").strip()
            user_aktif = next((u for u in daftar_pengguna if u.verifikasi_login(uname, pwd)), None)

            if not user_aktif:
                print("[!] Login gagal. Periksa kembali username/password.")
                continue

            print(f"\n[✓] Berhasil masuk sebagai {user_aktif.nama} ({type(user_aktif).__name__})")
            if isinstance(user_aktif, Pelanggan):
                menu_pelanggan(user_aktif, daftar_penerbangan, daftar_pemesanan, daftar_pembayaran)
            elif isinstance(user_aktif, Admin):
                menu_admin(user_aktif, daftar_pengguna, daftar_pemesanan, daftar_pembayaran)
            elif isinstance(user_aktif, PetugasMaskapai):
                menu_maskapai(user_aktif, daftar_penerbangan)
            elif isinstance(user_aktif, PetugasPembayaran):
                menu_pembayaran(user_aktif, daftar_pembayaran)

        elif aksi == "2":
            print("\n--- REGISTRASI PELANGGAN BARU ---")
            nama = input("Nama Lengkap : ").strip()
            email = input("Email        : ").strip()
            uname = input("Username     : ").strip()
            pwd = input("Password     : ").strip()
            if any(u.username == uname for u in daftar_pengguna):
                print("[!] Username sudah digunakan.")
            else:
                baru = Pelanggan(f"USR-{len(daftar_pengguna) + 1:02d}", uname, pwd, nama, email)
                daftar_pengguna.append(baru)
                print(f"[✓] Akun '{uname}' berhasil didaftarkan! Silakan Login.")

        elif aksi == "0":
            print("Terima kasih telah menggunakan Sistem Manajemen Penjualan Tiket Pesawat.")
            break


if __name__ == "__main__":
    main()