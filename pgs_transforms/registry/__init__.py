"""
governance/ — Namespace Package (transforms contribution)

This repository contributes to the governance namespace package.

Contributes: governance/registry/capability_transforms/

Uses pkgutil.extend_path to merge with other governance contributors.
"""

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
