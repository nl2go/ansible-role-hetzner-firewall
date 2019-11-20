[![Travis (.org) branch](https://img.shields.io/travis/nl2go/ansible-role-hetzner-firewall/master)](https://travis-ci.org/nl2go/ansible-role-hetzner-firewall)
[![Ansible Galaxy](https://img.shields.io/badge/role-nl2go.hetzner_firewall-blue.svg)](https://https://galaxy.ansible.com/nl2go/hetzner_firewall/)

# Ansible Role: Hetzner Firewall

An Ansible Role that manages [Hetzner Robot Firewall](https://wiki.hetzner.de/index.php/Robot_Firewall/en).

## Requirements

- Existing [Hetzner Online GmbH Account](https://accounts.hetzner.com).
- Configured [Hetzner Robot Webservice Account](https://robot.your-server.de/preferences).

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

    hetzner_firewall_webservice_base_url: https://robot-ws.your-server.de
 
Base url that is pointing to the [Hetzner Robot API](https://robot.your-server.de/doc/webservice/de.html). The variable is mostly utilized for testing purposes, there
is no need to change the default.

    hetzner_firewall_webservice_username: robot
    
Webservice login name. May be set/changed as described in the section [Change Access Data (Hetzner Wiki)](https://wiki.hetzner.de/index.php/KonsoleH:Zugangsdaten_aendern/en).

    hetzner_firewall_webservice_password: secret
    
Webservice password. May be set/changed as described in the section [Change Access Data (Hetzner Wiki)](https://wiki.hetzner.de/index.php/KonsoleH:Zugangsdaten_aendern/en).

    hetzner_firewall_templates:
      - name: New Template
        whitelist_hos: true
        is_default: false
        rules:
          input:
            - action: accept
              ip_version: ipv4
              name: Allow all
    
Multiple firewall templates may be managed using `hetzner_firewall_templates` variable. A firewall template is 
identified by the `name` attribute. The name must be unique to omit collision/unexpected behavior. 
The `state` attribute for a template defaults to `present`.

    hetzner_firewall_templates:
      - name: New Template
        state: absent

To ensure the template is removed add `state: absent`. The `name` attribute remains mandatory to identify origin state.

    hetzner_firewall_host:
      - name: New Template

Host firewall may be managed by referencing an existing firewall template from the `hetzner_firewall_templates` list.
The variable `hetzner_firewall_host` may be defined for a particular host group or a dedicated host. Undefined `hetzner_firewall_host`
leaves the related host or host group firewall being ignored by the role.

    hetzner_firewall_host:
        absent: true

To remove the firewall configuration for a particular host add `state: absent` to the host firewall configuration.
Additional configuration parameters do not take effect when `state: absent` is provided.

    hetzner_firewall_host:
        status: disabled

To disable the firewall for configuration for a particular host add `status: disabled` to the host firewall configuration.
Additional configuration parameters do not take effect when `state: disabled` is provided.                

## Dependencies

None.

## Example Playbook

Since the role is managing the communication with the [Hetzner Robot API](https://robot.your-server.de/doc/webservice/de.html)
only, it may be run on localhost.

    - hosts: localhost
      roles:
         - nl2go.hetzner-firewall

## Development
Use [docker-molecule](https://github.com/nl2go/docker-molecule) following the instructions to run [Molecule](https://molecule.readthedocs.io/en/stable/)
or install [Molecule](https://molecule.readthedocs.io/en/stable/) locally (not recommended, version conflicts might appear).


Use following to run tests:

    molecule test --all
       
This role relies on [hetzner-robot-api-mock](https://github.com/nl2go/hetzner-robot-api-mock) to simulate interactions with
the [Hetzner Robot API](https://robot.your-server.de/doc/webservice/de.html).

## License

See the [LICENSE.md](LICENSE.md) file for details.

## Author Information

This role was created by in 2019 by [Newsletter2Go GmbH](https://www.newsletter2go.com/).
