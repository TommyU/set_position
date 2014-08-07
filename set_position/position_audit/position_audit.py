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

class position_audit(osv.osv):
    _name = 'position.audit'
    
    def _step_get(self, cr, uid, ids, name, arg, context=None):
        step_translation={'draft':u'草稿',
                          'HR':u'人事审批',
                          'sectionManager':u'课长审批',
                          'deptManager':u'部长审批',
                          'VP':u'总经理审批',
                          'president':u'董事长审批',
                          'contract':u'合同录入',
                          'done':u'完成',
                          'cancel':u'取消',
                          }
        if context is None:
            context = {}
        result = {}
        for audit in self.browse(cr, uid, ids, context=context):
            result[audit.id] = step_translation.get(audit.step,audit.step)
        return result

    def _step_set(self, cr, uid, id, name, value, arg, context=None):
        super(position_audit, self).write(cr, uid, [id], {'step': value}, context=context)
        return True
    
    def _op_type_get(self, cr, uid, ids, name, arg, context=None):
        op_type_translation={'submit':u'提交','reject':'退回','cancel':u'撤销'}
        if context is None:
            context = {}
        result = {}
        for audit in self.browse(cr, uid, ids, context=context):
            result[audit.id] = op_type_translation.get(audit.op_type,audit.op_type)
        return result

    def _op_type_set(self, cr, uid, id, name, value, arg, context=None):
        super(position_audit, self).write(cr, uid, [id], {'op_type': value}, context=context)
        return True

    _columns = {
            'approver': fields.many2one('res.users', string='Approver',  ),
            'date': fields.datetime(string='Date',  ),
            'model': fields.many2one('ir.model', string='Model',  ),
            'res_id': fields.integer(string='resource id',  ),
            'step': fields.char(size=256, string='Step', required=False, help="the step/status of  the auditing flow"),
            'op_type': fields.char(size=256, string='Operation type', required=False, help="the type of the operation"),
            'step_text':fields.function(_step_get, fnct_inv=_step_set, string='Step', type="char"),
            'op_type_text':fields.function(_op_type_get, fnct_inv=_op_type_set, string='Operation type', type="char"),
            'comment': fields.text(string='Comment(s)',  ),
            'name': fields.char(size=128, string='Name', required=False, help="Name "),
    }
    
position_audit()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
