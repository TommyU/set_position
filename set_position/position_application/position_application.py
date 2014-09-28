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
from openerp import tools
from openerp.tools.translate import _
from openerp import netsvc
import time
from urllib import urlencode
from urlparse import urljoin

class position_application(osv.osv):
    _name = 'position.application'
    _has_full_access=False
    
    '''
    def __init__(self, pool, cr):
        super(position_application.self).__init__(pool,cr)
        _has_access = self.has_access(cr, uid)
    '''
    
    def _init_originals(self):
        return [[0,False,{u'name':u'身份证\n(ID CARD)'}],
                [0,False,{u'name':u'学历证\n(DIPLOMA)'}],
                [0,False,{u'name':u'健康、残疾证\n(PROOF OF HEALTH, DEFORMITY)'}],
                [0,False,{u'name':u'离职证明\n(PROOF OF DIMISION)'}],
                [0,False,{u'name':u'其他\n(OTHERS)'}],
                ]
        
    def _init_skills(self):
        return [[0,False,{u'name':u'英语(ENGLISH)'}],
                [0,False,{u'name':u'日语(JAPANESE)'}],
                [0,False,{u'name':u'广东话(CANTO.NESE)'}],
                [0,False,{u'name':u'电子(ELECTRONICS)'}],
                [0,False,{u'name':u'机械(MECHANICAL)'}],
                [0,False,{u'name':u'电脑(COMPUTER)'}],
                [0,False,{u'name':u'物理(PHYSICS)'}],
                [0,False,{u'name':u'数学(MATHS)'}],                
                ]
        
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.photo, avoid_resize_medium=True)
        return result

    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'photo': tools.image_resize_image_big(value)}, context=context)
    
    '''
    def _validate_user(self, cr, uid, ids, *a):
        res = {}
        my_dept_id= self.pool.get('hr.employee').browse(cr,1,uid).department_id.id
        for app in self.browse(cr,uid,ids):
            res[app.id] = (my_dept_id == app.target_department.id)
        return res
   '''

    _columns = {
            'state':fields.selection([(u'draft',u'draft'),
                                      #(u'origalsConfirming',u'Origals Confirming'),
                                      (u'HR',u'HR'),
                                      #(u'skills',u'Skills'),
                                      (u'sectionManager',u'Section Manager'),
                                      (u'deptManager',u'Dept. Manager'),
                                      (u'VP',u'Vice President'),
                                      (u'president',u'President'),
                                      (u'contract',u'Contract'),
                                      (u'done',u'Done'),
                                      (u'cancel',u'cancel'),],string='state', readonly=True),
            'application_date': fields.date(string='Date of application', readonly=True, states={'draft': [('readonly', False)]},required=True, ),
            'position_applied': fields.char(size=50, string='Position applied', readonly=True , states={'draft': [('readonly', False)]}, required=True, help="Position applied"),
            'expected_salary': fields.char(size=512, string='Expected salary', readonly=True , states={'draft': [('readonly', False)]}, required=False, help="Expected salary(currency:RMB), m ~ n RMB or anything"),
            'date_available': fields.date(string='Date available', readonly=True , states={'draft': [('readonly', False)]},  ),
            'staff_no': fields.char(size=20, string='NO.', readonly=True , states={'contract': [('readonly', False)]}, required=False, help="the staff number of the applier"),
            'photo': fields.binary(string='Photo', states={'draft': [('readonly', False)],'HR': [('readonly', False)]}, readonly=True  ),
            'chinese_name': fields.char(size=20, string='Name in Chinese', readonly=True, states={'draft': [('readonly', False)]}, required=True, help="Chinese' name if you have, or any name"),
            'english_name': fields.char(size=20, string='Name in English', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="English name if you have "),
            'sex': fields.selection([('female','female'),('male','male')], string='Sex', states={'draft': [('readonly', False)]}, readonly=True,  ),
            'nationality': fields.char(size=32, string='Nationality', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="the nationality of the employee"),
            'nation': fields.char(size=32, string='Nation', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="the nation of the employee"),
            'permanent_address': fields.char(size=512, string='Permanent address', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="the place where you're born "),
            'birthday': fields.date(string='Date of birth', readonly=True, states={'draft': [('readonly', False)]},  ),
            'height': fields.float(string='Height', readonly=True, states={'draft': [('readonly', False)]},  ),
            'telephone': fields.char(size=20, string='Telephone', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="the applier's telephone"),
            'Id_no': fields.char(size=20, string='I.D.NO.', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="the number of the identity card of the applier"),
            'id_address': fields.char(size=512, string='I.D. Address', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="the address on the I.D. card"),
            'address': fields.char(size=512, string='Address', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="the place where the applier can be touched"),
            'emergency_contact': fields.char(size=20, string='Emergency contact', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="emergency contact"),
            'relationship': fields.char(size=32, string='Relationship', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="Relation between the applier and the emergency contact person."),
            'tel_no': fields.char(size=20, string='TEL NO.', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="tel number of the emergency contact person"),
            'marital_status': fields.selection([('single','single'),('married','married'),('divorced','divorced'),('widowed','widowed')], string='Marital status', readonly=True, states={'draft': [('readonly', False)]},  ),
            'spouse_name': fields.char(size=20, string='Name of spouse', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="Name of the applier's spouse"),
            'child_number': fields.integer(string='NO. of children', readonly=True, states={'draft': [('readonly', False)]},  ),
            'handedness': fields.selection([('left','left'),('right','right')], string='Handedness', readonly=True, states={'draft': [('readonly', False)]},  ),
            'smoking': fields.boolean(string='Smoking', readonly=True, states={'draft': [('readonly', False)],'HR':[('readonly', False)]},  ),
            'left_eyesight': fields.float(string='Left eyesight', readonly=True, states={'draft': [('readonly', False)]},  ),
            'right_eyesight': fields.float(string='right eyesight', readonly=True, states={'draft': [('readonly', False)]},  ),
            'major_surgery': fields.char(size=512, string='Major surgery', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="the major surgery of the applier"),
            'occupational_diseases': fields.char(size=512, string='Occupational diseases', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="the occupational diseases of the applier"),
            'other_diseases': fields.char(size=512, string='Other diseases', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="other diseases of the applier"),
            'health': fields.selection([('good','good'),('delecate','delecate')], string='Health', readonly=True, states={'draft': [('readonly', False)]},  ),
            'education': fields.one2many('position.education', 'application_id', string='Education history', readonly=True, states={'draft': [('readonly', False)]},  ),
            'other_specialities': fields.char(size=512, string='Other specialities', readonly=True, states={'draft': [('readonly', False)]}, required=False, help="other things that the applier is good at"),
            'employment': fields.one2many('position.employment', 'application_id', string='Employment', readonly=True, states={'draft': [('readonly', False)]},  ),
            'originals_verification': fields.one2many('position.certification', 'application_id', string='Verification of originals', readonly=True, states={'HR': [('readonly', False)]},   ),
            'hr_comments': fields.text(string='Comment(s) of hr manager', readonly=True, states={'draft': [('readonly', False)],'HR': [('readonly', False)]},  ),
            'skills': fields.one2many('position.skills', 'application_id', string='level of skills', readonly=True, states={'sectionManager': [('readonly', False)]}, ),
            'section_supervisor_comment': fields.text(string='Comments from section supervisor', readonly=True, states={'sectionManager': [('readonly', False)]},  ),
            'dept_manager_comment': fields.text(string='Comment(s) from dept manager', readonly=True, states={'deptManager': [('readonly', False)]},  ),
            'position_assigned': fields.many2one('hr.job', string='Position(assigned)', readonly=True, states={'deptManager': [('readonly', False)]},  ),
            'grade': fields.many2one('position.grade', string='Grade', readonly=True, states={'deptManager': [('readonly', False)]},  ),
            'suggested_start_salary': fields.float(string='Suggested starting salary', readonly=True, states={'deptManager': [('readonly', False)]},  ),
            'currency': fields.many2one('res.currency', string='Currency', readonly=True, states={'deptManager': [('readonly', False)]},  ),
            'gm_comment': fields.selection([('accepted','accepted'),('unsuitable','not suitable'),('reserved','reserved')], string='G.M.', readonly=True, states={'VP': [('readonly', False)]},  ),
            'gm_remark': fields.text(string='Remark', readonly=True, states={'VP': [('readonly', False)]},  ),
            'gm_suggested_position': fields.many2one('hr.job', string='Position', readonly=True, states={'VP': [('readonly', False)]},  ),
            'gm_starting_salary': fields.float(string='Starting salary', readonly=True, states={'VP': [('readonly', False)]},  ),
            
            'president_comment': fields.selection([('accepted','accepted'),('unsuitable','not suitable'),('reserved','reserved')], string='President(comment)', readonly=True, states={'president': [('readonly', False)]},  ),
            'president_remark': fields.text(string='Remark', readonly=True, states={'president': [('readonly', False)]},  ),
            'final_starting_salary': fields.float(string='Starting salary', readonly=True, states={'president': [('readonly', False)]},  ),
            'final_position': fields.many2one('hr.job', string='Position', readonly=True, states={'president': [('readonly', False)]},  ),
            'contract_info': fields.one2many('position.contract', 'application_id', string='Position contract', readonly=True, states={'contract': [('readonly', False)]},  ),

            'name':fields.char(string = u'Name', readonly=True,size=64,),
            'image_medium': fields.function(_get_image, fnct_inv=_set_image,
                string="Medium-sized image", type="binary", multi="_get_image",
                store={
                    'position.application': (lambda self, cr, uid, ids, c={}: ids, ['photo'], 10),
                },
                help="Medium-sized image of the applier. It is automatically "\
                     "resized as a 128x128px image, with aspect ratio preserved, "\
                     "only when the image exceeds one of those sizes. Use this field in form views or some kanban views.",
                     states={'draft': [('readonly', False)],'HR': [('readonly', False)]}, readonly=True),
            'image_small': fields.function(_get_image, fnct_inv=_set_image,
                string="Small-sized image", type="binary", multi="_get_image",
                store={
                    'position.application': (lambda self, cr, uid, ids, c={}: ids, ['photo'], 10),
                },
                help="Small-sized image of the applier. It is automatically "\
                     "resized as a 64x64px image, with aspect ratio preserved. "\
                     "Use this field anywhere a small image is required."),
            #'attachments':fields.one2many('ir.attachment','res_id',string='attachments',),
            'target_department':fields.many2one('hr.department',string='target department',readonly=True,required=True,states={'draft': [('readonly', False)],'HR': [('readonly', False)]},help='department that the applier will work in if he/she is accepted.'),
            #'current_user_validation':fields.function(_validate_user,type='bool',string='current user validation',help='a sign indicates whether the current user is in the department specified by target_department attribute.',store=False),
            
    }
    
    _defaults={
               'application_date':fields.date.context_today,
               'originals_verification':lambda self, cr, uid, context:self._init_originals(),
               'skills':lambda self, cr, uid, context:self._init_skills(),
               'state':u'draft',
               'currency':8,
               }
    
    
    
    def get_verification(self,cr,uid,ids,context=None):
        """报表调用的方法，  yang.cai 2014.3.5 add
        """
        res={}
        positions=self.browse(cr,uid,ids,context)
        index=1
        for position in positions:
            for ver in position.originals_verification:
                res['a_'+str(index)]=ver.original_checked
                res['b_'+str(index)]=ver.copies_reserved
                index=index+1
                
        return res 
    
    def get_skills_name(self,cr,uid,ids,str,type,context=None):
        """报表调用函数，yang.cai 2014.3.25 add
        """
        arr=str.split('(')
        if type=='eng':
            ts='('+arr[1];
            return ts
        if type=='china':
            #ts=str(arr[0]).decode('gb2312')
            ts=arr[0]
            return ts
        
        return str

    
    def create(self,cr,uid,vals,context=None):
        if vals.get('name','')=='':
            vals['name'] = u'[%s]%s %s 职位申请表'%(vals.get('application_date',fields.date.context_today),vals.get('chinese_name',u'某人'),vals.get('position_applied',u'某职位'))
        return super(position_application,self).create(cr,uid,vals,context)
    
    def unlink(self,cr,uid,ids,context=None):
        for app in self.browse(cr,uid,ids,context):
            if app.state !='draft':
                raise osv.except_osv(_(u'无法删除'),_(u'无法删除非草稿状态的申请单'))
        return super(position_application,self).unlink(cr,uid,ids,context)
    
    #触发工作流
    def run_flow(self,cr,uid,ids,context=None):
        if context.get('signal',False):
            #1. 触发工作流跳转
            signal = context.get('signal')
            model = context.get('model',False)
            del(context['signal'])            
            if model:
                del(context['model'])
            else:
                model = "position.application"    
            if context.get('method',False):
                del(context['method'])
            wf_service = netsvc.LocalService("workflow")            
            [wf_service.trg_validate(uid, model, app_id, signal, cr) for app_id in ids]
            
            #2. 写日志
            comment = context.get('comment',False)
            if comment:
                del(context['comment'])
            title = context.get('title',False)
            if title:
                del(context['title'])
            current_step = context.get('current_step',False)#we don't use step info from context
            if context.get('current_step',False):
                del(context['current_step'])
            op_type = context.get('type',False)
            if op_type:
                del(context['type'])
            #uid,model,current_step,op_type,title,comment
            model_id = self.pool.get('ir.model').search(cr,1,[('model','=',model)])
            log_obj = self.pool.get('position.audit')
            [log_obj.create(cr,1,{
                  'approver':uid,
                  'date':time.strftime('%Y-%m-%d %H:%M:%S'),
                  'model':model_id[0] or False,
                  'res_id':res_id,
                  'step':current_step,
                  'op_type':op_type,
                  'comment':comment,
                  'name':title,
                  },context) for res_id in ids]
            
            #3. 发送邮件
            self.send_email(cr, uid, ids,current_step, op_type, title, comment)
            
            return True
        return False         
    
    def send_email(self,cr,uid,ids,current_step,op_type,title,comment,context=None):   
        '''
        '  发送邮件
        '''
        oper= self.pool.get('res.users').browse(cr,1,uid)
        mail_obj = self.pool.get('mail.mail')
        
        base_url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'web.base.url')
        query = {'db': cr.dbname}
        
        for app in self.browse(cr,uid,ids):
            #1.计算收件人列表
            #1)next step
            route_info =self._get_route_info(cr, current_step, op_type)
            
            next_user_list=route_info[1]
            additional_msg=route_info[2]
            next_steps= route_info[3]
            #发送邮件
            mail_to=self._get_mail_list(cr, app, next_user_list, next_steps)
            mail_cc_list =''
            fragment = {
                    'login': oper.login,
                    'model': 'position.application',
                    'id': app.id,
                }
            url = urljoin(base_url, "?%s#%s" % (urlencode(query), urlencode(fragment)))
            subject = app.name + 'has been '+ op_type +'ed'
            mail_id = mail_obj.create(cr,1,
                                 {'subject':subject,
                                  #'body':comment,
                                  'type':'email',
                                  #'date':fields.date.context_today,
                                  'email_from':'es@set-china.com',
                                  'email_to': mail_to,
                                  'email_cc': mail_cc_list,
                                  'body_html':"<span style='display:block; color:gray;'>"+
                                                                     additional_msg.replace("\n","<br>") + 
                                                                     #("</span><br><b>Comments from Mr./MS %s:</b><br>(%s先生/小姐的备注:)<br><br>"%(oper,oper)) +
                                                                     u'<table style=\'border-collapse:collapse;\'>'+
                                                                     u'<tr><td style=\'border:solid 1px #112233; width:200px; background-color:skyblue;\'>position application:<br>(职位申请表:)<br></td><td style=\'border:solid 1px #112233; width:400px\'>'+app.name+'</td></tr>'+
                                                                     u'<tr><td style=\'border:solid 1px #112233; width:200px; background-color:skyblue;\'>submitter:<br>(提交人:)<br></td><td style=\'border:solid 1px #112233; width:400px\'>'+oper.name+'</td></tr>'+
                                                                     u'<tr><td style=\'border:solid 1px #112233; width:200px; background-color:skyblue;\'>operation:<br>(操作:)<br></td><td style=\'border:solid 1px #112233; width:400px\'>'+op_type+'</td></tr>'+
                                                                     u'<tr><td style=\'border:solid 1px #112233; width:200px; background-color:skyblue;\'>summery:<br>(意见概要:)<br></td><td style=\'border:solid 1px #112233; width:400px\'>'+(title or ' ')+ '</td></tr>'+
                                                                     u'<tr><td style=\'border:solid 1px #112233; width:200px; background-color:skyblue;\'>detailed comment:<br>(意见详细:)<br></td><td style=\'border:solid 1px #112233; width:400px\'>'+(comment or ' ') +'</td></tr>'+
                                                                     u'<tr><td style=\'border:solid 1px #112233; width:200px; background-color:skyblue;\'>application link:<br>(申请表链接:)<br></td><td style=\'border:solid 1px #112233; width:400px\'><a href=\''+url+'\' target=\'_blank\'>'+app.name+'</a></td></tr>'+
                                                                     u'</table>' +
                                                                     u"<br>"+"="*64+
                                                                     u"<span style='display:block; color:gray;'>note(注意事项):<br>please do not reply on this email because it is a system email thus nobody will response to your reply.<br>请勿回复此邮件，因为这个是系统自动发送的邮件。<br>please do not transfer this email for information security.<br>为了信息保密安全请勿转发此邮件。</span>"
                                                                     +"="*64  
                                  }
                                 )
            mail_obj.send(cr,1,[mail_id])
            
    def _get_route_info(self,cr,current_step,operation_type,):
        '''
        ' 获取(下个节点的用户组，下个节点的用户组里面的所有用户(不考虑部门)，当前审批环节系统提示信息)
        '''
        route=[('draft','submit','HR',u'''The position application has been submitted by the applier,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由申请人提交，如果您收到这个提示，意味着您可能需要审核/补充资料/查阅这个申请表资料。
                                        '''),
               ('HR','submit','sectionManager',u'''The position application has been submitted by the H.R.,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由人资(确认资料并简评后)提交，如果您收到这个提示，意味着您可能需要审核/补充资料/查阅这个申请表资料。
                                        '''),
               ('sectionManager','submit','deptManager',u'''The position application has been submitted by the related section manager,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由相关部门主任/课长(技能确定并简评后)提交，如果您收到这个提示，意味着您可能需要审核/补充资料/查阅这个申请表资料。
                                        '''),
               ('deptManager','submit','VP',u'''The position application has been submitted by the related department manager,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由相关部门部长(填写意见后)提交，如果您收到这个提示，意味着您可能需要审核/补充资料/查阅这个申请表资料。
                                        '''),
               ('VP','submit','president',u'''The position application has been submitted by the vice president,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由董事总经理(填写意见后)提交，如果您收到这个提示，意味着您可能需要审核/补充资料/查阅这个申请表资料。
                                        '''),
               ('president','submit','contract',u'''The position application has been submitted by the president,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由董事长(填写意见后)提交，如果您收到这个提示，意味着您可能需要审核/补充资料/查阅这个申请表资料。
                                        '''),
               ('contract','submit','done',u'''The position application has been submitted by the H.R.,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由人资(录入后同)提交，如果您收到这个提示，意味着您可能需要审核/补充资料/查阅这个申请表资料。
                                        '''),
                
                
               ('president','reject','VP',u'''The position application has been rejected by the president,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由董事长退回，如果您收到这个提示，意味着您可能需要审核/补充资料/查阅这个申请表资料。
                                        '''),
               ('VP','reject','deptManager',u'''The position application has been rejected by the vice president,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由董事总经理退回，如果您收到这个提示，意味着您可能需要审核/补充资料/查阅这个申请表资料。
                                        '''),
               ('deptManager','reject','sectionManager',u'''The position application has been rejected by the related department manager,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经相关部门部长退回，如果您收到这个提示，意味着您可能需要审核/补充资料/查阅这个申请表资料。
                                        '''),
               ('sectionManager','reject','HR',u'''The position application has been rejected by the related section manager,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由相关部门课长退回，如果您收到这个提示，意味着您可能需要审核/补充资料/查阅这个申请表资料。
                                        '''),
               
               
               ('HR','cancel','cancel',u'''The position application has been canceled by the H.R.,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由人资课撤销，如果您收到这个提示，意味着您可能需要审核查阅这个申请表资料。
                                        '''),
               ('contract','cancel','cancel',u'''The position application has been canceled by the H.R.,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由人资课撤销，如果您收到这个提示，意味着您可能需要查阅这个申请表资料。
                                        '''),
               ('president','cancel','cancel',u'''The position application has been canceled by the president,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由董事长撤销，如果您收到这个提示，意味着您可能需要查阅这个申请表资料。
                                        '''),               
               ('VP','cancel','cancel',u'''The position application has been canceled by the vice president,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由董事总经理撤销，如果您收到这个提示，意味着您可能需要查阅这个申请表资料。
                                        '''),
               ('deptManager','cancel','cancel',u'''The position application has been canceled by the related department manager,If you hava receive this email, it means you may need to react to or just know about this.\n
                                          职位申请表已经由相关部门部长，如果您收到这个提示，意味着您可能需要查阅这个申请表资料。
                                        '''),               
                ]

        next_steps=filter(lambda x:x,map(lambda x:x[0]==current_step and x[1]==operation_type and x[2],route))
        additional_msg = map(lambda x:x[3],filter(lambda x:x[0]==current_step and x[1]==operation_type and x[2],route))
        if additional_msg:
            additional_msg = additional_msg[0]
        #2)step - group mapping
        step_group =[('draft','set_position.menu_guest'),
                          ('HR','set_position.menu_hr'),
                          ('sectionManager','set_position.menu_sm'),
                          ('deptManager','set_position.menu_dm'),
                          ('VP','set_position.menu_vp'),
                          ('president','set_position.menu_president'),
                          ('contract','set_position.menu_hr'),
                          ('done','set_position.menu_sm'),
                          ('cancel','set_position.menu_hr,set_position.menu_sm'),
                          ]
        
        next_user_groups=[]
        for n_step in next_steps:
            temp = map(lambda x:x[1],filter(lambda x:x[0]==n_step and x[1],step_group))
            next_user_groups = next_user_groups + list(temp)
            
        #next users
        next_user_list=[]
        obj = self.pool.get('ir.model.data')
        for n_group in next_user_groups:
            if n_group and not bool(n_group.strip()):
                    continue
            for s_group in n_group.split(','):
                if s_group and not bool(s_group.strip()):
                    continue
                app= s_group[ :s_group.find('.')]
                role = s_group[s_group.find('.')+1:]
                group_obj = obj.get_object(cr, 1, app, role)
                next_user_list = next_user_list+map(lambda x:x.id,group_obj.users)   
        return (next_user_groups,next_user_list,additional_msg,next_steps)
            
    def _get_mail_list(self,cr,application,mail_to_user_ids,next_steps):
        '''
                      获取邮件列表，格式：mail1,mail2,mail3 .
                      精确控制邮件范围（特别是部门审批和总经理审批时）
        '''
        next_step = next_steps[0] if next_steps else False#TODO:一个节点多个分支出去的情况
        if not next_step:
            raise Exception(u'Next step not found.')
        user_obj = self.pool.get('res.users')
        mail_to_addrs=''
        if next_step in ('sectionManager','deptManager'):#只发给相应部门
            mail_to_addrs = map(lambda x:x.notification_email_send!='none' and x.employee_id and x.employee_id.department_id.id ==application.target_department.id and x.email or '', user_obj.browse(cr,1,mail_to_user_ids))
        else:
            if next_step in ('VP',):#总经理
                #如果是 注塑/模具课，只到副总审批即可。其他正常(此部分硬编码,TODO:用配置实现)
                ym_uid = user_obj.search(cr,1,[(u'name','like',u'某某副总')])
                if u'注塑' in application.target_department.name or u'模具' in application.target_department.name:
                    mail_to_user_ids=ym_uid
                else:
                    mail_to_user_ids = list(set(mail_to_user_ids) - set(ym_uid))                  
                mail_to_addrs = map(lambda x:x.notification_email_send!='none' and x.email or '', user_obj.browse(cr,1,mail_to_user_ids))#TODO: design a fix for users who do not want system notification
            else:
                mail_to_addrs = map(lambda x:x.notification_email_send!='none' and x.email or '', user_obj.browse(cr,1,mail_to_user_ids))#TODO: design a fix for users who do not want system notification
        mail_to=''
        for addr in mail_to_addrs:
            if addr:
                mail_to +=addr+','        
        mail_to=mail_to.rstrip(',')
        return mail_to
    
    def fields_view_get(self, cr, user, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        '''重写以实现用户权限初始化'''
        result = super(position_application,self).fields_view_get( cr, user, view_id, view_type, context, toolbar, submenu)
        self._has_full_access = self.has_access(cr, user)
        return result
    '''
    def read(self, cr, user, ids, fields=None, context=None, load='_classic_read'):
        #context.update({''})
        result = super(position_application,self).read( cr, user, ids, fields, context, load)
        return result
    '''
   
    def has_access(self,cr,uid):
        '''权限判断'''
        if uid==1:
            return True
        #检查用户组，查看当前用户是否在相应的组（人事组/总经理组/董事长组）
        validated_list=[]
        obj = self.pool.get('ir.model.data')
        group_obj = obj.get_object(cr, uid, 'set_position', 'menu_hr')
        validated_list = validated_list+map(lambda x:x.id,group_obj.users)
        '''
        if uid in validated_list:
            return True
        group_obj = obj.get_object(cr, uid, 'set_position', 'menu_vp')
        validated_list = validated_list+map(lambda x:x.id,group_obj.users)
        '''
        
        if uid in validated_list:
            return True
        group_obj = obj.get_object(cr, uid, 'set_position', 'menu_president')
        validated_list = validated_list+map(lambda x:x.id,group_obj.users)

        if uid in validated_list:
            return True
                
        return False
    
    def _is_vp(self,cr,uid):
        '''判断uid是不是总经理'''
        group_obj = self.pool.get('ir.model.data').get_object(cr, uid, 'set_position', 'menu_vp')
        return uid in map(lambda x:x.id,group_obj.users)
    
    def search(self, cr, user, args, offset=0, limit=None, order=None, context=None, count=False):
        '''重写search实现权限控制'''
        if not self._has_full_access:#当前用户不是人资/董事长的话，只能看到相应部门的申请单
            if self._is_vp(cr, user):
                #总经理：如果是 注塑/模具课，只到副总审批即可。其他正常(此部分硬编码,TODO:用配置实现)
                ym_uid = self.pool.get('res.users').search(cr,1,[(u'name','like',u'某某副总')])
                ym_dept_ids=self.pool.get('hr.department').search(cr,1,['|',(u'name','like',u'注塑'),(u'name','like',u'模具')])
                if(user in ym_uid):
                    args.append([u'target_department',u'in',tuple(ym_dept_ids)])
                else:
                    args.append([u'target_department',u'not in',tuple(ym_dept_ids)])
            else:
                login_user = self.pool.get('res.users').browse(cr,1,user)
                my_dept_id= login_user.employee_id.department_id.id if login_user.employee_id and login_user.employee_id.department_id else False
                args.append([u'target_department',u'=',my_dept_id])
             
        result =super(position_application,self).search(cr, user, args, offset, limit, order, context, count)        
        return result

position_application()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
