# -*- coding: utf-8 -*-
#/#############################################################################
#
#    Tommy.Yu
#    Copyright (C) 2004-TODAY Tommy.Yu(tommy.ywt@gmail.com).
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
{
    'name': 'recruitment request',
    'version': '1.0',
    'category': '',
    "sequence": 20,
    'complexity': "easy",
    'description': """
    common position application for company position management.

    for more information,please contact me at tommy.ywt@gmail.com.

    """,
    'author': 'Tommy.Yu',
    'website': 'tommy.ywt@gmail.com',
    'images': [],
    'depends': ['base','hr'],
    'init_xml': [],
    'update_xml': [
        'res_users.xml',
        'wizard/audit_win.xml',
        'position_audit/position_audit_view.xml',
        'security/set_position_security.xml',    
        'position_application/position_application_view.xml',
        'position_application/position_application_workflow.xml',
        'position_education/position_education_view.xml',
        'position_employment/position_employment_view.xml',
        'position_certification/position_certification_view.xml',
        'position_skills/position_skills_view.xml',
        'position_contract/position_contract_view.xml',        
        'position_grade/position_grade_view.xml',
        'security/ir.model.access.csv',            
    ],
    'demo_xml': [],
    'test': [

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
