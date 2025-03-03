#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import shutil
import tempfile
import subprocess
import logging
import re
from pathlib import Path
import pyaxml
import requests
from apkpatcher.zipalign import zipalign
from collections import OrderedDict
import zipfile
import hashlib
import lzma
from typing import List

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree


def new_logger(level: "logging._Level") -> logging.Logger:
    logger = logging.getLogger("apkpatcher")

    class CustomFormatter(logging.Formatter):

        grey = "\x1b[38;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        tmp_format = (
            "%(asctime)s - %(name)s [ %(levelname)s ] - %(message)s (%(filename)s:%(lineno)d)"
        )

        FORMATS = {
            logging.DEBUG: grey + tmp_format + reset,
            logging.INFO: grey + tmp_format + reset,
            logging.WARNING: yellow + tmp_format + reset,
            logging.ERROR: red + tmp_format + reset,
            logging.CRITICAL: bold_red + tmp_format + reset,
        }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)

    ch = logging.StreamHandler()
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    logger.setLevel(level)
    return logger


def plba(filename: str | Path, arch):
    p = Path(filename)
    return f"{p.parent}/{p.stem}_{arch}.so"


def download_smali(output_file : Path):
    version = "3.0.9"
    r = requests.get(
        f"https://github.com/baksmali/smali/releases/download/{version}/smali-{version}-fat-release.jar"
    )
    with open(output_file, "wb") as f:
        f.write(r.content)


def download_baksmali(output_file : Path):
    version = "3.0.9"
    r = requests.get(
        f"https://github.com/baksmali/smali/releases/download/{version}/baksmali-{version}-fat-release.jar"
    )
    with open(output_file, "wb") as f:
        f.write(r.content)

def get_latest_version_directory(base_path : Path):
    try:
        from packaging.version import Version 
        dirs = [d for d in base_path.iterdir() if d.is_dir()]
        version_dirs = [d.name for d in dirs if re.match(r'^[0-9]+\.[0-9]+\.[0-9]+(-rc[0-9]+)?$', d.name)]
        latest_version = max(version_dirs, key=Version, default=None)
        return latest_version if latest_version else None
    except Exception as e:
        return None


class Patcher:

    ARCH_ARM = "arm"
    ARCH_ARM64 = "arm64"
    ARCH_X86 = "x86"
    ARCH_X64 = "x64"
    ARCH_X86_64 = "x86_64"

    DEFAULT_GADGET_NAME = "libfrida-gadget.so"
    DEFAULT_HOOKFILE_NAME = "libhook.js.so"
    DEFAULT_CONFIG_NAME = "generatedConfigFile.config"

    CONFIG_BIT = 1 << 0
    AUTOLOAD_BIT = 1 << 1

    INTERNET_PERMISSION = "android.permission.INTERNET"

    def __init__(
        self,
        apk: str | Path,
        version_buildtools: str,
        sdktools: str | Path = None,
        logger: logging.Logger | None = None,
    ):
        """
        Initialisation of patcher

        Parameters:
                    apk (str): path of the apk
                    sdktools (str): path of the sdktools for zipalign
                    version_buildtools (str): version_buildtools to choose the correct path of
                    logger (logging.Logger) logger

        """
        if logger is None:
            self.logger: logging.Logger = new_logger(logging.INFO)
        else:
            self.logger: logging.Logger = logger
        self.apk: Path = Path(apk)
        self.arch: str | None = None
        if sdktools is None:
            if not "ANDROID_SDK_ROOT" in os.environ:
                self.logger.error(
                    "\nArgument sdktools is missing, you should add '-s /usr/lib/android-sdk' or ANDROID_SDK_ROOT environment variable is not set"
                )
                self.logger.error(
                    "If you didn't have installed sdktools follow this tutorial: https://asthook.ci-yow.com/how.install.html#setup-sdktools"
                )
                raise ValueError("sdktools is not set is not set or incorrect")
            else:
                args.sdktools = os.environ["ANDROID_SDK_ROOT"]
        self.sdktools: Path = Path(sdktools)
        self.version: str = version_buildtools
        self.final_dir: Path = Path("")
        self._pause: bool = False
        self.plugin: Path | None = None
        self.entrypoint_smali_path: Path | None = None
        self.entrypoint_class: str | None = None

        self.debug_mode: bool = False

        self.keycertificate = Path("./apkpatcherkeystore")
        self.keyalias = "apkpatcheralias1"
        self.keypass = "password"

        self._keep_keycertificate = False

        self.v4_signature_file = None
        self.frida_downloaded: List[Path] = []

        self.hash_dict = {}

        if self.version is None:
            self.version = get_latest_version_directory(Path(f"{sdktools}/build-tools/"))
            if self.version is None:
                self.logger.error("\nArgument version_buildtools is missing, you should add it")
                self.logger.error("To know buildtools installed you can use: sdkmanager --list")
                raise ValueError("version_buildtools is not set or incorrect")

        self.path_build_tools = Path(
            f"{sdktools}/build-tools/{self.version}/" if (sdktools and self.version) else ""
        )
        if not self.path_build_tools.exists():
            self.logger.error("\nArgument version_buildtools is missing, you should add it")
            self.logger.error("To know buildtools installed you can use: sdkmanager --list")
            raise ValueError("version_buildtools is not set or incorrect")
        self.network_certificates: list[Path] = []
        import jnius_config

        smali_jar = Path(__file__).parent / "smali.jar"
        if not smali_jar.exists():
            download_smali(smali_jar)

        baksmali_jar = Path(__file__).parent / "baksmali.jar"
        if not baksmali_jar.exists():
            download_baksmali(baksmali_jar)

        jnius_config.set_classpath(
            baksmali_jar.as_posix(),
            smali_jar.as_posix(),
            f"{self.path_build_tools}/lib/apksigner.jar",
        )
        if not "JAVA_HOME" in os.environ:
            try:
                # Run the command to get the properties
                result = subprocess.run(
                    ["java", "-XshowSettings:properties", "-version"],
                    stderr=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,  # Redirect stdout to /dev/null
                    text=True,
                )
                # Filter the output to find the 'java.home' property
                for line in result.stderr.splitlines():
                    if "java.home" in line:
                        # Extract the value after the '='
                        java_home = line.split("=", 1)[1].strip()
                        os.environ["JAVA_HOME"] = java_home
                        break
            except FileNotFoundError:
                self.logger.error("Java is not installed or not found in PATH.")
        from jnius import autoclass, cast

        self.cast = cast
        self.smali = autoclass("com.android.tools.smali.smali.Main")
        self.baksmali = autoclass("com.android.tools.smali.baksmali.Main")

        self.File = autoclass("java.io.File")
        self.ArrayList = autoclass("java.util.ArrayList")
        self.Collections = autoclass("java.util.Collections")
        self.KeyStore = autoclass("java.security.KeyStore")
        self.FileInputStream = autoclass("java.io.FileInputStream")
        self.PrivateKey = autoclass("java.security.PrivateKey")

        self.ApkSigner_Builder = autoclass("com.android.apksig.ApkSigner$Builder")
        self.SignerConfig_Builder = autoclass("com.android.apksig.ApkSigner$SignerConfig$Builder")

    ################################################################################
    #                                                                              #
    #            CERTIFICATES                                                      #
    #                                                                              #
    ################################################################################

    def add_network_certificate(self, cert: Path):
        self.network_certificates.append(cert)

    def use_download_frida(self, frida_version: str):
        self.use_download_frida = frida_version

    def remove_frida_downloaded(self):
        for f in self.frida_downloaded:
            f.unlink()

    def download_frida(self):
        base_url = "https://github.com/frida/frida/releases/download/"
        if not self.arch:
            architectures = [
                self.ARCH_ARM,
                self.ARCH_ARM64,
                self.ARCH_X86,
                self.ARCH_X86_64,
            ]
        else:
            if self.arch == self.ARCH_X64:
                architectures = [self.ARCH_X86_64]
            else:
                architectures = [self.arch]
        self.remove_frida_downloaded()
        self.frida_downloaded: List[Path] = []

        for arch in architectures:
            filename = f"frida-gadget-{self.use_download_frida}-android-{arch}.so.xz"
            url = f"{base_url}{self.use_download_frida}/{filename}"
            output_file = Path(f"frida-gadget_{arch}.so")

            try:
                # Download the file
                self.logger.info(f"Downloading {url}...")
                response = requests.get(url)
                response.raise_for_status()

                # Save the compressed file
                compressed_path = Path(filename)
                with open(compressed_path, "wb") as f:
                    f.write(response.content)

                # Uncompress the file
                self.logger.info(f"Uncompressing {compressed_path}...")
                with lzma.open(compressed_path, "rb") as xz_file:
                    with open(output_file, "wb") as out_file:
                        out_file.write(xz_file.read())

                # Remove the compressed file
                compressed_path.unlink()
                self.frida_downloaded.append(output_file)

            except requests.HTTPError as e:
                self.logger.error(f"Failed to download {url}: {e}")
            except lzma.LZMAError as e:
                self.logger.error(f"Failed to uncompress {filename}: {e}")

        if len(self.frida_downloaded) == 1:
            return self.frida_downloaded[0].name
        elif self.frida_downloaded:
            return "frida-gadget"
        else:
            return None

    def inject_custom_network_certificate(self, rsc, path_network: str):
        netsec_path = self.final_dir / path_network
        ca_path = self.final_dir / "res/my_ca"

        _id = rsc.add_id_public(
            rsc.get_packages()[0], "raw", "network_security_config_ca", "res/my_ca"
        )

        buf = f"""
        <network-security-config>
            <base-config cleartextTrafficPermitted="true">
                <trust-anchors>
                    <certificates src="system"/>
                    <certificates src="user"/>
                    <certificates src="@{hex(_id)[2:]}"/>
                </trust-anchors>
            </base-config>
        </network-security-config>
        """

        root = etree.fromstring(buf)
        res_aml = pyaxml.axml.AXML()
        res_aml.from_xml(root)
        with open(netsec_path, "wb") as f:
            f.write(res_aml.pack())

        for cert in self.network_certificates:
            shutil.copyfile(cert, ca_path)
        self.logger.info("Custom certificate was injected inside the apk")

    def create_security_config_xml(self, path_network: str):
        """Create security config file for add certificate

        Args:
            path_network (str): path network
        """
        netsec_path = self.final_dir / path_network

        buf = """
        <network-security-config>
            <base-config cleartextTrafficPermitted="true">
                <trust-anchors>
                    <certificates src="system"/>
                    <certificates src="user"/>
                </trust-anchors>
            </base-config>
        </network-security-config>
        """
        root = etree.fromstring(buf)
        res_aml = pyaxml.axml.AXML()
        res_aml.from_xml(root)
        with open(netsec_path, "wb") as f:
            f.write(res_aml.pack())

        self.logger.info("The network_security_config.xml file was created!")

    def enable_user_certificates(self, rsc: pyaxml.ARSC):
        """Enable user certificate

        Args:
            rsc (pyaxml.ARSC): return ARSC file
        """
        path_network = self.inject_user_certificates_label(rsc)
        if path_network:
            if self.network_certificates:
                self.inject_custom_network_certificate(rsc, path_network)
            else:
                self.create_security_config_xml(path_network)

    def inject_user_certificates_label(self, rsc: pyaxml.ARSC) -> str:
        """Inject a proxy certificate directly inside the application

        Args:
            rsc (pyaxml.ARSC): ARSC file (resource file of Android)

        Raises:
            FileNotFoundError: raise when manifest is not found

        Returns:
            str: return the path of network file
        """
        self.logger.info("Injecting Network Security label to accept user certificates...")

        manifest_path = self.final_dir / "AndroidManifest.xml"

        if not manifest_path.is_file():
            self.logger.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            raise FileNotFoundError("manifest not found")

        with open(manifest_path, "rb") as fp:
            buf = fp.read()

            _id = rsc.get_id_public(rsc.get_packages()[0], "xml", "network_security_config")
            if not _id:
                path_network: str = "res/network_security_config.xml"
                _id = rsc.add_id_public(
                    rsc.get_packages()[0],
                    "xml",
                    "network_security_config",
                    path_network,
                )
            else:
                _id, path_network = _id
                path_network = pyaxml.StringBlocks(proto=rsc.proto.stringblocks).decode_str(
                    path_network
                )

            axml, _ = pyaxml.AXML.from_axml(buf)
            xml = axml.to_xml()
            application = xml.findall("./application")[0]
            application.attrib[
                "{http://schemas.android.com/apk/res/android}networkSecurityConfig"
            ] = f"@{hex(_id)[2:]}"
            res_aml = pyaxml.axml.AXML()
            res_aml.from_xml(xml)

            with open(manifest_path, "wb") as fp_out:
                fp_out.write(res_aml.pack())

            self.logger.info("The Network Security label was added!")

        return path_network

    ################################################################################
    #                                                                              #
    #                        PERMISSIONS                                           #
    #                                                                              #
    ################################################################################

    def has_permission(self, permission_name: str) -> bool:
        """
        Check if the apk have 'permission_name' as permission

        Parameters:
                    permission_name (str): name of the permission with format:
                    android.permission.XXX

        Returns:
                has_permission (bool): permission is present
        """
        manifest_path = self.final_dir / "AndroidManifest.xml"

        if not manifest_path.is_file():
            self.logger.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            raise FileNotFoundError("manifest not found")

        with open(manifest_path, "rb") as f:
            # Read AXML and get XML object
            axml, _ = pyaxml.AXML.from_axml(f.read())
            xml = axml.to_xml()

            # Search over all the application permissions
            android_name = "{http://schemas.android.com/apk/res/android}name"
            for permission in xml.findall("./uses-permission"):
                if permission.attrib[android_name] == permission_name:
                    self.logger.info(
                        "The app %s has the permission '%s'", self.apk, permission_name
                    )
                    return True

        self.logger.info("The app %s doesn't have the permission '%s'", self.apk, permission_name)
        return False

    def inject_permission_manifest(self, permission: str):
        """
        Inject permission on the Manifest
        """
        self.logger.info("Injecting permission %s in Manifest...", permission)

        manifest_path = self.final_dir / "AndroidManifest.xml"

        if not manifest_path.is_file():
            self.logger.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            return False

        with open(manifest_path, "rb") as fp:
            buf = fp.read()

            axml, _ = pyaxml.AXML.from_axml(buf)
            xml = axml.to_xml()
            res_aml: pyaxml.AXML | None = None
            for i, elt in enumerate(xml):  # range(len(xml)):
                if elt.tag in ("application", "uses-permission"):
                    newperm = etree.Element("uses-permission")
                    newperm.attrib["{http://schemas.android.com/apk/res/android}name"] = permission
                    xml.insert(i, newperm)
                    res_aml = pyaxml.axml.AXML()
                    res_aml.from_xml(xml)
                    break
        if res_aml is None:
            self.logger.error("resource file could not be found")
            return False
        with open(manifest_path, "wb") as fp:
            fp.write(res_aml.pack())
        return True

    ################################################################################
    #                                                                              #
    #                EXTRACT REPACK APK                                            #
    #                                                                              #
    ################################################################################

    def extract_apk(self):
        """
        Extract the apk on the temporary folder
        """

        self.logger.info("Extracting %s (without resources) to %s", self.apk, self.final_dir)
        # Ensure the extraction directory exists
        self.final_dir.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(self.apk.absolute().as_posix(), "r") as zip_ref:
                zip_ref.extractall(self.final_dir.absolute().as_posix())
                self.logger.info(f"Extraction complete.")
        except zipfile.BadZipFile as e:
            self.logger.error(f"Error: The file is not a valid zip file: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error during extraction: {e}")

        # Iterate over files in the directory
        for dex_file in self.final_dir.rglob("*.dex"):
            # Define the output directory
            output_dir = dex_file.parent / ("smali_" + dex_file.stem)

            self.logger.info(f"Processing {dex_file}...")

            self.baksmali.main(
                [
                    "d",
                    dex_file.as_posix(),
                    "-o",
                    output_dir.as_posix(),
                ]
            )
            self.compute_directory_hashes(output_dir)

    def add_certificate(self, keycertificate: Path | str, keyalias: str, keypass: str):
        """Add signature certificate

        Args:
            keycertificate (Path | str): certificate path
            keyalias (str): aliasname
            keypass (str): password
        """
        self.keycertificate = Path(keycertificate)
        self.keyalias = keyalias
        self.keypass = keypass
        self.keep_certificate()

    def keep_certificate(self):
        """keep certificate after use it"""
        self._keep_keycertificate = True

    def enable_v4_signature(self, file: Path | str):
        """enable v4 signature

        Args:
            file (Path | str): v4_signature file
        """
        self.v4_signature_file = Path(file)

    def sign_and_zipalign(self, apk_path: Path, splits_apk):
        """
        sign and zipalign file
        """

        self.logger.info("Optimizing with zipalign...")

        tmp_target_file: Path = apk_path.rename(
            apk_path.with_name(apk_path.stem.replace(".apk", "_tmp.apk"))
        )

        zipalign(tmp_target_file, apk_path)

        tmp_target_file.unlink()

        self.logger.info("Generating a random key...")
        if not self.keycertificate.exists():
            subprocess.call(
                f"keytool -genkey -keyalg RSA -keysize 2048 -validity 700 -noprompt -alias {self.keyalias} -dname "
                f'"CN=apk.patcher.com, OU=ID, O=APK, L=Patcher, S=Patch, C=BR" -keystore {self.keycertificate} '
                f"-storepass {self.keypass} -keypass {self.keypass} 2> /dev/null",
                shell=True,
            )

        self.logger.info("Signing the patched apk...")

        keyStore = self.KeyStore.getInstance("JKS")
        fis = self.FileInputStream(self.keycertificate.as_posix())
        keyStore.load(fis, self.keypass)

        privateKey = keyStore.getKey(self.keyalias, self.keypass)
        cert = keyStore.getCertificate(self.keyalias)

        l = self.ArrayList()
        l.add(self.cast("java.security.cert.X509Certificate", cert))
        signerConfig = self.SignerConfig_Builder(
            "signer", self.cast("java.security.PrivateKey", privateKey), l
        )
        signerconfig = signerConfig.build()

        tmp_target_file: Path = apk_path.rename(
            apk_path.with_name(apk_path.stem.replace(".apk", "_tmp.apk"))
        )

        signerBuilder = self.ApkSigner_Builder(self.Collections.singletonList(signerconfig))
        signerBuilder.setInputApk(self.File(tmp_target_file.as_posix()))
        signerBuilder.setOutputApk(self.File(apk_path.as_posix()))
        signerBuilder.setV1SigningEnabled(True)
        signerBuilder.setV2SigningEnabled(True)
        signerBuilder.setV3SigningEnabled(True)
        if self.debug_mode:
            signerBuilder.setDebuggableApkPermitted(True)
        if self.v4_signature_file:
            signerBuilder.setV4SigningEnabled(True)
            signerBuilder.setV4SignatureOutputFile(self.v4_signature_file.as_posix())

        apkSigner = signerBuilder.build()
        apkSigner.sign()

        tmp_target_file.unlink()

        for split in splits_apk:
            split_new_name = split.replace(".apk", "_new_signed.apk")
            signerBuilder = self.ApkSigner_Builder(self.Collections.singletonList(signerconfig))
            signerBuilder.setInputApk(self.File(split))
            signerBuilder.setOutputApk(self.File(split_new_name))
            signerBuilder.setV1SigningEnabled(True)
            signerBuilder.setV2SigningEnabled(True)
            signerBuilder.setV2SigningEnabled(True)
            signerBuilder.setV3SigningEnabled(True)
            if self.debug_mode:
                signerBuilder.setDebuggableApkPermitted(True)
            if self.v4_signature_file:
                signerBuilder.setV4SigningEnabled(True)
                signerBuilder.setV4SignatureOutputFile(self.v4_signature_file.as_posix())

            apkSigner = signerBuilder.build()
            apkSigner.sign()

        if not self._keep_keycertificate:
            self.keycertificate.unlink()

        self.logger.info("The apk was signed!")

        self.logger.info("The file was optimized!")

    def pause(self, pause: bool) -> None:
        """enable a pause during the process to edit the application

        Args:
            pause (bool): pause parameter
        """
        self._pause = pause

    def set_plugin(self, plugin: str | Path) -> None:
        """set a plugin

        Args:
            plugin (str | Path): _description_
        """
        self.plugin = Path(plugin)

    def calculate_sha256(self, file_path: Path):
        """
        Calculate the SHA-256 hash of a file.

        :param file_path: Path to the file.
        :return: SHA-256 hash as a hexadecimal string.
        """
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def compute_directory_hashes(self, base_directory, hash_dict: dict | None = None) -> None:
        """
        Compute SHA-256 hashes for all files in a directory and store them in a nested dictionary.

        :param base_directory: Path to the base directory.
        """
        base_path = Path(base_directory)
        if not base_path.is_dir():
            raise ValueError(f"Provided path is not a directory: {base_directory}")

        if hash_dict is None:
            hash_dict = self.hash_dict

        class_name = base_path.name  # Use the base directory name as the class_name

        for file_path in base_path.rglob("*"):  # Recursively iterate through all files
            if file_path.is_file():
                relative_path = file_path.relative_to(base_path).as_posix()
                file_hash = self.calculate_sha256(file_path)

                # Add to the dictionary
                if class_name not in hash_dict:
                    hash_dict[class_name] = {}
                hash_dict[class_name][relative_path] = file_hash

    def __check_if_dex_is_modified(self, class_dir: Path) -> bool:

        old_files = set()
        new_files = set()

        for path, hash_value in self.hash_dict[class_dir.name].items():
            old_files.add((path, hash_value))

        new_files_dict = {}
        self.compute_directory_hashes(class_dir, new_files_dict)

        for path, hash_value in new_files_dict[class_dir.name].items():
            new_files.add((path, hash_value))

        return len(new_files - old_files) != 0 or len(old_files - new_files) != 0

    def repackage_apk(self, target_file: Path | None = None):
        """
        repackage the apk

        Parameters:
                    - target_file (str) : the path of the new apk created if
                      none, a new apk will be created with suffix "_patched.apk"
        """
        if self.plugin:
            subprocess.run([self.plugin, self.final_dir], check=True)
        if self._pause:
            self.logger.info(f"You can modify the apk here: {self.final_dir}")
            input()
        if target_file is None:
            target_file = self.apk.with_name(self.apk.stem + "_patched.apk")

            if target_file.is_file():
                timestamp = str(time.time()).replace(".", "")
                new_file_name = target_file.with_name(f"{target_file.stem}_{timestamp}.apk")
                target_file = new_file_name

        self.logger.info("Repackaging apk to %s", target_file)
        self.logger.info("This may take some time...")

        # Iterate over directories starting with "classes"
        for classes_dir in self.final_dir.iterdir():
            if classes_dir.is_dir() and classes_dir.name.startswith("smali_"):
                dex_file_name = f"{classes_dir.name[6:]}.dex"
                dex_file_path = classes_dir.parent / dex_file_name

                self.logger.info(f"Processing {classes_dir}...")
                if self.__check_if_dex_is_modified(classes_dir):
                    self.smali.main(
                        [
                            "a",
                            classes_dir.as_posix(),
                            "-o",
                            dex_file_path.as_posix(),
                        ]
                    )
                shutil.rmtree(classes_dir)

        # Zip the contents of the parent directory
        zip_file_path = target_file.as_posix()
        self.logger.info(f"Creating zip archive: {zip_file_path}")
        try:
            with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_STORED) as zipf:
                for file in self.final_dir.rglob("*"):
                    zipf.write(file, arcname=file.relative_to(self.final_dir))
            self.logger.info(f"Successfully created zip archive: {zip_file_path}")
        except Exception as e:
            self.logger.error(f"Error creating zip archive: {e}")

        return target_file

    ################################################################################
    #                                                                              #
    #                INJECT NATIVE CODE                                            #
    #                                                                              #
    ################################################################################

    def get_entrypoint_class_name(self) -> str | None:
        """
        get the class name of the entrypoint
        """
        entrypoint_class = None
        manifest_path = self.final_dir / "AndroidManifest.xml"

        if not manifest_path.is_file():
            self.logger.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            raise FileNotFoundError("manifest not found")

        with open(manifest_path, "rb") as f:
            # Read AXML and get XML object
            axml, _ = pyaxml.AXML.from_axml(f.read())
            xml = axml.to_xml()
            # Look over all the activities and try to find either one with MAIN as action
            android_name = "{http://schemas.android.com/apk/res/android}name"
            for activity in xml.findall("./application/activity"):
                is_main = False
                for action in activity.findall("intent-filter/action"):
                    if action.attrib[android_name] == "android.intent.action.MAIN":
                        is_main = True
                        break
                if is_main:
                    for category in activity.findall("intent-filter/category"):
                        if category.attrib[android_name] == "android.intent.category.LAUNCHER":
                            entrypoint_class = activity.attrib[android_name]
                            break

            # Do the same for activities alias in case we did not find the main activity
            if not entrypoint_class:
                android_target_activity = (
                    "{http://schemas.android.com/apk/res/android}targetActivity"
                )
                for alias in xml.findall("./application/activity-alias"):
                    is_main = False
                    for action in alias.findall("intent-filter/action"):
                        if action.attrib[android_name] == "android.intent.action.MAIN":
                            is_main = True
                            break
                    if is_main:
                        for category in alias.findall("intent-filter/category"):
                            if category.attrib[android_name] == "android.intent.category.LAUNCHER":
                                entrypoint_class = alias.attrib[android_target_activity]
                                break

            # Check if entry point is relative, if so search in the Manifest package
            if entrypoint_class is None:
                self.logger.error("Fail to find entrypoint class")
                return entrypoint_class
            if entrypoint_class.startswith("."):
                entrypoint_class = xml.attrib["package"] + entrypoint_class

        if entrypoint_class is None:
            self.logger.error("Fail to find entrypoint class")

        return entrypoint_class

    def get_entrypoint_smali_path(self) -> Path | None:
        """
        get the path of apk entrypoint on the smali files
        """
        entrypoint_final_path = None
        if self.entrypoint_class is None:
            raise ValueError("entrypoint class is None")

        for file in self.final_dir.iterdir():
            if file.name.startswith("smali"):
                entrypoint_tmp = (
                    self.final_dir / file / (self.entrypoint_class.replace(".", "/") + ".smali")
                )
                if entrypoint_tmp.is_file():
                    entrypoint_final_path = entrypoint_tmp
                    break

        if entrypoint_final_path is None:
            self.logger.error("Couldn't find the application entrypoint")
            sys.exit(1)
        else:
            self.logger.info("Found application entrypoint at %s", entrypoint_final_path)

        return entrypoint_final_path

    def insert_frida_loader(self, frida_lib_name="frida-gadget"):
        """
        inject snippet to load frida-gadget in smali code
        """
        partial_injection_code = """
    const-string v0, "<LIBFRIDA>"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

        """.replace(
            "<LIBFRIDA>", frida_lib_name
        )

        full_injection_code = """
.method static constructor <clinit>()V
    .locals 1

    .prologue
    const-string v0, "<LIBFRIDA>"

    invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V

    return-void
.end method
        """.replace(
            "<LIBFRIDA>", frida_lib_name
        )

        with open(self.entrypoint_smali_path, "r", encoding="ascii") as smali_file:
            content = smali_file.read()

            if frida_lib_name in content:
                self.logger.info("The frida-gadget is already in the entrypoint. Skipping...")
                return False

            direct_methods_start_index = content.find("# direct methods")
            direct_methods_end_index = content.find("# virtual methods")

            if direct_methods_start_index == -1 and direct_methods_end_index == -1:
                self.logger.error("Could not find direct methods.")
                return False

            class_constructor_start_index = content.find(
                ".method static constructor <clinit>()V",
                direct_methods_start_index,
                direct_methods_end_index,
            )

            if class_constructor_start_index == -1:
                has_class_constructor = False
            else:
                has_class_constructor = True

            class_constructor_end_index = -1
            if has_class_constructor:
                class_constructor_end_index = content.find(
                    ".end method",
                    class_constructor_start_index,
                    direct_methods_end_index,
                )

                if has_class_constructor and class_constructor_end_index == -1:
                    self.logger.error("Could not find the end of class constructor.")
                    return False

            prologue_start_index = -1
            if has_class_constructor:
                prologue_start_index = content.find(
                    ".prologue",
                    class_constructor_start_index,
                    class_constructor_end_index,
                )

            no_prologue_case = False
            locals_start_index = -1

            # check for locals
            if has_class_constructor and prologue_start_index == -1:
                no_prologue_case = True

                locals_start_index = content.find(
                    ".locals ",
                    class_constructor_start_index,
                    class_constructor_end_index,
                )

            if not no_prologue_case or locals_start_index != -1:
                locals_end_index = -1
                if no_prologue_case:
                    locals_end_index = locals_start_index + len("locals ")  # X')
                    x = re.search(r"^ *\d+", content[locals_end_index + 1 :])
                    locals_end_index += x.span()[1]
            else:

                # check for registers
                if has_class_constructor and prologue_start_index == -1:
                    no_prologue_case = True

                    locals_start_index = content.find(
                        ".registers ",
                        class_constructor_start_index,
                        class_constructor_end_index,
                    )

                    if no_prologue_case and locals_start_index == -1:
                        self.logger.error(
                            'Has class constructor. No prologue case, but no "locals 0" found.'
                        )
                        return False

                if not no_prologue_case or locals_start_index != -1:
                    locals_end_index = -1
                    if no_prologue_case:
                        locals_end_index = locals_start_index + len("registers ")  # X')
                        x = re.search(r"^ *\d+", content[locals_end_index + 1 :])
                        locals_end_index += x.span()[1]

            prologue_end_index = -1
            if has_class_constructor and prologue_start_index > -1:
                prologue_end_index = prologue_start_index + len(".prologue") + 1

            if has_class_constructor:
                if no_prologue_case:
                    new_content = content[0:locals_end_index]

                    if content[locals_end_index] == "0":
                        new_content += "1"
                    else:
                        new_content += content[locals_end_index]

                    new_content += "\n\n    .prologue"
                    new_content += partial_injection_code
                    new_content += content[locals_end_index + 1 :]
                else:
                    new_content = content[0:prologue_end_index]
                    new_content += partial_injection_code
                    new_content += content[prologue_end_index:]
            else:
                tmp_index = direct_methods_start_index + len("# direct methods") + 1
                new_content = content[0:tmp_index]
                new_content += full_injection_code
                new_content += content[tmp_index:]

        # The newContent is ready to be saved

        with open(self.entrypoint_smali_path, "w", encoding="ascii") as smali_file:
            smali_file.write(new_content)

        self.logger.info("Frida loader was injected in the entrypoint smali file!")

        return True

    def create_lib_arch_folders(self, arch):
        """
        make lib folder in the apk to put native lib
        """
        # noinspection PyUnusedLocal
        sub_dir = None
        sub_dir_2 = None

        libs_path = self.final_dir / "lib"

        if not libs_path.is_dir():
            self.logger.info('There is no "lib" folder. Creating...')
            libs_path.mkdir(parents=True, exist_ok=True)

        if arch == self.ARCH_ARM:
            sub_dir = libs_path / "armeabi"
            sub_dir_2 = libs_path / "armeabi-v7a"

        elif arch == self.ARCH_ARM64:
            sub_dir = libs_path / "arm64-v8a"

        elif arch == self.ARCH_X86:
            sub_dir = libs_path / "x86"

        elif arch == self.ARCH_X64:
            sub_dir = libs_path / "x86_64"

        else:
            self.logger.error("Couldn't create the appropriate folder with the given arch.")
            return []

        if not sub_dir.is_dir():
            self.logger.info("Creating folder %s", sub_dir)
            sub_dir.mkdir(parents=True, exist_ok=True)

        if arch == self.ARCH_ARM:
            if not sub_dir_2.is_dir():
                self.logger.info("Creating folder %s", sub_dir_2)
                sub_dir_2.mkdir(parents=True, exist_ok=True)

        if arch == self.ARCH_ARM:
            return [sub_dir, sub_dir_2]
        return [sub_dir]

    def check_libextract(self) -> bool:
        """check if extractNativeLibs is enable and active it

        Returns:
            bool: return False if we didn't find manifest
        """
        self.logger.info("check if lib is extractable")

        manifest_path = self.final_dir / "AndroidManifest.xml"

        if not manifest_path.is_file():
            self.logger.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            return False

        with open(manifest_path, "rb") as fp:
            axml, _ = pyaxml.AXML.from_axml(fp.read())
            etree_xml = axml.to_xml()
            extract_native = etree_xml.findall(
                "./application/[@{http://schemas.android.com/apk/res/android}extractNativeLibs='false']"
            )
            if len(extract_native) > 0:
                extract_native[0].attrib[
                    "{http://schemas.android.com/apk/res/android}extractNativeLibs"
                ] = "true"

        with open(manifest_path, "wb") as fp:
            res_aml = pyaxml.axml.AXML()
            res_aml.from_xml(etree_xml)
            fp.write(res_aml.pack())
        return True

    def insert_frida_lib(
        self,
        gadget_path: str,
        arch: str,
        config_file_path=None,
        auto_load_script_path=None,
    ):
        """
        Insert native lib inside the apk

        Parameters:
                    - gadget_path (str): the path of the gadget to insert
        """
        arch_folders = self.create_lib_arch_folders(arch)

        if not arch_folders:
            self.logger.error("Some error occurred while creating the libs folders")
            return False

        for folder in arch_folders:
            if config_file_path and auto_load_script_path:
                self.delete_existing_gadget(
                    folder, delete_custom_files=self.CONFIG_BIT | self.AUTOLOAD_BIT
                )

            elif config_file_path and not auto_load_script_path:
                self.delete_existing_gadget(folder, delete_custom_files=self.CONFIG_BIT)

            elif auto_load_script_path and not config_file_path:
                self.delete_existing_gadget(folder, delete_custom_files=self.AUTOLOAD_BIT)

            else:
                self.delete_existing_gadget(folder, delete_custom_files=0)

            target_gadget_path = folder / self.DEFAULT_GADGET_NAME

            self.logger.info("Copying gadget to %s", target_gadget_path)

            shutil.copyfile(gadget_path, target_gadget_path)

            if config_file_path:
                target_config_path = target_gadget_path.replace(".so", ".config.so")

                self.logger.info("Copying config file to {target_config_path}")
                shutil.copyfile(config_file_path, target_config_path)

            if auto_load_script_path:
                target_autoload_path = target_gadget_path.replace(
                    self.DEFAULT_GADGET_NAME, self.DEFAULT_HOOKFILE_NAME
                )

                self.logger.info("Copying auto load script file to {target_autoload_path}")
                shutil.copyfile(auto_load_script_path, target_autoload_path)

        return True

    def delete_existing_gadget(self, arch_folder: Path, delete_custom_files: int = 0):
        """
        delete existing gadget inside the apk
        """
        gadget_path = arch_folder / self.DEFAULT_GADGET_NAME

        if gadget_path.is_file():
            gadget_path.unlink()

        if delete_custom_files & self.CONFIG_BIT:
            config_file_path: Path = arch_folder / self.DEFAULT_CONFIG_NAME

            if config_file_path.is_file():
                config_file_path.unlink()

        if delete_custom_files & self.AUTOLOAD_BIT:
            hookfile_path: Path = arch_folder / self.DEFAULT_HOOKFILE_NAME

            if hookfile_path.is_file():
                hookfile_path.unlink()

    ################################################################################
    #                                                                              #
    #                PATCHING                                                      #
    #                                                                              #
    ################################################################################

    def set_arch(self, arch: str):
        """set architecture of target phone where apk would be installed

        Args:
            arch (str): architecture
        """
        self.arch = arch

    def set_debug(self):
        """set debug mode"""
        self.debug_mode = True

    def enable_debug_mode(self) -> bool:
        self.logger.info("Injecting debuggable in Manifest...")

        manifest_path = self.final_dir / "AndroidManifest.xml"

        if not manifest_path.is_file():
            self.logger.error("Couldn't find the Manifest file. Something is wrong with the apk!")
            return False

        with open(manifest_path, "rb") as fp:
            buf = fp.read()

            axml, _ = pyaxml.AXML.from_axml(buf)
            xml = axml.to_xml()

            debuggable = "{http://schemas.android.com/apk/res/android}debuggable"
            application = xml.find(f"./application")

            # keep the order
            ordered_attrib = OrderedDict(application.attrib)

            # create the attribute and set a temporary position
            new_attrib = (debuggable, "true")
            position = -1

            # element that should be before debuggable
            element_should_before = [
                "{http://schemas.android.com/apk/res/android}theme",
                "{http://schemas.android.com/apk/res/android}label",
                "{http://schemas.android.com/apk/res/android}icon",
            ]

            i = 0
            for k in ordered_attrib.keys():
                i += 1
                if k in element_should_before:
                    position = i  # update position

            # insert debuggable
            items = list(ordered_attrib.items())
            if position != -1:
                items.insert(position, new_attrib)
            else:
                items.append(new_attrib)

            # update attributes
            application.attrib.clear()
            application.attrib.update(OrderedDict(items))
            res_aml = pyaxml.axml.AXML()
            res_aml.from_xml(xml)
        with open(manifest_path, "wb") as fp:
            fp.write(res_aml.pack())

    def patching(
        self,
        gadget_to_use: str | None = None,
        output_file: Path | None = None,
        user_certificate: bool = False,
        splits_apk: list[Path] | None = None,
        entrypoint=None,
    ):
        """
        patch the apk with gadget 'gadget_to_use'
        """
        if splits_apk is None:
            splits_apk = []
        if len(self.network_certificates) > 0:
            user_certificate = True
        if not self.apk.is_file():
            self.logger.error("The file %s couldn't be found!", self.apk)
            sys.exit(1)

        # Create tempory file
        with tempfile.TemporaryDirectory() as tmp_dir:
            apk_name = Path(self.apk).stem
            self.final_dir = Path(f"{tmp_dir}/{apk_name}")

            # extract the apk on temporary folder
            self.extract_apk()

            # add Internet permission
            has_internet_permission = self.has_permission(self.INTERNET_PERMISSION)
            if not has_internet_permission:
                if not self.inject_permission_manifest(self.INTERNET_PERMISSION):
                    sys.exit(1)
            if self.debug_mode:
                self.enable_debug_mode()

            # add users certificate
            if user_certificate:
                with open(self.final_dir / "resources.arsc", "r+b") as fp:
                    rsc, _ = pyaxml.ARSC.from_axml(fp.read())
                    self.enable_user_certificates(rsc)
                    rsc.compute()
                    fp.seek(0)
                    fp.write(rsc.pack())

            # inject frida library
            if entrypoint is None:
                self.entrypoint_class = self.get_entrypoint_class_name()
                if self.entrypoint_class is None:
                    return
            else:
                self.entrypoint_class = entrypoint
            if not self.entrypoint_class:
                return
            self.entrypoint_smali_path = self.get_entrypoint_smali_path()
            print(gadget_to_use, self.use_download_frida)
            if gadget_to_use is None and self.use_download_frida:
                gadget_to_use = self.download_frida()
            if gadget_to_use:
                self.insert_frida_loader()
            if not self.check_libextract():
                return

            if gadget_to_use:
                if not self.arch:
                    archs = [
                        (plba(gadget_to_use, self.ARCH_ARM), self.ARCH_ARM),
                        (plba(gadget_to_use, self.ARCH_ARM64), self.ARCH_ARM64),
                        (plba(gadget_to_use, self.ARCH_X86), self.ARCH_X86),
                        (plba(gadget_to_use, self.ARCH_X86_64), self.ARCH_X64),
                    ]
                else:
                    archs = [(gadget_to_use, self.arch)]
                for gadget, arch in archs:
                    self.insert_frida_lib(gadget, arch)

            # repackage the apk and sign + align it
            if output_file:
                output_file_path = self.repackage_apk(target_file=output_file)

            else:
                output_file_path = self.repackage_apk()

            self.sign_and_zipalign(output_file_path, splits_apk)

    @staticmethod
    def get_default_config_file() -> Path:
        """
        get a default config to frida to auto start frida at launch
        """

        config: str = f"""
{
    "interaction": {
        "type": "script",
        "address": "127.0.0.1",
        "port": 27042,
        "path": "./libhook.js.so"
    }
}
        """

        path = Path.cwd() / "generatedConfigFile.config"
        with open(path, "w", encoding="ascii") as f:
            f.write(config)

        return path
