from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server
import anvil.js
from anvil.js.window import jQuery, ej

import navigation as nav
from ... import app
from ... import Forms
from ... import Views


class HomePage(HomePageTemplate):
    def __init__(self, **properties):
        app.session.init_user_session()

        self.content_id = 'pm-content'
        self.content_control = None

        # Appbar configuration
        self.appbar = ej.navigations.AppBar({'colorMode': 'Primary', 'isSticky': True})
        self.appbar_logo = ej.buttons.Button({'cssClass': 'e-inherit'})
        self.appbar_sidebar_toggle = ej.buttons.Button(
            {'cssClass': 'e-inherit', 'iconCss': 'fa-solid fa-bars pm-appbar-menu-icon'})
        self.appbar_notification_list = ej.splitbuttons.DropDownButton({
            'cssClass': 'e-inherit e-caret-hide pm-menu-font',
            'iconCss': 'fa-solid fa-bell pm-appbar-menu-icon',
            'items': [{'text': 'No new notifications', 'disabled': True}],
            'open': self.appbar_menu_popup_open
        })
        appbar_help_menu_items = [
            {'text': 'Help', 'iconCss': 'fa-regular fa-info', 'id': 'pm_appbar_help_help'},
            {'text': 'How to', 'iconCss': 'fa-regular fa-file-lines', 'id': 'pm_appbar_help_howto'},
        ]
        self.appbar_help_menu = ej.splitbuttons.DropDownButton({
            'cssClass': 'e-inherit e-caret-hide pm-menu-font',
            'iconCss': 'fa-solid fa-question pm-appbar-menu-icon',
            'items': appbar_help_menu_items,
            'open': self.appbar_menu_popup_open
        })
        appbar_user_menu_items = [
            {'text': 'Adam<br>adam@wooldridgelawlv.com', 'disabled': True, 'id': 'pm_appbar_user_account_name'},
            {'text': 'Account', 'iconCss': 'fa-regular fa-user-gear', 'id': 'pm_appbar_user_settings'},
            {'text': 'Sign Out', 'iconCss': 'fa-regular fa-arrow-right-from-bracket', 'id': 'pm_appbar_sign_out'},
        ]
        self.appbar_user_menu = ej.splitbuttons.DropDownButton({
            'cssClass': 'e-inherit e-caret-hide pm-menu-font',
            'iconCss': 'fa-solid fa-user pm-appbar-menu-icon',
            'items': appbar_user_menu_items,
            'open': self.appbar_menu_popup_open
        })

        self.sidebar = nav.Sidebar(target_el='.pm-page-container', container_el='pm-sidebar',
                                   content_id=self.content_id)
        self.appbar_menu = nav.AppbarMenu(container_el='pm-appbar-menu', sidebar=self.sidebar,
                                          menu_items=nav.PMAPP_APPBAR_MENU)

    def form_show(self, **event_args):
        # Append appbar controls to elements
        self.appbar.appendTo(jQuery('#pm-appbar')[0])
        self.appbar_notification_list.appendTo(jQuery('#pm-appbar-notification-list')[0])
        self.appbar_help_menu.appendTo(jQuery('#pm-appbar-help-menu')[0])
        self.appbar_user_menu.appendTo(jQuery('#pm-appbar-user-menu')[0])
        self.appbar_sidebar_toggle.appendTo(jQuery('#pm-appbar-sidebar-toggle')[0])
        self.appbar_sidebar_toggle.element.addEventListener('click', self.sidebar.toggle)
        self.appbar_menu.show()

        # Show sidebar menu
        self.sidebar.show()

        # Show start page

    # Sidebar toggle event handler
    def sidebar_toggle(self, args):
        self.sidebar.toggle()

    # Appbar menu popup window position adjustment
    @staticmethod
    def appbar_menu_popup_open(args):
        args.element.parentElement.style.top = str(float(args.element.parentElement.style.top[:-2]) + 10) + 'px'

    # Sidebar menu popup window position adjustment
    @staticmethod
    def sidebar_menu_popup_open(args):
        args.element.parentElement.style.top = str(
            args.element.getBoundingClientRect().top - args.element.parentElement.offsetHeight + 44) + 'px'
        args.element.parentElement.style.left = '100px'

    @staticmethod
    def sidebar_menu_select(args):
        item = args['item']
        print(item.keys())
        for key in item.keys():
            print(key, item[key])
