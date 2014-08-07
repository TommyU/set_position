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

class position_employment(osv.osv):
    _name = 'position.employment'

    _columns = {
            'date_from': fields.date(string='From',  ),
            'date_to': fields.date(string='To',  ),
            'company': fields.char(size=100, string='Employer name', required=True, help="the company name "),
            'tel': fields.char(size=20, string='Telephone No.', required=False, help="the tel of the specified company"),
            'position': fields.char(size=20, string='Position', required=False, help="the position of the applier "),
            'salary': fields.float(string='Salary',  ),
            'leaving_reason': fields.char(size=512, string='Reasons of leaving', required=False, help="the reasens of leaving"),
            'name': fields.char(size=32, string='Name', required=False, help="name "),
            'application_id': fields.many2one('position.application', string='Position application',ondelete='cascade'  ),
    }

position_employment()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
