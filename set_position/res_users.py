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

class res_users(osv.osv):
    """ 
       modification: add a attribute emplyee_id attribute to the model        
    """
    _inherit = "res.users"

    _columns = {
        'employee_id': fields.many2one('hr.employee', required=False,
            string='Related Employee', ondelete='restrict',
            help='Employee-related data of the user'),
    }
    
res_users()
