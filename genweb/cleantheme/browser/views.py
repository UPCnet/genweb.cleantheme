# -*- coding: utf-8 -*-
from five import grok
from plone import api
from scss import Scss
from zope.interface import Interface
from genweb.core.utils import genweb_config
from genweb.cleantheme.browser.interfaces import IGenwebCleantheme
from plone.memoize import ram
import pkg_resources
import scss


def _render_cachekey(method, self, especific1, especific2):
    """Cache by the two specific colors"""
    return (especific1, especific2)


class dynamicCSS(grok.View):
    grok.name('dynamic.css')
    grok.context(Interface)
    grok.layer(IGenwebCleantheme)

    def update(self):
        self.especific1 = genweb_config().especific1
        self.especific2 = genweb_config().especific2

    def render(self):
        self.request.response.setHeader('Content-Type', 'text/css')
        self.request.response.addHeader('Cache-Control', 'must-revalidate, max-age=0, no-cache, no-store')
        if self.especific1 and self.especific2:
            return '@import "{}/genwebcustom.css";\n'.format(api.portal.get().absolute_url()) + \
                   self.compile_scss(especific1=self.especific1, especific2=self.especific2)
        else:
            default = '@import "{}/genwebcustom.css";'.format(api.portal.get().absolute_url())
            return default

    @ram.cache(_render_cachekey)
    def compile_scss(self, **kwargs):
        genwebcleathemeegg = pkg_resources.get_distribution('genweb.cleantheme')

        scssfile = open('{}/genweb/cleantheme/browser/scss/_dynamic.scss'.format(genwebcleathemeegg.location))

        settings = dict(especific1=self.especific1,
                        especific2=self.especific2)

        variables_scss = """

        $genwebPrimary: {especific1};
        $genwebTitles: {especific2};

        """.format(**settings)

        css = Scss(scss_opts={
                   'compress': False,
                   'debug_info': False,
                   })

        dynamic_scss = ''.join([variables_scss, scssfile.read()])

        return css.compile(dynamic_scss)
