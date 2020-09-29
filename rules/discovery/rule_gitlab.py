from core.redis   import rds
from core.triage  import Triage
from core.parser  import ScanParser, ConfParser

class Rule:
  def __init__(self):
    self.rule = 'DSC_OR39'
    self.rule_severity = 1
    self.rule_description = 'Checks for GitLab Panels'
    self.rule_confirm = 'Identified a GitLab Panel'
    self.rule_details = ''
    self.rule_mitigation = '''Identify whether the application in question is supposed to be exposed to the local network.'''
    self.rule_match_string = {    
    '/users/sign_in':{
      'app':'GITLAB1',
      'match':['Register for GitLab'],
      'title':'Gitlab'
     },
    '/users/sign_up':{
      'app':'GITLAB2',
      'match':['Register for GitLab'],
      'title':'Gitlab'
      },
    '/explore':{
      'app':'GITLAB3',
      'match':['Register for GitLab'],
      'title':'Gitlab'
      },
    }
    self.intensity = 2
    
  def check_rule(self, ip, port, values, conf):
    c = ConfParser(conf)
    t = Triage()
    p = ScanParser(port, values)
    
    domain  = p.get_domain()
    module  = p.get_module()
    
    if 'http' in module:
      for uri, values in self.rule_match_string.items():
        app_name = values['app']
        app_title = values['title']
  
        resp = t.http_request(ip, port, uri=uri)

        if resp is not None:
          for match in values['match']:
            if match in resp.text:
              self.rule_details = 'Exposed {} at {}'.format(app_title, uri)
              js_data = {
                  'ip':ip,
                  'port':port,
                  'domain':domain,
                  'rule_id':self.rule,
                  'rule_sev':self.rule_severity,
                  'rule_desc':self.rule_description,
                  'rule_confirm':self.rule_confirm,
                  'rule_details':self.rule_details,
                  'rule_mitigation':self.rule_mitigation
                }
              rds.store_vuln(js_data)
              break
              
    return
