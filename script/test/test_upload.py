#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import unittest
import os
import upload
from githubmock import Repo, Release, Asset
from mock import MagicMock

dirname = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dirname, '..'))


# get an existing release (in draft status) from GitHub given a tag name
class TestGetDraft(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()

    def test_returns_existing_draft(self):
        self.repo.releases._releases = [{'tag_name': 'test', 'draft': True}]
        self.assertEquals(upload.get_release(self.repo,
                                             'test')['tag_name'], 'test', False)

    def test_fails_on_existing_release(self):
        self.repo.releases._releases = [{'tag_name': 'test', 'draft': False, 'allow_published_release_updates': False}]
        self.assertRaises(UserWarning, upload.get_release, self.repo, 'test', False)

    def test_returns_none_on_new_draft(self):
        self.repo.releases._releases = [{'tag_name': 'old', 'draft': False}]
        upload.get_release(self.repo, 'new', False)
        self.assertEquals(upload.get_release(self.repo, 'test'), None)


class TestGetBravePackages(unittest.TestCase):
    get_pkgs_dir = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'test_get_pkgs')
    _is_setup = False

    def setUp(self):
        if not self._is_setup:
            for chan in ['Nightly', 'Dev', 'Beta', 'Release']:
                if chan not in 'Release':
                    for mode in ['Stub', 'Standalone']:
                        name = 'BraveBrowser{}{}Setup_70_0_56_8.exe'.format(
                            mode if mode not in 'Stub' else '', chan)
                        name32 = ('BraveBrowser{}{}Setup32_70_0_56_8.exe'
                                  .format(mode if mode not in 'Stub'
                                          else '', chan))
                        with open(os.path.join(self.get_pkgs_dir,
                                               'win32', name), 'w') as f:
                            f.write(name + '\n')
                        with open(os.path.join(self.get_pkgs_dir,
                                               'win32', name32), 'w') as f:
                            f.write(name32 + '\n')
                else:
                    for mode in ['Stub', 'Standalone']:
                        name = 'BraveBrowser{}Setup_70_0_56_8.exe'.format(
                            mode if mode not in 'Stub' else '')
                        name32 = 'BraveBrowser{}Setup32_70_0_56_8.exe'.format(
                            mode if mode not in 'Stub' else '')
                        with open(os.path.join(
                                self.get_pkgs_dir, 'win32', name), 'w') as f:
                            f.write(name + '\n')
                        with open(os.path.join(
                                self.get_pkgs_dir, 'win32', name32), 'w') as f:
                            f.write(name32 + '\n')
        self.__class__._is_setup = True

    def test_only_returns_nightly_darwin_package(self):
        upload.PLATFORM = 'darwin'
        pkgs = list(upload.get_brave_packages(os.path.join(
            self.get_pkgs_dir, upload.PLATFORM), 'nightly', '0.50.8'))
        self.assertEquals(pkgs, ['Brave-Browser-Nightly.dmg'])

    def test_only_returns_dev_darwin_package(self):
        upload.PLATFORM = 'darwin'
        pkgs = list(upload.get_brave_packages(os.path.join(
            self.get_pkgs_dir, upload.PLATFORM), 'dev', '0.50.8'))
        self.assertEquals(pkgs, ['Brave-Browser-Dev.dmg'])

    def test_only_returns_beta_darwin_package(self):
        upload.PLATFORM = 'darwin'
        pkgs = list(upload.get_brave_packages(
            os.path.join(self.get_pkgs_dir, upload.PLATFORM),
            'beta', '0.50.8'))
        self.assertEquals(pkgs, ['Brave-Browser-Beta.dmg'])

    def test_only_returns_release_darwin_package(self):
        upload.PLATFORM = 'darwin'
        pkgs = list(upload.get_brave_packages(
            os.path.join(self.get_pkgs_dir, upload.PLATFORM),
            'release', '0.50.8'))
        self.assertEquals(pkgs, ['Brave-Browser.dmg', 'Brave-Browser.pkg'])

    def test_only_returns_nightly_linux_packages(self):
        upload.PLATFORM = 'linux'
        pkgs = list(upload.get_brave_packages(os.path.join(self.get_pkgs_dir,
                                                           upload.PLATFORM),
                                              'nightly', '0.50.8'))
        self.assertEquals(sorted(pkgs),
                          sorted(['brave-browser-nightly-0.50.8-1.x86_64.rpm',
                                  'brave-browser-nightly_0.50.8_amd64.deb']))

    def test_only_returns_dev_linux_packages(self):
        upload.PLATFORM = 'linux'
        pkgs = list(upload.get_brave_packages(os.path.join(self.get_pkgs_dir,
                                                           upload.PLATFORM),
                                              'dev', '0.50.8'))
        self.assertEquals(sorted(pkgs),
                          sorted(['brave-browser-dev-0.50.8-1.x86_64.rpm',
                                  'brave-browser-dev_0.50.8_amd64.deb']))

    def test_only_returns_beta_linux_packages(self):
        upload.PLATFORM = 'linux'
        pkgs = list(upload.get_brave_packages(os.path.join(self.get_pkgs_dir,
                                                           upload.PLATFORM),
                                              'beta', '0.50.8'))
        self.assertEquals(sorted(pkgs),
                          sorted(['brave-browser-beta-0.50.8-1.x86_64.rpm',
                                  'brave-browser-beta_0.50.8_amd64.deb']))

    def test_only_returns_release_linux_packages(self):
        upload.PLATFORM = 'linux'
        pkgs = list(upload.get_brave_packages(os.path.join(self.get_pkgs_dir,
                                                           upload.PLATFORM),
                                              'release', '0.50.8'))
        self.assertEquals(sorted(pkgs),
                          sorted(['brave-browser-0.50.8-1.x86_64.rpm',
                                  'brave-browser_0.50.8_amd64.deb']))

    def test_only_returns_nightly_win_x64_package(self):
        upload.PLATFORM = 'win32'
        os.environ['TARGET_ARCH'] = 'x64'
        pkgs = list(upload.get_brave_packages(os.path.join(
            self.get_pkgs_dir, upload.PLATFORM), 'nightly', '0.56.8'))
        self.assertEquals(
            pkgs, ['BraveBrowserNightlySetup.exe', 'BraveBrowserStandaloneNightlySetup.exe'])

    def test_only_returns_nightly_win_ia32_package(self):
        upload.PLATFORM = 'win32'
        os.environ['TARGET_ARCH'] = 'ia32'
        pkgs = list(upload.get_brave_packages(
            os.path.join(self.get_pkgs_dir, upload.PLATFORM), 'nightly', '0.56.8'))
        self.assertEquals(
            sorted(pkgs), sorted(['BraveBrowserNightlySetup32.exe',
                                  'BraveBrowserStandaloneNightlySetup32.exe']))

    def test_only_returns_dev_win_x64_package(self):
        upload.PLATFORM = 'win32'
        os.environ['TARGET_ARCH'] = 'x64'
        pkgs = list(upload.get_brave_packages(os.path.join(
            self.get_pkgs_dir, upload.PLATFORM), 'dev', '0.56.8'))
        self.assertEquals(
            sorted(pkgs), sorted(['BraveBrowserDevSetup.exe',
                                  'BraveBrowserStandaloneDevSetup.exe']))

    def test_only_returns_dev_win_ia32_package(self):
        upload.PLATFORM = 'win32'
        os.environ['TARGET_ARCH'] = 'ia32'
        pkgs = list(upload.get_brave_packages(
            os.path.join(self.get_pkgs_dir, upload.PLATFORM), 'dev', '0.56.8'))
        self.assertEquals(
            sorted(pkgs), sorted(['BraveBrowserDevSetup32.exe',
                                  'BraveBrowserStandaloneDevSetup32.exe']))

    def test_only_returns_beta_win_x64_package(self):
        upload.PLATFORM = 'win32'
        os.environ['TARGET_ARCH'] = 'x64'
        pkgs = list(upload.get_brave_packages(
            os.path.join(self.get_pkgs_dir, upload.PLATFORM),
            'beta', '0.56.8'))
        self.assertEquals(
            sorted(pkgs), sorted(['BraveBrowserBetaSetup.exe',
                                  'BraveBrowserStandaloneBetaSetup.exe']))

    def test_only_returns_beta_win_ia32_package(self):
        upload.PLATFORM = 'win32'
        os.environ['TARGET_ARCH'] = 'ia32'
        pkgs = list(upload.get_brave_packages(
            os.path.join(self.get_pkgs_dir, upload.PLATFORM),
            'beta', '0.56.8'))
        self.assertEquals(
            sorted(pkgs), sorted(['BraveBrowserBetaSetup32.exe',
                                  'BraveBrowserStandaloneBetaSetup32.exe']))

    def test_only_returns_release_win_x64_package(self):
        upload.PLATFORM = 'win32'
        os.environ['TARGET_ARCH'] = 'x64'
        pkgs = list(upload.get_brave_packages(
            os.path.join(self.get_pkgs_dir, upload.PLATFORM),
            'release', '0.56.8'))
        self.assertEquals(sorted(pkgs), sorted(['BraveBrowserSetup.exe',
                                                'BraveBrowserStandaloneSetup.exe']))

    def test_only_returns_release_win_ia32_package(self):
        upload.PLATFORM = 'win32'
        os.environ['TARGET_ARCH'] = 'ia32'
        pkgs = list(upload.get_brave_packages(
            os.path.join(self.get_pkgs_dir, upload.PLATFORM),
            'release', '0.56.8'))
        self.assertEquals(sorted(pkgs), sorted(['BraveBrowserStandaloneSetup32.exe',
                                                'BraveBrowserSetup32.exe']))


# uploading a single file to GitHub
class TestUploadBrave(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.file_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)),
            'test_get_pkgs',
            'win32',
            'BraveBrowserSetup.exe')
        self.release = Release()
        self.release.id = 1
        self.release.tag_name = 'release-tag-here'
        self.asset = Asset(1, 'BraveBrowserSetup.exe')
        self.release.assets._assets.append(self.asset)
        self.repo.releases._releases = [self.release]
        self.repo.releases.assets = self.release.assets

        self._old_upload_sha256_checksum = upload.upload_sha256_checksum
        upload.upload_sha256_checksum = MagicMock()

        self._old_upload_io_to_github = upload.upload_io_to_github
        upload.upload_io_to_github = MagicMock()

        self._old_delete_file = upload.delete_file
        upload.delete_file = MagicMock()

    def tearDown(self):
        upload.upload_sha256_checksum = self._old_upload_sha256_checksum
        upload.upload_io_to_github = self._old_upload_io_to_github
        upload.delete_file = self._old_delete_file

    def test_calls_delete_if_asset_already_exists(self):
        upload.upload_brave(self.repo, self.release, self.file_path)
        self.asset.delete.assert_called()

    def test_does_not_call_delete_if_asset_not_present(self):
        empty_repo = Repo()
        upload.upload_brave(empty_repo, self.release, self.file_path)
        self.asset.delete.assert_not_called()

    def test_does_not_force_delete_before_upload_when_force_false(self):
        upload.upload_brave(self.repo, self.release, self.file_path)
        upload.delete_file.assert_not_called()

    def test_force_delete_before_upload_when_force_true(self):
        upload.upload_brave(self.repo, self.release,
                            self.file_path, None, True)
        upload.delete_file.assert_called_with(
            self.repo, self.release, self.release.assets._assets[0].name)

    def test_force_delete_before_upload_when_force_true_with_filename_override(self):
        fake_filename = 'fake-name-here'
        upload.upload_brave(self.repo, self.release,
                            self.file_path, fake_filename, True)
        upload.delete_file.assert_called_with(
            self.repo, self.release, fake_filename)

    def test_calls_upload(self):
        upload.upload_brave(self.repo, self.release, self.file_path)
        upload.upload_io_to_github.assert_called()

        args, kwargs = upload.upload_io_to_github.call_args
        self.assertTrue(args[0] == self.repo)
        self.assertTrue(args[2] == self.release.assets._assets[0].name)
        self.assertTrue(args[4] == 'application/zip')

    def test_calls_upload_with_filename_override(self):
        fake_filename = 'fake-name-here'
        upload.upload_brave(self.repo, self.release,
                            self.file_path, fake_filename)
        upload.upload_io_to_github.assert_called()

        args, kwargs = upload.upload_io_to_github.call_args
        self.assertTrue(args[0] == self.repo)
        self.assertTrue(args[2] == fake_filename)
        self.assertTrue(args[4] == 'application/zip')

    # NOTE: retries tested in test_helpers.py with TestRetryFunc

    def test_calls_uploads_checksum(self):
        upload.upload_brave(self.repo, self.release, self.file_path)
        upload.upload_sha256_checksum.assert_called_with(
            self.release.tag_name, self.file_path)

    # TODO: test `armv7l` code path


if __name__ == '__main__':
    print unittest.main()
