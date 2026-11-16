from abc import ABC


class Pesawat:
    def __init__(self, kode_pesawat: str, jenis: str, kapasitas: int):
        self.kode_pesawat = kode_pesawat
        self.jenis = jenis
        self.kapasitas = kapasitas


class Rute:
    def __init__(self, id_rute: str, asal: str, tujuan: str):
        self.id_rute = id_rute
        self.asal = asal
        self.tujuan = tujuan


class Kursi(ABC):
    def __init__(self, nomor_kursi: str, kelas: str):
        self.nomor_kursi = nomor_kursi
        self._kelas = kelas                  # Protected (#)
        self.__status_kursi = "TERSEDIA"     # Private (-)

    @property
    def kelas(self) -> str:
        return self._kelas

    @property
    def status_kursi(self) -> str:
        return self.__status_kursi

    def pesan_kursi(self) -> bool:
        if self.__status_kursi == "TERSEDIA":
            self.__status_kursi = "TERISI"
            return True
        return False

    def kosongkan_kursi(self) -> None:
        self.__status_kursi = "TERSEDIA"


class KursiEkonomi(Kursi):
    def __init__(self, nomor_kursi: str):
        super().__init__(nomor_kursi, "Ekonomi")


class KursiBisnis(Kursi):
    def __init__(self, nomor_kursi: str):
        super().__init__(nomor_kursi, "Bisnis")


class Penerbangan:
    def __init__(self, kode_penerbangan: str, pesawat: Pesawat, rute: Rute, jadwal: str, harga: float, jml_bisnis: int = 2, jml_ekonomi: int = 4):
        self.kode_penerbangan = kode_penerbangan
        self.pesawat = pesawat               # Association (1 -> 1)
        self.rute = rute                     # Association (1 -> 1)
        self.jadwal = jadwal
        self.__harga = harga                 # Private (-)
        self.__daftar_kursi = []             # Composition (1 *-- 1..*)

        # Inisialisasi komposisi objek Kursi di dalam Penerbangan
        for i in range(1, jml_bisnis + 1):
            self.__daftar_kursi.append(KursiBisnis(f"B{i}"))
        for i in range(1, jml_ekonomi + 1):
            self.__daftar_kursi.append(KursiEkonomi(f"E{i}"))

    @property
    def harga(self) -> float:
        return self.__harga

    @harga.setter
    def harga(self, nilai_baru: float) -> None:
        if nilai_baru > 0:
            self.__harga = nilai_baru

    @property
    def daftar_kursi(self) -> list:
        return self.__daftar_kursi

    def cek_ketersediaan_kursi(self) -> list:
        return [k for k in self.__daftar_kursi if k.status_kursi == "TERSEDIA"]