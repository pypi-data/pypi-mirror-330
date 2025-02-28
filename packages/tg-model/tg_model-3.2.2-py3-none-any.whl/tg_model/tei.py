# -*- coding: utf-8 -*-
# Copyright (C) 2023-2025 TUD | ZIH
# ralf.klammer@tu-dresden.de

import logging
import os

from copy import deepcopy
from datetime import datetime
from iso639 import Lang
from iso639.exceptions import InvalidLanguageValue
from lxml.etree import Comment, dump, ElementTree, tostring, SubElement

from .util import (
    get_type,
    get_unique_node_id,
    is_valid_date,
    build_xpath,
    get_files,
    strip_strings_in_dict,
)

from .util_eltec import (
    date_to_timeslot,
    gender_to_authorgender,
    wordcount_to_size,
)
from .xml import XMLParserBase
from .yaml import SynergyConfig, CollectionConfig, MainConfig

log = logging.getLogger(__name__)


class TEIParser(XMLParserBase):
    def __init__(
        self,
        tree=None,
        path=None,
        filename=None,
        fullpath=None,
        *args,
        **kw,
    ):
        if tree is not None:
            super().__init__(tree=tree, *args, **kw)
        elif fullpath:
            super().__init__(fullpath, *args, **kw)
            self.fullpath = fullpath
        elif all([path, filename]):
            self.path = path
            self.filename = filename
            self.fullpath = os.path.join(path, filename)
            super().__init__(os.path.join(path, filename), *args, **kw)
        else:
            raise ValueError("TEIParser incorrect initialized")

        self._pure_filename = None
        self._publication = None
        self._pub_place = None
        self._edtion_pub_place = None
        self._pub_date_edition = None
        self._author = None
        self._author_id = None
        self._edition_author_fullname = None
        self._edition_author_firstname = None
        self._edition_author_lastname = None
        self._edition_author_id = None
        self._author_firstname = None
        self._author_lastname = None
        self._author_fullname = None
        self._work_id = None
        self._work_date = None
        self._work_notBefore = None
        self._work_notAfter = None
        self._work_title = None
        self._edition_title = None
        self._language = None
        self._genre = None
        self._wordcount = None
        self._eltec_time_slot = None
        self._eltec_author_gender = None
        self._eltec_size = None
        self._eltec_reprint_count = None
        self._eltec_corpus_collection = None
        self._rights_holder = None
        self._rights_holder_url = None
        self._rights_holder_fullname = None
        self._collector = None
        self._collector_url = None
        self._collector_fullname = None
        self._attributes = None
        self._basic_classifications = None
        self._gnd_subjects = None

    def __repr__(self):
        return "<TEIParser: %s>" % self.uri

    def _get_via_config_value(self, config_val, multiple=False):
        if config_val and config_val.get("value"):
            return (
                config_val.get("value")
                if not multiple
                else [config_val.get("value")]
            )
        elif config_val and config_val["xpath"]:
            if multiple:
                return self.findall(config_val["xpath"]) or []
            else:
                return self.find(config_val["xpath"])
        else:
            return [] if multiple else None

    def get_via_config_value(self, value, section, multiple=False):
        config_val = section.get(value, None)
        return self._get_via_config_value(config_val, multiple=multiple)

    def set_config(self, config):
        self._config = config

    @property
    def config(self):
        if self._config is None:
            self.set_config(CollectionConfig())
        return self._config

    @property
    def pure_filename(self):
        if self.filename and self._pure_filename is None:
            self._pure_filename = self.filename.replace(".xml", "")
        return self._pure_filename

    @property
    def work_date(self):
        if self._work_date is None:
            self._work_date = self.get_via_config_value(
                "date", self.config.work["dateOfCreation"]
            )
            if self._work_date and not is_valid_date(self._work_date):
                self._work_date = False
        return self._work_date

    @property
    def work_notBefore(self):
        if self._work_notBefore is None:
            self._work_notBefore = self.get_via_config_value(
                "notBefore", self.config.work["dateOfCreation"]
            )
            if self._work_notBefore and not is_valid_date(
                self._work_notBefore
            ):
                self._work_notBefore = False
        return self._work_notBefore

    @property
    def work_notAfter(self):
        if self._work_notAfter is None:
            self._work_notAfter = self.get_via_config_value(
                "notAfter", self.config.work["dateOfCreation"]
            )
            if self._work_notAfter and not is_valid_date(self._work_notAfter):
                self._work_notAfter = False
        return self._work_notAfter

    def _get_date_range(self, notBefore, notAfter):
        return {
            "notBefore": notBefore,
            "notAfter": notAfter,
            "text": f"between {notBefore} and {notAfter}",
        }

    @property
    def work_dateRange(self):
        if all([self.work_notBefore, self.work_notAfter]):
            return self._get_date_range(
                self.work_notBefore, self.work_notAfter
            )

    @property
    def work_dateDefault(self):
        self.validate_work_date()
        return self._get_date_range(-4000, datetime.now().strftime("%Y-%m-%d"))

    def validate_work_date(self):
        if not any([self.work_date, self.work_dateRange]):
            log.warning(
                f"Invalid 'dateOfCreation' in {self.work_title} will cause PROBLEMS in final Publication!!!"
            )

    @property
    def pub_place(self):
        if self._pub_place is None:
            self._pub_place = self.get_via_config_value(
                "place", self.config.work
            )
        return self._pub_place

    @property
    def work_title(self):
        if self._work_title is None:
            self._work_title = self.get_via_config_value(
                "title", self.config.work
            )
        return self._work_title

    @property
    def work_id(self):
        if self._work_id is None:
            self._work_id = self.get_via_config_value(
                "id", self.config.work, multiple=True
            )
        return self._work_id

    @property
    def edition_title(self):
        if self._edition_title is None:
            self._edition_title = self.get_via_config_value(
                "title", self.config.attributes["edition"]
            )
        return self._edition_title

    @property
    def pub_date_edition(self):
        if self._pub_date_edition is None:
            self._pub_date_edition = self.get_via_config_value(
                "date", self.config.edition
            )
            if self._pub_date_edition and not is_valid_date(
                self._pub_date_edition
            ):
                self._pub_date_edition = False
        return self._pub_date_edition

    @property
    def edition_pub_place(self):
        if self._edtion_pub_place is None:
            self._edtion_pub_place = self.get_via_config_value(
                "place", self.config.edition
            )
        return self._edtion_pub_place

    @property
    def edition_author_fullname(self):
        if self._edition_author_fullname is None:
            self._edition_author_fullname = self.get_via_config_value(
                "fullname", self.config.edition["author"]
            )
            if not self._edition_author_fullname:
                if (
                    self.edition_author_lastname
                    and self.edition_author_firstname
                ):
                    self._edition_author_fullname = ", ".join(
                        [
                            self.edition_author_lastname,
                            self.edition_author_firstname,
                        ]
                    )
        return self._edition_author_fullname

    @property
    def edition_author_firstname(self):
        if self._edition_author_firstname is None:
            self._edition_author_firstname = self.get_via_config_value(
                "firstname", self.config.edition["author"]
            )
        return self._edition_author_firstname

    @property
    def edition_author_lastname(self):
        if self._edition_author_lastname is None:
            self._edition_author_lastname = self.get_via_config_value(
                "lastname", self.config.edition["author"]
            )
        return self._edition_author_lastname

    @property
    def edition_author_id(self):
        if self._edition_author_id is None:
            self._edition_author_id = self.get_via_config_value(
                "id", self.config.edition["author"]
            )
        return self._edition_author_id

    @property
    def language(self):
        if self._language is None:
            self._language = self.get_via_config_value(
                "language", self.config.edition
            )
            if self._language:
                self._language = self._language.split("-")[0]
                try:
                    self._language = Lang(self._language).pt3
                except InvalidLanguageValue as e:
                    log.warning(e)
                    log.warning("Did not set language for %s" % self)

        return self._language

    @property
    def author_id(self):
        if self._author_id is None:
            self._author_id = self.get_via_config_value(
                "id", self.config.work["author"]
            )
        return self._author_id

    @property
    def author_fullname(self, *args):
        if self._author_fullname is None:
            self._author_fullname = self.get_via_config_value(
                "fullname", self.config.work["author"]
            )
            if not self._author_fullname:
                if self.author_lastname and self.author_firstname:
                    self._author_fullname = (
                        f"{self.author_lastname}, {self.author_firstname}"
                    )
        return self._author_fullname

    @property
    def author_firstname(self):
        if self._author_firstname is None:
            self._author_firstname = self.get_via_config_value(
                "firstname", self.config.work["author"]
            )
        return self._author_firstname

    @property
    def author_lastname(self):
        if self._author_lastname is None:
            self._author_lastname = self.get_via_config_value(
                "lastname", self.config.work["author"]
            )
        return self._author_lastname

    @property
    def genre(self):
        # NOTE: This opens up a wider field, than it seems
        # Especially, as there is no clear definition/vocabulary on how 'genre'
        # needs to be described
        if self._genre is None:
            self._genre = self.get_via_config_value("genre", self.config.work)
        return self._genre

    @property
    def wordcount(self):
        if self._wordcount is None:
            self._wordcount = self.get_via_config_value(
                "wordcount", self.config.edition
            )
        return self._wordcount

    # **********
    # ELTeC specs
    @property
    def eltec_time_slot(self):
        if self._eltec_time_slot is None:
            self._eltec_time_slot = date_to_timeslot(self.work_date)
        return self._eltec_time_slot

    @property
    def eltec_author_gender(self):
        if self._eltec_author_gender is None:
            # idea is to try to get parameter directly from xpath value
            self._eltec_author_gender = self.get_via_config_value(
                "author_gender", self.config.eltec_specs
            )
            # and only 'generate' it, if it has not been found
            if self._eltec_author_gender:
                self._eltec_author_gender = gender_to_authorgender(
                    self._eltec_author_gender
                )
        return self._eltec_author_gender

    @property
    def eltec_size(self):
        if self._eltec_size is None:
            # idea is to try to get parameter directly from xpath value
            self._eltec_size = self.get_via_config_value(
                "size", self.config.eltec_specs
            )
            # and only 'generate' it, if it has not been found
            if not self._eltec_size:
                self._eltec_size = wordcount_to_size(self.wordcount)
        return self._eltec_size

    @property
    def eltec_reprint_count(self):
        if self._eltec_reprint_count is None:
            # idea is to try to get parameter directly from xpath value
            self._eltec_reprint_count = self.get_via_config_value(
                "reprint_count", self.config.eltec_specs
            )
            # ToDo:
            #   find an alternative xpaths and build formatter
        return self._eltec_reprint_count

    @property
    def eltec_corpus_collection(self):
        if self._eltec_corpus_collection is None:
            self._eltec_corpus_collection = self.get_via_config_value(
                "corpus_collection", self.config.eltec_specs
            )
        return self._eltec_corpus_collection

    # **********

    # MULTI fields
    # all fields, that can have multiple entries
    @property
    def rights_holder(self):
        if self._rights_holder is None:
            self._rights_holder = self.config.rights_holder
        return self._rights_holder

    @property
    def collector(self):
        if self._collector is None:
            self._collector = self.config.collector
        return self._collector

    def _get_classifications(self, config_method):
        classifications = []
        for classification in config_method():

            # get all values for each classification
            feature_sets = []
            for key in classification.keys():
                results = self._get_via_config_value(
                    classification[key], multiple=True
                )
                feature_sets.append(
                    {
                        "key": key,
                        "results": results if results else [],
                        "fixed_value": classification[key]["value"],
                    }
                )

            # get the minimum length of all results to initialize the
            # result list
            # we only initialize as many empty dicts as the minimum amount of
            # results
            max_length = max(len(d["results"]) for d in feature_sets)
            # if there are no results, initialize the list with one empty dict
            result = [
                {"id": None, "value": None, "url": None}
                for _ in range(max_length or 1)
            ]

            # fill the result list with the concrete values
            for d in feature_sets:
                key = d["key"]
                if d["fixed_value"]:
                    # set the fixed value for all results
                    for r in result:
                        r[key] = d["fixed_value"]
                else:
                    for i, value in enumerate(d["results"]):
                        result[i][key] = value

                        # if the value of 'id' is an URL, extract the ID
                        if key == "id" and value.startswith("http"):
                            result[i][key] = value.split("/")[-1]

            classifications += result

        return classifications

    @property
    def basic_classifications(self):
        if self._basic_classifications is None:
            self._basic_classifications = self._get_classifications(
                self.config.basic_classifications
            )
        return self._basic_classifications

    @property
    def gnd_subjects(self):
        if self._gnd_subjects is None:
            self._gnd_subjects = self._get_classifications(
                self.config.gnd_subjects
            )
        return self._gnd_subjects

    # **********

    def get_attributes(self):
        if self._attributes is None:
            self._attributes = {
                "id": self.pure_filename,
                "rights_holder": self.rights_holder(),
                "collector": self.collector(),
                "work": {
                    "id": self.work_id,
                    "title": self.work_title,
                    "author": {
                        "id": self.author_id,
                        "fullname": self.author_fullname,
                    },
                    "genre": self.genre,
                    "dateOfCreation": {
                        "date": self.work_date,
                        "range": self.work_dateRange,
                        "default": self.work_dateDefault,
                    },
                    "pub_place": self.pub_place,
                },
                "edition": {
                    "title": self.edition_title,
                    "pub_date": self.pub_date_edition,
                    "pub_place": self.edition_pub_place,
                    "author": {
                        "fullname": self.edition_author_fullname,
                        "id": self.edition_author_id,
                    },
                    "language": self.language,
                },
                "eltec": {
                    "time_slot": self.eltec_time_slot,
                    "gender": self.eltec_author_gender,
                    "size": self.eltec_size,
                    "reprint_count": self.eltec_reprint_count,
                    "corpus_collection": self.eltec_corpus_collection,
                },
                "basic_classifications": self.basic_classifications,
                "gnd_subjects": self.gnd_subjects,
            }
            self._attributes = strip_strings_in_dict(self._attributes)
        return self._attributes


class SynergyParser(TEIParser):
    def __init__(self, projectpath, *args, **kw):
        super().__init__(*args, **kw)
        self._principal = None
        self._rights_holder_url = None
        self._rights_holder_fullname = None
        self._rights_holder_firstname = None
        self._rights_holder_lastname = None
        self._collector_url = None
        self._collector_fullname = None
        self._collector_firstname = None
        self._collector_lastname = None
        self._short_title = None
        self._long_title = None
        self._config = None
        self.projectpath = projectpath

    @property
    def config(self):
        if self._config is None:
            self.set_config(SynergyConfig(self.projectpath))
        return self._config

    def get_via_config_value(self, value, section=None):
        config_val = self.config.get(value, section)
        result = ""
        if config_val and config_val["xpath"]:
            node = self.find(config_val["xpath"])
            if node is not None:
                result = node.text
        return result or None

    @property
    def short_title(self):
        if self._short_title is None:
            self._short_title = self.get_via_config_value("short", "title")
        return self._short_title

    @property
    def long_title(self):
        if self._long_title is None:
            self._long_title = self.get_via_config_value("long", "title")
        return self._long_title

    @property
    def rights_holder_url(self):
        if self._rights_holder_url is None:
            self._rights_holder_url = self.get_via_config_value(
                "url", "rights_holder"
            )
        return self._rights_holder_url

    @property
    def rights_holder_fullname(self):
        if self._rights_holder_fullname is None:
            self._rights_holder_fullname = self.get_via_config_value(
                "fullname", "rights_holder"
            )
            if not self._rights_holder_fullname:
                names = [
                    self.rights_holder_firstname,
                    self.rights_holder_lastname,
                ]
                if all(names):
                    self._rights_holder_fullname = " ".join(names)

        return self._rights_holder_fullname

    @property
    def rights_holder_firstname(self):
        if self._rights_holder_firstname is None:
            self._rights_holder_firstname = self.get_via_config_value(
                "firstname", "rights_holder"
            )
        return self._rights_holder_firstname

    @property
    def rights_holder_lastname(self):
        if self._rights_holder_lastname is None:
            self._rights_holder_lastname = self.get_via_config_value(
                "lastname", "rights_holder"
            )
        return self._rights_holder_lastname

    @property
    def collector_url(self):
        if self._collector_url is None:
            self._collector_url = self.get_via_config_value("url", "collector")
        return self._collector_url

    @property
    def collector_fullname(self):
        if self._collector_fullname is None:
            self._collector_fullname = self.get_via_config_value(
                "fullname", "collector"
            )
            if not self._collector_fullname:
                names = [
                    self.collector_firstname,
                    self.collector_lastname,
                ]
                if all(names):
                    self._collector_fullname = " ".join(names)

        return self._collector_fullname

    @property
    def collector_firstname(self):
        if self._collector_firstname is None:
            self._collector_firstname = self.get_via_config_value(
                "firstname", "collector"
            )
        return self._collector_firstname

    @property
    def collector_lastname(self):
        if self._collector_lastname is None:
            self._collector_lastname = self.get_via_config_value(
                "lastname", "collector"
            )
        return self._rights_holder_lastname


class SynergyAnalyzer(object):
    """
    This class helps to find completely synergetic nodes in a set of given
    TEI files.
    INPUT: list of file paths, e.g.: [./1.xml, 2.xml, /tmp/3.xml]
    OUTPUT: xml tree containing all synergetic nodes, e.g.:
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <principal>
                            <forename>John</forename>
                            <surname>Doe</surname>
                        </principal>
                    </titleStmt>
                </fileDesc>
            </teiHeader>
        </TEI>

    How it works (basically)!
    1. find synergies
        1.1 get all nodes (as xpath) from one (base) file
        1.2 check if each node exists in the other files
            (with same items & content)
            yes: keep node in list
            no: remove node from list
            --> list gets smaller after each checked file!
    2. recombinde synergetic nodes to xml tree structure
        2.1 find all parent nodes for each synergetic node
        2.2 find out which "parent" nodes have common childs
                --> "parent-child-relations"
        2.3 (re-)build tree structure from "parent-child-relations"
    """

    def __init__(
        self,
        subproject,
        projectpath,
        *args,
        **kw,
    ):
        self.subproject = subproject
        self.main_config = MainConfig(projectpath)

        self.sp_projectpath = self.subproject["basepath"]

        files = get_files(self.subproject["inpath"])
        self.files = sorted(files)
        if self.main_config.validate():
            raise LookupError(self.main_config.validate())
        self.base = TEIParser(fullpath=files[0])
        log.debug("This is the base: %s" % self.base)
        self.sourcefiles = [TEIParser(fullpath=target) for target in files]
        self.targets = self.sourcefiles[1:]
        self._synergetic_nodes = None
        self._node_relations = None
        self._tree = None
        self._parser = None

    def _get_nodes(self, elem, exclude=[], xpath="./"):
        # this function iters through all nodes/childs of the 'teiHeader'
        # and collects them in a list
        log.debug("_get_nodes: elem=%s" % elem)
        for child in elem.iterchildren():
            if child.tag is Comment or get_type(child) in exclude:
                continue
            if len(child.getchildren()):
                _xpath = build_xpath(child, xpath, include_items=True)
                self._get_nodes(
                    child,
                    exclude=exclude,
                    xpath=_xpath,
                )
            else:
                # v1.0 test it against base-file to check if the xpath is
                # well defined
                _xpath = build_xpath(child, xpath, include_items=True)
                found = self.base.findall(_xpath, text=child.text)
                if len(found) == 1:
                    self._synergetic_nodes.append(
                        {
                            "xpath": _xpath,
                            "content": child.text,
                        }
                    )
                else:
                    # TODO:
                    # Check cases and find a way to avoid it
                    # Known issues:
                    #   1: redundant elements without dedicated key-definitions
                    #       e.g.:
                    #           <respStmt>
                    #             <resp>Principal investigator</resp>
                    #             <name>Name1</name>
                    #           </respStmt>
                    #           <respStmt>
                    #             <resp>Encoding</resp>
                    #             <name>Name2</name>
                    #           </respStmt>
                    #   2: element specific namespace, e.g.:
                    #       <textDesc>
                    #            <authorGender xmlns="http://123" key="M"/>
                    #       </textDesc>
                    log.warning(
                        "%s is related to %s result(s)!" % (_xpath, len(found))
                    )

        return

    @property
    def synergetic_nodes(self):
        if self._synergetic_nodes is None:
            self._synergetic_nodes = []
            # 1.1 get all nodes from (base) file
            print(self.base)
            self._get_nodes(
                self.base.find(
                    "tei:teiHeader", get_node=True
                ),  # only analyze 'teiHeader'
                exclude=["abstract", "listBibl"],  # exclude some nodes
            )
            # 1.2 try to find each node in the other files
            for target in self.targets:
                log.debug("Current target: %s" % target)
                for node in self._synergetic_nodes:
                    check = bool(
                        target.findall(node["xpath"], text=node["content"])
                    )
                    # remove node from list, if not found
                    if check is False:
                        self._synergetic_nodes.remove(node)
            log.debug("*" * 50)
            log.debug(
                "Found %i identical nodes." % len(self._synergetic_nodes)
            )
            log.debug("-" * 50)
            for node in self._synergetic_nodes:
                log.debug("%s: %s" % (node["xpath"], node["content"]))
            log.debug("*" * 50)
            self._synergetic_nodes

        return self._synergetic_nodes

    def _recursive_iter_parents(self, node):
        # this function iterates recursively through all parents of a node
        # (within the original tree structure of base file)
        # results in a list of parents of the initial node
        log.debug("'_recursive_iter_parents' -> node: %s" % node)
        # need to 'cache' the original node, as all childs will be removed
        # and therefore also this node will be removed from the tree
        root_parent = node.getparent()
        parent = None
        if root_parent is None:
            # if root_parent is None, we reached the end of the recursion
            log.debug("'_recursive_iter_parents' -> ###end of recursion###")
            return []
        parent = deepcopy(root_parent)
        log.debug("'_recursive_iter_parents' -> parent: %s" % parent)

        parents = []

        log.debug("'_recursive_iter_parents' -> ###next recursion###")
        parents.append(parent)
        # remove all childs of parent, to have the 'pure' parent node
        for c in parent.iterchildren():
            log.debug("'_recursive_iter_parents/remove_childs' -> %s" % c)
            parent.remove(c)
        # recursion, to get the parent of this parent
        sub_parents = self._recursive_iter_parents(root_parent)
        if sub_parents:
            parents += sub_parents
        return parents

    def _add_node_relations(self, nodes):
        # This function takes a list of nodes and maps them to a kind of
        # parent-child-structure
        # Assumption: one node is the "parent" of the following node
        for i in range(len(nodes)):
            node = nodes[i]
            this_node_key = get_unique_node_id(node)
            if this_node_key not in self._node_relations:
                self._node_relations[this_node_key] = {
                    "childs": {},
                    "node": node,
                }
            if i + 1 < len(nodes):
                child_node_key = get_unique_node_id(nodes[i + 1])
                if (
                    child_node_key
                    not in self._node_relations[this_node_key]["childs"]
                ):
                    self._node_relations[this_node_key]["childs"][
                        child_node_key
                    ] = nodes[i + 1]

    def _set_node_relations(self, node):
        # This functions buils up a global dictionary containing:
        #   all nodes and
        #   the corresponding childs
        # This step is necessary, as some nodes belong to the same upper node
        # (parent)
        parents = self._recursive_iter_parents(node)
        parents.insert(0, node)
        self._add_node_relations(parents[::-1])

    def _recombine_related_nodes(self):
        for rel in self.node_relations:
            node = self.node_relations[rel]["node"]
            childs = self.node_relations[rel]["childs"]
            for child_key in childs:
                child = childs[child_key]
                node.append(child)

    @property
    def node_relations(self):
        # "parent-child-relations"
        # find out which synergetic nodes belong to the same "parent" node
        # to enable build up
        if self._node_relations is None:
            self._node_relations = {}
            # check for synergetic nodes initially, if not already happened
            if self.synergetic_nodes is None:
                self.set_synergetic_nodes()
            # loop through all synergetic nodes to rebuild tree structure
            for node in self.synergetic_nodes:
                self._set_node_relations(
                    self.base.find(node["xpath"], get_node=True)
                )
        return self._node_relations

    @property
    def tree(self):
        if self._tree is None:
            # we need to recombine the all nodes with their related "child"
            # nodes in order to get the full tree structure
            self._recombine_related_nodes()
            # afterwards we return the "base"-node to representing
            # the full structure
            base_tag = [*self.node_relations][0]
            self._tree = self.node_relations[base_tag]["node"]
        return self._tree

    def dump_tree(self):
        return tostring(
            self.tree, pretty_print=True, encoding="utf-8", with_tail=False
        )

    def print_tree(self):
        dump(self.tree)

    def write_tree(self, filename):
        self.add_files()
        ElementTree(self.tree).write(
            filename, pretty_print=True, xml_declaration=True, encoding="utf-8"
        )
        return filename

    def add_files(self):
        srcDesc = self.tree.find(".//sourceDesc")
        if srcDesc is None:
            srcDesc = SubElement(self.tree, "sourceDesc")
        for file in self.files:
            file_elem = SubElement(srcDesc, "file")
            file_elem.text = file
            file_elem.tail = "\n"

    @property
    def parser(self):
        if self._parser is None:
            self._parser = SynergyParser(self.sp_projectpath, tree=self.tree)
        return self._parser

    # def parse(self):
    #     return self.parser.as_dict

    def hits_in_sources(self, xpath):
        all_sources = [self.base] + self.targets
        count = 0
        for tree in all_sources:
            if tree.find(xpath) is not None:
                count += 1
        return round((count * 100) / len(all_sources), 2)
