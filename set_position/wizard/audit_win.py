# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################

from openerp.osv import osv, fields
from openerp.tools.translate import _
from openerp import netsvc

class audit_win(osv.osv_memory):
    _name = "audit.win"
    _description = "auditting window"
    
    _columns = {
                'name':fields.char(string=u'To do',help='the name of this action',size=128,),
                'comment':fields.char(string=u'comments',help='the infomation you want to deliver to person of the next step',size=512),
    }
    _defaults = {
        #'name': 1,
    }
    
    #审核动作
    def audit_win_submit(self,cr,uid,ids,context):
        model = context.get('model','position.application')
        res_ids = context.get('active_ids',[context.get('active_id')])
        obj = self.pool.get(model)
        fn = getattr(obj,context.get('method'))
        if not fn:
            return False
        audit = self.browse(cr,uid,ids[0])
        if audit:
            context.update({'title':audit.name,'comment':audit.comment})
        fn(cr,uid,res_ids,context)
        return True
    
    
    def load_view(self,cr,uid,ids,context=None):
        return {
            'domain': [],
            'name':u'职位申请表',
            'view_id':False,
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model': 'position.application',
            'type':'ir.actions.act_window',
            'context':{},
        }
    
  

audit_win()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
