# FAQ IT Helpdesk — SOP Internal Mustika & Bank Mega (Knowledge Base)

## 1. Reset Password SSO
Buka portal SSO -> klik Lupa Password -> masukkan NIK -> verifikasi OTP via email/WA -> buat password baru minimal 8 karakter (huruf besar, kecil, angka, simbol). Jika OTP tidak masuk cek spam atau hubungi IT dengan NIK.

## 2. Akun Terkunci (Locked)
Akun terkunci setelah 5x salah password. Tunggu 15 menit auto-unlock atau hubungi IT untuk unlock manual dengan verifikasi NIK + foto KTP.

## 3. Lupa Username SSO
Username = NIK atau email kantor. Cek di email onboarding. Jika lupa, hubungi IT dengan NIK dan nama lengkap.

## 4. Install Software Baru
Request via ticketing kategori Software + approval atasan langsung. IT install via SCCM remote. Jangan download installer dari situs tidak resmi.

## 5. Request Lisensi (Office, Adobe, AutoCAD)
Buat ticket Software-Lisensi, sebutkan software + kebutuhan + durasi. IT cek ketersediaan lisensi dan approval manager.

## 6. Printer Tidak Bisa Print
Cek kabel power & LAN/USB, restart printer, cek antrean di Control Panel > Devices and Printers > See what's printing -> Cancel All. Jika lampu merah berkedip, foto dan buat ticket Hardware-Printer dengan lokasi lantai.

## 7. Printer Paper Jam
Buka tutup depan, tarik kertas perlahan, jangan sobek. Bersihkan sisa sobekan. Jika sering jam, lapor IT untuk servis.

## 8. WiFi Tidak Connect
Coba lupakan jaringan (Forget) lalu connect ulang. Restart WiFi device. Jika 1 device saja bermasalah cek driver, jika semua device down kemungkinan AP/switch - lapor Network dengan lokasi.

## 9. VPN Tidak Connect (ERP/Akses Kantor)
Pastikan internet stabil, buka aplikasi VPN -> connect -> masukkan OTP. Error 403 = cek role VPN belum aktif, hubungi IT dengan NIK dan modul yang diakses.

## 10. Email Tidak Masuk / Tidak Terkirim
Cek folder Spam/Junk, cek kuota mailbox (>90% penuh hapus email lama), coba via webmail. Jika bounce, screenshot error dan buat ticket Email.

## 11. Email Kuota Penuh
Hapus email besar di Sent/Trash, kosongkan Deleted Items, arsip ke PST. Jika masih penuh, request tambah kuota via ticket.

## 12. Akses ERP Error 403 / 500
Pastikan VPN connect, clear cache browser, coba incognito. Jika tetap, catat modul (Finance/HR/Inventory) + screenshot, buat ticket ERP dengan NIK.

## 13. ERP Lambat / Timeout
Cek jaringan, coba jam tidak sibuk. Jika lambat terus, lapor IT dengan jam kejadian + modul + NIK untuk cek log server.

## 14. Request Hardware Baru (Laptop, Mouse, Headset)
Buat ticket Hardware-Request + alasan + approval atasan. IT cek stok dan jadwal pengadaan.

## 15. Laptop Lemot / Blue Screen
Restart, cek Task Manager proses berat, scan antivirus. Jika BSOD foto kode error (0x...), buat ticket Hardware dengan kronologi.

## 16. File Share / Drive Tidak Bisa Akses
Cek VPN, cek permission folder. Jika error Access Denied, sebutkan path folder + NIK, IT akan cek ACL.

## 17. Ticketing Portal Error
Clear cache, coba browser lain. Jika tidak bisa submit ticket, email ke helpdesk@company.co.id sementara dengan subjek dan deskripsi.

## 18. Onboarding Karyawan Baru
HR buat ticket Onboarding H-3 dengan NIK, divisi, kebutuhan akun (SSO, email, ERP, WiFi). IT setup akun H-1 dan kirim kredensial via channel aman.

## 19. Offboarding / Resign
Atasan buat ticket Offboarding, IT disable akun SSO/email/VPN H+1 setelah last day, backup data jika diminta.

## 20. Keamanan Data - Jangan Kirim Password
Jangan pernah kirim password plain text via ticket/chat/email. IT tidak pernah minta password. Jika diminta, lapor security. Untuk AI tools, password selalu dimask otomatis.

## 21. Pengajuan Cuti
Buka portal HR/ERP -> menu Cuti -> pilih jenis cuti (Tahunan/Sakit/Izin) -> isi tanggal & alasan -> submit -> notifikasi ke atasan untuk approval. Cek saldo cuti di dashboard HR. Jika butuh cuti mendadak, hubungi atasan + buat ticket HR-Cuti dengan NIK dan tanggal.
