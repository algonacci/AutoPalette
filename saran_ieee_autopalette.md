# Strategi Pengembangan AutoPalette untuk Konferensi IEEE

Dokumen ini merangkum analisis dan ide pengembangan repositori `AutoPalette` agar layak dipublikasikan di konferensi standar IEEE (Institute of Electrical and Electronics Engineers), khususnya pada track **Assistive Technology**, **Biomedical Engineering**, dan **Multimedia/Information Retrieval**.

---

## 1. Analisis Awal: Mengapa "Basic K-Means" Tidak Cukup?

Algoritma K-Means untuk ekstraksi warna adalah metode *textbook* yang sudah umum. Jika diajukan "as-is", paper kemungkinan besar akan ditolak (*reject*) karena kurangnya **Novelty (Kebaruan)** dan **Signifikansi Masalah**.

Untuk menembus publikasi ilmiah, kita perlu mengubah paradigma:
*   **Dari:** "Aplikasi untuk ekstrak warna" (Tools).
*   **Menjadi:** "Sistem pemecahan masalah spesifik menggunakan analisis warna" (Solution).

---

## 2. Track Utama: Assistive Technology (Rekomendasi Utama)

Ini adalah arah yang paling potensial sesuai diskusi, menargetkan bantuan bagi penyandang **Tuna Netra**.

### Konsep: "The Controlled Station"
Berbeda dengan aplikasi HP biasa yang rentan terhadap masalah pencahayaan dan guncangan tangan, ide Anda menggunakan **"Station"** (kotak/alat stasioner tempat meletakkan objek) adalah nilai jual ilmiah utama (*Scientific Merit*).

*   **Research Gap:** Aplikasi *color recognizer* di pasar (seperti Be My Eyes atau TapTapSee) sering tidak akurat karena faktor lingkungan (bayangan, cahaya redup). "Station" menjamin **Robustness** (ketahanan) dan **Consistency**.

### Skenario A: Daily Living Aid (General Objects)
Membantu tuna netra mengidentifikasi objek sehari-hari yang hanya bisa dibedakan lewat warna.

*   **Use Cases:**
    *   **Identifikasi Uang Kertas:** Membedakan nominal uang (misal: Rp 50.000 vs Rp 100.000) yang ukurannya mirip tapi warnanya beda.
    *   **Manajemen Obat:** Membedakan botol obat yang bentuknya sama persis (misal: botol obat jantung vs vitamin) hanya dari warna tutup atau labelnya.
    *   **Fashion Matching:** Membantu memilih pakaian yang warnanya serasi (misal: mencegah memakai kaos kaki belang).

*   **Judul Paper Potensial:**
    > *"Robust Object Identification System for Visually Impaired Users in Controlled Lighting Environments using K-Means Clustering."*

*   **Pengembangan Teknis yang Diperlukan:**
    1.  **Semantic Color Naming:** Mengubah output RGB/Hex menjadi bahasa manusia ("Merah Tua", "Biru Langit").
        *   *Metode:* Konversi RGB ke **CIELAB Color Space** lalu hitung *Euclidean Distance* ke dataset nama warna (misal: XKCD Colors atau CSS3).
    2.  **Audio Feedback:** Integrasi Text-to-Speech (TTS).

---

## 3. Track Alternatif: Biomedical Engineering Focus

Jika ingin memperkuat nuansa "Biomedis" namun tetap menggunakan teknologi yang sama.

### Skenario B: Auditory Reader for Colorimetric Assays
Membantu pasien tuna netra membaca hasil tes kesehatan mandiri yang berbasis perubahan warna.

*   **Masalah:** Pasien diabetes tuna netra tidak bisa membaca strip tes urin/keton sendiri karena hasilnya visual.
*   **Use Cases:**
    *   Membaca **Strip Urinalisis** (Glukosa, Protein, pH).
    *   Membaca **Indikator Kualitas ASI** atau **Expired Food Indicator**.
*   **Alur Logika:**
    1.  Deteksi warna area reaksi pada strip.
    2.  Petakan warna ke tabel medis (Kuning = Normal, Hijau = Bahaya).
    3.  Output suara interpretasi medis, bukan nama warnanya.

*   **Judul Paper Potensial:**
    > *"Accessible Home Diagnostic Framework: Automated Colorimetric Strip Reader for Visually Impaired Diabetic Patients."*

---

## 4. Track Alternatif: Multimedia & Image Processing

Jika ingin fokus pada algoritma dan pengolahan citra murni, bukan aspek manusianya.

### Skenario C: Saliency-Aware Extraction
Memperbaiki kelemahan K-Means yang "buta konteks" (menganggap background sama pentingnya dengan objek).

*   **Masalah:** K-Means biasa sering mengambil warna tembok/meja dominan, bukan warna objek kecil di tengah.
*   **Solusi:** Integrasikan **Saliency Map** (peta fokus mata manusia). Pixel yang berada di area fokus diberi bobot lebih tinggi saat clustering.

*   **Judul Paper Potensial:**
    > *"Enhancing Dominant Color Extraction using Saliency-Weighted K-Means Clustering for Content-Based Image Retrieval."*

---

## 5. Track Alternatif: Human-Computer Interaction (HCI) & Web Accessibility

Track ini sangat potensial jika Anda ingin fokus pada **Desain Inklusif** untuk pengguna dengan *Color Vision Deficiency* (CVD) atau buta warna.

### Skenario E: Adaptive Accessibility Palette Generator
Bukan sekadar mengekstrak warna, tapi **mengubah** warna tersebut agar aman dan dapat dibedakan oleh penyandang buta warna tanpa merusak estetika desain asli secara ekstrem.

*   **Masalah:** Desainer sering memilih palet warna yang terlihat bagus (estetik) bagi mata normal, namun memiliki kontras yang buruk atau tidak dapat dibedakan oleh penyandang Protanopia/Deuteranopia.
*   **Novelty (Kebaruan):** "Constraint-Based Palette Optimization".
    *   **Simulasi:** Sistem mensimulasikan bagaimana palet terlihat oleh mata CVD (menggunakan matriks transformasi LMS).
    *   **Optimasi:** Jika ada dua warna yang "bertabrakan" (terlihat sama) bagi CVD, algoritma akan menggeser *Hue* atau *Saturation* sedikit saja sampai jarak persepsinya cukup aman (`Delta-E > Threshold`), namun tetap menjaga harmoni warna asli.
    
*   **Judul Paper Potensial:**
    > *"AutoPalette-Access: Automated Color Palette Adaptation Framework for Color-Deficient Vision using Constraint-Based Clustering."*

---

## 6. Track Alternatif: Information Retrieval

### Skenario D: Semantic Image Search
Menggunakan palet warna sebagai *query* pencarian gambar (Search by Vibe).

*   **Konsep:** User mencari gambar dengan *query* "Suasana Senja Hangat", sistem mencari gambar dengan palet warna dominan oranye-ungu-kuning.
*   **Pengembangan:** Menggunakan histogram warna sebagai *feature vector* dan menghitung kemiripan antar gambar menggunakan **Earth Mover's Distance (EMD)**.

---

## Ringkasan Action Plan (Roadmap to Paper)

Berikut adalah langkah teknis yang perlu dilakukan pada repo `AutoPalette` untuk menuju prototype paper (mengambil **Track Assistive Technology**):

1.  **Refine Input Processing:**
    *   Asumsikan input dari "Station" (webcam statis).
    *   Tambahkan fitur **Center Crop** otomatis (fokus ke tengah objek).

2.  **Color Naming Algorithm (CRITICAL):**
    *   Buat database mini berisi nama warna dasar & variasinya (JSON).
    *   Buat fungsi `rgb_to_color_name(r, g, b)` yang mencari kecocokan terdekat menggunakan jarak warna Cartesian atau Delta-E.

3.  **Simulasi Output Suara:**
    *   Untuk tahap awal (web), tampilkan output teks deskriptif: *"Objek terdeteksi berwarna: Biru Dongker. Kemungkinan: Uang Rupiah 50.000."*

4.  **Eksperimen & Data:**
    *   Kumpulkan 20-30 foto objek dalam "station" (kotak kardus lampu).
    *   Ukur akurasi tebakan warna sistem vs warna asli. Data ini adalah "daging"-nya paper Anda.
