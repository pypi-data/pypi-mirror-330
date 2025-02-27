# -*- coding: utf-8 -*-
# Copyright (C) 2023-2024 TUD | ZIH
# ralf.klammer@tu-dresden.de

import logging

from .collection import CollectionModeler
from .util import RenderBase
from .yaml import MainConfig

log = logging.getLogger(__name__)


class Project(RenderBase):

    def __init__(self, projectpath, templates=None, *args, **kw):
        super().__init__(projectpath, templates=templates)
        self.templates = templates
        self.collectors = []
        self._main_config = None
        self._avatar = None
        self._xslt = None

    @property
    def main_config(self):
        if self._main_config is None:
            self._main_config = MainConfig(self.projectpath)
        return self._main_config

    def render_project(self):

        for subproject in self.main_config.content["subprojects"]:
            collection = CollectionModeler(
                subproject, self.projectpath, templates=self.templates
            )
            collection.render_collection()
            self.main_config.other_files.add_facets(collection.facets)

        self.main_config.other_files.render_all()
