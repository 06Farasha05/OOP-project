from abc import ABC, abstractmethod
from datetime import datetime


class Tiket(ABC):
    def __init__(self, id_tiket: str, penerbangan, kursi):
        self.id_tiket = id_tiket
        self.penerbangan = penerbangan
        self.kursi = kursi

    @abstractmethod
    def hitung_harga(self) -> float:
        pass


class TiketEkonomi(Tiket):
    def hitung_harga(self) -> float:
        return self.penerbangan.harga


class TiketBisnis(Tiket):
    def hitung_harga(self) -> float:
        # Kelas Bisnis dikenakan tarif 1.5x dari harga dasar penerbangan
        return self.penerbangan.harga * 1.5


class Pemesanan:
    def __init__(self, nomor_pemesanan: str, pelanggan, penerbangan, list_kursi: list):
        self.nomor_pemesanan = nomor_pemesanan
        self.pelanggan = pelanggan
        self.penerbangan = penerbangan
        self.daftar_tiket = []               # Composition (1 *-- 1..*)
        self.status_pemesanan = "MENUNGGU PEMBAYARAN"
        self.tanggal_pesan = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Membuat objek Tiket sesuai kelas kursi yang dipesan (Polymorphism)
        for idx, kursi in enumerate(list_kursi, start=1):
            id_tkt = f"TKT-{nomor_pemesanan}-{idx}"
            if kursi.kelas == "Bisnis":
                tiket = TiketBisnis(id_tkt, penerbangan, kursi)
            else:
                tiket = TiketEkonomi(id_tkt, penerbangan, kursi)
            self.daftar_tiket.append(tiket)

    def hitung_total_bayar(self) -> float:
        return sum(t.hitung_harga() for t in self.daftar_tiket)

    def ubah_status(self, status: str) -> None:
        self.status_pemesanan = status

    def batalkan_pemesanan(self) -> None:
        if self.status_pemesanan == "DIBATALKAN":
            print("[!] Pemesanan ini sudah dibatalkan sebelumnya.")
            return
        if self.status_pemesanan == "MENGAJUKAN PEMBATALAN":
            print("[i] Pengajuan pembatalan sudah dikirim dan sedang menunggu konfirmasi Admin.")
            return

        # Tahap 1: Jika belum ada pembayaran, langsung batal otomatis
        if self.status_pemesanan == "MENUNGGU PEMBAYARAN":
            for tiket in self.daftar_tiket:
                tiket.kursi.kosongkan_kursi()
            self.status_pemesanan = "DIBATALKAN"
            print(f"[✓] Pemesanan {self.nomor_pemesanan} langsung dibatalkan & kursi kembali TERSEDIA.")

        # Tahap 2: Jika sudah dibayar/lunas, wajib melalui persetujuan Admin
        elif self.status_pemesanan in ("MENUNGGU VERIFIKASI", "LUNAS"):
            self.status_pemesanan = "MENGAJUKAN PEMBATALAN"
            print(f"[✓] Pengajuan pembatalan {self.nomor_pemesanan} terkirim. Menunggu konfirmasi Admin.")

    def hitung_refund(self) -> float:
        # Refund 70% dari total pembayaran tiket
        return self.hitung_total_bayar() * 0.70