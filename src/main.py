#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Regular scraping of DKB documents """
import os
import argparse
import json
from datetime import datetime, timedelta
from dkb_robo import DKBRobo


def write_transactions(dkb, out_folder, date_from, date_to):
    link = dkb.account_dic[0]["transactions"]
    _type = dkb.account_dic[0]["type"]

    print("Getting Transactions from %s to %s" % (date_from, date_to))

    transaction_list = dkb.get_transactions(link, _type, date_from, date_to)
    with open(os.path.join(out_folder, "transactions.json"), "w", newline="") as f:
        json.dump(transaction_list, f, ensure_ascii=False)


def write_postbox(dkb, out_folder):
    postbox_dic = dkb.scan_postbox()
    with open(os.path.join(out_folder, "postbox.json"), "w") as f:
        json.dump(postbox_dic, f, ensure_ascii=False)


def write_credit_limits(dkb, out_folder):
    cli = dkb.get_credit_limits()
    with open(os.path.join(out_folder, "credit_limits.json"), "w") as f:
        json.dump(cli, f, ensure_ascii=False)


def write_standing_orders(dkb, out_folder):
    sto = dkb.get_standing_orders()
    with open(os.path.join(out_folder, "standing_orders.json"), "w") as f:
        json.dump(sto, f, ensure_ascii=False)


def write_exemption_orders(dkb, out_folder):
    exo = dkb.get_exemption_order()
    with open(os.path.join(out_folder, "exemption_orders.json"), "w") as f:
        json.dump(exo, f, ensure_ascii=False)


def write_dkb_points(dkb, out_folder):
    points = dkb.get_points()
    with open(os.path.join(out_folder, "dkb_points.json"), "w") as f:
        json.dump(points, f, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--secret_file", type=str, help="Path which stores the DKB credentials",
    )
    parser.add_argument(
        "--out_folder", "-o", type=str, help="Where to store the results"
    )
    parser.add_argument(
        "--max_tries", "-m", type=int, default=2, help="How many login attempts to do"
    )
    args = parser.parse_args()

    date_to = datetime.now()
    date_from = date_to - timedelta(days=90)
    out_folder = os.path.join(args.out_folder, date_to.strftime("%Y-%m-%d"))
    os.makedirs(out_folder, exist_ok=True)

    with open(args.secret_file) as f:
        user, password = f.read().split(":")

    tries = 0
    with DKBRobo(user.strip(), password.strip()) as dkb:
        while not dkb.account_dic and tries < args.max_tries:
            tries = tries + 1
            dkb.login()
        if not dkb.account_dic:
            print("Failed to login to account")
            exit(1)

        write_transactions(
            dkb,
            out_folder,
            date_from.strftime("%d.%m.%Y"),
            date_to.strftime("%d.%m.%Y"),
        )
        write_postbox(dkb, out_folder)
        write_credit_limits(dkb, out_folder)
        write_standing_orders(dkb, out_folder)
        write_exemption_orders(dkb, out_folder)
        write_dkb_points(dkb, out_folder)
