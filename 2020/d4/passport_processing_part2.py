"""
@author: fconil
https://adventofcode.com/2020/day/4

python3 passport_processing_part2.py 2>&1 | grep ":VALID" | cut -d " " -f 4 | sort | uniq
python3 passport_processing_part2.py 2>&1 | grep ":VALID" | cut -d " " -f 7 | sort | uniq
python3 passport_processing_part2.py 2>&1 | grep ":VALID" | cut -d " " -f 10 | sort | uniq
python3 passport_processing_part2.py 2>&1 | grep ":VALID" | cut -d " " -f 13 | sort | uniq
python3 passport_processing_part2.py 2>&1 | grep ":VALID" | cut -d " " -f 17 | sort | uniq
python3 passport_processing_part2.py 2>&1 | grep ":VALID" | cut -d " " -f 20 | sort | uniq
python3 passport_processing_part2.py 2>&1 | grep ":VALID" | cut -d " " -f 23 | sort | uniq
"""
import logging
import re

logger = logging.getLogger(__name__)

PASSPORT_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}


def valid_interval(value, min, max):
    valid = False

    try:
        year = int(value)

        if (year >= min) and (year <= max):
            valid = True

    except ValueError as e:
        logger.warning(f"Invalid integer {value}, {e.message}")

    return valid


class Passport:
    all_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}

    def __init__(self):
        self.byr = None
        self.iyr = None
        self.eyr = None
        self.hgt = None
        self.hcl = None
        self.ecl = None
        self.pid = None
        # cid (Country ID)      - ignored, missing or not.
        self.cid = None

        self.valid = True

    def format_passport(self, r_passport):
        missing = set(self.all_fields)

        for elts in r_passport:
            field, value = elts.split(":")

            # We could convert integers but they
            #  are not used and this is done by
            # valid functions
            setattr(self, field, value)

            missing.remove(field)

        if (len(missing) > 1) or (
            (len(missing) == 1) and (len(missing.intersection({"cid"})) == 0)
        ):
            logger.warning(f"INVALID - missing fields {missing}")
            self.valid = False

    def valid_byr(self):
        # byr (Birth Year)      - four digits; at least 1920 and at most 2002
        valid = valid_interval(self.byr, 1920, 2002)
        logger.debug(f"Checked byr: {self.byr}, {valid}")
        return valid

    def valid_iyr(self):
        # iyr (Issue Year)      - four digits; at least 2010 and at most 2020.
        valid = valid_interval(self.iyr, 2010, 2020)
        logger.debug(f"Checked iyr: {self.iyr}, {valid}")
        return valid

    def valid_eyr(self):
        # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
        valid = valid_interval(self.eyr, 2020, 2030)
        logger.debug(f"Checked eyr: {self.eyr}, {valid}")
        return valid

    def valid_hgt(self):
        # hgt (Height)          - a number followed by either cm or in:
        #     If cm, the number must be at least 150 and at most 193.
        #     If in, the number must be at least 59 and at most 76.
        valid = False
        pattern = re.compile("(\d+)(cm|in)")
        m = pattern.match(self.hgt)
        if m is not None:
            size, unit = m.groups()
            if unit == "cm":
                valid = valid_interval(size, 150, 193)
            if unit == "in":
                valid = valid_interval(size, 59, 76)
        logger.debug(f"Checked hgt: {self.hgt}, {valid}")
        return valid

    def valid_hcl(self):
        # hcl (Hair Color)      - a # followed by exactly six characters 0-9 or a-f.
        pattern = re.compile(r"#[0-9a-f]{6}")
        valid = pattern.match(self.hcl) is not None
        logger.debug(f"Checked hcl: {self.hcl}, {valid}")
        return valid

    def valid_ecl(self):
        # ecl (Eye Color)       - exactly one of: amb blu brn gry grn hzl oth.
        pattern = re.compile(r"(amb|blu|brn|gry|grn|hzl|oth)")
        valid = pattern.match(self.ecl) is not None
        logger.debug(f"Checked ecl: {self.ecl}, valid")
        return valid

    def valid_pid(self):
        # pid (Passport ID)     - a nine-digit number, including leading zeroes.
        pattern = re.compile("^\d{9}$")
        valid = pattern.match(self.pid) is not None
        logger.debug(f"Checked pid: {self.pid}, valid")
        return valid

    def check_passport(self):
        v_byr = self.valid_byr()
        v_iyr = self.valid_iyr()
        v_eyr = self.valid_eyr()
        v_hgt = self.valid_hgt()
        v_hcl = self.valid_hcl()
        v_ecl = self.valid_ecl()
        v_pid = self.valid_pid()
        self.valid = v_byr and v_iyr and v_eyr and v_hgt and v_hcl and v_ecl and v_pid
        logger.warning(
            f"{'VALID' if self.valid else 'INVALID'} - "
            f"byr: {self.byr} {v_byr}, iyr: {self.iyr} {v_iyr}, "
            f"eyr: {self.eyr} {v_eyr}, hgt: {self.hgt} {v_hgt}, "
            f" hcl: {self.hcl} {v_hcl}, ecl: {self.ecl} {v_ecl}, "
            f"pid: {self.pid} {v_pid}"
        )


def load_batch():
    """"""
    with open("input", "r") as f:
        l_input = [l.rstrip("\n") for l in f.readlines()]  # noqa E741

    p_list = []
    passport = []

    for line in l_input:
        logger.debug(f"Line : {line}")
        if len(line) == 0:
            logger.debug("empty line, changing passport")
            p_list.append(passport)
            passport = []
        else:
            elts = line.split(" ")
            logger.debug(f"Put {elts} in passport")
            passport.extend(elts)

    p_list.append(passport)

    return p_list


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.DEBUG)

    nb_valid_passports = 0

    passport_list = load_batch()

    for raw_passport in passport_list:
        logger.info(f"Formatting {raw_passport}")

        passport = Passport()
        passport.format_passport(raw_passport)

        if passport.valid:
            passport.check_passport()

            if passport.valid:
                nb_valid_passports += 1

    print(f"nb_passports: {len(passport_list)} => nb_valid: {nb_valid_passports}")
