import argparse
import logging
import sys
from pathlib import Path
from apkpatcher import Patcher, conf, new_logger, download_baksmali, download_smali


def main() -> int:
    """cli function"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--apk", help="Specify the apk you want to patch")
    parser.add_argument("-m", "--multiple_split", nargs="*", help="provided multiple split apks")
    parser.add_argument(
        "-g",
        "--gadget",
        help="Specify the frida-gadget file \
                        file.so or file with no architecture specified will be \
                        autocomplete with file_<arch>.so",
    )
    parser.add_argument(
        "--download_frida_version",
        help="Specify the frida version you want to inject. it should be use \
        only if you didn't download .so file. for instance: --download_frida_version 16.3.3",
    )
    parser.add_argument("-s", "--sdktools", help="Path of the sdktools")
    parser.add_argument("-b", "--version_buildtools", help="version for buildtools")
    parser.add_argument(
        "-r",
        "--arch",
        choices=[
            Patcher.ARCH_ARM,
            Patcher.ARCH_ARM64,
            Patcher.ARCH_X86,
            Patcher.ARCH_X64,
        ],
        help="architecture targeted",
    )
    parser.add_argument(
        "-v", "--verbosity", help="Verbosity level (0 to 3). Default is 3", type=int
    )

    parser.add_argument(
        "-e",
        "--enable-user-certificates",
        help="Add some configs in apk to accept user certificates",
        action="store_true",
    )
    parser.add_argument(
        "--enable-debug",
        help="enable debuggable",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--custom-certificate",
        help="Install a custom network certificate inside the apk",
    )

    parser.add_argument(
        "--keycertificate",
        help="use a specific certificate to generate the apk",
    )

    parser.add_argument(
        "--keyalias",
        help="alias name to use a specific certificate to generate the apk",
    )

    parser.add_argument(
        "--keypass",
        help="password to use a specific certificate to generate the apk",
    )

    parser.add_argument(
        "--keep-keycertificate",
        help="generate a certificate to sign apk and keep it at the end",
        action="store_true",
    )

    parser.add_argument(
        "--v4",
        help="use a v4 signature file to sign APK",
    )

    parser.add_argument("-o", "--output-file", help="Specify the output file (patched)")

    parser.add_argument("-p", "--pause", help="pause before repackage the apk", action="store_true")
    parser.add_argument(
        "--plugin",
        help="execute load plugin (a python file with as argument the folder before the packaging)",
    )
    parser.add_argument("-V", "--version", help="version of apkpatcher", action="store_true")
    parser.add_argument(
        "--entrypoint",
        help="specify the class name where you want to inject your library",
    )
    parser.add_argument(
        "--download-jars",
        help="download jars files",
        action="store_true",
    )

    args = parser.parse_args()

    if args.version:
        print(f"version {conf.VERSION}")
        return 0
    
    if args.download_jars:
        smali_jar = Path(__file__).parent / "smali.jar"
        if not smali_jar.exists():
            download_smali(smali_jar)

        baksmali_jar = Path(__file__).parent / "baksmali.jar"
        if not baksmali_jar.exists():
            download_baksmali(baksmali_jar)
        return 0


    if not args.sdktools:
        import os
        if "ANDROID_SDK_ROOT" in os.environ:
            args.sdktools = os.environ["ANDROID_SDK_ROOT"]

    if len(sys.argv) == 1 or not (args.apk and args.sdktools):
        print("apkpatcher -a <apk> -s <sdktools> -b <version> [options]")
        if not args.apk:
            print("\nArgument apk is missing, you should add '-a myapk.apk'")
        if not args.sdktools:
            print("\nArgument sdktools is missing, you should add '-s /usr/lib/android-sdk' or ANDROID_SDK_ROOT environment variable is not set")
            print(
                "If you didn't have installed sdktools follow this tutorial: https://asthook.ci-yow.com/how.install.html#setup-sdktools"
            )
        parser.print_help()
        return 1

    logger = None
    if args.verbosity:
        if args.verbosity == 3:
            logger = new_logger(logging.DEBUG)
        elif args.verbosity == 2:
            logger = new_logger(logging.INFO)
        else:
            logger = new_logger(logging.ERROR)
    else:
        logger = new_logger(logging.INFO)
    patcher = Patcher(args.apk, args.version_buildtools, args.sdktools, logger)
    if args.custom_certificate:
        patcher.add_network_certificate(Path(args.custom_certificate))
    if args.arch:
        patcher.set_arch(args.arch)
    patcher.pause(args.pause)
    if args.keycertificate and args.keyalias and args.keypass:
        patcher.add_certificate(args.keycertificate, args.keyalias, args.keypass)
    if args.keep_keycertificate:
        patcher.keep_certificate()
    if args.v4:
        patcher.enable_v4_signature(args.v4)
    if args.enable_debug:
        patcher.set_debug()
    if args.plugin:
        patcher.set_plugin(args.plugin)
    if args.download_frida_version:
        patcher.use_download_frida(args.download_frida_version)
    if args.multiple_split:
        splits_apk = args.multiple_split
    else:
        splits_apk = []
    if args.entrypoint:
        entrypoint = args.entrypoint
    else:
        entrypoint = None

    if args.output_file:
        patcher.patching(
            args.gadget,
            output_file=Path(args.output_file),
            user_certificate=args.enable_user_certificates,
            splits_apk=splits_apk,
            entrypoint=entrypoint,
        )
    else:
        patcher.patching(
            args.gadget,
            user_certificate=args.enable_user_certificates,
            splits_apk=splits_apk,
            entrypoint=entrypoint,
        )
    patcher.remove_frida_downloaded()
    return 0
