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

class position_certification(osv.osv):
    _name = 'position.certification'
    _rec_name="copies_name"
    
    def _data_get(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        result = {}
        #location = self.pool.get('ir.config_parameter').get_param(cr, uid, 'ir_attachment.location')
        #bin_size = context.get('bin_size')
        for attach in self.browse(cr, uid, ids, context=context):
            #if location and attach.store_fname:
            #    result[attach.id] = self._file_read(cr, uid, location, attach.store_fname, bin_size)
            #else:
            result[attach.id] = attach.copies_data
        return result

    def _data_set(self, cr, uid, id, name, value, arg, context=None):
        # We dont handle setting data to null
        super(position_certification, self).write(cr, uid, [id], {'copies_data': value}, context=context)
        return True


    _columns = {
            'name': fields.char(size=32, string='Name', required=True, help="name of the certification/originals"),
            'original_checked': fields.boolean(string='Originals checked',  ),
            'copies_reserved': fields.boolean(string='Copies reserved',  ),
            'copies_data': fields.binary(string='Copies'),
            'copies': fields.function(_data_get, fnct_inv=_data_set, string='Copies', type="binary", nodrop=True),
            'copies_name':fields.char(string='File name',size=256),
            #'copies':fields.one2many('ir.attachment', 'res_id', string='attchments of the originals',  ),
            'remark': fields.char(size=256, string='Remark(s)', required=False, help="note,memo etc"),
            'identifier': fields.many2one('res.users', string='Identifier',  ),
            'application_id': fields.many2one('position.application', string='Position application',ondelete='cascade'  ),
    }

position_certification()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
