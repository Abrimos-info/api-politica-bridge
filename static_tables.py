from sheets import sheet_reader
from utils import colors_to_list, make_banner, make_table, write_csv
import json
import sys 

CSV_DB_PATH = 'csv_db_officeholders'

CONFIG_FILE = sys.argv[2];

with open(CONFIG_FILE, 'r') as f:
    CONFIG = json.load(f)


def get_end_range(value):
    end = value.split(":")[1];
    number = end[1:]
    return number


def read_country_tables(country):

    SHEET_ID = CONFIG["sheets"][country]["SHEET_ID"]

    # Struct read ranges
    ST_RANGES = CONFIG["sheets"][country]["ST_RANGES"]

    make_banner(f"Getting static tables data as defined in {CONFIG_FILE} for "+country)
    # AREA
    area_data[country] = sheet_reader(SHEET_ID, f"Table area!{ST_RANGES['area']}")
    area_header = area_data[country][0].keys()
    write_csv(make_table(area_header, area_data[country]), f"{CSV_DB_PATH}/area")
    for area in area_data[country]:
        if area["area_id"] == "":
            area["is_deleted"] = True
        
        del area["area_id"]

    # CHAMBER
    chamber_data[country] = sheet_reader(SHEET_ID, f"Table chamber!{ST_RANGES['chamber']}")
    chamber_header = chamber_data[country][0].keys()
    write_csv(make_table(chamber_header, chamber_data[country]), f"{CSV_DB_PATH}/chamber")
    for chamber in chamber_data[country]:
        if chamber["chamber_id"] == "":
            chamber["is_deleted"] = True
        del chamber["chamber_id"]

    # ROLE
    role_data[country] = sheet_reader(SHEET_ID, f"Table role!{ST_RANGES['role']}")
    role_header = role_data[country][0].keys()
    write_csv(make_table(role_header, role_data[country]), f"{CSV_DB_PATH}/role")
    for role in role_data[country]:
        if role["role_id"] == "":
            role["is_deleted"] = True
        del role["role_id"]

    # COALITION
    coalition_data[country] = sheet_reader(SHEET_ID,
                                f"Table coalition!{ST_RANGES['coalition']}")
    coalition_header = coalition_data[country][0].keys()
    write_csv(make_table(coalition_header, coalition_data[country]),
            f"{CSV_DB_PATH}/coalition")
    coalition_data[country] = colors_to_list(coalition_data[country])
    for coalition in coalition_data[country]:
        del coalition["coalition_id"]
    coalitions_catalogue[country] = sheet_reader(SHEET_ID, f"Table coalition!B2:B{get_end_range(ST_RANGES['coalition'])}",
                                        as_list=True)

    # PARTY
    party_data[country] = sheet_reader(SHEET_ID, f"Table party!{ST_RANGES['party']}")
    party_header = party_data[country][0].keys()
    write_csv(make_table(party_header, party_data[country]), f"{CSV_DB_PATH}/party")
    party_data[country] = colors_to_list(party_data[country])
    for party in party_data[country]:
        if party["party_id"] == "":
            party["is_deleted"] = True
        del party["party_id"]
    parties[country] = sheet_reader(SHEET_ID, f"Table party!C2:C{get_end_range(ST_RANGES['party'])}", as_list=True)

    # CONTEST
    contest_data[country] = sheet_reader(SHEET_ID, f"Table contest!{ST_RANGES['contest']}")
    contest_header = contest_data[country][0].keys()
    write_csv(make_table(contest_header, contest_data[country]), f"{CSV_DB_PATH}/contest")
    for contest in contest_data[country]:
        if contest["contest_id"] == "":
            contest["is_deleted"] = True
        del contest["contest_id"]

    contest_chambers[country] = sheet_reader(SHEET_ID, f"Table contest!C2:G{get_end_range(ST_RANGES['contest'])}",
                                    as_list=True)
    # PROFESSION
    profession_range = f"Catalogue profession!{ST_RANGES['profession']}"
    profession_data[country] = sheet_reader(SHEET_ID, profession_range)
    profession_header = profession_data[country][0].keys()
    write_csv(make_table(profession_header, profession_data[country]),
            f"{CSV_DB_PATH}/profession")
    for profession in profession_data[country]:
        del profession["profession_id"]
    professions_catalogue[country] = sheet_reader(SHEET_ID, f"Catalogue profession!B2:B{get_end_range(ST_RANGES['profession'])}",
                                        as_list=True)
    # URL types Catalogue
    url_types[country] = sheet_reader(SHEET_ID, f"Catalogue url_types!{ST_RANGES['url_types']}", as_list=True)

area_data = {}
chamber_data = {}
role_data = {}
coalition_data = {}
party_data = {}
profession_data = {}
contest_data= {}

area_catalogue = {}
chamber_catalogue = {}
role_catalogue = {}
coalitions_catalogue = {}
parties = {}
professions_catalogue = {}
contest_chambers= {}
url_types = {}

read_country_tables("mx");
read_country_tables("ar");
read_country_tables("co");

