#! /usr/bin/env python3
import itertools
import sys
from copy import deepcopy

from player import Player
from simulator import Fight
import demons
from my_cards import my_cards
import cards

DEBUG = False
PLAYER_LVL = 31


def get_possible_decks():
    decks = list()
    for r in range(1, len(my_cards) + 1):
        if r > Player(PLAYER_LVL).get_num_of_cards_allowed():
            continue
        print('Getting combinations for {} cards.'.format(r))
        decks.extend(list(itertools.combinations(my_cards, r=r)))
    print('Calculated {} possible deck combinations.'.format(len(decks)))
    return decks


def handle_reports(reports):
    max_dpm = 0
    best_report = dict()
    for report in reports:
        if report['dpm'] > max_dpm:
            max_dpm = report['dpm']
            best_report = deepcopy(report)
    print('Best Deck: ')
    for i, card in enumerate(best_report['deck']):
        print('\t{}. {}'.format(i + 1, card))
    print('Max Damage Per Minute: {:.0f}'.format(best_report['dpm']))
    print('Average Damage Done: {:.0f}'.format(best_report['avg_dmg']))


def create_new_players(deck):
    player = Player(PLAYER_LVL)
    for card in deck:
        player.assign_card(card)
    demon_player = demons.DemonPlayer()
    demon_player.assign_card(demons.DarkTitan())
    return player, demon_player


def handle_simulations(cnt=1):
    decks = get_possible_decks()
    reports = list()
    for deck in decks:
        dmg_done = 0
        dmg_per_min = 0
        for _ in itertools.repeat(None, cnt):
            player, demon_player = create_new_players(deck)
            fight = Fight(player, demon_player)
            dmg_done += fight.dmg_done
            dmg_per_min += fight.dmg_per_min
        reports.append({
            'dpm': dmg_per_min / cnt,
            'avg_dmg': dmg_done/cnt,
            'deck': deck
        })
    handle_reports(reports)


def handle_single_deck_simulation(cnt=1):
    # deck = (cards.HeadlessHorseman(10), cards.WoodElfArcher(10))
    deck = (cards.HeadlessHorseman(10), cards.HeadlessHorseman(10))
    dmg_done = 0
    dmg_per_min = 0
    for _ in itertools.repeat(None, cnt):
        player, demon_player = create_new_players(deck)
        fight = Fight(player, demon_player)
        dmg_done += fight.dmg_done
        dmg_per_min += fight.dmg_per_min
    print('Average Damage Per Minute: {:.0f}'.format(dmg_per_min/cnt))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        try:
            count = int(sys.argv[2])
        except ValueError:
            err_msg = 'Expected integer received {} instead'.format(
                type(sys.argv[1]))
            raise TypeError(err_msg)
        handle_single_deck_simulation(count)
        sys.exit()
    elif len(sys.argv) == 2:
        try:
            count = int(sys.argv[1])
        except ValueError:
            err_msg = 'Expected integer received {} instead'.format(
                type(sys.argv[1]))
            raise TypeError(err_msg)
    elif len(sys.argv) == 1:
        count = 1
    else:
        err_msg = 'run_simulation takes 1 positional argument but {} were ' \
                  'given'.format(len(sys.argv) - 1)
        raise TypeError(err_msg)
    handle_simulations(count)
