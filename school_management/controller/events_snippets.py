# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteEvents(http.Controller):
    """Handles the Data of latest events and their details"""
    @http.route('/get_latest_events', type='json', auth='public', website=True)
    def get_latest_events(self):
        """Return event data"""
        events = request.env['events.club'].sudo().search([], order='create_date DESC', limit=5)
        values = {
            'events': [
                {
                    'id': event.id,
                    'name': event.name,
                    'club_id': event.club_id.id,
                    'start_date': event.start_date,
                    'end_date': event.end_date,
                    'desc': event.desc,
                    'image_url': f"/web/image/events.club/{event.id}/event_image" if event.event_image else False,
                }
                for event in events
            ]
        }
        print(values)
        return values

    @http.route('/event/details/<int:event_id>', auth='public', type='http', website=True)
    def event_details(self, event_id, **kwargs):
        """Returns the event details on view details action"""
        event = request.env['events.club'].sudo().browse(event_id)
        return request.render('school_management.event_details_template', {
            'event': event,
        })
