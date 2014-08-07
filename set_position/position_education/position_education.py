# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tommy.Yu
#    Copyright (C) 2004-TODAY Tommy.Yu(https://me.alipay.com/tommysz).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#/#############################################################################
from osv import osv, fields

class position_education(osv.osv):
    _name = 'position.education'

    _columns = {
            'school': fields.char(size=100, string='School', required=True, help="school that the applier was ever in"),
            'date_from': fields.date(string='From',  ),
            'date_to': fields.date(string='To',  ),
            'major': fields.char(size=512, string='Major', required=False, help="the main course "),
            'qualification': fields.char(size=200, string='Qualification', required=False, help="the qualification of the applier"),
            'name': fields.char(size=32, string='Name', required=False, help="Name of this record"),
            'application_id': fields.many2one('position.application', string='Position application', ondelete='cascade' ),
    }

position_education()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
