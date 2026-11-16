

class Pengguna:
    def __init__(self, id_pengguna: str, username: str, password: str, nama: str, email: str, status_aktif: bool = True):
        self._id_pengguna = id_pengguna      # Protected (#)
        self.__username = username           # Private (-)
        self.__password = password           # Private (-)
        self.nama = nama                     # Public (+)
        self.__email = email                 # Private (-)
        self.status_aktif = status_aktif     # Public (+)

    @property
    def id_pengguna(self) -> str:
        return self._id_pengguna

    @property
    def username(self) -> str:
        return self.__username

    @property
    def email(self) -> str:
        return self.__email

    def verifikasi_login(self, u: str, p: str) -> bool:
        if self.__username == u and self.__password == p:
            if not self.status_aktif:
                print(f"[!] Akun '{u}' sedang dinonaktifkan oleh Admin.")
                return False
            return True
        return False

    def kelola_profil(self, n: str, e: str) -> None:
        if n.strip():
            self.nama = n.strip()
        if e.strip():
            self.__email = e.strip()
        print(f"[✓] Profil diperbarui -> Nama: {self.nama} | Email: {self.__email}")


class Pelanggan(Pengguna):
    def __init__(self, id_pengguna: str, username: str, password: str, nama: str, email: str):
        super().__init__(id_pengguna, username, password, nama, email)
        self.riwayat_pemesanan = []


class Admin(Pengguna):
    def ubah_status_akun(self, target: Pengguna, status: bool) -> None:
        if isinstance(target, Admin):
            print("[!] Tidak dapat menonaktifkan sesama akun Admin.")
            return
        target.status_aktif = status
        ket = "AKTIF" if status else "NONAKTIF"
        print(f"[✓] Status akun '{target.username}' ({target.nama}) diubah menjadi {ket}.")

    def konfirmasi_pembatalan(self, pemesanan, daftar_pembayaran: list, setuju: bool) -> None:
        if pemesanan.status_pemesanan != "MENGAJUKAN PEMBATALAN":
            print("[!] Pemesanan ini tidak dalam status pengajuan pembatalan.")
            return

        byr = next((b for b in daftar_pembayaran if b.pemesanan == pemesanan and b.status_pembayaran == "TERVERIFIKASI"), None)

        if setuju:
            for tiket in pemesanan.daftar_tiket:
                tiket.kursi.kosongkan_kursi()

            pemesanan.ubah_status("DIBATALKAN")

            if byr:
                nominal_refund = pemesanan.hitung_refund()
                byr.set_status_pembayaran("REFUND 70%")
                print(
                    f"[✓] Pembatalan {pemesanan.nomor_pemesanan} DISETUJUI.\n"
                    f"    Kursi dilepas | Refund 70%: Rp{nominal_refund:,.0f} "
                    f"(Biaya pembatalan 30%: Rp{byr.jumlah - nominal_refund:,.0f})"
                )
            else:
                print(f"[✓] Pembatalan {pemesanan.nomor_pemesanan} DISETUJUI (belum ada dana masuk).")
        else:
            pemesanan.ubah_status("LUNAS" if byr else "MENUNGGU VERIFIKASI")
            print(f"[i] Pengajuan pembatalan {pemesanan.nomor_pemesanan} DITOLAK.")


class PetugasMaskapai(Pengguna):
    def tambah_penerbangan(self, daftar_penerbangan: list, penerbangan_baru) -> None:
        daftar_penerbangan.append(penerbangan_baru)
        print(f"[✓] Penerbangan {penerbangan_baru.kode_penerbangan} berhasil ditambahkan.")

    def hapus_penerbangan(self, daftar_penerbangan: list, kode: str) -> None:
        for i, p in enumerate(daftar_penerbangan):
            if p.kode_penerbangan.upper() == kode.upper():
                daftar_penerbangan.pop(i)
                print(f"[✓] Penerbangan {kode.upper()} berhasil dihapus.")
                return
        print(f"[!] Kode penerbangan '{kode}' tidak ditemukan.")


class PetugasPembayaran(Pengguna):
    def verifikasi_transaksi(self, pembayaran, pemesanan) -> None:
        pembayaran.set_status_pembayaran("TERVERIFIKASI")
        pemesanan.ubah_status("LUNAS")
        print(f"[✓] Pembayaran {pembayaran.id_pembayaran} TERVERIFIKASI. Tiket {pemesanan.nomor_pemesanan} resmi diterbitkan.")