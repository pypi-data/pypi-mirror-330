# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from gi import require_version
require_version("Gtk", "4.0")
require_version("Adw", "1")

from gi.repository import Gtk, Adw, GLib, Gio
from eFatura       import e_fatura
from ..Libs        import dosya_ver

class KekikGUI(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id = "org.KekikAkademi.eFatura",
            flags          = Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        # Ana pencere oluştur
        self.win = Adw.ApplicationWindow(application=app)
        self.win.set_default_size(300, 200)
        self.win.set_resizable(False)
        self.win.set_title("eFatura")
        self.win.connect("close-request", self.pencereyi_kapat)

        # Stil yöneticisi - karanlık tema için
        style_manager = Adw.StyleManager.get_default()
        style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

        # HeaderBar oluştur
        self.header  = Adw.HeaderBar()
        title_widget = Adw.WindowTitle()
        title_widget.set_title("eFatura")
        title_widget.set_subtitle("Mükellefiyet Sorgu Aracı")
        self.header.set_title_widget(title_widget)

        # Hakkında butonu
        self.hakkinda_butonu = Gtk.Button()
        self.hakkinda_butonu.set_icon_name("help-about-symbolic")
        self.hakkinda_butonu.connect("clicked", self.hakkinda_ac)
        self.header.pack_end(self.hakkinda_butonu)

        # Ana içerik kutusu
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Header'ı ana kutuya ekle
        main_box.append(self.header)

        # İçerik kutusu
        self.pencere = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.pencere.set_margin_start(20)
        self.pencere.set_margin_end(20)
        self.pencere.set_margin_top(20)
        self.pencere.set_margin_bottom(20)
        main_box.append(self.pencere)

        # Program içeriğini oluştur
        Program(self)

        # Pencereye içeriği ayarla ve göster
        self.win.set_content(main_box)
        self.win.present()

    def pencereyi_kapat(self, action=None, param=None):
        dialog = Adw.MessageDialog.new(self.win)
        dialog.set_heading("Program Kapanıyor")
        dialog.set_body("Bunu yapmak istediğinize emin misiniz?")
        dialog.add_response("cancel", "İptal")
        dialog.add_response("ok", "Tamam")
        dialog.set_default_response("cancel")
        dialog.set_response_appearance("ok", Adw.ResponseAppearance.DESTRUCTIVE)

        dialog.connect("response", self.__kapatma_dialog_yanit)
        dialog.present()

        return True  # True döndürmek, pencerenin hemen kapanmasını engeller

    def __kapatma_dialog_yanit(self, dialog, response):
        if response == "ok":
            self.quit()

        dialog.destroy()

    def hakkinda_ac(self, widget):
        about = Adw.AboutWindow(
            transient_for    = self.props.active_window,
            version          = "1.1.3",
            application_name = "eFatura Sorgu",
            application_icon = "org.KekikAkademi.eFatura",
            comments         = "Vergi veya TC Kimlik Numarasından E-Fatura Mükellefiyet Sorgusu",
            developers       = ["keyiflerolsun"],
            website          = "https://keyiflerolsun.dev/Kahve",
            issue_url        = "https://github.com/keyiflerolsun/eFatura/issues",
            license_type     = Gtk.License.GPL_3_0,
            copyright        = (
                '© tüm hakları açık keyfinizce takılın 🕊\n'
                '\n'
                '"\n'
                'Bilgi güçtür. Fakat her zaman olduğu gibi bu gücü kendine saklamak isteyenler var...\n'
                'Bu durumu değiştirmek için mücadele edenler de var...\n'
                '\n'
                'Ama bütün bu eylemler karanlıkta, yeraltında gizlenerek ilerliyordu.\n'
                'Hırsızlık veya korsanlık denildi, sanki bir bilgi hazinesini paylaşmak bir gemiyi soyup mürettebatı öldürmek ile ahlaken eşdeğermiş gibi.\n'
                'Fakat paylaşmak ahlaken yanlış değildir, aksine ahlaki bir buyruktur. Yalnız açgözlülükten gözü dönmüş birisi arkadaşına istediği kopyayı vermez...\n'
                '\n'
                'Nerede depolanmış olursa olsun, bilgiyi almalı, kendi kopyalarımızı çıkarmalı ve dünya ile paylaşmalıyız. Telif hakkı biten şeyleri alıp arşive eklemeliyiz.\n'
                'Gizli veritabanlarını satın alıp İnternete koymalıyız. Bilimsel dergileri indirip dosya paylaşım ağlarına yüklemeliyiz. Gerilla Açık Erişim için savaşmalıyız.\n'
                '\n'
                'Bütün dünyada yeterince fazla sayıda olursak, yalnızca bilginin özelleştirilmesine karşı güçlü bir mesaj vermekle kalmayacağız, aynı zamanda onu tarihe gömeceğiz.\n'
                'Bize katılıyor musunuz?\n'
                '\n'
                'Aaron Swartz\n'
                'Temmuz 2008, Eremo, İtalya\n'
                '"\n'
                '\n'
                'Sağlıcakla kalın ve Özgür Kalın ✌🏼\n'
            ),
        )
        about.add_credit_section("Özel Teşekkürler", ["@KekikAkademi", "@KekikKahve"])

        about.present()

class Program():
    def __init__(self, parent):
        self.parent = parent

        # Sorgu alanı
        sorgu_alani = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        parent.pencere.append(sorgu_alani)

        # Arama metni girişi
        self.arama_metni = Gtk.Entry()
        self.arama_metni.set_placeholder_text("Vergi / TC Kimlik Numarası")
        self.arama_metni.connect("activate", self.ara_butonuna_tiklandiginda)
        sorgu_alani.append(self.arama_metni)

        # Ara butonu
        self.ara_butonu = Gtk.Button(label="Ara")
        self.ara_butonu.connect("clicked", self.ara_butonuna_tiklandiginda)
        self.ara_butonu.add_css_class("suggested-action")
        sorgu_alani.append(self.ara_butonu)

        # Çıktı alanı
        self.cikti_alani = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        parent.pencere.append(self.cikti_alani)

        # İlk odaklanma
        self.ara_butonu.grab_focus()

    def ara_butonuna_tiklandiginda(self, widget):
        self.ara_butonu.grab_focus()
        arama_sorgusu = self.arama_metni.get_text()
        self.arama_metni.set_text("")

        # Çıktı alanını temizle
        while self.cikti_alani.get_first_child():
            self.cikti_alani.remove(self.cikti_alani.get_first_child())

        # Bekleme etiketi
        bekleme_etiketi = Gtk.Label()
        bekleme_etiketi.set_markup("<span foreground='#EF7F1A' font_desc='12'>Lütfen Bekleyiniz...</span>")
        bekleme_etiketi.set_margin_top(10)
        bekleme_etiketi.set_halign(Gtk.Align.CENTER)
        bekleme_etiketi.set_justify(Gtk.Justification.CENTER)
        bekleme_etiketi.set_wrap(True)
        bekleme_etiketi.set_max_width_chars(30)
        self.cikti_alani.append(bekleme_etiketi)

        def arama_tamamlandi():
            try:
                sonuc = e_fatura(arama_sorgusu)
                if sonuc:
                    bekleme_etiketi.set_markup(
                        f"<span foreground='#28a745' font_desc='16'><b>{arama_sorgusu}</b></span>\n"
                        "<span font_desc='12'>✅ E-Fatura Mükellefidir.</span>"
                    )
                else:
                    bekleme_etiketi.set_markup(
                        f"<span foreground='#dc3545' font_desc='16'><b>{arama_sorgusu}</b></span>\n"
                        "<span font_desc='12'>❌ E-Fatura Mükellefi Değildir.</span>"
                    )
            except Exception as hata:
                bekleme_etiketi.set_markup(
                    f"<span foreground='#ffc107' font_desc='16'><b>{arama_sorgusu}</b></span>\n"
                    "<span font_desc='12'>⚠️ Sorgulama sırasında beklenmedik bir hata oluştu!</span>\n\n"
                    f"<span foreground='#dc3545' font_desc='10'><i>{hata}</i></span>"
                )

            return False  # GLib.timeout_add için False döndür ki tekrar çağrılmasın

        GLib.timeout_add(100, arama_tamamlandi)