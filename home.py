# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from lxml import etree
import traceback
import os
import unittest

import pytz
import werkzeug
import werkzeug.routing
import werkzeug.utils
import redis
import time
import pickle
import traceback

import odoo
from odoo import api, models, registry
from odoo import SUPERUSER_ID
from odoo.http import request
from odoo.tools import config
from odoo.tools.safe_eval import safe_eval
from odoo.osv.expression import FALSE_DOMAIN, OR

from odoo.addons.base.models.qweb import QWebException
from odoo.addons.http_routing.models.ir_http import ModelConverter, _guess_mimetype
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo import http
from datetime import datetime, date,timedelta
from .home_league_boxes import HomeLeagueBoxes


_logger = logging.getLogger(__name__)


class Http(models.AbstractModel, HomeLeagueBoxes):
    _inherit = 'ir.http'

    @classmethod
    def _serve_page(cls):
        red = redis.Redis("sgs-docker_redis_1")
        req_page = request.httprequest.path
        page_domain = [('url', '=', req_page)] + \
            request.website.website_domain()
        published_domain = page_domain
        # need to bypass website_published, to apply is_most_specific
        # filter later if not publisher
        pages = request.env['website.page'].sudo().search(
            published_domain, order='website_id')
        pages = pages.filtered("is_published")

        if not request.website.is_publisher():
            pages = pages.filtered('is_visible')

        mypage = pages[0] if pages else False
        _, ext = os.path.splitext(req_page)
        if mypage:
            # OVERRIDE TO ADD LOCATION POINTES
            blog = request.env['blog.post'].sudo()
            event_obj = request.env['sgs.event'].sudo()
            partner_obj = request.env['sgs.partner'].sudo()
            res_partner_obj =request.env['res.partner'].sudo()
            # league_obj = request.env['sgs.league'].sudo()
            line_obj = request.env['league.fixture'].sudo()
            fixture_obj = request.env['league.fixture'].sudo()
            photo_obj = request.env['sgs.photo'].sudo()
            attachment = request.env['ir.attachment'].sudo()
            blog_id = http.request.env.ref("sgs.news_sgs").id
            try:

                res_events = []
                if( type( red.get('res_events_timestamp')) == bytes ):
                    prev_time = float( red.get('res_events_timestamp'))
                else:
                    prev_time = 0.0
                if( prev_time > time.time() - 600 ):
                    events_list = event_obj.search([('event_type', '=', 'public'), ('date', '>=', date.today())])
                    for event in events_list:
                        image_id = attachment.sudo().search([
                            ('res_model', '=', "sgs.event"),
                            ('res_field', '=', "cover"),
                            ('res_id', '=', event.id)
                        ])
                        res_events.append({
                            'name': event.name,
                            'date': event.date,
                            'description': event.description,
                            'id': event.id,
                            'image_url': ("/web/binary/image?model=ir.attachment&field=datas&id=" + str(image_id.id)) if image_id else '#',
                        })
                    red.mset({'res_events': pickle.dumps( res_events ), 'res_events_timestamp': time.time()})
                else:
                    res_events = pickle.loads( red.get('res_events'))

            except Exception as e:
                print( f"{e} {traceback.format_exc}" )


          
            partners_list = []
            try : 
                if( type( red.get('partners_list_timestamp')) == bytes ):
                    prev_time = float( red.get('partners_list_timestamp'))
                else:
                    prev_time = 0.0
            except Exception as e:
                prev_time = 0.0

            if( prev_time < time.time() - 600 ):
                for partner in partner_obj.search([]):
                    image_id = attachment.sudo().search([
                        ('res_model', '=', "sgs.partner"),
                        ('res_field', '=', "cover"),
                        ('res_id', '=', partner.id)
                    ])
                    if image_id:
                        partners_list.append(
                            "/web/binary/image?model=ir.attachment&field=datas&id=" + str(image_id.id))
                red.mset({'partners_list': pickle.dumps( partners_list ), 'partners_list_timestamp': time.time()})
            else:
                partners_list = pickle.loads( red.get('partners_list'))

            events_gallery = []
            try : 
                if( type( red.get('events_gallery_timestamp')) == bytes ):
                    prev_time = float( red.get('events_gallery_timestamp'))
                else:
                    prev_time = 0.0
            except Exception as e:
                prev_time = 0.0
            if( prev_time < time.time() - 600 ):
                for e in photo_obj.search([('section', '=', 'event')]):
                    image_id = attachment.sudo().search([
                        ('res_model', '=', "sgs.photo"),
                        ('res_field', '=', "image"),
                        ('res_id', '=', e.id)
                    ])
                    if image_id:
                        events_gallery.append(
                            "/web/binary/image?model=ir.attachment&field=datas&id=" + str(image_id.id))
                red.mset({'events_gallery': pickle.dumps( events_gallery ), 'events_gallery_timestamp': time.time()})
            else:
                events_gallery = pickle.loads( red.get('events_gallery'))

            tournament_gallery = []
            try : 
                if( type( red.get('tournament_gallery_timestamp')) == bytes ):
                    prev_time = float( red.get('tournament_gallery_timestamp'))
                else:
                    prev_time = 0.0
            except Exception as e:
                prev_time = 0.0
            if( prev_time < time.time() - 600 ):
                for e in photo_obj.search([('section', '=', 'tournament')]):
                    image_id = attachment.sudo().search([
                        ('res_model', '=', "sgs.photo"),
                        ('res_field', '=', "image"),
                        ('res_id', '=', e.id)
                    ])
                    if image_id:
                        tournament_gallery.append(
                            "/web/binary/image?model=ir.attachment&field=datas&id=" + str(image_id.id))
                red.mset({'tournament_gallery': pickle.dumps( tournament_gallery ), 'tournament_gallery_timestamp': time.time()})
            else:
                tournament_gallery = pickle.loads( red.get('tournament_gallery'))

            academy_gallery = []
            for e in photo_obj.search([('section', '=', 'academy')]):
                image_id = attachment.sudo().search([
                    ('res_model', '=', "sgs.photo"),
                    ('res_field', '=', "image"),
                    ('res_id', '=', e.id)
                ])
                if image_id:
                    academy_gallery.append(
                        "/web/binary/image?model=ir.attachment&field=datas&id=" + str(image_id.id))
            # league_gallery = []
            # for e in photo_obj.search([('section', '=', 'league')]):
            #     image_id = attachment.sudo().search([
            #         ('res_model', '=', "sgs.photo"),
            #         ('res_field', '=', "image"),
            #         ('res_id', '=', e.id)
            #     ])
            #     if image_id:
            #         league_gallery.append(
            #             "/web/binary/image?model=ir.attachment&field=datas&id=" + str(image_id.id))
            all_gallery = []
            for e in photo_obj.search([('section', '!=', '')]):
                image_id = attachment.sudo().search([
                    ('res_model', '=', "sgs.photo"),
                    ('res_field', '=', "image"),
                    ('res_id', '=', e.id)
                ])
                if image_id:
                    all_gallery.append(
                        "/web/binary/image?model=ir.attachment&field=datas&id=" + str(image_id.id))
            league_res = []
            today = datetime.today()
            fixtures_list = line_obj.search([('date', '>',today - timedelta(days=7)), ('state', '=', 'close')])


            for fixture in fixtures_list:
                fixture_res = []
                ts = fixture.players.search([('id', 'in', fixture.players.ids)], order='rank', limit=5)
                _logger.info(ts)
                for player in ts:
                    fixture_res.append({
                        'id':player.name.id,
                        'rank':player.rank,
                        'name': player.name.name,
                        'net': player.net,
                    })
                wn_partner = False
                wn = False
                wi = False
                if fixture_res:
                    wn = fixture_res[0]['name']
                    wn_partner = res_partner_obj.sudo().search([
                        ('id', '=', fixture_res[0]['id'])
                    ])




                    wi = '/image/get/' + str(fixture_res[0]['id'])
                    image_id = attachment.sudo().search([
                        ('res_model', '=', "res.partner"),
                        ('res_field', '=', "image"),
                        ('res_id', '=', fixture_res[0]['id'])
                    ])
                    if image_id:
                        wi ="/web/binary/image?model=ir.attachment&field=datas&id=" + str(image_id.id)
                league_res.append({
                    'fixture': fixture.name,
                    'winner': {'name':wn,'image':wi},
                    'league': fixture.league_id.name,
                    'fixture_results': fixture_res,
                    'wn_partner': wn_partner.image,

                })

            try : 
                if( type( red.get('leagues_timestamp')) == bytes ):
                    prev_time = float( red.get('leagues_timestamp'))
                else:
                    prev_time = 0.0
            except Exception as e:
                prev_time = 0.0

            if( prev_time < time.time() - 600 ):
                red.set('leagues_timestamp', time.time())
                leagues = cls.get_all_leagues(cls)
                red.mset({'leagues': pickle.dumps( leagues ), 'leagues_timestamp': time.time()})
            else:
                leagues = pickle.loads( red.get('leagues'))

            try : 
                if( type( red.get('league_results_box_timestamp')) == bytes ):
                    prev_time = float( red.get('league_results_box_timestamp'))
                else:
                    prev_time = 0.0
            except Exception as e:
                prev_time = 0.0

            if( prev_time < time.time() - 600 ):
                red.set('league_results_box_timestamp', time.time())
                running_leagues = cls.get_latest_running_leagues(cls, leagues)
                with open('/tmp/python-logs.log', 'a') as f:
                    f.write(f"running_leagues: {running_leagues} \n")

                # Now looping the running league and collecting their first tournament results in a list
                league_result_boxes = []
                for running_league in running_leagues:
                    league_results_box = cls.get_league_tournament_results(cls, running_league['event'])
                    league_results_box['sgs_leagueID'] = running_league['event']['id']
                    league_result_boxes.append(league_results_box)

                red.mset({
                    'league_result_boxes': pickle.dumps( league_result_boxes ),
                    'league_results_box_timestamp': time.time(),
                    'running_leagues': pickle.dumps(running_leagues)
                })
            else:
                league_result_boxes = pickle.loads( red.get('league_result_boxes'))
                running_leagues = pickle.loads(red.get('running_leagues'))

            return request.render('sgs.home', {
                # 'path': req_page[1:],

                'deletable': True,
                'main_object': mypage,
                'blog_posts': blog.search([('blog_id', '=', blog_id), ('website_published', '=', True)], limit=4),
                'partners': partners_list,
                'events': res_events,
                'events_gallery': events_gallery,
                'tournament_gallery': tournament_gallery,
                'academy_gallery': academy_gallery,
                'all_gallery': all_gallery,
                'league_results': league_res,
                'partner_presentation': request.env.ref('sgs.partner_book_init').id,
                'banner_images': request.env.ref('sgs.banner_images_init'),
                'test': "Hello World",
                'league_result_boxes': league_result_boxes,
                'leagues': running_leagues

            }, mimetype=_guess_mimetype(ext))
        return False
