__author__    = "Ole Weidner"
__copyright__ = "Copyright 2012-2013, The SAGA Project"
__license__   = "MIT"

import uuid
import saga
import unittest
import saga.utils.test_config as sutc

from copy import deepcopy


class TestFile(unittest.TestCase):

    # -------------------------------------------------------------------------
    #
    @classmethod
    def setUpClass(self):
        """Setup called once per class instance"""
        self.uniquefilename1 = "saga-unittests-"+str(uuid.uuid1())
        self.uniquefilename2 = "saga-unittests-"+str(uuid.uuid1())

    # -------------------------------------------------------------------------
    #
    @classmethod
    def tearDownClass(self):
        """Teardown called once per class instance"""
        try:
            # do the cleanup
            tc = sutc.TestConfig()
            d = saga.filesystem.Directory(tc.filesystem_url)
            d.remove(self.uniquefilename1)
            d.remove(self.uniquefilename2)
        except saga.SagaException as ex:
            pass


    # -------------------------------------------------------------------------
    #
    def test_nonexisting_host_file_open(self):
        """ Testing if opening a file on a non-existing host causes an exception.
        """
        try:
            tc = sutc.TestConfig()
            invalid_url = deepcopy(saga.Url(tc.filesystem_url))
            invalid_url.host += ".does.not.exist"
            f = saga.filesystem.File(invalid_url)
            assert False, "Expected BadParameter exception but got none."
        except saga.BadParameter:
            assert True
        except saga.SagaException as ex:
            assert False, "Expected BadParameter exception, but got %s" % ex


    # -------------------------------------------------------------------------
    #
    def test_nonexisting_file_open(self):
        """ Testing if opening a non-existing file causes an exception.
        """
        try:
            pass
            tc = sutc.TestConfig()
            nonex_file = deepcopy(saga.Url(tc.filesystem_url))
            nonex_file.path += "/file.does.not.exist"
            f = saga.filesystem.File(nonex_file)
            assert False, "Expected DoesNotExist exception but got none."
        except saga.DoesNotExist:
            assert True
        except saga.SagaException as ex:
            assert False, "Expected DoesNotExist exception, but got %s" % ex


    # -------------------------------------------------------------------------
    #
    def test_nonexisting_file_create_open(self):
        """ Testing if opening a non-existing file with the 'create' flag set works.
        """
        try:
            pass
            tc = sutc.TestConfig()
            nonex_file = deepcopy(saga.Url(tc.filesystem_url))
            nonex_file.path += "/%s" % self.uniquefilename1
            f = saga.filesystem.File(nonex_file, saga.filesystem.CREATE)
            assert f.size == 0  # this should fail if the file doesn't exist!
        except saga.SagaException as ex:
            assert False, "Unexpected exception: %s" % ex


    # -------------------------------------------------------------------------
    #
    def test_existing_file_open(self):
        """ Testing if we can open an existing file.
        """
        try:
            pass
            tc = sutc.TestConfig()
            filename = deepcopy(saga.Url(tc.filesystem_url))
            filename.path += "/%s" % self.uniquefilename1
            f = saga.filesystem.File(filename, saga.filesystem.CREATE)

            f2 = saga.filesystem.File(f.url)
            assert f2.size == 0  # this should fail if the file doesn't exist!

        except saga.SagaException as ex:
            assert False, "Unexpected exception: %s" % ex
