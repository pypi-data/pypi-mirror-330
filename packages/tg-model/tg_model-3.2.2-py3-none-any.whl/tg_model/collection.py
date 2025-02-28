# -*- coding: utf-8 -*-
# Copyright (C) 2023-2025 TUD | ZIH
# ralf.klammer@tu-dresden.de

import logging

import os
import shutil

from .util import prepare_path, get_files, RenderBase
from .tei import TEIParser
from .yaml import CollectionConfig

log = logging.getLogger(__name__)


class CollectionModeler(RenderBase):

    def __init__(self, subproject, projectpath, templates=None, *args, **kw):
        super().__init__(projectpath, templates=templates)
        self.subproject = subproject

        self.load_configs()
        self.in_path = self.subproject["inpath"]
        self.out_path = prepare_path(self.subproject["outpath"], create=True)

        self.facets = {}

    def load_configs(self):
        self.collection_config = CollectionConfig(
            projectpath=self.subproject["basepath"]
        )
        if self.collection_config.get_missing_params():
            raise Exception(
                "Missing config values for collection.yaml: %s"
                % ", ".join(self.collection_config.get_missing_params())
            )

    def render_collection(self):
        self.render_collection_base()
        self.render_collection_meta()
        self.render_edition()

    def render_collection_base(self):
        files = []
        for file in get_files(self.in_path, as_tuple=True):
            _file = file[1].replace(".xml", "")
            files.append({"path": _file, "name": f"{_file}.edition"})

        self.render(
            "%s/%s.collection"
            % (
                self.out_path,
                self.collection_config.short_title(),
            ),
            {
                "title": self.collection_config.short_title(),
                "files": files,
            },
            "{{ collection }}.collection",
        )

    def render_collection_meta(self):
        self.render(
            "%s/%s.collection.meta"
            % (
                self.out_path,
                self.collection_config.short_title(),
            ),
            {
                "collectors": [
                    c
                    for c in self.collection_config.collector()
                    if c["fullname"]
                ],
                "title": self.collection_config.long_title(),
            },
            "{{ collection }}.collection.meta",
        )

    def add_facet(self, facet_key, facet_value):
        if facet_key not in self.facets:
            self.facets[facet_key] = []
        self.facets[facet_key].append(facet_value)

    def collect_facets(self, attributes):
        for key, value in attributes.items():
            if key in ["basic_classifications", "gnd_subjects"]:
                for item in value:
                    if all(item.values()):
                        self.add_facet(key, item)
            elif key == "eltec":
                if value["gender"]:
                    self.add_facet("gender", value["gender"])
            elif key in ["language", "genre"]:
                if value:
                    self.add_facet(key, value)
            # else:
            #     print(key, value)

    def render_edition(self):
        files = get_files(self.in_path, as_tuple=True)
        for path, filename in files:
            tei_file = TEIParser(path=path, filename=filename)
            tei_file.set_config(self.collection_config)

            # create one directory for each file, which will contain all
            # related files afterwards
            file_path = prepare_path(
                "/".join([self.out_path, tei_file.pure_filename]),
                create=True,
            )

            self.render_edition_base(tei_file, file_path)
            self.render_edition_meta(tei_file, file_path)
            self.render_edition_work(tei_file, file_path)

            self.collect_facets(tei_file.get_attributes())

    def render_edition_base(self, tei_file, file_path):
        # add one *.edition file per source file
        self.render(
            "%s/%s.edition" % (file_path, tei_file.pure_filename),
            tei_file.get_attributes(),
            "{{ id }}.edition",
        )

    def render_edition_meta(self, tei_file, file_path):
        # add one *.edtion.meta file per source file
        self.render(
            "%s/%s.edition.meta" % (file_path, tei_file.pure_filename),
            tei_file.get_attributes(),
            "{{ id }}.edition.meta",
        )

    def render_edition_work(self, tei_file, file_path):
        # add *.work file
        self.render(
            "%s/%s.work" % (file_path, tei_file.pure_filename),
            {},
            "{{ id }}.work",
        )
        # add *.work.meta file
        self.render(
            "%s/%s.work.meta" % (file_path, tei_file.pure_filename),
            tei_file.get_attributes(),
            "{{ id }}.work.meta",
        )

        # add original TEI file as *.xml
        shutil.copyfile(
            tei_file.fullpath,
            f"{os.path.join(file_path, tei_file.pure_filename)}.xml",
        )

        # add *.xml.meta file
        self.render(
            "%s/%s.xml.meta" % (file_path, tei_file.pure_filename),
            tei_file.get_attributes(),
            "{{ id }}.xml.meta",
        )
