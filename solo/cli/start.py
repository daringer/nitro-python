# -*- coding: utf-8 -*-





# import binascii
# import os
import sys
from time import sleep, time

import click
# import solo
# import solo.fido2
# from cryptography.hazmat.primitives import hashes
# from fido2.client import ClientError as Fido2ClientError
# from fido2.ctap1 import ApduError
# from solo.cli.update import update

from subprocess import check_output

from solo.start.gnuk_token import get_gnuk_device
from solo.start.usb_strings import get_devices as get_devices_strings
from usb.core import USBError



# https://pocoo-click.readthedocs.io/en/latest/commands/#nested-handling-and-contexts
@click.group()
def start():
    """Interact with 'Nitrokey Start' keys, see subcommands."""
    pass


@click.command()
def list():
    """list connected devices"""
    print(":: 'Nitrokey Start' keys:")
    for dct in get_devices_strings():
        print(f"{dct['Serial']}: {dct['Vendor']} {dct['Product']} ({dct['Revision']})")


@click.command()
@click.argument("identity")
def set_identity(identity):
    """set given identity (one of: 0, 1, 2)"""
    if not identity.isdigit():
        print("identity number must be a digit")
        sys.exit(1)
    identity = int(identity)
    if identity < 0 or identity > 2:
        print("identity must be 0, 1 or 2")
        sys.exit(1)
    print(f"Trying to set identity to {identity}")
    for x in range(3):
        try:
            gnuk = get_gnuk_device()
            gnuk.cmd_select_openpgp()
            try:
                gnuk.cmd_set_identity(identity)
            except USBError:
                print("device has reset, and should now have the new identity")
                sys.exit(0)

        except ValueError as e:
            if 'No ICC present' in str(e):
                print("Could not connect to device, trying to close scdaemon")
                result = check_output(["gpg-connect-agent",
                                       "SCD KILLSCD", "SCD BYE",
                                       "/bye"])  # gpgconf --kill all might be better?
                sleep(3)
            else:
                print('*** Found error: {}'.format(str(e)))


@click.command()
def update():
    """update device"""
    pass




# @click.group()
# def rng():
#     """Access TRNG on key, see subcommands."""
#     pass
#
#
# @click.command()
# @click.option("--count", default=8, help="How many bytes to generate (defaults to 8)")
# @click.option("-s", "--serial", help="Serial number of Solo to use")
# def hexbytes(count, serial):
#     """Output COUNT number of random bytes, hex-encoded."""
#     if not 0 <= count <= 255:
#         print(f"Number of bytes must be between 0 and 255, you passed {count}")
#         sys.exit(1)
#
#     print(solo.client.find(serial).get_rng(count).hex())
#
#
# @click.command()
# @click.option("-s", "--serial", help="Serial number of Solo to use")
# def raw(serial):
#     """Output raw entropy endlessly."""
#     p = solo.client.find(serial)
#     while True:
#         r = p.get_rng(255)
#         sys.stdout.buffer.write(r)
#
# @click.command()
# @click.option("-s", "--serial", help="Serial number of Solo to use")
# @click.option("-b", "--blink", is_flag=True, help="Blink in the meantime")
# def status(serial, blink: bool):
#     """Print device's status"""
#     p = solo.client.find(serial)
#     t0 = time()
#     while True:
#         if time() - t0 > 5 and blink:
#             p.wink()
#         r = p.get_status()
#         for b in r:
#             print('{:#02d} '.format(b), end='')
#         print('')
#         sleep(0.3)


# @click.command()
# @click.option("--count", default=64, help="How many bytes to generate (defaults to 8)")
# @click.option("-s", "--serial", help="Serial number of Solo to use")
# def feedkernel(count, serial):
#     """Feed random bytes to /dev/random."""
#
#     if os.name != "posix":
#         print("This is a Linux-specific command!")
#         sys.exit(1)
#
#     if not 0 <= count <= 255:
#         print(f"Number of bytes must be between 0 and 255, you passed {count}")
#         sys.exit(1)
#
#     p = solo.client.find(serial)
#
#     import struct
#     import fcntl
#
#     RNDADDENTROPY = 0x40085203
#
#     entropy_info_file = "/proc/sys/kernel/random/entropy_avail"
#     print(f"Entropy before: 0x{open(entropy_info_file).read().strip()}")
#
#     r = p.get_rng(count)
#
#     # man 4 random
#
#     # RNDADDENTROPY
#     #       Add some additional entropy to the input pool, incrementing the
#     #       entropy count. This differs from writing to /dev/random or
#     #       /dev/urandom, which only adds some data but does not increment the
#     #       entropy count. The following structure is used:
#
#     #           struct rand_pool_info {
#     #               int    entropy_count;
#     #               int    buf_size;
#     #               __u32  buf[0];
#     #           };
#
#     #       Here entropy_count is the value added to (or subtracted from) the
#     #       entropy count, and buf is the buffer of size buf_size which gets
#     #       added to the entropy pool.
#
#     entropy_bits_per_byte = 2  # maximum 8, tend to be pessimistic
#     t = struct.pack(f"ii{count}s", count * entropy_bits_per_byte, count, r)
#
#     with open("/dev/random", mode="wb") as fh:
#         fcntl.ioctl(fh, RNDADDENTROPY, t)
#     print(f"Entropy after:  0x{open(entropy_info_file).read().strip()}")
#
#
# @click.command()
# @click.option("-s", "--serial", help="Serial number of Solo use")
# @click.option(
#     "--host", help="Relying party's host", default="solokeys.dev", show_default=True
# )
# @click.option("--user", help="User ID", default="they", show_default=True)
# @click.option(
#     "--udp", is_flag=True, default=False, help="Communicate over UDP with software key"
# )
# @click.option(
#     "--prompt",
#     help="Prompt for user",
#     default="Touch your authenticator to generate a credential...",
#     show_default=True,
# )
# def make_credential(serial, host, user, udp, prompt):
#     """Generate a credential.
#
#     Pass `--prompt ""` to output only the `credential_id` as hex.
#     """
#
#     import solo.hmac_secret
#
#     solo.hmac_secret.make_credential(
#         host=host, user_id=user, serial=serial, output=True, prompt=prompt, udp=udp
#     )
#
#
# @click.command()
# @click.option("-s", "--serial", help="Serial number of Solo use")
# @click.option("--host", help="Relying party's host", default="solokeys.dev")
# @click.option("--user", help="User ID", default="they")
# @click.option(
#     "--udp", is_flag=True, default=False, help="Communicate over UDP with software key"
# )
# @click.option(
#     "--prompt",
#     help="Prompt for user",
#     default="Touch your authenticator to generate a reponse...",
#     show_default=True,
# )
# @click.argument("credential-id")
# @click.argument("challenge")
# def challenge_response(serial, host, user, prompt, credential_id, challenge, udp):
#     """Uses `hmac-secret` to implement a challenge-response mechanism.
#
#     We abuse hmac-secret, which gives us `HMAC(K, hash(challenge))`, where `K`
#     is a secret tied to the `credential_id`. We hash the challenge first, since
#     a 32 byte value is expected (in original usage, it's a salt).
#
#     This means that we first need to setup a credential_id; this depends on the
#     specific authenticator used. To do this, use `solo key make-credential`.
#
#     If so desired, user and relying party can be changed from the defaults.
#
#     The prompt can be suppressed using `--prompt ""`.
#     """
#
#     import solo.hmac_secret
#
#     solo.hmac_secret.simple_secret(
#         credential_id,
#         challenge,
#         host=host,
#         user_id=user,
#         serial=serial,
#         prompt=prompt,
#         output=True,
#         udp=udp,
#     )
#
#
# @click.command()
# @click.option("-s", "--serial", help="Serial number of Solo use")
# @click.option(
#     "--udp", is_flag=True, default=False, help="Communicate over UDP with software key"
# )
# @click.argument("hash-type")
# @click.argument("filename")
# def probe(serial, udp, hash_type, filename):
#     """Calculate HASH."""
#
#     # hash_type = hash_type.upper()
#     assert hash_type in ("SHA256", "SHA512", "RSA2048", "Ed25519")
#
#     data = open(filename, "rb").read()
#     # < CTAPHID_BUFFER_SIZE
#     # https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-client-to-authenticator-protocol-v2.0-id-20180227.html#usb-message-and-packet-structure
#     # also account for padding (see data below....)
#     # so 6kb is conservative
#     assert len(data) <= 6 * 1024
#
#     p = solo.client.find(serial, udp=udp)
#     import fido2
#
#     serialized_command = fido2.cbor.dumps({"subcommand": hash_type, "data": data})
#     from solo.commands import SoloBootloader
#
#     result = p.send_data_hid(SoloBootloader.HIDCommandProbe, serialized_command)
#     result_hex = result.hex()
#     print(result_hex)
#     if hash_type == "Ed25519":
#         print(f"content: {result[64:]}")
#         # print(f"content from hex: {bytes.fromhex(result_hex[128:]).decode()}")
#         print(f"content from hex: {bytes.fromhex(result_hex[128:])}")
#         print(f"signature: {result[:128]}")
#         import nacl.signing
#
#         # verify_key = nacl.signing.VerifyKey(bytes.fromhex("c69995185efa20bf7a88139f5920335aa3d3e7f20464345a2c095c766dfa157a"))
#         verify_key = nacl.signing.VerifyKey(
#             bytes.fromhex(
#                 "c69995185efa20bf7a88139f5920335aa3d3e7f20464345a2c095c766dfa157a"
#             )
#         )
#         try:
#             verify_key.verify(result)
#             verified = True
#         except nacl.exceptions.BadSignatureError:
#             verified = False
#         print(f"verified? {verified}")
#     # print(fido2.cbor.loads(result))
#
#
# # @click.command()
# # @click.option("-s", "--serial", help="Serial number of Solo to use")
# # @click.argument("filename")
# # def sha256sum(serial, filename):
# #     """Calculate SHA256 hash of FILENAME."""
#
# #     data = open(filename, 'rb').read()
# #     # CTAPHID_BUFFER_SIZE
# #     # https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-client-to-authenticator-protocol-v2.0-id-20180227.html#usb-message-and-packet-structure
# #     assert len(data) <= 7609
# #     p = solo.client.find(serial)
# #     sha256sum = p.calculate_sha256(data)
# #     print(sha256sum.hex().lower())
#
# # @click.command()
# # @click.option("-s", "--serial", help="Serial number of Solo to use")
# # @click.argument("filename")
# # def sha512sum(serial, filename):
# #     """Calculate SHA512 hash of FILENAME."""
#
# #     data = open(filename, 'rb').read()
# #     # CTAPHID_BUFFER_SIZE
# #     # https://fidoalliance.org/specs/fido-v2.0-id-20180227/fido-client-to-authenticator-protocol-v2.0-id-20180227.html#usb-message-and-packet-structure
# #     assert len(data) <= 7609
# #     p = solo.client.find(serial)
# #     sha512sum = p.calculate_sha512(data)
# #     print(sha512sum.hex().lower())
#
#
# @click.command()
# @click.option("-s", "--serial", help="Serial number of Solo to use")
# def reset(serial):
#     """Reset key - wipes all credentials!!!"""
#     if click.confirm(
#         "Warning: Your credentials will be lost!!! Do you wish to continue?"
#     ):
#         print("Press the button to confirm -- again, your credentials will be lost!!!")
#         solo.client.find(serial).reset()
#         click.echo("....aaaand they're gone")
#
#
# @click.command()
# @click.option("--pin", help="PIN for to access key")
# @click.option("-s", "--serial", help="Serial number of Solo to use")
# @click.option(
#     "--udp", is_flag=True, default=False, help="Communicate over UDP with software key"
# )
# def verify(pin, serial, udp):
#     """Verify key is valid Solo Secure or Solo Hacker."""
#
#     # Any longer and this needs to go in a submodule
#     print("Please press the button on your Solo key")
#     try:
#         cert = solo.client.find(serial, udp=udp).make_credential(pin=pin)
#     except ValueError as e:
#         # python-fido2 library pre-emptively returns `ValueError('PIN required!')`
#         # instead of trying, and returning  `CTAP error: 0x36 - PIN_REQUIRED`
#         if "PIN required" in str(e):
#             print("Your key has a PIN set. Please pass it using `--pin <your PIN>`")
#             sys.exit(1)
#         raise
#
#     except Fido2ClientError as e:
#         cause = str(e.cause)
#         # error 0x31
#         if "PIN_INVALID" in cause:
#             print("Your key has a different PIN. Please try to remember it :)")
#             sys.exit(1)
#         # error 0x34 (power cycle helps)
#         if "PIN_AUTH_BLOCKED" in cause:
#             print(
#                 "Your key's PIN authentication is blocked due to too many incorrect attempts."
#             )
#             print("Please plug it out and in again, then again!")
#             print(
#                 "Please be careful, after too many incorrect attempts, the key will fully block."
#             )
#             sys.exit(1)
#         # error 0x32 (only reset helps)
#         if "PIN_BLOCKED" in cause:
#             print(
#                 "Your key's PIN is blocked. To use it again, you need to fully reset it."
#             )
#             print("You can do this using: `solo key reset`")
#             sys.exit(1)
#         # error 0x01
#         if "INVALID_COMMAND" in cause:
#             print("Error getting credential, is your key in bootloader mode?")
#             print("Try: `solo program aux leave-bootloader`")
#             sys.exit(1)
#         raise
#
#     hashdb = {
#         b'd7a23679007fe799aeda4388890f33334aba4097bb33fee609c8998a1ba91bd3': "Nitrokey FIDO2 1.x",
#         b'6d586c0b00b94148df5b54f4a866acd93728d584c6f47c845ac8dade956b12cb': "Nitrokey FIDO2 2.x",
#         b'e1f40563be291c30bc3cc381a7ef46b89ef972bdb048b716b0a888043cf9072a': "Nitrokey FIDO2 Dev 2.x ",
#     }
#
#     dev_fingerprint = cert.fingerprint(hashes.SHA256())
#     a_hex = binascii.b2a_hex(dev_fingerprint)
#     if a_hex in hashdb:
#         print('Found device: {}'.format(hashdb[a_hex]))
#     else:
#         print("Unknown fingerprint! ", a_hex)
#
#
# @click.command()
# @click.option("-s", "--serial", help="Serial number of Solo to use")
# @click.option(
#     "--udp", is_flag=True, default=False, help="Communicate over UDP with software key"
# )
# def version(serial, udp):
#     """Version of firmware on key."""
#
#     try:
#         res = solo.client.find(serial, udp=udp).solo_version()
#         major, minor, patch = res[:3]
#         locked = ""
#         if len(res) > 3:
#             if res[3]:
#                 locked = "locked"
#             else:
#                 locked = "unlocked"
#         print(f"{major}.{minor}.{patch} {locked}")
#
#     except solo.exceptions.NoSoloFoundError:
#         print("No Solo found.")
#         print("If you are on Linux, are your udev rules up to date?")
#     except (solo.exceptions.NoSoloFoundError, ApduError):
#         # Older
#         print("Firmware is out of date (key does not know the SOLO_VERSION command).")
#
#
# @click.command()
# @click.option("-s", "--serial", help="Serial number of Solo to use")
# @click.option(
#     "--udp", is_flag=True, default=False, help="Communicate over UDP with software key"
# )
# def wink(serial, udp):
#     """Send wink command to key (blinks LED a few times)."""
#
#     solo.client.find(serial, udp=udp).wink()
#
# @click.command()
# @click.option("-s", "--serial", help="Serial number of Solo to use")
# @click.option(
#     "--udp", is_flag=True, default=False, help="Communicate over UDP with software key"
# )
# def reboot(serial, udp):
#     """Send reboot command to key (development command)"""
#     print('Reboot')
#     CTAP_REBOOT = 0x53
#     dev = solo.client.find(serial, udp=udp).dev
#     try:
#         dev.call(CTAP_REBOOT ^ 0x80, b'')
#     except OSError:
#         pass
#
start.add_command(list)
start.add_command(set_identity)
start.add_command(update)
# start.add_command(rng)
# start.add_command(reboot)
# rng.add_command(hexbytes)
# rng.add_command(raw)
# rng.add_command(feedkernel)
# start.add_command(make_credential)
# start.add_command(challenge_response)
# start.add_command(reset)
# start.add_command(status)
# start.add_command(update)
# start.add_command(probe)
# # key.add_command(sha256sum)
# # key.add_command(sha512sum)
# start.add_command(version)
# start.add_command(verify)
# start.add_command(wink)
