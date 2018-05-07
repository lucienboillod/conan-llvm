#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os, platform

class llvmConan(ConanFile):
    name = "llvm"
    version = "5.0.1"
    description = "Conan.io package for LLVM library."
    url = "https://github.com/lucienboillod/conan-llvm"
    license = "http://releases.llvm.org/2.8/LICENSE.TXT"
    exports = ["LICENSE.md"]
    source_dir = "{name}-{version}.src".format(name=name, version=version)
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {'shared': [True, False]}
    default_options = 'shared=False'
    short_paths = True

    def build_requirements(self):
        if platform.system() == "Windows":
            self.build_requires("7z_installer/1.0@conan/stable")

    def extractFromUrl(self, url):
        self.output.info('download {}'.format(url))
        sources = os.path.basename(url)
        tools.download(url, sources)
        if platform.system() != "Windows":
            cmd = "tar -xJf {sources}".format(sources=sources)
            self.run(cmd)
        else:
            cmd = "7z.exe e {sources}".format(sources=sources)
            self.run(cmd)
            tools.unzip(self.source_dir + ".tar", ".")
            os.unlink(self.source_dir + ".tar")
        os.unlink(sources)

    def source(self):
        url = 'http://releases.llvm.org/' + self.version + '/llvm-' + self.version + '.src.tar.xz'
        self.extractFromUrl(url)

    def build(self):
        with tools.chdir(os.path.join(self.source_folder, self.source_dir)):
            cmake = CMake(self)
            cmake.verbose = True
            cmake.definitions["BUILD_SHARED_LIBS"] = "OFF"
            cmake.definitions["LIBCXX_INCLUDE_TESTS"] = "OFF"
            cmake.definitions["LIBCXX_INCLUDE_DOCS"] = "OFF"
            cmake.definitions["LLVM_INCLUDE_TOOLS"] = "ON"
            cmake.definitions["LLVM_INCLUDE_TESTS"] = "OFF"
            cmake.definitions["LLVM_INCLUDE_EXAMPLES"] = "OFF"
            cmake.definitions["LLVM_INCLUDE_GO_TESTS"] = "OFF"
            cmake.definitions["LLVM_BUILD_TOOLS"] = "ON"
            cmake.definitions["LLVM_BUILD_TESTS"] = "OFF"
            cmake.configure(source_dir=os.path.join(self.source_folder, self.source_dir))
            cmake.build()
            cmake.install()

    def package(self):
        self.copy('*', dst='', src='install')
