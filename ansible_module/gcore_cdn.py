#!/usr/bin/python
# -*- coding: utf-8 -*-

### Documentation
"""My custom module
"""
DOCUMENTATION = '''
module: gcore_cdn
short_description: This is module for managing GCore_CDN
description:
    - This is module to create / delete / manage CDN Resources in GCore CDN
version_added: "0.1"
author: "khramov.vladimir@gmail.com"
options:
# One or more of the following
    api_url:
        description:
            - URL of GCore api url
        required: false
        default: 'https://api.gcdn.co/auth/jwt/login'
        version_added: "0.1"
    action:
        description:
            - What should be done with resource
        choices:
          - list_resources
          - clean_cache
        required: true
        version_added: "0.1"
    cname:
        description:
            - CNAME or ID of CDN-resource
        required: true
        version_added: "0.1"
notes:
    - Other things consumers of your module should know.
requirements:
    - requests
    - validators
'''
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}
EXAMPLES = '''
# list CDN resoureces
- name: List CDN resoureces
  gcore_cdn:
    cname: 'CDN_CNNAME'
    login: myemail@mail.ru
    password: mypassword
    action: list_resources
'''
RETURN = '''
'''
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

def main():
    # 
    # required_together = [[ if there will be options that'll be needed together]]
    arguments = dict(
            cname = dict(required=True),
            login = dict(required=True),
            password = dict(required=True, no_log=True),
            action = dict(required=True),
            api_url = dict(required=True)
    )
    module = AnsibleModule (
        argument_spec=arguments,
        # required_together=required_together, # uncomment if need to add required parameters
        support_check_mode=True
    )
    login_params = {
       
    }
    url_params = {
        
    }
    if module.check_mode:
        module.exit_json(changed=True)
    
    response, info = fetch_url(module, url, module.jsonify(url_params), headers=headers)

    if info['status'] == 200:
        module.exit_json(change=True)
    else:
        module.fail_json(msg='unable to call API')


if __name__ == '__main__':
    main()
