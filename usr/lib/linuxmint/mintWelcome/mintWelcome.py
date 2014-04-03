#!/usr/bin/env python

import gi
from gi.repository import Gtk, Gdk
from gi.repository import WebKit
from gi.repository.GdkPixbuf import Pixbuf

import sys
import commands
import os
import gettext
from user import home
import string

# i18n
gettext.install("mintwelcome", "/usr/share/linuxmint/locale")

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

class MintWelcome():
    def __init__(self):
        window = Gtk.Window()
        window.set_title(_("Welcome Screen"))
        window.set_icon_from_file("/usr/share/linuxmint/logo.png")
        window.set_position(Gtk.WindowPosition.CENTER)
        window.connect("destroy", Gtk.main_quit)

        sys.path.append('/usr/lib/linuxmint/common')
        from configobj import ConfigObj
        config = ConfigObj("/etc/linuxmint/info")
        codename = config['CODENAME'].capitalize()
        edition = config['EDITION']
        release = config['RELEASE']
        desktop = config['DESKTOP']
        self.release_notes = config['RELEASE_NOTES_URL']
        self.user_guide = config['USER_GUIDE_URL']
        self.new_features = config['NEW_FEATURES_URL']
        
        bgcolor =  Gdk.RGBA()
        bgcolor.parse("#f7f7f7")
        fgcolor =  Gdk.RGBA()
        fgcolor.parse("#3e3e3e")

        headerbar = Gtk.HeaderBar()
        headerbar.set_show_close_button(True)
        titlebox = Gtk.HBox()
        titlebox.set_spacing(6)
        logo = Gtk.Image()
        if "KDE" in desktop:
            logo.set_from_file("/usr/lib/linuxmint/mintWelcome/icons/logo_kde.png")
        else:
            logo.set_from_file("/usr/lib/linuxmint/mintWelcome/icons/logo.png")
        label = Gtk.Label()
        label.set_markup("<b><big>%s</big></b>" % _("Welcome"))
        titlebox.add(logo)
        titlebox.add(label)
        headerbar.pack_start(titlebox)
        window.set_titlebar(headerbar)

        main_box = Gtk.VBox()   

        event_box = Gtk.EventBox()
        event_box.override_background_color(Gtk.StateType.NORMAL, bgcolor)
        event_box.override_color(Gtk.StateType.NORMAL, fgcolor)
        main_box.pack_start(event_box, True, True, 0)

        vbox = Gtk.VBox()
        vbox.set_border_width(6)
        vbox.set_spacing(0)
        event_box.add(vbox)   
        
        headerbox = Gtk.VBox()
        label = Gtk.Label()
        if "KDE" in desktop:
            label.set_markup("<span font='12.5' fgcolor='#3e3e3e'>Linux Mint %s '<span fgcolor='#3267b8'>%s</span>'</span>" % (release, codename))
        else:
            label.set_markup("<span font='12.5' fgcolor='#3e3e3e'>Linux Mint %s '<span fgcolor='#709937'>%s</span>'</span>" % (release, codename))
        headerbox.pack_start(label, False, False, 0)
        label = Gtk.Label()
        label.set_markup("<span font='8' fgcolor='#3e3e3e'><i>%s</i></span>" % edition)
        headerbox.pack_start(label, False, False, 2)
        vbox.pack_start(headerbox, False, False, 10)

        welcome_label = Gtk.Label()
        welcome_message = _("Welcome and thank you for choosing Linux Mint. We hope you'll enjoy using it as much as we did designing it. The links below will help you get started with your new operating system. Have a great time and don't hesitate to send us your feedback.")
        welcome_label.set_markup("<span font='9' fgcolor='#3e3e3e'>%s</span>" % welcome_message)
        welcome_label.set_line_wrap(True)
        vbox.pack_start(welcome_label, False, False, 10)

        separator = Gtk.Image()
        separator.set_from_file('/usr/lib/linuxmint/mintWelcome/icons/separator.png')
        vbox.pack_start(separator, False, False, 10)
                
        liststore = Gtk.ListStore(Pixbuf, str, str, str)
        iconview = Gtk.IconView.new()
        iconview.set_model(liststore)
        iconview.set_pixbuf_column(0)
        iconview.set_text_column(2)
        iconview.set_tooltip_column(3)
        iconview.set_columns(4)
        iconview.set_margin(0)
        iconview.set_spacing(6)
        iconview.set_item_padding(4)
        iconview.set_row_spacing(20)
        iconview.set_column_spacing(20)
        iconview.override_background_color(Gtk.StateType.NORMAL, bgcolor)
        iconview.override_color(Gtk.StateType.NORMAL, fgcolor)
        iconview.connect("selection-changed", self.item_activated)        
        hbox = Gtk.HBox()
        hbox.pack_start(iconview, True, True, 30)
        vbox.pack_start(hbox, False, False, 10)

        actions = []
        actions.append(['new_features', _("New features"), _("See what is new in this release")])
        actions.append(['known_problems', _("Important information"), _("Find out about important information, limitations, known issues and their solution")])
        actions.append(['software', _("Software reviews"), _("Install additional software")])
        actions.append(['hardware', _("Hardware database"), _("Find hardware that is compatible with Linux, or information about your hardware")])

        actions.append(['user_guide', _("User guide (PDF)"), _("Learn all the basics to get started with Linux Mint")])
        actions.append(['forums', _("Forums"), _("Seek help from other users in the Linux Mint forums")])
        actions.append(['chatroom', _("Chat room"), _("Chat live with other users in the chat room")])
        actions.append(['tutorials', _("Tutorials"), _("Find tutorials about Linux Mint")])        
        
        actions.append(['get_involved', _("Get involved"), _("Find out how to get involved in the Linux Mint project")])
        actions.append(['ideas', _("Idea pool"), _("Submit new ideas to the development team")])
        actions.append(['donors', _("Donations"), _("Make a donation to the Linux Mint project")])
        actions.append(['sponsors', _("Sponsors"), _("Apply to become a Linux Mint sponsor")])   

        if "Gnome" in desktop and "debian" not in codename:
            # Some GNOME editions (Cinnamon, MATE) can come without codecs
            import apt
            cache = apt.Cache()
            if "mint-meta-codecs" in cache:
                pkg = cache["mint-meta-codecs"]
                if not pkg.is_installed:
                    actions.append(['codecs', _("Install Multimedia Codecs"), _("Add all the missing multimedia codecs")])

        for action in actions:
            pixbuf = Pixbuf.new_from_file('/usr/lib/linuxmint/mintWelcome/icons/%s.png' % action[0])
            liststore.append([pixbuf, action[0], action[1], action[2]])
        
        statusbar = Gtk.Statusbar()
        main_box.pack_end(statusbar, False, False, 0)

        hbox = Gtk.HBox()
        checkbox = Gtk.CheckButton()
        checkbox.set_label(_("Show this dialog at startup"))
        checkbox.override_color(Gtk.StateType.NORMAL, fgcolor)
        if not os.path.exists(home + "/.linuxmint/mintWelcome/norun.flag"):
            checkbox.set_active(True)
        checkbox.connect("toggled", self.on_button_toggled)
        hbox.pack_end(checkbox, False, False, 2)
        statusbar.pack_end(hbox, False, False, 2)
        
        window.add(main_box)
        window.set_size_request(640, 520)
        window.set_default_size(640, 520)                            
        window.show_all()

    def on_button_toggled(self, button):
        if button.get_active():
            if os.path.exists(home + "/.linuxmint/mintWelcome/norun.flag"):
                os.system("rm -rf " + home + "/.linuxmint/mintWelcome/norun.flag")
        else:  
            os.system("mkdir -p " + home + "/.linuxmint/mintWelcome")
            os.system("touch " + home + "/.linuxmint/mintWelcome/norun.flag")

    def item_activated(self, view):
        paths = view.get_selected_items()        
        if (len(paths) > 0):
            path = paths[0]
            treeiter = view.get_model().get_iter(path)
            value = view.get_model().get_value(treeiter, 1)
            if value == "chatroom":
                for client in ["/usr/bin/xchat-gnome", "/usr/bin/xchat", "/usr/bin/hexchat", "/usr/bin/konversation", "/usr/bin/quassel"]:
                    if os.path.exists(client):
                        os.system("%s &" % client)
            elif value == "new_features":
                os.system("xdg-open %s &" % self.new_features)
            elif value == "known_problems":
                os.system("xdg-open %s &" % self.release_notes)
            elif value == "user_guide":
                os.system("xdg-open %s &" % self.user_guide)
            elif value == "forums":
                os.system("xdg-open http://forums.linuxmint.com &")
            elif value == "tutorials":
                os.system("xdg-open http://community.linuxmint.com/tutorial &")
            elif value == "ideas":
                os.system("xdg-open http://community.linuxmint.com/idea &")
            elif value == "software":
                os.system("mintinstall &")
            elif value == "hardware":
                os.system("xdg-open http://community.linuxmint.com/hardware &")
            elif value == "get_involved":
                os.system("xdg-open http://www.linuxmint.com/getinvolved.php &")
            elif value == "sponsors":
                os.system("xdg-open http://www.linuxmint.com/sponsors.php &")
            elif value == "donors":
                os.system("xdg-open http://www.linuxmint.com/donors.php &")            
            elif value == "codecs":
                if self.codecs_pkg is not None:
                    os.system("xdg-open apt://mint-meta-codecs?refresh=yes &")

if __name__ == "__main__":
    MintWelcome()
    Gtk.main()
