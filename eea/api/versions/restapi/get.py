from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service

from zope.interface import Interface

from zope.interface import implementer
from zope.component import adapter


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class EEAVersions:
    """ EEA Versions """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False, prefix="expand.eea."):
        result = {
            "eea.versions": {
                "@id": f"{self.context.absolute_url()}/@eea.versions"
            }
        }
        res = {
            "newer_versions": {
                "@id": f"{self.context.absolute_url()}/@newer-versions"
            },
            "older_versions": {
                "@id": f"{self.context.absolute_url()}/@older-versions"
            }
        }
        result["eea.versions"].update(res)
        return result


class EEAVersionsGet(Service):
    """ EEA Versions Get """

    def reply(self):
        """Reply with versions"""
        versions = EEAVersions(self.context, self.request)
        return versions(expand=True, prefix="expand.eea.")[
            "versions"
        ]
