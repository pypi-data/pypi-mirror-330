##
#
# File:    CreateRWTree.py
# Author:  E. Peisach
# Date:    22-Oct-2018
# Version: 0.001
##
"""
Copies selected mock-data to a r/w tree for test cases.

"""

__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import logging
import shutil
import os

from typing import List, Any, Optional, Union

logger = logging.getLogger(__name__)


class CreateRWTree(object):
    def __init__(self, source: Optional[str] = None, destination: Optional[str] = None) -> None:
        self.__srcDir = source
        self.__dstDir = destination
        self.__reqOpts = {
            "site-config": "_copysiteconfig",
            "actiondata": "_copyactiondata",
            "archive": "_copyarchive",
            "depuiresources": "_copydepuiresources",
            "emdresources": "_copyemdresources",
            "wsresources": "_copywsresources",
            "webapps": "_copywebapps",
        }

    def createtree(self, objlist: Optional[List[Any]] = None) -> None:
        if objlist is None:
            logger.error("createtree with no objlist - Fatal")
            return
        for obj in objlist:
            if type(obj) is str:
                req = obj
                opt_arg = None
            else:
                req = obj[0]
                if len(obj) > 1:
                    opt_arg = obj[1]
                else:
                    opt_arg = None

            if req in self.__reqOpts:
                mth = getattr(self, self.__reqOpts[req], None)
                if mth is None:
                    logger.error("Could not locate %s - fatal", self.__reqOpts[req])
                    return
                if opt_arg:
                    mth(opt_arg)
                else:
                    mth()
            else:
                logger.error("%s not known", req)

    def _copysiteconfig(self) -> None:
        """Copies the site config tree down so that MockTopDir will be the top of the r/w tree"""
        logger.info("Creating %s", self.__dstDir)
        if self.__srcDir is None or self.__dstDir is None:
            logger.error("srcDir of dstDir not set --- FATAL")
            return
        src = os.path.join(self.__srcDir, "site-config")
        dst = os.path.join(self.__dstDir, "site-config")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    def _copyactiondata(self) -> None:
        """Copies the actondata definitions"""
        if self.__srcDir is None or self.__dstDir is None:
            logger.error("srcDir of dstDir not set --- FATAL")
            return
        src = os.path.join(self.__srcDir, "da_top", "resources_ro", "actionData.xml")
        dst = os.path.join(self.__dstDir, "da_top", "resources_ro", "actionData.xml")
        logger.info("Copying %s to %s", src, dst)
        dst_base = os.path.dirname(dst)
        if os.path.exists(dst):
            os.unlink(dst)
        if not os.path.exists(dst_base):
            os.makedirs(dst_base)
        shutil.copyfile(src, dst)

    def _copydepuiresources(self) -> None:
        """Copies the depui resources tree so that MockTopDir will be the top of the r/w tree"""
        logger.info("Creating %s", self.__dstDir)
        if self.__srcDir is None or self.__dstDir is None:
            logger.error("srcDir of dstDir not set --- FATAL")
            return
        src = os.path.join(self.__srcDir, "da_top", "resources_ro", "depui")
        dst = os.path.join(self.__dstDir, "da_top", "resources_ro", "depui")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    def _copyemdresources(self) -> None:
        """Copies the emd  resources tree so that MockTopDir will be the top of the r/w tree"""
        logger.info("Creating %s", self.__dstDir)
        if self.__srcDir is None or self.__dstDir is None:
            logger.error("srcDir of dstDir not set --- FATAL")
            return
        src = os.path.join(self.__srcDir, "da_top", "resources_ro", "emd")
        dst = os.path.join(self.__dstDir, "da_top", "resources_ro", "emd")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    def _copywsresources(self) -> None:
        """Copies the content_ws resources tree so that MockTopDir will be the top of the r/w tree"""
        logger.info("Creating %s", self.__dstDir)
        if self.__srcDir is None or self.__dstDir is None:
            logger.error("srcDir of dstDir not set --- FATAL")
            return
        src = os.path.join(self.__srcDir, "da_top", "resources_ro", "content_ws")
        dst = os.path.join(self.__dstDir, "da_top", "resources_ro", "content_ws")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    def _copywebapps(self, modules: Optional[Union[str, List[Any]]] = None) -> None:
        """Copies selected webapps resources tree so that MockTopDir will be the top of the r/w tree"""
        if type(modules) is str:
            modules = [modules]

        # Copy version number
        if self.__srcDir is None or self.__dstDir is None:
            logger.error("srcDir of dstDir not set --- FATAL")
            return
        websrcdir = os.path.join(self.__srcDir, "da_top", "webapps")
        webdstdir = os.path.join(self.__dstDir, "da_top", "webapps")
        src = os.path.join(websrcdir, "version.json")
        dst = os.path.join(webdstdir, "version.json")
        if not os.path.exists(webdstdir):
            os.makedirs(webdstdir)
        if os.path.exists(src):
            logger.info("Copying %s to %s", src, dst)
            shutil.copy(src, dst)
        else:
            logger.info("Source %s missing", src)

        if modules:
            basesrcdir = os.path.join(websrcdir, "htdocs")
            basedstdir = os.path.join(webdstdir, "htdocs")
            for mod in modules:
                logger.info("Creating %s", self.__dstDir)
                src = os.path.join(basesrcdir, mod)
                dst = os.path.join(basedstdir, mod)
                logger.info("Copying %s to %s", src, dst)
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)

    def _copyarchive(self, idlist: Union[str, List[Any]]) -> None:
        """Copies the archive directory down so that MockTopDir will be the top of the r/w tree"""
        if self.__srcDir is None or self.__dstDir is None:
            logger.error("srcDir of dstDir not set --- FATAL")
            return

        if type(idlist) is str:
            idlist = [idlist]

        for did in idlist:
            src = os.path.join(self.__srcDir, "da_top", "data", "archive", did)
            dst = os.path.join(self.__dstDir, "da_top", "data", "archive", did)
            logger.info("Copying %s to %s", src, dst)
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
