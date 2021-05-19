# -*- coding: utf-8 -*-

from odoo import models, fields, api
import ast
from datetime import datetime, date
import logging

_logger = logging.getLogger(__name__)

GENDERS = [
    ('male', "Male"),
    ('female', "Female"),
]
HANDS = [
    ('right', "Right"),
    ('left', "Left"),
]

USERS_TYPES = [
    ('play', "SGS Play"),
    ('member', "SGS Member"),
    ('pro', "SGS Pro")
]

PACKAGES_PRIORITIES = [
    ('play', "Play"),
    ('member', "Member"),
    ('pro', "Pro"),
]

SGS_CONSTANT = 1


class Profile(models.Model):
    _inherit = "res.partner"

    gender = fields.Selection(GENDERS, "Gender", default='male', )
    date_of_birth = fields.Date("Date of Birth")
    handicap_par = fields.Char("Par 3 Handicap")
    handicap_par_url = fields.Char("Par 3 Handicap URL")
    handicap_official = fields.Char("Official Handicap")
    hand = fields.Selection(HANDS, "Hand", default='right')
    size_glove = fields.Char("Glove Size")
    size_shirt = fields.Char("Shirt Size")
    sgs_gain = fields.Text("WHAT WOULD YOU LIKE TO GAIN FROM BEING AN SGS MEMBER?")
    membership_no = fields.Char("Membership N.O.", compute="_generate_membership_no")
    # egf_no=fields.Char('EGF No')
    # egolf_no=fields.Char('EGolf No')
    package_id = fields.Many2one('sgs.package', "Subscription Package")
    expiry_date = fields.Date("Expiry Date")
    user_type = fields.Selection(USERS_TYPES, "User Type", default='play')
    expired_users = fields.Boolean(compute='_compute_expired_user', string="Expired Users", store=True)

    @api.depends('is_company', 'name', 'parent_id.name', 'type', 'company_name')
    def _compute_display_name(self):
        for partner in self:
            partner.display_name = partner.name

    @api.depends('expiry_date')
    def _compute_expired_user(self):
        current_date = datetime.now().date()
        _logger.info("========================================")
        _logger.info(current_date)
        for each in self:
            if each.expiry_date:

                if each.expiry_date > current_date:
                    _logger.info("****************")
                    _logger.info(each.expiry_date)
                    each.expired_users = False
                else:
                    each.expired_users = True

    def open_my_profile(self):
        view_id = self.env.ref("sgs.myprofile_form_view")
        view_id = view_id and view_id.id or False
        return {
            'name': 'My Profile',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.partner',
            'res_id': self.env.user.partner_id.id,
            'view_id': view_id,
            'context': {'user_id': self.env.user.id, 'no_create': True, 'no_edit': True},
            'type': 'ir.actions.act_window',
        }

    @api.one
    def _generate_membership_no(self):
        tar = self.id * SGS_CONSTANT
        self.membership_no = "SGS-" + "{:0>5}".format(tar)

    def archive_partner(self):
        partner_user = self.env['res.users'].search([('partner_id', '=', self.id)], limit=1)
        if partner_user:
            partner_user.archive_user()
        self.active = False

    def reactivate_partner(self):
        partner_user = self.env['res.users'].search([('partner_id', '=', self.id)], limit=1)
        if partner_user:
            partner_user.reactivate_user()
        self.active = True


class User(models.Model):
    _inherit = 'res.users'

    package_id = fields.Many2one('sgs.package', "Package")
    user_type = fields.Selection(USERS_TYPES, "User Type", related='partner_id.user_type', default='customer')

    def archive_user(self):
        self.active = False

    def reactivate_user(self):
        self.active = True


class UserPackage(models.Model):
    _name = 'sgs.package'
    _description = "User Subscription Packages"

    name = fields.Char("Name", required=True)
    price = fields.Float("Price")
    cover = fields.Binary("Cover", attachment=True)
    description = fields.Text("Description")
    priority = fields.Selection(PACKAGES_PRIORITIES, "Priority", required=True, default='play')
    validity = fields.Integer("Validity/ days")
    expiry_date = fields.Date("Expiry Date")