from ..Pages import *


class CaseDashboardPage:
    def __init__(self, container_id):
        print('Case Dashboard')
        self.container_id = container_id
        self.container_el = jQuery(f"#{self.container_id}")[0]
        self.content_id = str(uuid.uuid4()).replace('-', '')
        self.css = '<link href="_/theme/case-dashboard-page.css" rel="stylesheet">'
        self.html = f'<div id="pm-content-{self.content_id}-dashboard" class="pm-content-dashboard">\
                    <div id="pm-content-{self.content_id}-dashboard-left" class="pm-content-dashboard-left"></div>\
                    <div id="pm-content-{self.content_id}-dashboard-middle" class="pm-content-dashboard-middle"></div>\
                    <div id="pm-content-{self.content_id}-dashboard-right" class="pm-content-dashboard-right"></div>\
                  </div>'
        self.content = self.css + self.html

        self.left_panel_items = [
            {'header': 'Last Update', 'content': ''},
            {'header': 'Overview', 'content':
                '<b>Case Name:</b> Doe.John (99HCL000001-0000)<br><br><b>Practice Area:</b> Criminal '
                'Defense<be><br><b>Case Stage:</b> Lower Court<br><br>SOL: N/A<br><br> <b>Cause(s) of '
                'Action:</b><br>-Kidnapping, first degree, no substantial bodily harm'},
            {'header': 'Case Details', 'content': '<br>'},
            {'header': 'Custody Status', 'content': '<br>'},
            {'header': 'Staff & Contacts', 'content': '<br>'},
            {'header': 'Record Data', 'content': '<br>'},
        ]
        self.right_panel_items = [
            {'header': 'Payment Status', 'content': '<br>'},
            {'header': 'Fee Details', 'content': '<br>'},
            {'header': 'Retainer Details', 'content': '<br>'},
            {'header': 'Time Entire', 'content': '<br>'},
            {'header': 'Expenses', 'content': '<br>'},
            {'header': 'Balances', 'content': '<br>'},
        ]
        self.left_panel = ej.navigations.Accordion({'items': self.left_panel_items})
        self.right_panel = ej.navigations.Accordion({'items': self.right_panel_items})

    @property
    def target_id(self):
        return f"pm-content-{self.content_id}-dashboard-middle"

    @property
    def target_el(self):
        return jQuery(f"#{self.target_id}")[0]

    def form_show(self):
        self.container_el.innerHTML = self.content
        self.left_panel.appendTo(f"#pm-content-{self.content_id}-dashboard-left")
        self.right_panel.appendTo(f"#pm-content-{self.content_id}-dashboard-right")

        self.left_panel.items[0].content = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod ' \
                                            'tempor incididunt ut labore et dolore magna aliqua.'

    def destroy(self):
        jQuery(f"#{self.container_id}")[0].innerHtml = ''
        self.left_panel.destroy()
        self.right_panel.destroy()
