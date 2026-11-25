# Self-score — Mode ④ (10 Prompt Nemesis), news-image-20261124

Penilaian jujur atas gambar final `entry.png` v6 (SHA256
`7d203750b025e51d40b9242f978774eee3e0183209d8d06b0085dc1e557300cf`,
1024×1024, 225,258 bytes) dan program `main.py`, setelah rebuild total
dari nol atas permintaan nemesis ("gambar peta gk jelas gambar newsnya
juga kayak apa itu kwkwk dahlah kamu lihat referensi top rank news
sebelumnya coba"). Dinilai dengan mata setelah membaca gambar hasil
render utuh + crop hero, grid, dan peta, ditambah verifikasi skrip
(wrap, lebar teks, jarak pin, determinisme), bukan dari niat.

## Total: 96 / 100 (v5: 96, v4: 95, v3: 93)

### Akurasi — 24 / 25 (tidak berubah)
- 35 cerita, semua bertanggal Selasa 24 Nov 2026 (UTC); 8 region; tiap
  cerita bernomor, berstatus (CONFIRMED/OFFICIAL/REPORTED/CLAIM), bersumber.
- Larangan riset dipatuhi: klaim ranjau Hormuz = CLAIM + "UNCONFIRMED"
  (bukan fakta); Shenzhou-24 hanya "crew named, launch 25 Nov"; COP31
  "ended 22 Nov" di DATE CHECK; penyelamatan Cartagena "finished early
  25 Nov" di Not yet; klaim Houthi atas Riyadh "came 25 Nov"; gempa Nepal
  ditulis M5.6/M5.3 (keduanya); putusan ICJ "19 Nov" di DATE CHECK.
- Angka terverifikasi: 3 tanker, 11 luka, Nasdaq +6.51%, Nvidia +30%,
  Huawei 10/12, 60 bank / 70 kapal, 25–30 sandera, 2 tewas / 30+ luka,
  6.500+ pemulangan, 74 cambukan, $8 miliar / 800+ tersangka, $237.5 miliar.
- Baru di v6 — klaim PRESS TIME 23:59 UTC DIHAPUS total (bukan lagi
  dibuktikan dengan label waktu per kartu). Strip timeline kini hanya
  "TUESDAY IN UTC" dengan 6 item jujur: 2 jam pasti (01:32 Nepal,
  20:25* Hormuz) + 4 bagian hari (Morning/Midday/Afternoon/Evening).
  Tanda `*` dijelaskan di DATE CHECK: "*Hormuz: 20:25 UTC 23 Nov"
  (insiden 23 Nov UTC, pertama dilaporkan 24 Nov).
- Dua penyingkatan headline demi muat 2 baris (fakta tidak berubah):
  grid 7 "14 NATIONS BACK ICJ ROHINGYA RULING" → "ICJ RULING BACKED BY
  14 NATIONS" (kata "Rohingya" dipindah ke deck); grid 9 "EU PLANS
  SANCTIONS: 60 BANKS, 70 SHIPS" → "EU SANCTIONS: 60 BANKS, 70 SHIPS".
- (−1) "14 fields" di header masih tidak didefinisikan di dalam gambar;
  juri harus menghitung sendiri.

### Kepraktisan — 24 / 25 (tidak berubah)
- Deterministik: 2 run → SHA256 identik (diuji v6, 2×). Tanpa network,
  tanpa file eksternal, hanya Pillow + font sistem. PNG 225,258 byte
  (≤1 MiB, dalam target 200–300 KB), 1024×1024.
- `main.py` di root folder, menulis `./entry.png` dan `/output/entry.png`;
  README + LICENSE MIT lengkap.
- (−1) Bundle transkrip v6 belum dibuat — v6 DITAHAN, bukan disubmit
  (keputusan nemesis 2026-11-26 01:32 WIB, ditegaskan lagi "jangan entry
  dulu"). Bundle baru dibuat parent hanya kalau nemesis bilang yakin
  dan v6 jadi disubmit.

### Keunikan — 23 / 25 (v5: 24, −1)
- 3 hero dengan adegan vektor spesifik berita 24 Nov (3 tanker + api,
  menara PIF + drone, grafik saham naik), banner angka spesifik
  (3 TANKERS HIT, 11 HURT, NASDAQ +6.51%), DATE CHECK audit lebih ketat
  dari pemenang (4 excluded + 3 not-yet, semua spesifik), color-coding
  region konsisten di strip, kartu, brief, dan pin peta.
- Judul submission tetap yang dibuat di v5 (menyebut 3 headline spesifik:
  Hormuz / Riyadh / Nasdaq) — bukan parafrasa regian 23 Nov.
- (−1) v6 sengaja meniru struktur rank 1 23 Nov (regian) hampir
  1:1 — layout, urutan zona, dan gaya datar. Itu keputusan sadar demi
  kejelasan setelah v5 dikritik "jelek dan kaku", tapi orisinalitas
  format memang lebih rendah dari v5 (inset Eropa + label waktu per
  kartu dihapus).
- (−1) Format masih mengikuti template frontpage pemenang 20–23 Nov.

### Kemudahan pemahaman — 25 / 25 (v5: 24, +1)
- Hierarki terbaca dalam 3 detik: tanggal raksasa → 3 hero → grid →
  peta → brief → DATE CHECK. Ini yang diperbaiki v6: adegan hero kini
  BESAR dan sederhana (kapal + api, menara + drone, grafik naik) dan
  terbaca dalam 1 detik, bukan pita tipis yang tidak jelas seperti v5.
- SEMUA teks isi minimal 10 px (verifikasi: `grep` ukuran font di
  `main.py` → minimum 10 px; headline grid 14 px serif, deck grid
  10 px, brief 10 px, footer 10 px, timeline 10 px); 0 headline/deck
  melebihi 2 baris (verifikasi: simulasi wrap → semua hero/grid 2 baris);
  0 brief terpotong; timeline 1 baris muat penuh (berakhir x=978 dari
  batas 1010); DATE CHECK 3 baris muat penuh (lebar maks 981 dari 996,
  baris 1 mepet — sudah diukur dan terlihat utuh di render).
- Peta kini JELAS (ini perbaikan utama v6): peta kecil sederhana,
  daratan solid krem di laut biru pucat, pin 1–13 berdiameter 20 px
  dengan angka putih 12 px, jarak pusat minimum 28,3 px (pasangan 5–13)
  vs diameter 20 px — semua pin terpisah penuh tanpa inset; pin yang
  digeser dari titik sebenarnya memakai leader line pendek ke titik
  kecil di lokasi sebenarnya. Tanpa inset Eropa yang membingungkan,
  tanpa peta titik-titik, tanpa bayangan.
- (−0) Tidak ada pengurangan di kategori ini: tidak ada teks yang
  tumpang tindih (diverifikasi lewat crop hero + grid + peta + bawah),
  header grid "E. ASIA & PAC." tidak lagi terpotong pill.

## Tiga pendapat bertentangan (Mode ③, ringkas)
1. "Meniru regian 1:1 itu membosankan; v5 lebih orisinal." — Diterima
   sebagian: v6 memang kurang orisinal (−1 keunikan), tapi nemesis
   sendiri yang minta lihat referensi top rank karena v5 tidak jelas.
   Kejelasan menang atas orisinalitas untuk juri yang membandingkan
   2 gambar sekaligus.
2. "29 cerita seperti bagarte 22 Nov (85,44%) akan lebih lega dari 35."
   — Ditolak: pemenang 23 Nov (84,07%) dan 21 Nov (86,11%) menang
   dengan 35 cerita; v6 sudah mengimbangi kepadatan dengan deck pendek
   dan brief satu baris.
3. "PRESS TIME 23:59 UTC sebaiknya dipertahankan sebagai pembeda."
   — Ditolak: klaim itu tidak bisa dibuktikan dari isi gambar tanpa
   label waktu per kartu, dan label per kartu justru membuat header
   kartu v5 berantakan. Menghapusnya lebih jujur.

## Putaran poles yang dilakukan
1. v1 → v2: deck hero dipendekkan (max 2 baris), geometri hero diubah,
   timeline jadi flow layout 2 baris, brief dipotong dengan elipsis,
   legenda peta 2 baris, "13EUROPE" diperbaiki.
2. v2 → v3: ikon grid diperbaiki agar muat di kotak (trofi, globe, ledakan,
   timbangan meluber), deck kartu 11 dipendekkan, brief dipendekkan agar
   hampir semua tampil utuh tanpa elipsis, pin Hormuz/Riyadh digeser.
3. v3 → v4 (poles kejelasan, atas permintaan nemesis):
   brief 9 px → 10 px; timeline 26 px → 30 px; pin peta diberi leader
   line; ikon grid lebih spesifik; "PRESS TIME 23:59 UTC" + "Final
   edition — outcomes, not previews".
4. v4 → v5 (poles desain menyeluruh, atas permintaan nemesis "jelek dan
   kaku, poles dan bikin bagus, peta juga"): bayangan lembut, sudut
   lebih bulat, adegan hero ber-tint, inset "EUROPE ENLARGED", label
   waktu per kartu, semua teks ≥10 px, judul submission baru.
5. v5 → v6 (REBUILD TOTAL dari nol, atas permintaan nemesis "gambar peta
   gk jelas gambar newsnya juga kayak apa itu, lihat referensi top rank
   news sebelumnya"):
   - Baca visual 3 gambar rank 1 (regian 23 Nov, bagarte 22 Nov,
     superskie 21 Nov) + winner-analysis.md; tiru strukturnya.
   - Datar total: tanpa bayangan, tanpa sudut bulat berlebihan, tanpa
     tint; kartu putih bersih, border tipis navy/abu.
   - Hero: adegan BESAR sederhana (kapal 3 + api, menara PIF lebar +
     drone + ledakan, grafik 4 bar naik + panah), banner stat merah
     20 px; deck hero 3 dipendekkan agar muat 2 baris.
   - Grid: adegan mini datar BESAR (ikon diperbesar 1,25×) + chip stat
     navy/merah di pojok scene; headline grid 15 px → 14 px serif agar
     semua muat 2 baris; header region disingkat "E. ASIA & PAC." agar
     tidak terpotong pill.
   - Peta: KECIL, SEDERHANA, JELAS — daratan solid, pin 20 px bernomor
     besar, jarak minimum 28,3 px, leader line pendek ke titik asli;
     inset Eropa DIHAPUS; tanpa peta titik-titik.
   - Timeline: 1 baris tipis navy, 6 item jujur, font 10 px; PRESS TIME
     DIHAPUS; `*` Hormuz dijelaskan di DATE CHECK.
   - DATE CHECK jadi 3 baris (2 excluded + 1 not-yet) agar tidak meluber.
   - Audit skrip sebelum menilai: font minimum 10 px, 0 headline/deck
     melebihi 2 baris, 0 brief terpotong, timeline berakhir x=978/1010,
     DATE CHECK maks 981/996, jarak pin minimum 28,3 px, determinisme
     2× SHA identik.

## Judul submission yang disarankan (untuk parent, bila v6 jadi disubmit)
"Tuesday 24 November 2026 — Hormuz: 3 Tankers Hit, Riyadh Tower: 11 Hurt,
Nasdaq +6.51%: 35 Dated Stories, 8 Regions, 14 Fields, UTC Timeline &
Date-Check Audit"

## Status — HOLD, jangan submit
- v3 SUDAH submit dan lolos checks (submission `01a213f6-be42-71b6-8f58-ad896efa857c`,
  stage `checked`; lihat SUBMIT-RECEIPT.md). V3 tidak bisa dibatalkan.
- v4 (skor 95) dan v5 (skor 96) adalah cadangan yang TIDAK disubmit.
- v6 ini adalah cadangan terbaru (skor 96, sama dengan v5 tapi jauh lebih
  jelas — kemudahan pemahaman 25/25 vs 24/25). TIDAK disubmit sampai
  nemesis bilang yakin. Submit v6 sebelum deadline 2026-11-26 00:00 UTC
  (07:00 WIB) akan menggantikan v3 sebagai entry final. Kuota masih
  cukup (9/hari tersisa setelah submit v3).
