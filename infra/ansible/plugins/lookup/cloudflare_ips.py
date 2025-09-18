#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Corvin Vale
# MIT License (see LICENSE-CODE or https://opensource.org/license/mit/)

"""Ansible lookup plugin for retrieving Cloudflare IP addresses."""

import time
from typing import Any, ClassVar
from urllib.error import HTTPError, URLError

from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native, to_text
from ansible.module_utils.urls import (
    ConnectionError as URLConnectionError,
    SSLValidationError,
    open_url,
)
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

DOCUMENTATION = r"""
name: cloudflare_ips
author: EVEData Infrastructure Team
version_added: "1.0.0"
short_description: Retrieve Cloudflare IP addresses
description:
  - Retrieves Cloudflare's IP addresses from their public endpoints.
  - Returns a list of IP address ranges used by Cloudflare's network.
  - For configuring firewalls, security groups, or allowlists.
options:
  ip_version:
    description:
      - Filter results to specific IP version.
      - Use 'ipv4' for IPv4 addresses only.
      - Use 'ipv6' for IPv6 addresses only.
      - Use 'all' or omit to get both IPv4 and IPv6.
    type: str
    required: false
    default: all
    choices: ['ipv4', 'ipv6', 'all']
requirements:
  - python >= 3.13
notes:
  - Fetches from https://www.cloudflare.com/ips-v4/ and https://www.cloudflare.com/ips-v6/
  - Returns cached results for 24 hours by default to minimize requests.
"""

EXAMPLES = r"""
# Retrieve all Cloudflare IP addresses (IPv4 and IPv6)
- name: Get all Cloudflare IPs
  ansible.builtin.debug:
    var: lookup('cloudflare_ips', wantlist=True)

# Retrieve only IPv4 addresses
- name: Get Cloudflare IPv4 addresses
  ansible.builtin.debug:
    var: lookup('cloudflare_ips', ip_version='ipv4', wantlist=True)

# Retrieve only IPv6 addresses
- name: Get Cloudflare IPv6 addresses
  ansible.builtin.debug:
    var: lookup('cloudflare_ips', ip_version='ipv6', wantlist=True)

# Use in firewall configuration
- name: Configure UFW to allow Cloudflare IPs
  ansible.builtin.ufw:
    rule: allow
    src: "{{ item }}"
    port: 443
    proto: tcp
  loop: "{{ lookup('cloudflare_ips', ip_version='ipv4', wantlist=True) }}"

# Store in variables for multiple uses
- name: Cache Cloudflare IPs
  ansible.builtin.set_fact:
    cloudflare_ipv4: "{{ lookup('cloudflare_ips', ip_version='ipv4', wantlist=True) }}"
    cloudflare_ipv6: "{{ lookup('cloudflare_ips', ip_version='ipv6', wantlist=True) }}"
"""

RETURN = r"""
_list:
  description:
    - List of IP address ranges in CIDR notation.
    - Contains IPv4 and/or IPv6 addresses based on ip_version parameter.
  type: list
  elements: str
  sample:
    - "173.245.48.0/20"
    - "103.21.244.0/22"
    - "2400:cb00::/32"
    - "2606:4700::/32"
"""

CACHE_TTL = 86400
HTTP_OK = 200
HTTP_TIMEOUT = 30

display = Display()


class LookupModule(LookupBase):
    """Lookup plugin for retrieving Cloudflare IP addresses."""

    _cache: ClassVar[dict[str, dict[str, Any]]] = {}

    def run(self, terms, variables=None, **kwargs) -> list[str]:  # type: ignore[override] # base class lacks type hints  # noqa: ARG002
        """Main entry point for the lookup plugin.

        Args:
            terms: Not used for this lookup, but required by interface
            variables: Ansible variables context
            **kwargs: Additional keyword arguments

        Returns:
            List of IP addresses in CIDR notation

        Raises:
            AnsibleError: If fetch fails
        """
        self.set_options(var_options=variables, direct=kwargs)

        ip_version = self.get_option("ip_version") or "all"

        valid_versions = ["ipv4", "ipv6", "all"]
        if ip_version not in valid_versions:
            msg = (
                f"Invalid ip_version '{ip_version}'. "
                f"Must be one of: {', '.join(valid_versions)}"
            )
            raise AnsibleError(msg)

        cache_key = ip_version

        if cache_key in self._cache:
            cached_data = self._cache[cache_key]
            if time.time() - cached_data["timestamp"] < CACHE_TTL:
                display.vvvv("using cached cloudflare ip data")
                return cached_data["data"]

        try:
            ip_list = self._fetch_cloudflare_ips(ip_version)
        except Exception as e:
            msg = f"Failed to retrieve Cloudflare IPs: {e!s}"
            raise AnsibleError(msg) from e
        else:
            self._cache[cache_key] = {"timestamp": time.time(), "data": ip_list}
            return ip_list

    def _fetch_cloudflare_ips(self, ip_version: str) -> list[str]:
        ip_list = []

        if ip_version in ["ipv4", "all"]:
            ipv4_cidrs = self._fetch_ips_from_url(
                "https://www.cloudflare.com/ips-v4/", "IPv4"
            )
            ip_list.extend(ipv4_cidrs)

        if ip_version in ["ipv6", "all"]:
            ipv6_cidrs = self._fetch_ips_from_url(
                "https://www.cloudflare.com/ips-v6/", "IPv6"
            )
            ip_list.extend(ipv6_cidrs)

        if not ip_list:
            display.warning(f"no ip addresses found for ip_version='{ip_version}'")

        return ip_list

    def _fetch_ips_from_url(self, url: str, ip_type: str) -> list[str]:
        display.vvvv(f"fetching cloudflare {ip_type} addresses")

        try:
            response = open_url(
                url,
                timeout=HTTP_TIMEOUT,
                validate_certs=True,
                http_agent="ansible-httpget",
            )
            data = to_text(response.read()).strip()
        except HTTPError as err:
            msg = f"HTTP error fetching {ip_type} addresses: {to_native(err)}"
            raise AnsibleError(msg) from err
        except URLError as err:
            msg = f"URL error fetching {ip_type} addresses: {to_native(err)}"
            raise AnsibleError(msg) from err
        except SSLValidationError as err:
            msg = f"SSL validation error fetching {ip_type} addresses: {to_native(err)}"
            raise AnsibleError(msg) from err
        except URLConnectionError as err:
            msg = f"Connection error fetching {ip_type} addresses: {to_native(err)}"
            raise AnsibleError(msg) from err
        except Exception as err:
            msg = f"Unexpected error fetching {ip_type} addresses: {to_native(err)}"
            raise AnsibleError(msg) from err

        if data:
            cidrs = [ip.strip() for ip in data.split("\n") if ip.strip()]
            display.vvvv(f"found {len(cidrs)} {ip_type} cidr blocks")
            return cidrs
        return []
