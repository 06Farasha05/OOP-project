from abc import ABC, abstractmethod


class Pembayaran(ABC):
    def __init__(self, id_pembayaran: str, pemesanan, jumlah: float):
        self.id_pembayaran = id_pembayaran
        self.pemesanan = pemesanan
        self.__jumlah = jumlah                              # Private (-)
        self.__status_pembayaran = "MENUNGGU VERIFIKASI"    # Private (-)

    @property
    def jumlah(self) -> float:
        return self.__jumlah

    @property
    def status_pembayaran(self) -> str:
        return self.__status_pembayaran

    def set_status_pembayaran(self, status: str) -> None:
        self.__status_pembayaran = status

    @abstractmethod
    def proses_pembayaran(self) -> str:
        pass


class PembayaranTransfer(Pembayaran):
    def __init__(self, id_pembayaran: str, pemesanan, jumlah: float, rekening_tujuan: str):
        super().__init__(id_pembayaran, pemesanan, jumlah)
        self.rekening_tujuan = rekening_tujuan

    def proses_pembayaran(self) -> str:
        return (
            f"Transfer Bank ke Rekening {self.rekening_tujuan} | "
            f"Nominal: Rp{self.jumlah:,.0f} | Status: {self.status_pembayaran}"
        )


class PembayaranEWallet(Pembayaran):
    def __init__(self, id_pembayaran: str, pemesanan, jumlah: float, provider: str):
        super().__init__(id_pembayaran, pemesanan, jumlah)
        self.provider = provider

    def proses_pembayaran(self) -> str:
        return (
            f"Pembayaran E-Wallet ({self.provider}) | "
            f"Nominal: Rp{self.jumlah:,.0f} | Status: {self.status_pembayaran}"
        )


class Laporan:
    def __init__(self, periode: str):
        self.periode = periode

    def rekap_penjualan(self, daftar_pembayaran: list) -> tuple:
        total_transaksi = 0
        total_pendapatan = 0.0

        for b in daftar_pembayaran:
            if b.status_pembayaran == "TERVERIFIKASI":
                total_transaksi += 1
                total_pendapatan += b.jumlah
            elif b.status_pembayaran == "REFUND 70%":
                # 70% dikembalikan ke pelanggan, 30% tetap menjadi pendapatan maskapai
                total_pendapatan += b.jumlah * 0.30

        return total_transaksi, total_pendapatan