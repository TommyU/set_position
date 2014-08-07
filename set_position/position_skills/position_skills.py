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

class position_skills(osv.osv):
    _name = 'position.skills'

    _columns = {
            'name': fields.char(size=32, string='Name', required=True, help="name of the skill"),
            'level': fields.selection([('excellent','excellent'),('fair','fair'),('general','general'),('poor','poor')], string='Level',  ),
            'remark': fields.char(size=100, string='Remark(s)', required=False, help="note/memo etc."),
            'application_id': fields.many2one('position.application', string='Position application',ondelete='cascade'  ),
    }

position_skills()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
